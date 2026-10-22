import { useState } from 'react';
import ItemList from '../components/ItemList';
import Input from '../components/Input';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import EmptyState from '../components/EmptyState';
import { useItems } from '../hooks/useItems';

/**
 * 게시물 목록 및 제목 검색 페이지
 * 조회 상태와 검색 결과에 따라 화면을 표시
 */
function ItemsPage() {
  const { items, isLoading, error } = useItems();
  const [searchTerm, setSearchTerm] = useState('');

  const filteredItems = items.filter((item) =>
    item.title.toLowerCase().includes(searchTerm.trim().toLowerCase()),
  );

  if (isLoading) {
    return <LoadingState message="게시물을 불러오는 중입니다..." />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <section>
      <h1>게시물 목록</h1>

      {items.length === 0 ? (
        <EmptyState message="등록된 게시물이 없습니다." />
      ) : (
        <>
          <Input
            id="search"
            label="게시물 제목 검색"
            value={searchTerm}
            onChange={(event) => setSearchTerm(event.target.value)}
          />

          {filteredItems.length === 0 ? (
            <EmptyState message="검색 결과가 없습니다." />
          ) : (
            <ItemList items={filteredItems} />
          )}
        </>
      )}
    </section>
  );
}

export default ItemsPage;
