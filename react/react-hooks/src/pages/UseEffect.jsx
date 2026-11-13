import { useState, useEffect } from "react";

function UseEffect() {
  const [count, setCount] = useState(0);
  const [seconds, setSeconds] = useState(0);

  useEffect(() => {
    document.title = `Count: ${count}`;

    return () => {
      document.title = "React Hooks";
    };
  }, [count]);

  useEffect(() => {
    const timer = setInterval(() => {
      setSeconds((prev) => prev + 1);
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  return (
    <main>
      <h1>useEffect</h1>
      <p>외부 시스템과 동기화하는 Hook</p>

      <h2>Count: {count}</h2>
      <button onClick={() => setCount((prev) => prev + 1)}>제목 변경</button>

      <h2>경과 시간: {seconds}초</h2>
    </main>
  );
}

export default UseEffect;
