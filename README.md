# SQL Study

Pagila 샘플 DB 위에서 SQL을 공부하면서, 학습 데이터를 JSONL로 쌓아가는 개인 프로젝트.
목표: SQL 숙련 → 학습 데이터 분석 → 복습 알고리즘 프로토타입.

## 디렉토리 구조

```
sql-coding-test/
├── docs/                       학습 문서
│   ├── methodology.md          학습 방법론 (원칙·커리큘럼·플랫폼)
│   └── checkpoints.md          점검 트리거 규칙
├── infra/                      실행 환경
│   ├── docker-compose.yml      PostgreSQL 16 + Pagila
│   └── init/                   (gitignore) Pagila 덤프, bootstrap으로 재생
├── scripts/
│   ├── log.py                  학습 로그 기록·조회 CLI
│   └── bootstrap.sh            Pagila SQL 다운로드 (최초 1회)
├── logs/
│   └── sessions.jsonl          학습 이벤트 로그
├── index.sql                   (gitignore) 풀이용 스크래치 패드
├── pyproject.toml              uv 프로젝트
├── .python-version             3.12
└── README.md
```

## 요구사항
- Docker Desktop
- [uv](https://docs.astral.sh/uv/) (Python 환경)
- DataGrip (또는 아무 SQL 클라이언트)
- Git Bash (bootstrap.sh 실행용, Windows 기준)

## 최초 세팅

```bash
# 1. Pagila 덤프 다운로드
bash scripts/bootstrap.sh

# 2. PostgreSQL 기동
docker compose -f infra/docker-compose.yml up -d

# 3. 동작 확인
docker exec sql-study-pg psql -U postgres -d pagila -c \
  "SELECT COUNT(*) FROM actor;"   # 200 이어야 정상
```

## DataGrip 연결

| 항목 | 값 |
|------|-----|
| Host | `localhost` |
| Port | `5432` |
| Database | `pagila` |
| User | `postgres` |
| Password | `postgres` |

## 학습 로그 사용법

`scripts/log.py` — 학습 이벤트를 `logs/sessions.jsonl` 에 append.

```bash
# 문제 풀이 기록
uv run scripts/log.py add \
  --topic WHERE --pid p-007 --diff easy --result correct \
  --problem "film 테이블에서 rental_rate > 3 필터" \
  --time 45 --note ""

# 누적 지표
uv run scripts/log.py stats

# 현재 세션 지표
uv run scripts/log.py stats --session

# 최근 엔트리
uv run scripts/log.py tail -n 5
```

세션 구분은 자동 (직전 이벤트와 30분 이상 공백이면 새 세션).

### 필드 스펙
- `ts` (ISO 8601, KST)
- `session_id` (`YYYY-MM-DD-NN`)
- `topic` (SELECT, WHERE, JOIN...)
- `problem_id` (`p-001`...)
- `problem` (문제 설명)
- `result` — `correct` / `wrong` / `partial` / `gave_up`
- `difficulty` — `easy` / `medium` / `hard`
- `time_sec` (선택)
- `stuck_on` (막힌 지점 태그, 없으면 `null`)
- `retry_of` (재도전이면 원 problem_id)
- `note` (자유 텍스트)

## 학습 흐름

1. `docs/methodology.md` 원칙 확인
2. 세션 시작 → 문제 풀이 (DataGrip의 `index.sql` 스크래치 패드에서 작업, 문제 끝나면 비움)
3. 풀이마다 `log.py add`
4. `docs/checkpoints.md` 트리거에 걸리면 점검
5. 세션 종료 시 `log.py stats --session` 리포트

## 자주 쓰는 명령

```bash
# 상태
docker compose -f infra/docker-compose.yml ps

# 로그
docker logs sql-study-pg

# 정지 (데이터 보존)
docker compose -f infra/docker-compose.yml stop

# 재시작
docker compose -f infra/docker-compose.yml start

# 완전 초기화 (볼륨 삭제)
docker compose -f infra/docker-compose.yml down -v
```

## 샘플 DB: Pagila
- MySQL Sakila 의 PostgreSQL 포팅 (DVD 대여점 도메인)
- 유지: Devrim Gündüz (PostgreSQL 공식 RPM 메인테이너)
- License: PostgreSQL License
- https://github.com/devrimgunduz/pagila