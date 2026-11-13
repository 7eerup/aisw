import { Link } from "react-router";

const hooks = [
  { name: "useState", path: "/state", description: "상태 관리" },
  { name: "useEffect", path: "/effect", description: "부수 효과 처리" },
  { name: "useContext", path: "/context", description: "데이터 공유" },
  { name: "useRef", path: "/ref", description: "DOM 참조" },
  { name: "useMemo", path: "/memo", description: "계산 결과 재사용" },
  { name: "useCallback", path: "/callback", description: "함수 참조 재사용" },
];

function Home() {
  return (
    <main>
      <h1>React Hooks</h1>
      <p>React + Vite 기반 주요 Hook 실습 프로젝트</p>

      <h2>학습 목록</h2>
      <ul>
        {hooks.map((hook) => (
          <li key={hook.name}>
            <Link to={hook.path}>{hook.name}</Link>
            {" - "}
            {hook.description}
          </li>
        ))}
      </ul>
    </main>
  );
}

export default Home;
