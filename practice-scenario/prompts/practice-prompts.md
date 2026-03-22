# 실습 프롬프트

순서대로 따라해보세요.

---

## Step 1: 코드 품질 점검 (Skill)

```
/lint
```

> 코드 중복, 구조 문제, Pythonic하지 않은 패턴을 찾아냅니다.
> ID 검증 중복, 제목 검증 중복 등이 발견됩니다.

**확인 포인트**: 점수가 몇 점인지, 어떤 중복이 발견되었는지 확인하세요.

---

## Step 2: 새 기능 추가 (Skill)

```
/scaffold priority
```

> 기존 코드 패턴을 분석하여 우선순위(priority) 기능을 자동 생성합니다.
> store.py에 priority 필드가, app.py에 필터링 API가 추가됩니다.

**확인 포인트**: 기존 코드 스타일(타입 힌트, Pydantic 모델)과 일관성 있게 생성되었는지 확인하세요.

---

## Step 3: 리팩토링 + 문서화 (Multi-Agent)

```
이 프로젝트를 개선해줘.

1. refactor-agent로 코드 중복을 정리해줘 (ID 검증, 제목 검증 통합)
2. docs-agent로 현재 API 전체 문서를 생성해줘
3. 결과를 정리해줘:
   - 리팩토링 변경 사항
   - 생성된 문서 위치

두 에이전트를 동시에 실행해줘.
```

> refactor-agent가 중복 코드를 정리하고, docs-agent가 API 문서를 생성합니다.
> 두 에이전트가 병렬로 작업합니다.

**확인 포인트**: 중복이 제거되었는지, API 문서에 curl 예시가 포함되어 있는지 확인하세요.

---

## 보너스: 나만의 Skill/Agent 만들기

### Skill 만들기: `/api-map`

현재 API 엔드포인트를 표로 정리해서 보여주는 스킬입니다.

**skill-creator로 한 번에 생성 + 실행:**
```
/skill-creator api-map 스킬을 만들어줘.

- 설명: FastAPI 소스 코드에서 API 엔드포인트 목록을 추출하여 표로 정리합니다
- 대상: practice-scenario/src/app.py
- 수행 절차:
  1. app.py를 읽고 @app.get, @app.post 등 라우트 데코레이터를 찾는다
  2. 각 엔드포인트의 HTTP 메서드, 경로, 함수명, 파라미터, 인증 여부를 추출
  3. 표 형식으로 출력
- 출력 형식:
  | 메서드 | 경로 | 함수명 | 파라미터 | 인증 |
  |--------|------|--------|----------|------|
  | GET | /api/todos | list_todos | - | X |
- 코드를 수정하지 않고 분석 결과만 출력
```

> skill-creator가 `.claude/skills/api-map/SKILL.md` 파일을 자동으로 생성해줍니다.

**실행:**
```
/api-map
```

---

### Agent 만들기: `docstring-agent`

함수와 엔드포인트에 한글 docstring을 자동으로 추가하는 에이전트입니다.

**1단계: 파일 생성**
```
.claude/agents/docstring-agent.md 파일을 만들어줘. 아래 내용으로:

- 이름: docstring-agent
- 설명: Python 함수에 docstring을 자동으로 추가하는 에이전트
- 대상: practice-scenario/src/app.py, practice-scenario/src/store.py
- 역할:
  1. 대상 파일을 읽고 docstring이 없는 함수를 찾는다
  2. 각 함수의 파라미터, 반환값, 동작을 분석한다
  3. Google 스타일 한글 docstring을 직접 코드에 추가한다
- DON'T: 함수 로직 변경, 새 함수 추가
- 출력 형식: 추가된 docstring 건수와 목록
```

**2단계: 실행**
```
docstring-agent로 practice-scenario/src/의 모든 함수에 docstring을 추가해줘.
```

---

## 트러블슈팅

| 증상 | 해결 |
|------|------|
| Skill이 안 됨 | `.claude/skills/`에 SKILL.md가 있는지 확인 |
| Agent가 안 됨 | `.claude/agents/`에 파일이 있는지 확인 |
| import 에러 | `pip install -r requirements.txt` 실행 |
| Python 버전 | 3.10 이상 필요 (`python --version`) |
