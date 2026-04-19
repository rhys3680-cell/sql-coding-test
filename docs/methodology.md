# SQL 학습 방법론

> 목표: "강의를 다 들었는데 쿼리는 못 짠다"는 함정을 피하고, **실제로 문제를 보면 쿼리가 나오는 상태**에 도달하는 것.

---

## 1. 핵심 원칙 (Why before How)

### 원칙 1. Learn by Doing — 눈으로 읽지 말고 손으로 쳐라
- SQL은 **언어**이자 **사고 방식**이다. 읽어서 이해되는 것과 쓸 수 있는 것은 완전히 다름.
- 강의 1시간 시청 < 문제 10분 풀이. 시청은 "아는 착각"을 만든다.
- **규칙**: 새 문법을 배우면 반드시 그날 안에 DB에 직접 쳐본다. 복붙 금지.

### 원칙 2. Active Recall + Spaced Repetition
인지과학 연구에서 **유일하게 "high utility"로 평가된 두 기법**.
- **Active Recall (인출 연습)**: 보고 이해하는 게 아니라, **백지에서 꺼내는** 연습.
  - 예: "LEFT JOIN과 INNER JOIN 차이?" → 문서 보지 말고 먼저 말/글로 설명 → 그다음 확인.
- **Spaced Repetition (간격 반복)**: 망각곡선(Ebbinghaus)에 맞춰 **간격을 늘려가며** 복습.
  - 2357 법칙: 학습 후 2일, 3일, 5일, 7일 뒤에 복습.
  - 틀린 문제는 **다시 풀 목록**에 넣고 일주일 뒤 재도전.

### 원칙 3. Short & Consistent > Long & Sporadic
- 주말에 몰아서 5시간 < 매일 30분.
- **20~30분 x 주 4~5회**가 이상적. 뇌가 소화할 시간이 필요함.

### 원칙 4. 문법과 실습을 병렬로
- 문법 100% 끝내고 문제 푸는 게 아니라, **기본 SELECT/WHERE 배우면 바로 문제**. 배운 만큼만 풀어도 된다.
- 문법 → 실습 → 막힘 → 문법 보강. 이 사이클이 핵심.

---

## 2. 학습 사이클 (매주 반복)

```
[ 개념 학습 ] → [ 즉시 실습 ] → [ 문제 풀이 ] → [ 오답 노트 ] → [ 간격 복습 ]
   (15분)         (15분)          (30분)          (5분)           (주말)
```

### 각 단계에서 할 것

| 단계 | 할 것 | 하지 말 것 |
|------|-------|-----------|
| 개념 학습 | 한 번에 **한 주제만** (예: JOIN 하나) | 여러 문법 동시 학습 |
| 즉시 실습 | 로컬 DB에 직접 쳐보기, 의도적으로 에러도 내보기 | 강의 화면 보며 따라치기만 |
| 문제 풀이 | 먼저 **말로 설계** → 쿼리 작성 → 실행 | 바로 키보드부터 두드리기 |
| 오답 노트 | **왜 틀렸는지** 한 줄로 기록 | 정답 쿼리만 복붙 저장 |
| 간격 복습 | 2일/3일/7일 뒤 **다시 풀기** (보지 말고) | 정답을 읽기만 하기 |

---

## 3. 단계별 커리큘럼 (3~6개월)

### Phase 1. 기초 문법 (2~3주)
관계형 DB의 기본 개념 + 가장 많이 쓰는 문법.

- [ ] 관계형 DB 개념 (테이블, 행/열, PK/FK)
- [ ] `SELECT`, `FROM`, `WHERE`, `ORDER BY`, `LIMIT`, `DISTINCT`
- [ ] 연산자: `AND`, `OR`, `NOT`, `IN`, `BETWEEN`, `LIKE`, `IS NULL`
- [ ] 집계 함수: `COUNT`, `SUM`, `AVG`, `MIN`, `MAX`
- [ ] `GROUP BY`, `HAVING`
- [ ] `JOIN`: INNER, LEFT, RIGHT (FULL, SELF는 Phase 2로)
- [ ] 문자열/날짜 함수 기초

**완료 기준**: 테이블 2~3개 조인해서 집계 쿼리를 **막힘없이** 쓸 수 있음.

### Phase 2. 실전 문제 풀이 (4~6주)
배운 문법을 **문제로 체화**. 가장 중요한 단계.

- [ ] 서브쿼리 (스칼라, 인라인뷰, EXISTS)
- [ ] `CASE WHEN`
- [ ] `UNION`, `UNION ALL`
- [ ] 복잡한 JOIN (FULL OUTER, SELF JOIN)
- [ ] NULL 처리 (`COALESCE`, `IFNULL`)

**학습법**: 하루 2~3문제, 주 5일. 총 **60~80문제 누적**이 목표.

### Phase 3. 심화 (4주+)
실무/면접에서 변별력이 갈리는 영역.

- [ ] **Window Function**: `ROW_NUMBER`, `RANK`, `DENSE_RANK`, `LAG`, `LEAD`, `SUM() OVER()`
- [ ] `PARTITION BY`
- [ ] **CTE**: `WITH` 구문, 재귀 CTE
- [ ] 쿼리 최적화: 인덱스, 실행계획(`EXPLAIN`), N+1 문제
- [ ] 트랜잭션, 격리 수준 (백엔드 방향일 경우)
- [ ] 정규화 / 반정규화 (설계 방향일 경우)

---

## 4. 환경 구축 (1일차에 반드시)

**로컬 DB 없이는 학습이 안 된다.** 웹 에디터만 쓰면 손에 안 붙음.

### 추천 조합
- **DB**: PostgreSQL (또는 SQLite로 가볍게 시작)
- **클라이언트**: DBeaver (무료, 크로스플랫폼) 또는 VSCode + SQL 확장
- **샘플 데이터**: Sakila (영화 대여), Chinook (음악), Northwind (이커머스)

---

## 5. 연습 플랫폼 비교

| 플랫폼 | 특징 | 추천 대상 |
|--------|------|-----------|
| **프로그래머스 SQL 고득점 Kit** | 한국어, 난이도 단계적, 무료 | 입문~중급, 국내 취업 |
| **HackerRank SQL** | 초보자 트랙이 체계적, 무료 | 완전 초심자 |
| **LeetCode Database** | 면접 빈출 문제, 약 150문제 | 해외 취업/면접 대비 |
| **StrataScratch** | 실제 데이터 분석 면접 문제 1000+ | 데이터 분석가 지망 |
| **SQLZoo** | 문법별 튜토리얼식 문제 | 기초 문법 다질 때 |

**추천 경로**: HackerRank Easy → 프로그래머스 Kit → LeetCode Medium → StrataScratch

---

## 6. 흔한 함정

1. **강의 완주병**: 강의 끝내는 게 목표가 되면 망함. 강의는 참고서지 교과서 아님.
2. **문법 암기병**: 함수 이름 외우기보다 **언제 어떤 함수를 쓸지** 감 익히기.
3. **복붙 의존**: 한 번이라도 복붙하면 그 쿼리는 내 것이 아님.
4. **쉬운 문제 반복**: 10문제 풀었는데 다 Easy면 실력은 제자리.
5. **해설 먼저 보기**: 20분은 혼자 고민. 고민 없이 본 해설은 안 남음.

---

## 7. 주간 루틴 예시 (하루 30~60분 가정)

| 요일 | 활동 |
|------|------|
| 월 | 새 문법 학습 + 즉시 실습 |
| 화 | 문제 2~3개 (월요일 문법 적용) |
| 수 | 문제 2~3개 + 화요일 오답 복습 |
| 목 | 새 문법 or 심화 학습 |
| 금 | 문제 2~3개 (주중 내용 종합) |
| 토 | **주간 복습** (Spaced Repetition) + 오답 재도전 |
| 일 | 휴식 또는 프로젝트성 쿼리 (내 관심 데이터 분석) |

---

## 8. 진척도 체크 질문 (매 주말)

스스로에게 질문. 머뭇거리면 다음 단계 가지 말 것.

- [ ] 이번 주 배운 문법을 **문서 안 보고** 쿼리로 쓸 수 있나?
- [ ] 왜 이 문법을 쓰는지 **한 문장으로 설명** 가능한가?
- [ ] 틀렸던 문제를 **다시 풀었을 때** 맞히는가?
- [ ] 다음 단계로 갈 **구멍 없는 자신감**이 있는가?

---

## 참고 자료

- [SQL Roadmap (roadmap.sh)](https://roadmap.sh/sql)
- [Learn SQL in 2026: A Practical Beginner Roadmap (LearnSQL.com)](https://learnsql.com/blog/sql-learning-roadmap/)
- [SQL Roadmap: 12-Month Learning Path (DataCamp)](https://www.datacamp.com/blog/sql-roadmap)
- [데이터 분석을 위한 SQL 공부법 (brunch)](https://brunch.co.kr/@minu-log/5)
- [비전공자를 위한 SQL (zzsza)](https://zzsza.github.io/development/2018/03/18/sql-for-everyone/)
- [LeetCode vs HackerRank vs StrataScratch (StrataScratch)](https://www.stratascratch.com/blog/leetcode-vs-hackerrank-vs-stratascratch-for-data-science)
- [Active Recall & Spaced Repetition (SC Training)](https://training.safetyculture.com/blog/how-to-use-active-recall-and-spaced-repetition/)
- [Spaced Repetition and 2357 Method (BCU)](https://www.bcu.ac.uk/exams-and-revision/best-ways-to-revise/spaced-repetition)
