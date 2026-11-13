import { createContext, useContext, useState } from "react";

const ThemeContext = createContext(null);

function ThemeDisplay() {
  const { theme, toggleTheme } = useContext(ThemeContext);

  return (
    <div
      style={{
        backgroundColor: theme === "dark" ? "#222" : "#eee",
        color: theme === "dark" ? "#fff" : "#222",
        padding: "20px",
        marginTop: "16px",
        borderRadius: "8px",
      }}
    >
      <p>현재 테마: {theme}</p>
      <button onClick={toggleTheme}>테마 변경</button>
    </div>
  );
}

function UseContext() {
  const [theme, setTheme] = useState("light");

  const toggleTheme = () => {
    setTheme((prev) => (prev === "light" ? "dark" : "light"));
  };

  return (
    <main>
      <h1>useContext</h1>
      <p>컴포넌트 간 데이터를 공유하는 Hook</p>

      <ThemeContext.Provider value={{ theme, toggleTheme }}>
        <ThemeDisplay />
      </ThemeContext.Provider>
    </main>
  );
}

export default UseContext;
