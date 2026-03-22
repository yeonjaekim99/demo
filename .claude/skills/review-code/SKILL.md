---
name: review-code
description: 코드 리뷰를 수행하여 보안 취약점을 분석합니다. 사용자가 보안 리뷰, 코드 리뷰, 취약점 분석, SQL Injection/XSS/인증 점검을 요청할 때 이 스킬을 사용하세요. `/review-code` 명령으로도 트리거됩니다.
---

# Code Review Skill

`demo-scenario/src/`의 소스 코드를 보안 관점에서 리뷰합니다.

## 수행 절차

1. `demo-scenario/src/server.py`와 `demo-scenario/src/db.py`를 읽습니다.
2. 아래 6가지 보안 항목을 점검합니다.

## 점검 항목

### 1. SQL Injection
- f-string, format으로 SQL 쿼리를 조립하는 코드가 있는지 확인
- 파라미터 바인딩(`?`)을 사용하지 않는 쿼리 찾기

### 2. XSS (Cross-Site Scripting)
- HTMLResponse에 사용자 입력을 이스케이프 없이 직접 삽입하는지 확인
- `html.escape()` 미사용 여부

### 3. 하드코딩된 시크릿
- JWT_SECRET 등 시크릿이 소스코드에 문자열로 노출되어 있는지 확인
- `os.environ.get()` 사용 여부

### 4. 인증/인가 누락
- admin, debug 등 민감한 엔드포인트에 인증이 없는지 확인
- `verify_token()` 또는 `Depends()` 미사용 여부

### 5. JWT 설계 결함
- JWT 토큰 페이로드에 비밀번호 등 민감 정보가 포함되는지 확인

### 6. 민감 정보 노출
- 디버그 엔드포인트에서 환경변수, 시크릿 키를 반환하는지 확인
- os.environ, JWT_SECRET 등이 응답에 포함되는지

## 출력 형식

```
## 코드 리뷰 결과

### 🔴 Critical
- [파일:라인] 이슈 설명
  → 수정 방안

### 🟡 Warning
- [파일:라인] 이슈 설명
  → 수정 방안

### 요약
- Critical: N건
- Warning: N건
- 총 N건의 보안 이슈 발견
```
