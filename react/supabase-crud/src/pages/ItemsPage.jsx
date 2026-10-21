import ItemList from '../components/ItemList';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import { useItems } from '../hooks/useItems';

function ItemsPage() {
  const { items, isLoading, error } = useItems();

  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <main>
      <h1>게시물 목록</h1>
      <ItemList items={items} />
    </main>
  );
}

export default ItemsPage;
