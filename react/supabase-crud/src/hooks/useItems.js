import { useEffect, useState } from 'react';
import { getItems } from '../lib/items';

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
