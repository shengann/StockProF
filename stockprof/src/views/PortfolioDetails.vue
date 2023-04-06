<template>
    <div class="page-portfolio">   
        <!-- <h1 class="title">Sector : {{category}}</h1> -->
        <div v-if="outlierStocks.length>1" class="box mt-6">
            <h2 class="title">Outlier Stocks</h2>

            <table class="table table-striped table-bordered table-sm">
            <thead>
              <tr>
                <th class="text-center" scope="col">Name</th>
                <th class="text-center" scope="col">Code</th>
                <th class="text-center" scope="col">Total asset turnover</th>
                <th class="text-center" scope="col">Cash ratio</th>
                <th class="text-center" scope="col">Debt ratio</th>
                <th class="text-center" scope="col">Return on equity </th>
                <th class="text-center" scope="col">Dividend yield</th>
                <th class="text-center" scope="col">Price earnings ratio </th>
                <th class="text-center" scope="col">Capital Gain/Loss </th>

              </tr>
            </thead>
            <tbody>
              <tr v-for="(financialRatio, index) in outlierFinancialratio" :key="index">
                <td scope="row">{{ this.outlierStocks[index].Name }}</td>
                <td scope="row">{{ this.outlierStocks[index].Symbol }}</td>
                <td scope="row">{{ financialRatio[0].assetturnover }}</td>
                <td scope="row">{{ financialRatio[0].quickratio }}</td>
                <td scope="row">{{ financialRatio[0].debttoequity }}</td>
                <td scope="row">{{ financialRatio[0].roe }}</td>
                <td scope="row">{{ financialRatio[0].dividendyield }}</td>
                <td scope="row">{{ financialRatio[0].pricetoearnings }}</td>
                <td scope="row"></td>
              </tr>
            </tbody>
          </table>
        </div>

        <div id="plot" class="my-6"></div> 

        <div class="columns box">
            <div class="column is-one-third"
            v-for="(stockList,index) in clusteredStocks"
            v-bind:key="stockList.id">
                <div>
                    <h2 class="title">Portfolio {{index+1}}</h2>
                    <table class="table table-striped table-bordered table-sm">
                    <thead>
                    <tr>
                        <th class="text-center" scope="col">Name</th>
                        <th class="text-center" scope="col">Code</th>
                    </tr>
                    </thead>
                    <tbody>
                    <tr v-for="stock in stockList" v-bind:key="stock.id">
                        <td scope="row">{{ stock.Name }}</td>
                        <td scope="row">{{ stock.Symbol }}</td>
                    </tr>
                    </tbody>
                    </table>
                </div>
                <!-- <div class="field">
                    <label class="label">Portfolio Type</label>
                    <div class="control">
                        <div class="select is-rounded">
                            <select v-model="portfolioTypeOptions[index]" @change="showInput(index)">
                                <option value="Aggressive">Aggressive</option>
                                <option value="Average">Average</option>
                                <option value="Defensive">Defensive</option>
                                <option value=Custom>Custom</option>
                            </select>
                        </div>
                    </div>
                </div> -->
                <!-- <input 
                    v-if="showTextInput[index]"
                    v-model="portfolioTypeOptions[index]" 
                    class="input my-4" type="text" 
                    placeholder="Portfolio type"
                > -->
            
            </div>
        </div>

    </div> 
</template>

<script>
import axios from "axios"
import * as d3 from 'd3';
export default {
  name: 'PortfolioDetails',
  data() {
    return {
      id : this.$route.params.id,
      clusteredStocksSymbols :[],
      outlierStocksSymbols:[],
      portfolioTypeOptions: [],
      clusteredStocks: [],
      outlierStocks: [],
      outlierFinancialratio: [],
      boxPlotData: []
    }
  },
    mounted() {
        this.getHistoryDetails()

        document.title = 'Portfolio' + ' | StockProF'
    },
    methods :{
       async getHistoryDetails(){
        await axios
          .get(`api/history/${this.id}`,)
          .then(response =>{
            return axios.post(`api/user-portfolio-details`,{
              clusteredStocksSymbols : response.data[0].clusteredStocksSymbols,
              outlierStocksSymbols : response.data[0].outlierStocksSymbols
            })
              .then(response1=>{
                this.clusteredStocksSymbols= response.data[0].clusteredStocksSymbols
                this.outlierStocksSymbols = response.data[0].outlierStocksSymbols
                this.clusteredStocks = response1.data.portfolio
                this.outlierStocks = response1.data.outlier
                const outlierFinancialratio = response1.data.outlier.map(financial_ratios => financial_ratios.financial_ratios);
                this.outlierFinancialratio = outlierFinancialratio
                this.getBoxPlotData()
              })
              .catch(error =>{
                console.log(error)
              })
          })
          .catch(error=>{
            console.log(error)
          })

      },
              async getBoxPlotData() {
            await axios
                .post('api/portfolio/box-plot-data',{
                    "portfolio_list": this.clusteredStocksSymbols
                }) 
                .then(response => {
                    this.boxPlotData = response.data

                    const margin = { top: 10, right: 30, bottom: 30, left: 40 };
                    const width = 1600 - margin.left - margin.right;
                    const height = 400 - margin.top - margin.bottom;

                    // append the svg object to the selected DOM element
                    const svg = d3.select("#plot")
                        .append('svg')
                        .attr('width', width + margin.left + margin.right)
                        .attr('height', height + margin.top + margin.bottom)
                        .append('g')
                        .attr('transform', `translate(${margin.left},${margin.top})`);

                    // Compute quartiles, median, inter quantile range min and max
                    const sumstat = this.boxPlotData.map((d) => {
                        const q1 = d.q1;
                        const median = d.q2;
                        const q3 = d.q3;
                        const interQuantileRange = d.iqr;
                        const min = q1 - 1.5 * interQuantileRange;
                        const max = q3 + 1.5 * interQuantileRange;
                        return ({ name: d.name, q1, median, q3, interQuantileRange, min, max });
                    });
                    
                    // Show the X scale
                    const x = d3.scaleBand()
                        .range([0, width])
                        .domain(this.boxPlotData.map((d) => d.name))
                        .paddingInner(1)
                        .paddingOuter(0.5);
                    svg.append('g')
                        .attr('transform', `translate(0,${height})`)
                        .call(d3.axisBottom(x));

                    // Show the Y scale
                    const y = d3.scaleLinear()
                        .domain([-0.5, 1])
                        .range([height, 0]);
                    svg.append('g').call(d3.axisLeft(y));

                    // Show the main vertical line
                    svg
                        .selectAll('vertLines')
                        .data(sumstat)
                        .enter()
                        .append('line')
                        .attr('x1', (d) => x(d.name))
                        .attr('x2', (d) => x(d.name))
                        .attr('y1', (d) => y(d.min))
                        .attr('y2', (d) => y(d.max))
                        .attr('stroke', 'black')
                        .style('width', 40);

                    // rectangle for the main box
                    const boxWidth = 50;
                    svg
                        .selectAll('boxes')
                        .data(sumstat)
                        .enter()
                        .append('rect')
                        .attr('x', (d) => x(d.name) - boxWidth / 2)
                        .attr('y', (d) => y(d.q3))
                        .attr('height', (d) => y(d.q1) - y(d.q3))
                        .attr('width', boxWidth)
                        .attr('stroke', 'black')
                        .style('fill', '#69b3a2');

                    // Show the median
                    svg
                        .selectAll('medianLines')
                        .data(sumstat)
                        .enter()
                        .append('line')
                        .attr('x1', (d) => x(d.name) - boxWidth / 2)
                        .attr('x2', (d) => x(d.name) + boxWidth/2)
                        .attr("y1", function (d) { return (y(d.median)) }  )
                        .attr("y2", function (d) { return (y(d.median)) }  )
                        .attr("stroke", "black")
                        .style("width", 80)
                })
                .catch(error => {
                    console.log(error)
                }
                )
        }
    }
}
</script>