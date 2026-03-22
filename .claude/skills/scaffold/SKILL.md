---
name: scaffold
description: 새로운 기능에 필요한 코드를 기존 패턴에 맞춰 자동으로 생성(스캐폴딩)합니다. 사용자가 새 기능 추가, 코드 자동 생성, 스캐폴딩, 보일러플레이트 생성을 요청할 때 이 스킬을 사용하세요. `/scaffold [기능명]` 명령으로도 트리거됩니다.
---

# Scaffold Skill

사용자가 요청한 기능에 대한 Python 코드를 자동 생성합니다.

## 사용법
```
/scaffold [기능명]
```

예: `/scaffold priority`, `/scaffold due_date`

## 수행 절차

1. 현재 프로젝트 구조를 파악합니다 (`practice-scenario/src/` 파일 목록, 기존 코드 패턴 확인)
2. `practice-scenario/src/app.py`와 `practice-scenario/src/store.py`의 기존 코드 패턴과 컨벤션을 분석합니다:
   - FastAPI 라우트 등록 방식
   - Pydantic 모델 정의 패턴
   - store.py의 데이터 함수 패턴
   - 에러 처리 방식 (HTTPException)
   - 응답 형식
3. 기존 패턴에 맞춰 새 기능 코드를 생성합니다:
   - `practice-scenario/src/store.py`에 데이터 관련 함수 추가
   - `practice-scenario/src/app.py`에 Pydantic 모델 + API 엔드포인트 추가
4. 생성된 코드 위치와 사용법을 안내합니다

## 생성 규칙
- 기존 코드 스타일을 따릅니다 (PEP 8, 타입 힌트)
- 새 파일보다는 기존 파일에 추가하는 것을 선호합니다
- 주석으로 추가된 부분을 명확히 표시합니다
- Pydantic 모델로 입력 검증을 포함합니다

## 예시

### `/scaffold priority` 실행 시:

**store.py에 추가:**
- Todo 딕셔너리에 `priority` 필드 추가 (기본값: "medium")
- `get_todos_by_priority(priority: str)` 함수

**app.py에 추가:**
- `CreateTodoRequest`에 `priority: str = "medium"` 필드
- `GET /api/todos?priority=high` 쿼리 파라미터 필터링
- priority 유효성 검증 (high/medium/low만 허용)
