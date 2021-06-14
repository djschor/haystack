import React, { Component } from 'react';
import FusionCharts from 'fusioncharts';
import TimeSeries from 'fusioncharts/fusioncharts.timeseries';
import ReactFC from 'react-fusioncharts';

ReactFC.fcRoot(FusionCharts, TimeSeries);


import { PageLoading } from '@ant-design/pro-layout';
const jsonify = res => res.json();

const dataFetch = fetch(
  'https://s3.eu-central-1.amazonaws.com/fusion.store/ft/data/candlestick-chart-data.json'
).then(jsonify);
// This is the remote url to fetch the schema.
const schemaFetch = fetch(
  'https://s3.eu-central-1.amazonaws.com/fusion.store/ft/schema/candlestick-chart-schema.json'
).then(jsonify);

export default class ProTimeSeries extends React.Component {
  state = {
    loading: false,
    timeseriesDs: {
      type: 'timeseries',
      renderAt: 'container',
      width: '600',
      height: '400',
      dataSource: {
        caption: {
          text: 'Apple Inc. Stock Price'
        },
        yAxis: [
          {
            plot: {
              open: 'Open',
              high: 'High',
              low: 'Low',
              close: 'Close',
              type: 'candlestick'
            },
            title: 'Value'
          }
        ],
        // Initially data is set as null
        data: null
      }
    },
  };
  async componentDidMount() {
    const [dat, schem] = await Promise.all([dataFetch, schemaFetch]
    );
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
    const { timeseriesDs, loading } = this.state;
    return loading === false ? (
      <PageLoading />
    ) : (
      <ReactFC {...timeseriesDs}  />
    );
  }
}
