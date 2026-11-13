import { useState, useMemo } from "react";

const items = [
  "React",
  "JavaScript",
  "TypeScript",
  "Node.js",
  "Express",
  "Vite",
  "Next.js",
];

function UseMemo() {
  const [search, setSearch] = useState("");

  const filteredItems = useMemo(() => {
    return items.filter((item) =>
      item.toLowerCase().includes(search.toLowerCase()),
    );
  }, [search]);

  return (
    <main>
      <h1>useMemo</h1>
      <p>계산 결과를 캐싱하는 Hook</p>

      <input
        value={search}
        onChange={(event) => setSearch(event.target.value)}
        placeholder="기술 검색"
      />

      <ul>
        {filteredItems.map((item) => (
          <li key={item}>{item}</li>
        ))}
      </ul>
    </main>
  );
}

export default UseMemo;
