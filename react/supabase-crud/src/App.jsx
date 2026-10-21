import { Link, Routes, Route } from 'react-router';

import HomePage from './pages/HomePage';
import ItemsPage from './pages/ItemsPage';
import ItemDetailPage from './pages/ItemDetailPage';
import ItemCreatePage from './pages/ItemCreatePage';
import ItemEditPage from './pages/ItemEditPage';
import AboutPage from './pages/AboutPage';
import NotFoundPage from './pages/NotFoundPage';

function App() {
  return (
    <>
      <header>
        <h1>Supabase CRUD</h1>
        <nav>
          <Link to="/">홈</Link> | <Link to="/items">게시물 목록</Link> |{' '}
          <Link to="/items/new">게시물 등록</Link> |{' '}
          <Link to="/about">소개</Link>
        </nav>
      </header>

      <main>
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/items" element={<ItemsPage />} />
          <Route path="/items/new" element={<ItemCreatePage />} />
          <Route path="/items/:id" element={<ItemDetailPage />} />
          <Route path="/items/:id/edit" element={<ItemEditPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="*" element={<NotFoundPage />} />
        </Routes>
      </main>
    </>
  );
}

export default App;
