import type { Effect, Reducer } from 'umi';
import type { HistoricalPricingType, CurrentUser, StockProfileType } from './data.d';
import { queryStockProfile, queryAntCurrent, queryHistorical } from './service';
var ProfileState = { 
  profile: { 
    name: '',
    currency: '',
    exchange: '',
    industry: '',
    website: '',
    description: '',
    ceo: '',
    sector: '',
    country: '',
    fullTimeEmployees: '',
    address: '',
    city: '',
    state: '',
    zip: '',
    price: '',
    dcf:  0,
    image: '',
    ipoDate: '',
  },
}
var DcfState = {
  dcf: {
    date: '',
    dcf: 0,
    stockPrice: 0,
  }
}
var RatioState = {
  ratios: {
    dividendYielPercentageTTM: 0,
    peRatioTTM: 0,
    pegRatioTTM: 0,
    returnOnAssetsTTM: 0,
    returnOnEquityTTM: 0,
    priceToBookRatioTTM: 0,
    debtRatioTTM: 0,
    debtEquityRatioTTM: 0,
    longTermDebtToCapitalizationTTM: 0,
  },
}
var TargetState = {
  targets: {
    symbol: '',
    updatedDate: '',
    priceTargetAverage: 0,
    priceTargetHigh: 0,
    priceTargetLow: 0,
    numberOfAnalysts: 0,
    currency: '',
  },
}
var RatingsState = {
  ratings: {
    date: '',
    ratingScore: 0,
    ratingDetailsDCFScore: 0,
    ratingDetailsROAScore: 0,
    ratingDetailsDEScore: 0,
    ratingDetailsPEScore: 0,
    ratingDetailsPBScore: 0,
  },
}
var GrowthState = {
  growth: {
    ebitgrowth: 0,
    revenueGrowth: 0,
    epsgrowth: 0,
    debtGrowth: 0,
    dividendsperShareGrowth: 0,
  }
}
var NewsState = {
  news: {
    image: '',
    publishedDate: '',
    site: '',
    symbol: '',
    text: '',
    title: '',
    url: '',
  },
}
var AttributeState = {
  attributes: {
    growth: [{
      price_target_to_share_price: 0,
      price_target_to_share_price_pct: 0,
      ebitgrowth: 0,
      ebitgrowth_pct: 0,
      ebitgrowth_rank: 0,
      epsgrowth: 0,
      epsgrowth_pct: 0,
      epsgrowth_rank: 0,
      revenueGrowth: 0,
      revenueGrowth_pct: 0,
      revenueGrowth_rank: 0,
    }],
    value: [{
      symbol: '',
      dcf_to_share_price: 0,
      price_target_to_share_price_pct: 0,
      price_target_to_share_price_rank: 0,
      peRatioTTM_pct: 0,
      peRatioTTM_rank: 0,
      pegRatioTTM: 0,
      pegRatioTTM_pct: 0,
      pegRatioTTM_rank: 0,
      priceToBookRatioTTM: 0,
      priceToBookRatioTTM_pct: 0,
      priceToBookRatioTTM_rank: 0,
      pe_ratio: 0,
    }],
    capef: [{
      returnOnAssetsTTM: 0,
      returnOnAssetsTTM_pct: 0,
      returnOnAssetsTTM_rank: 0,
      returnOnEquityTTM: 0,
      returnOnEquityTTM_pct: 0,
      returnOnEquityTTM_rank: 0,
    }],
    debt: [{
      debtEquityRatioTTM: 0,
      debtEquityRatioTTM_pct: 0,
      debtEquityRatioTTM_rank: 0,
      longTermDebtToCapitalizationTTM: 0,
      longTermDebtToCapitalizationTTM_pct: 0,
      longTermDebtToCapitalizationTTM_rank: 0,
      debtGrowth: 0,
      debtGrowth_pct: 0,
      debtGrowth_rank: 0,
      debtToAssets: 0,
      debtToAssets_pct: 0,
      debtToAssets_rank: 0,
    }],
    div: [{
      dividendsperShareGrowth: 0,
      dividendsperShareGrowth_pct: 0,
      dividendsperShareGrowth_rank: 0,
      dividendYielPercentageTTM: 0,
      dividendYielPercentageTTM_pct: 0,
      dividendYielPercentageTTM_rank: 0,
    }],
    key_metrics: [{
      revenuePerShare: 0,
      netIncomePerShare: 0,
      operatingCashFlowPerShare: 0,
      cashPerShare: 0,
      bookValuePerShare: 0,
      marketCap: 0,
      enterpriseValue : 0,
      peRatio: 0,
      debtToEquity: 0,
      debtToAssets: 0,
      dividendYield: 0,
      roe: 0,
    }],
    targets: [{
      symbol: '',
      updatedDate: '',
      priceTargetAverage: 0,
      priceTargetHigh: 0,
      priceTargetLow: 0,
      numberOfAnalysts: 0,
      currency: '',
    }],
    ratios: [{
      dividendYielPercentageTTM: 0,
      peRatioTTM: 0,
      pegRatioTTM: 0,
      returnOnAssetsTTM: 0,
      returnOnEquityTTM: 0,
      priceToBookRatioTTM: 0,
      debtRatioTTM: 0,
      debtEquityRatioTTM: 0,
      longTermDebtToCapitalizationTTM: 0,
    }],
    ratings: [{ 
      date: '',
      ratingScore: 0,
      ratingDetailsDCFScore: 0,
      ratingDetailsROAScore: 0,
      ratingDetailsDEScore: 0,
      ratingDetailsPEScore: 0,
      ratingDetailsPBScore: 0,
    }]
  }
}

var StockProfileState = {
  pk: '',
  sk: '',
  symbol: '',
  profile: ProfileState,
  dcf: DcfState,
  ratios: RatioState,
  targets: TargetState,
  ratings: RatingsState,
  growth: GrowthState,
  news: NewsState,
  attributes: AttributeState,
}

export interface ModalState {
  currentUser?: CurrentUser;
  historicalPricing: HistoricalPricingType;
  stockProfile: StockProfileType;
}

export interface ModelType {
  namespace: string;
  state: ModalState;
  reducers: {
    save: Reducer<ModalState>;
    clear: Reducer<ModalState>;
  };
  effects: {
    init: Effect;
    fetchCurrentUser: Effect;
    fetchStockProfile: Effect;
    fetchHistoricalPricing: Effect;
  };
}

const Model: ModelType = {
  namespace: 'stockAndprofile',
  state: {
    currentUser: {
      name: '',
      avatar: '',
      userid: '',
      email: '',
      tags: [],
      notifyCount: 0,
      unreadCount: 0,
      country: '',
      phone: '',
    },
    stockProfile: StockProfileState,
    historicalPricing: {
      symbol: '',
      historical: []
    }
  },
  
  effects: {
    *init(_, { put }) {
      yield put({ type: 'fetchCurrentUser' });
      yield put({ type: 'fetchStockProfile' });
      yield put({ type: 'fetchHistoricalPricing' });
    },

    *fetchCurrentUser(_, { call, put }) {
      const response = yield call(queryAntCurrent);
      console.log('STOCK QUERY ANT CURRENT: ', response, 'type: ', typeof response)
      yield put({
        type: 'save',
        payload: {
          currentUser: Object.keys(response).length > 1 ? response : {},
        },
      });
    },
    *fetchStockProfile(_, { call, put }) {
      const response = yield call(queryStockProfile, 'AAPL');
      console.log('RESPONSE', response)

      yield put({
        type: 'save',
        payload: {
          stockProfile: Object.keys(response).length > 1 ? response : {},
        },
      });
    },
    *fetchHistoricalPricing(_, { call, put }) {
      const response = yield call(queryHistorical, 'AAPL');
      console.log('RESPONSE', response)
      yield put({
        type: 'save',
        payload: {
          historicalPricing: Object.keys(response).length > 1 ? response : {},
        },
      });
    },
  },
  reducers: {
    save(state, { payload }) {
      return {
        ...state,
        ...payload,
      };
    },
    clear() {
      return {
        currentUser: {},
        stockProfile: StockProfileState,
        historicalPricing: {
          symbol: '',
          historical: []
        }
      }
    }
  },
};

export default Model;
