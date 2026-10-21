import { useEffect, useState } from 'react';
import { getItemById } from '../lib/items';

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
