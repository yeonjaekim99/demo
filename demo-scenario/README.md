# Demo Scenario: API 서버 보안 점검

보안 취약점이 의도적으로 포함된 FastAPI 서버를 Claude Code의 **Skills**와 **Agents**로 점검·수정하는 시연입니다.

## 의도된 취약점 (6건)

| # | 취약점 | 파일 | 핵심 |
|---|--------|------|------|
| 1 | SQL Injection | db.py | `find_user_by_username`에 f-string 쿼리 |
| 2 | SQL Injection | db.py | `search_posts`에 f-string 쿼리 |
| 3 | XSS | server.py | HTMLResponse에 이스케이프 없이 삽입 |
| 4 | 하드코딩 시크릿 | server.py | JWT_SECRET이 소스코드에 노출 |
| 5 | 인증/인가 누락 | server.py | admin, debug API에 인증 없음 |
| 6 | JWT 설계 결함 | server.py | 토큰 페이로드에 비밀번호 포함 |

## Skill vs Agent 역할 분리

| 도구 | 역할 | 코드 수정 |
|------|------|-----------|
| `/review` (Skill) | 이슈 분석·보고 | X |
| `/gen-test` (Skill) | 테스트 파일 생성 | 테스트만 |
| security-agent | 취약점 직접 수정 | O |
| test-agent | 기존 테스트 실행·결과 보고 | X |

## 시연 흐름 (3단계)

```
Step 1  /review     →  Skill이 취약점을 발견 (분석만)
Step 2  /gen-test   →  Skill이 테스트를 생성 → 일부 실패 (증명)
Step 3  Multi-Agent →  security-agent가 수정 + test-agent가 검증 (해결)
```

## 사전 준비

```bash
pip install -r requirements.txt
```

## 프롬프트

`prompts/demo-prompts.md`의 프롬프트를 순서대로 실행하세요.
