import { memo, useCallback, useState } from "react";

const CounterButton = memo(function CounterButton({ onIncrement }) {
  console.log("CounterButton 렌더링");

  return <button onClick={onIncrement}>Count 증가</button>;
});

function UseCallback() {
  const [count, setCount] = useState(0);
  const [text, setText] = useState("");

  const increment = useCallback(() => {
    setCount((prev) => prev + 1);
  }, []);

  return (
    <main>
      <h1>useCallback</h1>
      <p>함수 참조를 캐싱하는 Hook</p>

      <h2>Count: {count}</h2>

      <CounterButton onIncrement={increment} />

      <div>
        <input
          value={text}
          onChange={(event) => setText(event.target.value)}
          placeholder="텍스트 입력"
        />
      </div>

      <p>입력값: {text}</p>
      <p>Console에서 자식 컴포넌트 렌더링을 확인하세요.</p>
    </main>
  );
}

export default UseCallback;
