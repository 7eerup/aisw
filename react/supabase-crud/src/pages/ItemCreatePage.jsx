import { useNavigate } from 'react-router';
import ItemForm from '../components/ItemForm';
import { createItem } from '../lib/items';

function ItemCreatePage() {
  const navigate = useNavigate();

  async function handleCreate(values) {
    const item = await createItem(values);

    navigate(`/items/${item.id}`);
  }

  return (
    <section>
      <h1>게시물 등록</h1>
      <ItemForm onSubmit={handleCreate} />
    </section>
  );
}

export default ItemCreatePage;
