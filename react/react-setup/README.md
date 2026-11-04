# React Setup

Vite와 React를 활용한 프론트엔드 개발 환경 구성 및 빌드 과정 정리

## 1. Vite와 React

| 구분 | Vite | React |
|---|---|---|
| 정의 | 프론트엔드 개발·빌드 도구 | JavaScript UI 라이브러리 |
| 역할 | 개발 서버 실행 및 빌드 | 컴포넌트 기반 UI 구성 |
| 특징 | HMR, 빠른 개발 서버, 간편한 설정 | 재사용 가능한 UI 컴포넌트 |

## 2. React 프로젝트 생성

- **Node.js 및 npm 버전 확인**

```bash
node -v
npm -v
```

- **프로젝트 생성 및 의존성 설치**

```bash
npm create vite@latest react-setup -- --template react
cd react-setup
npm install
```

## 3. 프로젝트 구조

```text
react-setup/
├── node_modules/      # 설치된 패키지
├── public/            # 정적 파일
├── src/               # 소스 코드
│   ├── assets/        # 이미지 등 리소스
│   ├── App.jsx        # 최상위 컴포넌트
│   ├── App.css        # App 스타일
│   ├── index.css      # 전역 스타일
│   └── main.jsx       # React 진입점
├── index.html         # HTML 진입 파일
├── package.json       # 프로젝트 설정 및 의존성
├── package-lock.json  # 의존성 버전 잠금
├── vite.config.js     # Vite 설정
└── README.md          # 프로젝트 문서
```

## 4. package.json 주요 항목

| 항목 | 역할 |
|---|---|
| `name` | 프로젝트 이름 |
| `version` | 프로젝트 버전 |
| `scripts` | npm 실행 명령어 |
| `dependencies` | 애플리케이션 실행에 필요한 패키지 |
| `devDependencies` | 개발 및 빌드 도구 |

## 5. 개발 도구 설치

- **ESLint:** JavaScript 및 React 코드 품질 검사
- **Prettier:** 들여쓰기·따옴표·줄바꿈 등 코드 스타일 자동 정리
- **React Router:** React SPA의 클라이언트 사이드 라우팅

```bash
# 설치 여부 확인
npm list eslint prettier --depth=0

# ESLint 및 Prettier 설치
npm install -D eslint prettier

# React Router 설치
npm install react-router
```

## 6. npm Scripts

| 명령어 | 역할 |
|---|---|
| `npm run dev` | 개발 서버 실행 |
| `npm run build` | 배포용 빌드 생성 |
| `npm run preview` | 빌드 결과 미리보기 |
| `npm run lint` | ESLint 코드 검사 |

- `npm start`는 `package.json`에 정의된 경우에만 실행 가능

## 7. 개발 서버 및 HMR

- **개발 서버:** `npm run dev`로 Vite 실행
- **기본 주소:** `http://localhost:5173`
- **HMR:** 코드 변경 시 가능한 경우 전체 페이지 새로고침 없이 변경 사항 반영

## 8. 코드 정렬 및 검사

```bash
# 코드 자동 정렬
npx prettier src --write

# 코드 스타일 검사
npx prettier . --check

# ESLint 코드 검사
npm run lint
```

## 9. Production Build

```bash
# 배포용 빌드 생성
npm run build

# 빌드 결과 미리보기
npm run preview
```

- **빌드:** 최적화된 배포 파일을 `dist/` 디렉토리에 생성
- **미리보기:** 생성된 배포 파일을 로컬 환경에서 확인

## 10. VS Code 확장 프로그램

- **Prettier - Code formatter:** 코드 스타일 자동 정리
- **ESLint:** JavaScript 및 React 코드 규칙 검사

## 11. 전체 개발 흐름

1. Node.js 및 npm 설치 확인
2. Vite + React 프로젝트 생성
3. 의존성 및 개발 도구 설치
4. 개발 서버 실행 및 코드 작성
5. Prettier·ESLint 검사
6. Production Build 생성
7. 빌드 결과 확인

---
