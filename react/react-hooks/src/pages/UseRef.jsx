import { useRef } from "react";

function UseRef() {
  const inputRef = useRef(null);

  const handleFocus = () => {
    inputRef.current?.focus();
  };

  const handleClear = () => {
    if (inputRef.current) {
      inputRef.current.value = "";
      inputRef.current.focus();
    }
  };

  return (
    <main>
      <h1>useRef</h1>
      <p>DOM 요소를 참조하는 Hook</p>

      <input ref={inputRef} placeholder="텍스트 입력" />

      <button onClick={handleFocus}>포커스</button>
      <button onClick={handleClear}>초기화</button>
    </main>
  );
}

export default UseRef;
