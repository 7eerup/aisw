import { supabase } from './supabase';

export async function getItems() {
  const { data, error } = await supabase
    .from('items')
    .select('id, title, content, created_at')
    .order('created_at', { ascending: false });

  if (error) {
    throw error;
  }

  return data;
}
