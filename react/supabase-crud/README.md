# supabase-crud

- React와 Supabase를 활용한 게시물 CRUD 웹 서비스

- React Router를 이용한 SPA 라우팅, 재사용 컴포넌트 설계, 커스텀 훅 기반 상태 관리, 비동기 데이터 처리를 학습하기 위해 구현했습니다.

## 기술 스택

- Frontend: React, JavaScript, Vite
- Routing: React Router
- Database: PostgreSQL
- State Management: React Hooks (`useState`, `useEffect`)
- Styling: CSS
- Code Quality: ESLint, Prettier
- Deployment: Vercel
- Deployment URL: [서비스 바로가기](https://aisw-ten.vercel.app)

## 주요 기능

- 게시물 목록 및 상세 조회
- 게시물 등록, 수정, 삭제
- 게시물 제목 검색
- 등록 및 수정 폼 유효성 검사
- 로딩, 오류, 빈 데이터 상태 처리
- 제출 및 삭제 진행 상태 표시
- 404 Not Found 페이지

## 주요 라우트

| 경로              | 설명                     |
| ----------------- | ------------------------ |
| `/`               | 홈                       |
| `/items`          | 게시물 목록 및 검색      |
| `/items/new`      | 게시물 등록              |
| `/items/:id`      | 게시물 상세 조회 및 삭제 |
| `/items/:id/edit` | 게시물 수정              |
| `/about`          | 서비스 소개              |
| `*`               | Not Found                |

## 프로젝트 구조

```text
src/
├── components/   # 재사용 UI 컴포넌트
├── pages/        # 라우트별 페이지
├── hooks/        # 커스텀 훅
├── lib/          # Supabase 클라이언트 및 CRUD 함수
├── App.jsx
└── main.jsx
```

## 로컬 실행

Node.js / npm 설치

```bash
npm install
npm run dev

http://localhost:5173
```

## 환경변수 설정

다음 두 환경변수가 필요합니다.

```dotenv
VITE_SUPABASE_URL=your_supabase_project_url
VITE_SUPABASE_PUBLISHABLE_KEY=your_supabase_publishable_key
```

- 로컬 개발 환경은 `vite.config.js`의 `envDir` 설정을 통해 상위 디렉터리의 `.env` 파일을 사용하도록 구성했습니다.

- 다른 환경에서 독립적으로 실행할 경우에는 해당 환경에 맞게 `envDir`을 설정하거나 프로젝트 환경변수를 별도로 구성해야 합니다.

- Secret Key와 `service_role` 키는 프론트엔드에 사용하지 않습니다.

## 코드 검사 및 빌드

```bash
npx prettier . --check
npm run lint
npm run build
```
