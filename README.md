# FastAPI Project

FastAPI 기반 백엔드 서비스입니다. 비동기 PostgreSQL 연결, JWT 인증, SQLAlchemy ORM을 지원합니다.

## Tech Stack

- **Framework**: FastAPI
- **ORM**: SQLAlchemy 2.0 (async)
- **Database**: PostgreSQL (asyncpg)
- **Authentication**: JWT (PyJWT), bcrypt, passlib
- **Migration**: Alembic

## Requirements

| 항목 | 버전 |
|------|------|
| Python | >= 3.13 |
| uv | latest |

### uv 설치

```bash
# macOS / Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

## Installation

```bash
# 저장소 클론
git clone <repository-url>
cd test

# 의존성 설치 (가상환경 자동 생성)
uv sync
```

## Run

### Development Server

```bash
# 방법 1: FastAPI CLI 사용 (hot reload 포함)
uv run fastapi dev app/main.py

# 방법 2: main.py 직접 실행
uv run python main.py
```

서버 실행 후 접속:
- API: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc

### Production Server

```bash
uv run fastapi run app/main.py
```

## Test

```bash
# 전체 테스트 실행
uv run pytest

# 상세 출력
uv run pytest -v

# 특정 파일만 테스트
uv run pytest tests/test_main.py

# 커버리지 포함 (coverage 설치 필요)
uv run pytest --cov=app
```

## Linting & Formatting

### Ruff (Linter)

```bash
# 린트 검사
uv run ruff check .

# 자동 수정
uv run ruff check . --fix
```

### Black (Formatter)

```bash
# 포맷 검사만
uv run black --check .

# 자동 포맷팅
uv run black .
```

### 한번에 실행

```bash
# 검사만
uv run ruff check . && uv run black --check .

# 자동 수정/포맷팅
uv run ruff check . --fix && uv run black .
```

## Security Check

### Bandit

Python 코드의 보안 취약점을 검사합니다.

```bash
# app 디렉토리 검사
uv run bandit -r app

# 전체 프로젝트 검사 (tests 제외 - pyproject.toml 설정)
uv run bandit -r .

# 상세 출력
uv run bandit -r app -v

# 특정 심각도 이상만 표시 (l: low, m: medium, h: high)
uv run bandit -r app -ll  # medium 이상
uv run bandit -r app -lll # high만
```

### Semgrep (Optional)

```bash
# 기본 스캔
uv run semgrep scan

# Windows 인코딩 이슈 해결
# PowerShell
$env:PYTHONUTF8=1; uv run semgrep scan

# CMD
set PYTHONUTF8=1 && uv run semgrep scan
```

## Project Structure

```
.
├── app/
│   ├── __init__.py
│   └── main.py          # FastAPI 앱 엔트리포인트
├── tests/
│   ├── __init__.py
│   └── test_main.py     # 테스트 파일
├── main.py              # uvicorn 직접 실행용
├── pyproject.toml       # 프로젝트 설정 및 의존성
└── uv.lock              # 의존성 lock 파일
```