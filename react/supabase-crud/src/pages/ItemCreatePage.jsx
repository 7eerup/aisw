import ItemForm from '../components/ItemForm';

function ItemCreatePage() {
  async function handleCreate(values) {
    console.log('등록할 게시물:', values);
  }

  return (
    <main>
      <h1>게시물 등록</h1>
      <ItemForm onSubmit={handleCreate} />
    </main>
  );
}

export default ItemCreatePage;
