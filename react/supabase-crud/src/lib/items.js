import { supabase } from './supabase';

/**
 * 게시물 목록 최신순으로 조회
 * @returns {Promise<Object[]>} 게시물 목록
 */
export async function getItems() {
  const { data, error } = await supabase
    .from('items')
    .select('id, title, content, created_at')
    .order('created_at', { ascending: false });

  if (error) throw error;

  return data;
}

/**
 * ID로 게시물 상세 정보 조회
 * @param {string|number} id - 게시물 ID
 * @returns {Promise<Object>} 게시물 정보
 */
export async function getItemById(id) {
  const { data, error } = await supabase
    .from('items')
    .select('id, title, content, created_at')
    .eq('id', id)
    .maybeSingle();

  if (error) throw error;

  return data;
}

/**
 * 새 게시물 등록
 * @param {{ title: string, content: string }} values - 게시물 입력값
 * @returns {Promise<{ id: number }>} 생성된 게시물 ID
 */
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

/**
 * 게시물 수정
 * @param {string|number} id - 게시물 ID
 * @param {{ title: string, content: string }} values - 수정할 데이터
 * @returns {Promise<{ id: number }>} 수정된 게시물 ID
 */
export async function updateItem(id, values) {
  const { data, error } = await supabase
    .from('items')
    .update({
      title: values.title,
      content: values.content,
    })
    .eq('id', id)
    .select('id')
    .single();

  if (error) {
    throw error;
  }

  return data;
}

/**
 * ID로 게시물 삭제
 * @param {string|number} id - 게시물 ID
 * @returns {Promise<Object[]>} 삭제된 게시물 ID 목록
 */
export async function deleteItem(id) {
  const { data, error } = await supabase
    .from('items')
    .delete()
    .eq('id', id)
    .select('id');

  if (error) {
    throw error;
  }

  if (data.length === 0) {
    throw new Error('삭제할 게시물을 찾을 수 없습니다.');
  }

  return data;
}
