import { useState } from 'react';
import Button from './Button';
import Input from './Input';
import Textarea from './Textarea';
import ErrorState from './ErrorState';

function ItemForm({ initialValues = { title: '', content: '' }, onSubmit }) {
  const [title, setTitle] = useState(initialValues.title);
  const [content, setContent] = useState(initialValues.content);
  const [error, setError] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);

  async function handleSubmit(event) {
    event.preventDefault();

    if (!title.trim() || !content.trim()) {
      setError('제목과 내용을 모두 입력하세요.');
      return;
    }

    setError('');
    setIsSubmitting(true);

    try {
      await onSubmit({
        title: title.trim(),
        content: content.trim(),
      });
    } catch {
      setError('저장 중 오류가 발생했습니다.');
    } finally {
      setIsSubmitting(false);
    }
  }

  return (
    <form onSubmit={handleSubmit}>
      <Input
        id="title"
        label="제목"
        value={title}
        onChange={(event) => setTitle(event.target.value)}
      />

      <Textarea
        id="content"
        label="내용"
        value={content}
        onChange={(event) => setContent(event.target.value)}
      />

      {error && <ErrorState message={error} />}

      <Button type="submit" disabled={isSubmitting}>
        {isSubmitting ? '저장 중...' : '저장'}
      </Button>
    </form>
  );
}

export default ItemForm;
