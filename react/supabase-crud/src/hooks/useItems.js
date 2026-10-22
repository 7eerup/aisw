import { useEffect, useState } from 'react';
import { getItems } from '../lib/items';

/**
 * 게시물 목록 조회 및 로딩·오류 상태 관리
 *
 * @returns {{ items: Object[], isLoading: boolean, error: string|null }}
 */
export function useItems() {
  const [items, setItems] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;

    async function fetchItems() {
      try {
        const data = await getItems();

        if (active) {
          setItems(data);
        }
      } catch (err) {
        if (active) {
          setError(err.message);
        }
      } finally {
        if (active) {
          setIsLoading(false);
        }
      }
    }

    fetchItems();

    return () => {
      active = false;
    };
  }, []);

  return { items, isLoading, error };
}
