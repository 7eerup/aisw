import { useEffect, useState } from 'react';
import { getItemById } from '../lib/items';

/**
 * 게시물 상세 조회 및 로딩·오류 상태 관리
 *
 * @param {string} id - 조회할 게시물 ID
 * @returns {{ item: Object|null, isLoading: boolean, error: string|null }}
 */
export function useItemDetail(id) {
  const [item, setItem] = useState(null);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let active = true;

    async function fetchItem() {
      try {
        const data = await getItemById(id);

        if (active) {
          setItem(data);
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

    fetchItem();

    return () => {
      active = false;
    };
  }, [id]);

  return { item, isLoading, error };
}
