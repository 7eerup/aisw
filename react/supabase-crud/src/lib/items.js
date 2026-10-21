import { supabase } from './supabase';

export async function getItems() {
  const { data, error } = await supabase
    .from('items')
    .select('id, title, content, created_at')
    .order('created_at', { ascending: false });

  if (error) throw error;

  return data;
}

export async function getItemById(id) {
  const { data, error } = await supabase
    .from('items')
    .select('id, title, content, created_at')
    .eq('id', id)
    .single();

  if (error) throw error;

  return data;
}

export async function createItem(values) {
  const { data, error } = await supabase
    .from('items')
    .insert({
      title: values.title,
      content: values.content,
    })
    .select('id')
    .single();

  if (error) throw error;

  return data;
}
