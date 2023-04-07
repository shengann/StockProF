<template>
  <div class="page-portfolio">
    <!-- <h1 class="title">Sector : {{category}}</h1> -->
    <div v-if="outlierStocks.length > 1" class="box mt-6">
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

    <box-plot v-if="boxPlotData.length" :box-plot-data="boxPlotData"></box-plot>

    <div class="columns box">
      <div class="column is-one-third" v-for="(stockList, index) in clusteredStocks" v-bind:key="stockList.id">
        <div>
          <h2 class="title">Portfolio {{ index + 1 }}</h2>
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
import BoxPlot from '@/components/BoxPlot'
export default {
  name: 'PortfolioDetails',
  data() {
    return {
      id: this.$route.params.id,
      clusteredStocksSymbols: [],
      outlierStocksSymbols: [],
      portfolioTypeOptions: [],
      clusteredStocks: [],
      outlierStocks: [],
      outlierFinancialratio: [],
      boxPlotData: []
    }
  },
  components: {
    BoxPlot
  },
  mounted() {
    this.getHistoryDetails()

    document.title = 'Portfolio' + ' | StockProF'
  },
  methods: {
    async getHistoryDetails() {
      await axios
        .get(`api/history/${this.id}`,)
        .then(response => {
          return axios.post(`api/user-portfolio-details`, {
            clusteredStocksSymbols: response.data[0].clusteredStocksSymbols,
            outlierStocksSymbols: response.data[0].outlierStocksSymbols
          })
            .then(response1 => {
              this.clusteredStocksSymbols = response.data[0].clusteredStocksSymbols
              this.outlierStocksSymbols = response.data[0].outlierStocksSymbols
              this.clusteredStocks = response1.data.portfolio
              this.outlierStocks = response1.data.outlier
              const outlierFinancialratio = response1.data.outlier.map(financial_ratios => financial_ratios.financial_ratios);
              this.outlierFinancialratio = outlierFinancialratio
              this.getBoxPlotData()
            })
            .catch(error => {
              console.log(error)
            })
        })
        .catch(error => {
          console.log(error)
        })

    },
    async getBoxPlotData() {
      await axios
        .post('api/portfolio/box-plot-data', {
          "portfolio_list": this.clusteredStocksSymbols
        })
        .then(response => {
          this.boxPlotData = response.data
        })
        .catch(error => {
          console.log(error)
        }
        )
    }
  }
}
</script>