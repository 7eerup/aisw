import ItemList from '../components/ItemList';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';

const sampleItems = [];

function ItemsPage() {
  const isLoading = false;
  const error = '';

  if (isLoading) {
    return <LoadingState />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  return (
    <main>
      <h1>게시물 목록</h1>
      <ItemList items={sampleItems} />
    </main>
  );
}

export default ItemsPage;
