import { useState } from 'react';
import { Link, useNavigate, useParams } from 'react-router';
import { useItemDetail } from '../hooks/useItemDetail';
import { deleteItem } from '../lib/items';
import Button from '../components/Button';
import LoadingState from '../components/LoadingState';
import ErrorState from '../components/ErrorState';

function ItemDetailPage() {
  const { id } = useParams();
  const navigate = useNavigate();
  const { item, isLoading, error } = useItemDetail(id);

  const [isDeleting, setIsDeleting] = useState(false);
  const [deleteError, setDeleteError] = useState('');

  async function handleDelete() {
    const confirmed = window.confirm('정말 이 게시물을 삭제하시겠습니까?');

    if (!confirmed) {
      return;
    }

    setDeleteError('');
    setIsDeleting(true);

    try {
      await deleteItem(id);
      navigate('/items');
    } catch (err) {
      setDeleteError(err.message);
    } finally {
      setIsDeleting(false);
    }
  }

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
        <Button onClick={handleDelete} disabled={isDeleting}>
          {isDeleting ? '삭제 중...' : '삭제하기'}
        </Button>
      </p>

      {deleteError && <ErrorState message={deleteError} />}

      <p>
        <Link to="/items">목록으로</Link>
      </p>
    </section>
  );
}

export default ItemDetailPage;
