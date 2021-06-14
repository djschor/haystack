export interface TagType {
  key: string;
  label: string;
}
export interface VisitDataType {
  x: string;
  y: number;
}

export interface SearchDataType {
  index: number;
  keyword: string;
  count: number;
  range: number;
  status: number;
}

export interface OfflineDataType {
  name: string;
  cvr: number;
}

export interface OfflineChartData {
  x: any;
  y1: number;
  y2: number;
}

export interface AnalysisData {
  visitData: VisitDataType[];
  visitData2: VisitDataType[];
  salesData: VisitDataType[];
  searchData: SearchDataType[];
  offlineData: OfflineDataType[];
  offlineChartData: OfflineChartData[];
  salesTypeData: VisitDataType[];
  salesTypeDataOnline: VisitDataType[];
  salesTypeDataOffline: VisitDataType[];
}

export interface CurrentUser {
  name: string;
  avatar: string;
  userid: string;
  email: string;
  tags: TagType[];
  notifyCount: number;
  unreadCount: number;
  country: string;
  phone: string;
}
export interface Member {
  avatar: string;
  name: string;
  id: string;
}
export interface HistoricalType {
  date: string;
  close: number;
}
export interface HistoricalPricingType {
  symbol: string;
  historical: HistoricalType[];
}

export interface ProfileType { 
  profile: { 
    name: string;
    currency: string;
    exchange: string;
    industry: string;
    website: string;
    description: string;
    ceo: string;
    sector: string;
    country: string;
    fullTimeEmployees: string;
    address: string;
    city: string;
    state: string;
    zip: string;
    price: string;
    dcf:  number;
    image: string;
    ipoDate: string;
  };
}
export interface DcfType {
  dcf: {
    date: string;
    dcf: number;
    stockPrice: number;
  }
}
export interface RatioType {
  ratios: {
    dividendYielPercentageTTM: number;
    peRatioTTM: number;
    pegRatioTTM: number;
    returnOnAssetsTTM: number;
    returnOnEquityTTM: number;
    priceToBookRatioTTM: number;
    debtRatioTTM: number;
    debtEquityRatioTTM: number;
    longTermDebtToCapitalizationTTM: number;
  };
}
export interface TargetType {
  targets: {
    symbol: string;
    updatedDate: string;
    priceTargetAverage: number;
    priceTargetHigh: number;
    priceTargetLow: number;
    numberOfAnalysts: number;
    currency: string;
  };
}
export interface RatingsType {
  ratings: {
    date: string;
    ratingScore: number;
    ratingDetailsDCFScore: number;
    ratingDetailsROAScore: number;
    ratingDetailsDEScore: number;
    ratingDetailsPEScore: number;
    ratingDetailsPBScore: number;
  };
}
export interface GrowthType {
  growth: {
    ebitgrowth: number;
    revenueGrowth: number;
    epsgrowth: number;
    debtGrowth: number;
    dividendsperShareGrowth: number;
  }
}

export interface NewsType {
  news: {
    image: string;
    publishedDate: string;
    site: string;
    symbol: string;
    text: string;
    title: string;
    url: string;
  };
}
export interface AttributesType {
  attributes: {
    growth: [{
      price_target_to_share_price: number;
      price_target_to_share_price_pct: number;
      ebitgrowth: number;
      ebitgrowth_pct: number;
      ebitgrowth_rank: number;
      epsgrowth: number;
      epsgrowth_pct: number;
      epsgrowth_rank: number;
      revenueGrowth: number;
      revenueGrowth_pct: number;
      revenueGrowth_rank: number;
    }];
    value: [{
      symbol: number;
      dcf_to_share_price: number;
      price_target_to_share_price_pct: number;
      price_target_to_share_price_rank: number;
      peRatioTTM_pct: number;
      peRatioTTM_rank: number;
      pegRatioTTM: number;
      pegRatioTTM_pct: number;
      pegRatioTTM_rank: number;
      priceToBookRatioTTM: number;
      priceToBookRatioTTM_pct: number;
      priceToBookRatioTTM_rank: number;
      pe_ratio: number;
    }];
    capef: [{
      returnOnAssetsTTM: number;
      returnOnAssetsTTM_pct: number;
      returnOnAssetsTTM_rank: number;
      returnOnEquityTTM: number;
      returnOnEquityTTM_pct: number;
      returnOnEquityTTM_rank: number;
    }];
    debt: [{
      debtEquityRatioTTM: number;
      debtEquityRatioTTM_pct: number;
      debtEquityRatioTTM_rank: number;
      longTermDebtToCapitalizationTTM: number;
      longTermDebtToCapitalizationTTM_pct: number;
      longTermDebtToCapitalizationTTM_rank: number;
      debtGrowth: number;
      debtGrowth_pct: number;
      debtGrowth_rank: number;
      debtToAssets: number;
      debtToAssets_pct: number;
      debtToAssets_rank: number;
    }];
    div: [{
      dividendsperShareGrowth: number;
      dividendsperShareGrowth_pct: number;
      dividendsperShareGrowth_rank: number;
      dividendYielPercentageTTM: number;
      dividendYielPercentageTTM_pct: number;
      dividendYielPercentageTTM_rank: number;
    }];
    key_metrics: [{
      revenuePerShare: number;
      netIncomePerShare: number;
      operatingCashFlowPerShare: number;
      cashPerShare: number;
      bookValuePerShare: number;
      marketCap: number;
      enterpriseValue : number;
      peRatio: number;
      debtToEquity: number;
      debtToAssets: number;
      dividendYield: number;
      roe: number;
    }];
    targets: [{
      symbol: string;
      updatedDate: string;
      priceTargetAverage: number;
      priceTargetHigh: number;
      priceTargetLow: number;
      numberOfAnalysts: number;
      currency: string;
    }];
    ratios: [{
      dividendYielPercentageTTM: number;
      peRatioTTM: number;
      pegRatioTTM: number;
      returnOnAssetsTTM: number;
      returnOnEquityTTM: number;
      priceToBookRatioTTM: number;
      debtRatioTTM: number;
      debtEquityRatioTTM: number;
      longTermDebtToCapitalizationTTM: number;
    }];
    ratings: [{ 
      date: string;
      ratingScore: number;
      ratingDetailsDCFScore: number;
      ratingDetailsROAScore: number;
      ratingDetailsDEScore: number;
      ratingDetailsPEScore: number;
      ratingDetailsPBScore: number;
    }]
  }
}
export interface StockProfileType {
  pk: string;
  sk: string;
  symbol: string;
  profile: ProfileType;
  dcf: DcfType;
  ratios: RatioType;
  targets: TargetType;
  ratings: RatingsType;
  growth: GrowthType;
  news: NewsType[];
  attributes: AttributesType;
  
}


export interface ActivitiesType {
  id: string;
  updatedAt: string;
  user: {
    name: string;
    avatar: string;
  };
  group: {
    name: string;
    link: string;
  };
  project: {
    name: string;
    link: string;
  };

  template: string;
}
