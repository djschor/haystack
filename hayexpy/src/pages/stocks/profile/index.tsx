import React, {Component} from 'react';
import {PageContainer} from '@ant-design/pro-layout';
import styles from './style.less';
import type {Dispatch} from'umi';
import {Link, connect} from'umi';
import type {CurrentUser, HistoricalPricingType, StockProfileType} from './data.d';
import type {ModalState} from './model';
import {Avatar, Skeleton, Statistic, Col, Row, Card} from'antd';
// import { AppleFilled } from '@ant-design/icons';

interface ProfileProps {
  currentUser?: CurrentUser;
  historicalPricing: HistoricalPricingType[];
  stockProfile: StockProfileType[];
  dispatch: Dispatch;
  currentUserLoading: boolean;
  pricingLoading: boolean;
  stockProfileLoading: boolean;
}

const PageHeaderContent: React.FC<{ currentUser: CurrentUser }> = ({ currentUser }) => {
  const loading = currentUser && Object.keys(currentUser).length;
  if (!loading) {
    return <Skeleton avatar paragraph={{ rows: 1 }} active />;
  }
  return (
    <div className={styles.pageHeaderContent}>
      <div className={styles.avatar}>
        <Avatar size="large" src={currentUser.avatar} />
      </div>
      <div className={styles.content}>
        <div className={styles.contentTitle}>
          {currentUser.name}
        </div>
        <div>
          {currentUser} |{currentUser.name}
        </div>
      </div>
    </div>
  );
};

const ExtraContent: React.FC<{}> = () => (
  <div className={styles.extraContent}>
    <div className={styles.statItem}>
      <Statistic title="Number of items" value={56} />
    </div>
    <div className={styles.statItem}>
      <Statistic title="Rank within the team" value={8} suffix="/ 24" />
    </div>
    <div className={styles.statItem}>
      <Statistic title="Project access" value={2223} />
    </div>
  </div>
);

class Profile extends Component<ProfileProps> {
  componentDidMount() {
    const {dispatch} = this.props;
    dispatch({
      type:'stockAndprofile/init',
    });
    console.log('finished mounting')
  }

  componentWillUnmount() {
    const {dispatch} = this.props;
    dispatch({
      type:'stockAndprofile/clear',
    });
  }
  render() {
    const {
      currentUser, 
      historicalPricing, 
      stockProfile,
      pricingLoading,
      stockProfileLoading,
    } = this.props;

    if (!currentUser || !currentUser.userid) {
      return null;
    }
    return (
      <PageContainer
        content={<PageHeaderContent currentUser={currentUser} />}
        extraContent={<ExtraContent />}
      >
        <Row gutter={24}>
          <Col xl={16} lg={24} md={24} sm={24} xs={24}>
            <Card
                bodyStyle={{ paddingTop: 12, paddingBottom: 12 }}
                bordered={false}
                title="Profile"
                loading={stockProfileLoading}
              >
                <div className={styles.members}>
                  <Row gutter={24}>
                    {/* {stockProfile.map((item) => (
                      <Col span={12} key={`${item.symbol}`}>
                        <Link to={item.profile.website}>
                          <Avatar src={item.profile.image} size="small" />
                          <span className={styles.member}>{item.profile.description}</span>
                        </Link>
                      </Col>
                    ))} */}
                    {stockProfile}
                  </Row>
                </div>
              </Card>
              <Card
                bodyStyle={{ paddingTop: 12, paddingBottom: 12 }}
                bordered={false}
                title="Historical Price Chart"
                loading={pricingLoading}
              >
                <div className={styles.members}>
                    {historicalPricing}
{/*                     
                    {historicalPricing.map((item) => (
                      <Col span={12} key={`${item.symbol}`}>
                        <Link to={'apple.com'}>
                          <span className={styles.member}>{item.historical[0].date}</span>
    
                        </Link>
                      </Col>
                    ))} */}
                </div>
              </Card>
          </Col>
          <Col xl={8} lg={24} md={24} sm={24} xs={24}>
          </Col>
        </Row>
    </PageContainer>
    );
  }
}

export default connect(
  ({
    stockAndprofile: {currentUser, historicalPricing, stockProfile},
    loading,
  }: {
    stockAndprofile: ModalState;
    loading: {
      effects: Record<string, boolean>;
    };
  }) => ({
    currentUser,
    historicalPricing,
    stockProfile,
    currentUserLoading: loading.effects['stockAndprofile/fetchCurrentUser'],
    pricingLoading: loading.effects['stockAndprofile/fetchHistoricalPricing'],
    stockProfileLoading: loading.effects['stockAndprofile/fetchStockProfile'],
  }),
)(Profile);