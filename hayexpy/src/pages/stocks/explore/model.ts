import type { Effect, Reducer } from 'umi';
import { addFakeList, queryFakeList, removeFakeList, updateFakeList, queryHistorical} from './service';

import type { BasicListItemDataType, HistoricalPricingType } from './data.d';

export interface StateType {
  list: BasicListItemDataType[];
  historicalPrice: HistoricalPricingType[];
}

export interface ModelType {
  namespace: string;
  state: StateType;
  effects: {
    fetchHistoricalPricing: Effect;
    fetch: Effect;
    appendFetch: Effect;
    submit: Effect;
  };
  reducers: {
    queryList: Reducer<StateType>;
    historicalPrice: Reducer<StateType>;
    appendList: Reducer<StateType>;
  };
}

const Model: ModelType = {
  namespace: 'stockAndExplore',
  state: {
    list: [],
    historicalPrice: [],
  },
  effects: {
    *fetchHistoricalPricing(_, { call, put }) {
      const response = yield call(queryHistorical, 'AAPL');
      console.log('RESPONSE', response)
      yield put({
        type: 'historicalPrice',
        payload: {
          historicalPricing: Array.isArray(response) ? response : [],
        },
      });
    },
    *fetch({ payload }, { call, put }) {
      const response = yield call(queryFakeList, payload);
      console.log('FETCH: ', response)
      yield put({
        type: 'queryList',
        payload: Array.isArray(response) ? response : [],
      });
    },
    *appendFetch({ payload }, { call, put }) {
      const response = yield call(queryFakeList, payload);
      console.log('append FETCH: ', response)
      yield put({
        type: 'appendList',
        payload: Array.isArray(response) ? response : [],
      });
    },
    *submit({ payload }, { call, put }) {
      let callback;
      if (payload.id) {
        callback = Object.keys(payload).length === 1 ? removeFakeList : updateFakeList;
      } else {
        callback = addFakeList;
      }
      const response = yield call(callback, payload); // post
      yield put({
        type: 'queryList',
        payload: response,
      });
    },
  },

  reducers: {
    historicalPrice(state = { historicalPrice: [], list: []}, { payload }) {
      return {
        ...state,
        historicalPrice: payload,
      };
    },
    queryList(state, action) {
      return {
        ...state,
        list: action.payload,
        historicalPrice: []
      };
    },
    appendList(state = { list: [], historicalPrice: [] }, action) {
      return {
        ...state,
        list: state.list.concat(action.payload),
      };
    },
  },
};

export default Model;
