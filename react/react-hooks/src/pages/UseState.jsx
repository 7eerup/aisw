import { useState } from "react";

function UseState() {
  const [count, setCount] = useState(0);

  return (
    <main>
      <h1>useState</h1>
      <p>컴포넌트의 상태를 관리하는 Hook</p>

      <h2>Count: {count}</h2>

      <button onClick={() => setCount((prev) => prev + 1)}>증가</button>

      <button onClick={() => setCount((prev) => prev - 1)}>감소</button>

      <button onClick={() => setCount(0)}>초기화</button>
    </main>
  );
}

export default UseState;
