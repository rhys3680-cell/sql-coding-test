#!/usr/bin/env python3
"""
학습 로그 기록 스크립트. JSONL append + 세션 자동 판정 + 지표 조회.

사용:
  python log.py add --topic SELECT --pid p-007 --problem "..." --result correct --diff easy
  python log.py add --topic WHERE --pid p-008 --problem "..." --result wrong --diff medium --stuck "NULL 비교" --time 120 --note "= NULL 은 동작 안 함"
  python log.py stats            # 누적 지표
  python log.py stats --session  # 이번 세션만
  python log.py tail -n 5        # 최근 5개
"""
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

LOG_PATH = Path(__file__).resolve().parent.parent / "logs" / "sessions.jsonl"
KST = timezone(timedelta(hours=9))
NEW_SESSION_GAP_MIN = 30  # 직전 이벤트와 이 분 이상 떨어지면 새 세션

RESULTS = {"correct", "wrong", "partial", "gave_up"}
DIFFS = {"easy", "medium", "hard"}


def read_all() -> list[dict]:
    if not LOG_PATH.exists():
        return []
    out = []
    for i, line in enumerate(LOG_PATH.read_text(encoding="utf-8").splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError as e:
            sys.exit(f"[line {i}] JSON parse error: {e}")
    return out


def next_session_id(now: datetime, history: list[dict]) -> str:
    today_prefix = now.strftime("%Y-%m-%d")
    if history:
        last = history[-1]
        last_ts = datetime.fromisoformat(last["ts"])
        if (now - last_ts) < timedelta(minutes=NEW_SESSION_GAP_MIN):
            return last["session_id"]
    todays = [h for h in history if h["session_id"].startswith(today_prefix)]
    seq = len({h["session_id"] for h in todays}) + 1
    return f"{today_prefix}-{seq:02d}"


def cmd_add(args: argparse.Namespace) -> None:
    if args.result not in RESULTS:
        sys.exit(f"--result must be one of {RESULTS}")
    if args.diff not in DIFFS:
        sys.exit(f"--diff must be one of {DIFFS}")

    history = read_all()
    now = datetime.now(KST).replace(microsecond=0)
    entry = {
        "ts": now.isoformat(),
        "session_id": next_session_id(now, history),
        "topic": args.topic,
        "problem_id": args.pid,
        "problem": args.problem,
        "result": args.result,
        "difficulty": args.diff,
        "time_sec": args.time,
        "stuck_on": args.stuck,
        "retry_of": args.retry_of,
        "note": args.note or "",
    }

    with LOG_PATH.open("a+", encoding="utf-8") as f:
        f.seek(0, 2)
        if f.tell() > 0:
            f.seek(f.tell() - 1)
            if f.read(1) != "\n":
                f.write("\n")
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")
    print(f"logged [{entry['session_id']}] {entry['problem_id']} -> {entry['result']}")


def cmd_stats(args: argparse.Namespace) -> None:
    rows = read_all()
    rows = [r for r in rows if r["topic"] != "setup"]
    if args.session:
        if not rows:
            print("no entries")
            return
        sid = rows[-1]["session_id"]
        rows = [r for r in rows if r["session_id"] == sid]
        print(f"[session {sid}]")
    else:
        print("[cumulative]")
    if not rows:
        print("no entries")
        return

    total = len(rows)
    correct = sum(1 for r in rows if r["result"] == "correct")
    wrong = sum(1 for r in rows if r["result"] == "wrong")
    partial = sum(1 for r in rows if r["result"] == "partial")
    gave_up = sum(1 for r in rows if r["result"] == "gave_up")
    topics = sorted({r["topic"] for r in rows})
    by_diff = {d: sum(1 for r in rows if r["difficulty"] == d) for d in DIFFS}
    stuck = [r["stuck_on"] for r in rows if r.get("stuck_on")]

    rate = f"{correct / total:.0%}" if total else "-"
    print(f"problems : {total}")
    print(f"correct  : {correct} ({rate})")
    print(f"wrong    : {wrong}   partial: {partial}   gave_up: {gave_up}")
    print(f"topics   : {', '.join(topics)}")
    print(f"difficulty: easy={by_diff['easy']} medium={by_diff['medium']} hard={by_diff['hard']}")
    if stuck:
        print(f"stuck_on : {len(stuck)}건")
        for s in stuck:
            print(f"  - {s}")


def cmd_tail(args: argparse.Namespace) -> None:
    rows = read_all()
    for r in rows[-args.n :]:
        print(json.dumps(r, ensure_ascii=False))


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description="SQL study log")
    sub = p.add_subparsers(dest="cmd", required=True)

    a = sub.add_parser("add", help="log a problem attempt")
    a.add_argument("--topic", required=True)
    a.add_argument("--pid", required=True, help="problem id (e.g. p-007)")
    a.add_argument("--problem", required=True)
    a.add_argument("--result", required=True, help=f"one of {sorted(RESULTS)}")
    a.add_argument("--diff", required=True, help=f"one of {sorted(DIFFS)}")
    a.add_argument("--time", type=int, default=None, help="seconds spent")
    a.add_argument("--stuck", default=None, help="what tripped you up (tag)")
    a.add_argument("--retry-of", dest="retry_of", default=None)
    a.add_argument("--note", default="")
    a.set_defaults(func=cmd_add)

    s = sub.add_parser("stats", help="show metrics")
    s.add_argument("--session", action="store_true", help="current session only")
    s.set_defaults(func=cmd_stats)

    t = sub.add_parser("tail", help="show recent entries")
    t.add_argument("-n", type=int, default=10)
    t.set_defaults(func=cmd_tail)

    return p


if __name__ == "__main__":
    args = build_parser().parse_args()
    args.func(args)