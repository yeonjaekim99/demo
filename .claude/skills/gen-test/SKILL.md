---
name: gen-test
description: API 엔드포인트에 대한 테스트 코드를 자동 생성합니다. 사용자가 테스트 생성, pytest 작성, API 테스트, 보안 테스트 생성을 요청할 때 이 스킬을 사용하세요. `/gen-test` 명령으로도 트리거됩니다.
---

# Test Generation Skill

`demo-scenario/src/server.py`의 API 엔드포인트에 대한 pytest 테스트를 생성합니다.
테스트만 생성하고 실행하지는 않습니다. 실행은 `test-agent`가 담당합니다.

## 수행 절차

1. `demo-scenario/src/server.py`와 `demo-scenario/src/db.py`를 읽고 모든 API 엔드포인트를 파악합니다.
2. 각 엔드포인트에 대해 정상/에러 테스트를 생성합니다.
3. 아래 6가지 보안 항목에 대한 테스트를 포함합니다.
4. 생성된 테스트를 `demo-scenario/src/tests/test_server.py`에 저장합니다.

## 보안 테스트 항목 (필수 포함)

아래 6가지 항목에 대한 테스트를 반드시 포함하세요. `/review` 스킬이 찾는 항목과 동일합니다.

### 1. SQL Injection 방어
- `find_user_by_username`에 `' OR '1'='1' --` 페이로드로 로그인 우회 시도 → 401이어야 함
- `search_posts`에 `'; DROP TABLE posts; --` 페이로드 → 에러 없이 처리되어야 함

### 2. XSS 방어
- `POST /api/posts`의 title에 `<script>alert('xss')</script>` 삽입 → HTML 응답에 `<script>` 태그가 그대로 나오면 안 됨

### 3. 하드코딩 시크릿
- `server.py` 내에서 JWT_SECRET이 문자열 리터럴이 아닌 `os.environ`에서 로드되는지 확인

### 4. 인증/인가
- `GET /api/admin/users` 인증 없이 요청 → 401 또는 403이어야 함
- `GET /api/debug` 인증 없이 요청 → 401 또는 403이어야 함

### 5. JWT 설계
- 로그인 후 받은 토큰을 디코딩하여 `password` 필드가 없어야 함

### 6. 민감 정보 노출
- `GET /api/debug` 응답에 `env`, `secret` 키가 없어야 함

## 테스트 코드 템플릿

```python
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

import pytest
from fastapi.testclient import TestClient
from server import app

client = TestClient(app)


class TestEndpointName:
    """엔드포인트 그룹 설명"""

    def test_정상_케이스(self):
        response = client.get("/api/path")
        assert response.status_code == 200

    def test_보안_테스트(self):
        # 보안 항목 검증
        pass
```

## 생성 규칙
- 각 엔드포인트당 최소 2개 테스트 (정상 + 보안)
- 클래스 기반으로 엔드포인트별 그룹화
- 한글 테스트 설명 사용
- fixture로 테스트 데이터 관리
- 테스트 파일 상단에 `sys.path` 설정으로 `demo-scenario/src/` 디렉토리를 import 경로에 추가
- 테스트 생성 후 **실행하지 않음** (실행은 test-agent가 담당)
