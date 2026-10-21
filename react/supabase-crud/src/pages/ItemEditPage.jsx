import { useNavigate, useParams } from 'react-router';
import ItemForm from '../components/ItemForm';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';
import { useItemDetail } from '../hooks/useItemDetail';
import { updateItem } from '../lib/items';

function ItemEditPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { item, isLoading, error } = useItemDetail(id);

  async function handleUpdate(values) {
    await updateItem(id, values);
    navigate(`/items/${id}`);
  }

  if (isLoading) {
    return <LoadingState message="게시물을 불러오는 중입니다..." />;
  }

  if (error) {
    return <ErrorState message={error} />;
  }

  if (!item) {
    return <p>게시물을 찾을 수 없습니다.</p>;
  }

  return (
    <section>
      <h1>게시물 수정</h1>
      <ItemForm
        key={item.id}
        initialValues={{
          title: item.title,
          content: item.content,
        }}
        onSubmit={handleUpdate}
      />
    </section>
  );
}

export default ItemEditPage;
