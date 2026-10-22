import { useNavigate } from 'react-router';
import ItemForm from '../components/ItemForm';
import { createItem } from '../lib/items';

/**
 * 게시물 등록 페이지
 * 등록 완료 후 해당 게시물의 상세 페이지로 이동
 */
function ItemCreatePage() {
  const navigate = useNavigate();

  /**
   * 게시물을 생성하고 상세 페이지로 이동
   * @param {{ title: string, content: string }} values - 게시물 입력값
   */
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
