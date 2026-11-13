import { Link, Routes, Route } from "react-router";

import Home from "./pages/Home.jsx";
import UseState from "./pages/UseState.jsx";
import UseEffect from "./pages/UseEffect.jsx";
import UseContext from "./pages/UseContext.jsx";
import UseRef from "./pages/UseRef.jsx";
import UseMemo from "./pages/UseMemo.jsx";
import UseCallback from "./pages/UseCallback.jsx";

function App() {
  return (
    <>
      <nav>
        <Link to="/">Home</Link> | <Link to="/state">useState</Link> |{" "}
        <Link to="/effect">useEffect</Link> |{" "}
        <Link to="/context">useContext</Link> | <Link to="/ref">useRef</Link> |{" "}
        <Link to="/memo">useMemo</Link> |{" "}
        <Link to="/callback">useCallback</Link>
      </nav>

      <hr />

      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/state" element={<UseState />} />
        <Route path="/effect" element={<UseEffect />} />
        <Route path="/context" element={<UseContext />} />
        <Route path="/ref" element={<UseRef />} />
        <Route path="/memo" element={<UseMemo />} />
        <Route path="/callback" element={<UseCallback />} />
      </Routes>
    </>
  );
}

export default App;
