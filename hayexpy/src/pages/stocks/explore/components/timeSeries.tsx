import React from 'react';
import ReactFC from 'react-fusioncharts';
import FusionCharts from 'fusioncharts';
import Charts from 'fusioncharts/fusioncharts.charts';
import Widgets from 'fusioncharts/fusioncharts.widgets';
FusionCharts.options['license']({
  key: 'VnC3bqB-8A1I4A1B10C6C5A2B2C2E4F3B9sbdC4E3mmaA-21jA1B3awh1I2J3A4B6B5F5B4F3E3E3F2B6D4C7A3B4wjjH3B5D7jF4D5D3D-8buB6A6E3sudC1G2B1wikB1A4B4B2A21A14B12A4D8D5B4lffB2A5UA5vraA2A1A1pcB2DB2G2yyjC2B2C8D4E3D2G2F3A1B2D8D2D1F4p==',
  creditLabel: false,
})


ReactFC.fcRoot(FusionCharts, Widgets, Charts);

interface IOwnProps {
  belowAverageValue: string;
  averageValue: string;
  highValue: string;
  existingValue: string;
}

type IProp = IOwnProps;

class LinearChart extends React.PureComponent<IProp> {
  public async componentDidMount() {
    const [histoPrice] = await Promise.all([
      fetch(
        '/api/stock/historical/AAPL',
      ).then((d) => d.json()),
    ]);
    console.log('fetched histo: ', histoPrice)
    this.setState({
      data: histoPrice,
      loading: true,
    });
  }
  render() {
    const linearChartConfigs = {
      type : 'hlineargauge',
      width : '700',
      height : '150',
      dataFormat : 'json',
      dataSource : {
        chart: {
          caption: "Example Flow Chart",
          bgColor: '#f7fcff',
          upperLimit: this.props.highValue,
          chartTopMargin: '20',
          chartBottomMargin: '20',
          valueFontSize: '12',
          gaugeFillMix: '{light-30}',
          showValue: '1',
          majorTMNumber: '11',
          majorTMColor: '#1e5779',
          showBorder: '0',
        },
        colorRange: {
          color: [
            {
              maxValue: this.props.averageValue,
              code: '#FFC533',
              label: "averageValue",
            },
            {
              maxValue: this.props.belowAverageValue,
              code: '#F2726F',
              label: "belowAverageValue",
            },
            {
              maxValue: this.props.highValue,
              code: '#62B58F',
              label: "highValue",
            },
          ],
        },
        pointers: {
          pointer: [
            {
              value: this.props.existingValue,
              showValue: '0',
              radius: '10',
              bgColor: '#6400ff',
              BorderColor: '#6400ff',
            },
          ],
        },
        trendPoints: {
          point: [
            {
              startValue: this.props.existingValue,
              endValue: this.props.highValue,
              thickness: '1',
              markerColor: '#0075c2',
              markerBorderColor: '#666666',
              markerRadius: '5',
              alpha: '30',
              displayValue: ' ',
            },
            {
              startValue: this.props.averageValue,
              thickness: '1',
              useMarker: '1',
              markerColor: '#87dc9',
              markerBorderColor: '#fff',
              markerRadius: '5',
              displayValue: ('average' + '<br/>' + 'count:' + this.props.averageValue + '<br/>'),
            },
            {
              startValue: this.props.belowAverageValue,
              thickness: '1',
              useMarker: '1',
              markerColor: '#f5be416',
              markerBorderColor: '#fff',
              markerRadius: '5',
              displayValue: ('below average' + '<br/>' + 'count:' +this.props.belowAverageValue + '<br/>'),
            },
          ],
        },
      },
    };
    const { data, loading } = this.state;
    return <ReactFC {...linearChartConfigs} />;
  }
}

export default LinearChart;