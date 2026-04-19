# SQL Study — 환경 구축

PostgreSQL 16 + Pagila 샘플 DB를 Docker로 띄우는 학습용 환경.

## 사전 요구사항
- Docker Desktop (Compose v2 포함)
- DataGrip (또는 psql, DBeaver 등 아무 SQL 클라이언트)

## 구조
```
sql-coding-test/
├── docker-compose.yml        PostgreSQL 정의
├── init/                     최초 기동 시 자동 실행되는 SQL
│   ├── 01-pagila-schema.sql  테이블 정의
│   └── 02-pagila-data.sql    데이터 적재
├── index.md                  학습 방법론
└── README.md
```

## 실행

```bash
docker compose up -d
```

최초 기동 시 스키마·데이터가 자동 로드됩니다 (약 20~30초). 이후 기동은 수 초.

## DataGrip 연결 정보

| 항목 | 값 |
|------|-----|
| Host | `localhost` |
| Port | `5432` |
| Database | `pagila` |
| User | `postgres` |
| Password | `postgres` |

DataGrip → `+` → **Data Source** → **PostgreSQL** → 위 정보 입력 → **Test Connection**.

드라이버가 없으면 DataGrip이 자동으로 다운로드 안내함.

## 동작 확인 쿼리

```sql
-- 테이블 개수 (29개 나와야 정상)
SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';

-- 주요 테이블 로우 수
SELECT 'actor' AS t, COUNT(*) FROM actor
UNION ALL SELECT 'film', COUNT(*) FROM film
UNION ALL SELECT 'customer', COUNT(*) FROM customer
UNION ALL SELECT 'rental', COUNT(*) FROM rental;
```

**기대값**: actor 200 / film 1000 / customer 599 / rental 16044

## 자주 쓰는 명령

```bash
# 컨테이너 상태
docker compose ps

# 로그 보기
docker logs sql-study-pg

# 정지 (데이터 보존)
docker compose stop

# 재시작
docker compose start

# 완전 삭제 + 데이터 초기화 (처음부터 다시)
docker compose down -v
```

## 주의

- `docker-entrypoint-initdb.d`의 스크립트는 **볼륨이 비어있을 때만** 실행됨.
- 스키마를 다시 로드하려면 `docker compose down -v`로 볼륨을 지워야 함.
- 포트 `5432`가 이미 사용 중이면 compose의 `ports` 매핑을 `5433:5432` 등으로 변경.

## 샘플 DB 정보

- **Pagila**: MySQL Sakila의 PostgreSQL 포팅. DVD 대여점 도메인.
- 유지보수: Devrim Gündüz (PostgreSQL 공식 RPM 메인테이너)
- 라이선스: PostgreSQL License
- 저장소: https://github.com/devrimgunduz/pagila

### 주요 테이블 (22개 기본 + 파티션)

| 도메인 | 테이블 |
|--------|--------|
| 영화 | `film`, `film_actor`, `film_category`, `actor`, `category`, `language`, `inventory` |
| 사람 | `customer`, `staff`, `address`, `city`, `country` |
| 거래 | `rental`, `payment` (월별 파티션), `store` |