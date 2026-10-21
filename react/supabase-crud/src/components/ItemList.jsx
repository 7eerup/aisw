import { Link } from 'react-router';
import Card from './Card';
import EmptyState from './EmptyState';

function ItemList({ items }) {
  if (items.length === 0) {
    return <EmptyState message="등록된 게시물이 없습니다." />;
  }

  return (
    <section>
      {items.map((item) => (
        <Card key={item.id} title={item.title}>
          <Link to={`/items/${item.id}`}>상세 보기</Link>
        </Card>
      ))}
    </section>
  );
}

export default ItemList;
