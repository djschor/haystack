import request from '@/utils/request';

export async function query(): Promise<any> {
  return request('/api/users');
}

export async function queryAntCurrent(): Promise<any> {
  return request('/api/currentUser');
}

export async function queryNotices(): Promise<any> {
  return request('/api/notices');
}
