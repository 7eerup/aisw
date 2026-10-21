import { Link, useParams } from 'react-router';
import { useItemDetail } from '../hooks/useItemDetail';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';

function ItemDetailPage() {
  const { id } = useParams();
  const { item, isLoading, error } = useItemDetail(id);

  if (isLoading) return <LoadingState />;
  if (error) return <ErrorState message={error} />;
  if (!item) return <p>게시물을 찾을 수 없습니다.</p>;

  return (
    <section>
      <h1>{item.title}</h1>
      <p>{item.content}</p>
      <p>작성일: {new Date(item.created_at).toLocaleString()}</p>

      <Link to={`/items/${id}/edit`}>수정하기</Link>

      <p>
        <Link to="/items">목록으로</Link>
      </p>
    </section>
  );
}

export default ItemDetailPage;
