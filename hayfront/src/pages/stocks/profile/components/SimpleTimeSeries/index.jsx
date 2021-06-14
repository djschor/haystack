import * as React from 'react';
import FusionCharts from 'fusioncharts';
import TimeSeries from 'fusioncharts/fusioncharts.timeseries';
import ReactFC from 'react-fusioncharts';
import { PageLoading } from '@ant-design/pro-layout';

FusionCharts.options['license']({
  key: 'VnC3bqB-8A1I4A1B10C6C5A2B2C2E4F3B9sbdC4E3mmaA-21jA1B3awh1I2J3A4B6B5F5B4F3E3E3F2B6D4C7A3B4wjjH3B5D7jF4D5D3D-8buB6A6E3sudC1G2B1wikB1A4B4B2A21A14B12A4D8D5B4lffB2A5UA5vraA2A1A1pcB2DB2G2yyjC2B2C8D4E3D2G2F3A1B2D8D2D1F4p==',
  creditLabel: false,
})

ReactFC.fcRoot(FusionCharts, TimeSeries);

export default class SimpleTimeSeries extends React.Component {
  state = {
    loading: false,
    timeseriesDs: {
      type: 'timeseries',
      renderAt: 'container',
      width: '600',
      height: '400',
      dataSource: {
          caption: { text: 'Historical Price Movement' },
          data: null,
          yAxis: [{
              plot: [{
                  value: 'Apple Stock Price'
              }]
          }]
      }
    }
    
  };
  async componentDidMount() {
    const [dat, schem] = await Promise.all([
      fetch(
        'http://localhost:8080/api/stock/historicaldata/AAPL',
      ).then((d) => d.json()),
      fetch(
        'http://localhost:8080/api/stock/timeschema',
      ).then((d) => d.json()),
    ]);
    const fusionTable = new FusionCharts.DataStore().createDataTable(dat, schem);
    console.log('got fusion table', fusionTable)
    const timeseriesDs = Object.assign({}, this.state.timeseriesDs);
    timeseriesDs.dataSource.data = fusionTable;
    this.setState({
      timeseriesDs,
      loading: true,
    });
  } 
  render() {
    const { loading, timeseriesDs } = this.state;
    console.log(timeseriesDs)
    return loading === false ? (
      <PageLoading />
    ) : (
      <div>
        <ReactFC {...timeseriesDs}  />
      </div>
    );
  }
}

