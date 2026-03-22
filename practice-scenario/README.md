# Practice Scenario: Todo 앱 기능 추가

Todo CRUD API에 새 기능을 추가하고 코드 품질을 개선하는 실습입니다.

## 현재 상태

- Todo CRUD는 구현됨 (생성, 조회, 수정, 삭제)
- 우선순위(priority) 기능 없음
- API 문서 없음
- 코드에 중복이 있음 (ID 검증, 제목 검증이 여러 곳에 반복)

## Skill vs Agent 역할 분리

| 도구 | 역할 | 코드 수정 |
|------|------|-----------|
| `/lint` (Skill) | 코드 품질 분석·보고 | X |
| `/scaffold` (Skill) | 새 기능 코드 생성 | O (추가만) |
| refactor-agent | 기존 코드 구조 개선 | O (리팩토링) |
| docs-agent | API 문서 자동 생성 | O (문서 파일) |

## 실습 흐름 (3단계)

```
Step 1  /lint              →  Skill로 코드 품질 점검 (분석만)
Step 2  /scaffold priority →  Skill로 새 기능 추가 (코드 생성)
Step 3  Multi-Agent        →  refactor-agent 구조 개선 + docs-agent 문서 생성
```

## 사전 준비

```bash
pip install -r requirements.txt
```

## 프롬프트

`prompts/practice-prompts.md`의 프롬프트를 순서대로 실행하세요.
