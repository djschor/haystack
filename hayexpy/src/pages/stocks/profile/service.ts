import request from 'umi-request';

export type SymbolType = {
  symbol: string;
};

export async function queryStockProfile(symbol: SymbolType) {
  return request(`/api/stock/${symbol}`);
}

export async function query4hr(symbol: SymbolType) {
  return request(`/api/stock/4hr/${symbol}`);
}

export async function query1hr(symbol: SymbolType) {
  return request(`/api/stock/1hr/${symbol}`);
}

export async function query30min(symbol: SymbolType) {
  return request(`/api/stock/4hr/${symbol}`);
}

export async function query15min(symbol: SymbolType) {
  return request(`/api/stock/4hr/${symbol}`);
}

export async function query1min(symbol: SymbolType) {
  return request(`/api/stock/4hr/${symbol}`);
}

export async function queryHistorical(symbol: SymbolType) {
  console.log('SYMBOL PARAM:', symbol)
  return request(`/api/stock/historical/${symbol}`);
}

export async function queryCurrent() {
  return request('/api/currentUser');
}

export async function queryAntCurrent() {
  return request('/api/ant/currentUser');
}
