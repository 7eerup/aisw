# React Hooks

React + Vite 환경에서 주요 React Hooks의 개념과 동작 원리를 학습하는 실습 프로젝트

## 기술 스택

| 구분 | 기술 |
|---|---|
| Language | JavaScript (JSX) |
| Library | React |
| Build Tool | Vite |
| Routing | React Router |
| Linter | ESLint |
| Formatter | Prettier |

## React Hooks

React Hook은 함수형 컴포넌트에서 상태 관리, 외부 시스템 동기화 등 React 기능을 사용할 수 있도록 제공하는 함수

| Hook | 역할 | 실습 기능 |
|---|---|---|
| `useState` | 상태 관리 | 카운터 증가·감소·초기화 |
| `useEffect` | 외부 시스템 동기화 | 문서 제목 변경 및 타이머 |
| `useContext` | Context 데이터 공유 | 라이트·다크 테마 전환 |
| `useRef` | DOM 요소 참조 | 입력창 포커스 및 초기화 |
| `useMemo` | 계산 결과 캐싱 | 검색 목록 필터링 |
| `useCallback` | 함수 참조 캐싱 | 자식 컴포넌트 렌더링 최적화 |

### Hook 사용 규칙

1. 함수형 컴포넌트 또는 커스텀 Hook에서 호출합니다.
2. Hook은 함수 또는 커스텀 Hook의 최상위 수준에서 호출합니다.
3. 조건문, 반복문, 중첩 함수 내부에서 호출하지 않습니다.

## 프로젝트 구조

```text
react-hooks/
├── public/
├── src/
│   ├── pages/
│   │   ├── Home.jsx
│   │   ├── UseState.jsx
│   │   ├── UseEffect.jsx
│   │   ├── UseContext.jsx
│   │   ├── UseRef.jsx
│   │   ├── UseMemo.jsx
│   │   └── UseCallback.jsx
│   ├── App.jsx
│   ├── main.jsx
│   └── index.css
├── eslint.config.js
├── package.json
├── vite.config.js
└── README.md
```

- `pages/`: Hook별 독립적인 실습 컴포넌트
- `App.jsx`: React Router 경로 및 페이지 구성
- `main.jsx`: React 애플리케이션 진입점 및 BrowserRouter 설정

## 라우팅

| 경로 | 페이지 |
|---|---|
| `/` | Home |
| `/state` | useState |
| `/effect` | useEffect |
| `/context` | useContext |
| `/ref` | useRef |
| `/memo` | useMemo |
| `/callback` | useCallback |
