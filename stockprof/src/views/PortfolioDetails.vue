<template>
  <div class="page-portfolio-details">
    <h1 class="title">Sector : {{ category }}</h1>
    <div style="text-align: left;">
      <button @click="editable = true" class="btn btn-primary mt-4">Edit</button>
    </div>
    <div
      v-if="outlierFinancialratio && outlierFinancialratio.length > 0 && outlierStocks && outlierStocks.length > 0 && stockTypeOptions && stockTypeOptions.length > 0"
      class="box mt-6 box has-background-white border border-primary border-2 my-5">
      <h2 class="title">Outlier Stocks</h2>
      <table class="table table-striped table-bordered table-sm ">
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
            <th class="text-center" scope="col">Stock Type</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(financialRatio, index) in outlierFinancialratio" :key="index">
            <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">
              {{ this.outlierStocks[index].Name }}</td>
            <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">
              {{ this.outlierStocks[index].Symbol }}</td>
            <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">
              {{ (financialRatio[0]).assetturnover }}</td>
            <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">
              {{ (financialRatio[0]).quickratio }}</td>
            <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">
              {{ (financialRatio[0]).debttoequity }}</td>
            <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">
              {{ (financialRatio[0]).roe }}</td>
            <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">
              {{ (financialRatio[0]).dividendyield }}</td>
            <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">
              {{ (financialRatio[0]).pricetoearnings }}</td>
            <td scope="row" v-if="OutlierCapitalGainLoss.length > 0">{{
              OutlierCapitalGainLoss[index].toFixed(2) }}%</td>
            <td scope="row">
                <div v-if="editable" >
                  <div class="select is-small mb-3 mr-3">
                  <select v-model="stockTypeOptions[index]" @change="showOutlierInput(index)">
                    <option value="Outperforming">Outpeforming</option>
                    <option value="Underperforming">Underperforming</option>
                    <option value="custom">Custom</option>
                  </select>
                  </div>
                  <input v-if="showOutlierTextInput[index]" v-model="stockTypeOptions[index]" class="input is-small"
                    type="text" style="width:120px;" placeholder="Stock type">
                </div>
                <div v-if="editable == false" class=" is-small mb-3 mr-3">
                  <input :value="stockTypeOptions[index]" disabled>
                </div>


              </td>
          </tr>
        </tbody>
      </table>

      <div class="columns is-multiline">
        <div class="column is-half" v-for="(outlierBoxPlotData, index) in outlierBoxPlotData" :key="outlierBoxPlotData.id"
          :class="{ 'is-12-mobile': (index % 2 === 0) }">
          <h2 class="title">{{ this.outlierTitle[index] }}</h2>
          <box-plot :box-plot-data="outlierBoxPlotData" :id="'box-plot-' + index"></box-plot>
          <div>
            <table class="table table-striped table-bordered table-sm my-6">
              <thead>
                <tr>
                  <th class="text-center" scope="col">Fianncial Ratio</th>
                  <th class="text-center" scope="col">Q1</th>
                  <th class="text-center" scope="col">Median</th>
                  <th class="text-center" scope="col">Q3</th>
                  <th class="text-center" scope="col">Min</th>
                  <th class="text-center" scope="col">Max</th>
                </tr>
              </thead>
              <tbody v-for="(data, index) in outlierBoxPlotData" v-bind:key="data.id">
                <td scope="row">{{ financial_ratios[index] }}</td>
                <td scope="row">{{ parseFloat(data.q1).toFixed(2) }}</td>
                <td scope="row">{{ parseFloat(data.q2).toFixed(2) }}</td>
                <td scope="row">{{ parseFloat(data.q3).toFixed(2) }}</td>
                <td scope="row">{{ parseFloat(data.min).toFixed(2) }}</td>
                <td scope="row">{{ parseFloat(data.max).toFixed(2) }}</td>
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <button v-if="editable" type="button" @click="OutlierStockProfile()" class="btn btn-primary mt-3">Outlier Stock
        Profile</button>
    </div>

    <div class="columns is-multiline box has-background-white border border-primary border-2 my-6">
      <div class="column is-full">
        <h3 class="title my-5 has-text-centered">Portfolio For Non-outlier stocks</h3>
      </div>
      <div class="column is-half" v-for="(boxPlotData, index) in boxPlotData" v-bind:key="boxPlotData.id">
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
              <tr v-for="stock in clusteredStocks[index]" v-bind:key="stock.id">
                <td scope="row" style="cursor: pointer;" @click="showChartDialog(stock.Symbol)">{{
                  stock.Name }}</td>
                <td scope="row" style="cursor: pointer;" @click="showChartDialog(stock.Symbol)">{{
                  stock.Symbol }}</td>
              </tr>
            </tbody>
          </table>
          <box-plot :box-plot-data="boxPlotData" :id="'cluster-box-plot-' + index"></box-plot>
          <div>
            <table class="table table-striped table-bordered table-sm my-6">
              <thead>
                <tr>
                  <th class="text-center" scope="col">Fianncial Ratio</th>
                  <th class="text-center" scope="col">Q1</th>
                  <th class="text-center" scope="col">Median</th>
                  <th class="text-center" scope="col">Q3</th>
                  <th class="text-center" scope="col">Min</th>
                  <th class="text-center" scope="col">Max</th>
                </tr>
              </thead>
              <tbody v-for="(data, index) in boxPlotData" v-bind:key="data.id">
                <td scope="row">{{ financial_ratios[index] }}</td>
                <td scope="row">{{ parseFloat(data.q1).toFixed(2) }}</td>
                <td scope="row">{{ parseFloat(data.q2).toFixed(2) }}</td>
                <td scope="row">{{ parseFloat(data.q3).toFixed(2) }}</td>
                <td scope="row">{{ parseFloat(data.min).toFixed(2) }}</td>
                <td scope="row">{{ parseFloat(data.max).toFixed(2) }}</td>
              </tbody>
            </table>
          </div>

        </div>
        <div class="label" v-if="ClusterCapitalGainLoss.length > 0">Capital Gain & Loss :
          {{ ClusterCapitalGainLoss[index].toFixed(2) }}%</div>
        <div class="field">
          <label class="label">Portfolio Type</label>
          <div class="control">
            <div v-if="editable">
              <div class="select is-rounded">
                <select v-model="portfolioTypeOptions[index]" @change="showInput(index)">
                  <option value="Aggressive">Aggressive</option>
                  <option value="Average">Average</option>
                  <option value="Defensive">Defensive</option>
                  <option value=Custom>Custom</option>
                </select>
              </div>
              <input v-if="showTextInput[index]" v-model="portfolioTypeOptions[index]" class="input my-4" type="text"
                placeholder="Portfolio type">
            </div>

            <div class="is-rounded" v-if="this.portfolioTypeOptions.length > 0 && editable == false">
              <input :value="portfolioTypeOptions[index]" disabled>

            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-if="chartId != ''">
      <stock-chart :show-modal="this.showModal" :ticker="this.chartId" @modal-closed="handleModalClosed"></stock-chart>
    </div>

    <button v-if="editable" @click="updateResult()" class="btn btn-primary mt-4">Update Results</button>

  </div>
</template>

<script>
import axios from "axios"
import BoxPlot from '@/components/BoxPlot'
import StockChart from '@/components/StockChart'
import { toast } from 'bulma-toast'

export default {
  name: 'PortfolioDetails',
  data() {
    return {
      id: this.$route.params.id,
      category: this.$route.params.category,
      clusteredStocksSymbols: [],
      outlierStocksSymbols: [],
      portfolioTypeOptions: [],
      clusteredStocks: [],
      outlierStocks: [],
      outlierFinancialratio: [],
      boxPlotData: [],
      outlierStockProfile: true,
      outlierBoxPlotData: [],
      portfolioTypeOptions: [],
      showTextInput: [],
      showOutlierTextInput: [],
      stockTypeOptions: [],
      ClusterCapitalGainLoss: [],
      OutlierCapitalGainLoss: [],
      editable: false,
      outlierTitle: [],
      saveResult_showModal: false,
      remark: '',
      financial_ratios: ['Total asset turnover', 'Cash ratio', 'Debt ratio', 'Return on equity', 'Dividend yield', 'Price earnings ratio'],
      showModal: false,
      chartId: '',

    }
  },
  components: {
    BoxPlot,
    StockChart
  },
  mounted() {
    console.log("test cattegory", this.$route.params.id)
    this.getHistoryDetails()

    document.title = 'Portfolio' + ' | StockProF'
  },
  methods: {
    showOutlierInput(index) {
      console.log(this.stockTypeOptions[index])
      if (this.stockTypeOptions[index] !== 'Outperforming' && this.stockTypeOptions[index] !== 'Underperforming') {
        this.showOutlierTextInput[index] = true;
        if (this.stockTypeOptions[index] == 'custom') {
          this.stockTypeOptions[index] = ''
          console.log(this.showOutlierTextInput[index])
        }
      }
      else {
        this.showOutlierTextInput[index] = false;
      }
    },
    showInput(index) {
      if (this.portfolioTypeOptions[index] !== 'Aggressive' && this.portfolioTypeOptions[index] !== 'Average' && this.portfolioTypeOptions[index] !== 'Defensive') {
        this.showTextInput[index] = true;
        if (this.portfolioTypeOptions[index] == 'Custom') {
          this.portfolioTypeOptions[index] = ''
        }
      }
      else {
        this.showTextInput[index] = false;
      }
    },
    handleModalClosed() {
      this.chartId = "";
    },
    showChartDialog(index) {
      console.log("index", index)
      this.showModal = true
      this.chartId = index
    },
    async getHistoryDetails() {
      await axios
        .get(`api/history/${this.id}`,)
        .then(response => {
          return axios.post(`api/user-portfolio-details`, {
            clusteredStocksSymbols: response.data[0].clusteredStocksSymbols,
            outlierStocksSymbols: response.data[0].outlierStocksSymbols
          })
            .then(response1 => {
              this.outlierStocksSymbols = response.data[0].outlierStocksSymbols
              this.portfolioTypeOptions = response.data[0].portfolioTypeOptions
              this.stockTypeOptions = response.data[0].stockTypeOptions
              this.outlierStocks = response1.data.outlier
              const outlierFinancialratio = response1.data.outlier.map(financial_ratios => financial_ratios.financial_ratios);
              this.outlierFinancialratio = outlierFinancialratio
              this.clusteredStocks = response1.data.portfolio
              for (let i = 0; i < response1.data.portfolio.length; i++) {
                const clustered_symbols = response1.data.portfolio[i].map(symbol => symbol.Symbol);
                this.clusteredStocksSymbols.push(clustered_symbols)
                if (response.data[0].portfolioTypeOptions[i] !== 'Aggressive' && response.data[0].portfolioTypeOptions[i] !== 'Average'  && response.data[0].portfolioTypeOptions[i] !== 'Defensive') {
                  this.showTextInput[i] = true
                }
                else {
                  this.showTextInput[i] = false
                }
              }
              for (let j = 0; j < response1.data.outlier.length; j++) {
                if (response.data[0].stockTypeOptions[j] !== 'Outperforming'  && response.data[0].stockTypeOptions[j] !== 'Underperforming'){
                  this.showOutlierTextInput[j]= true
                }
                else{
                  this.showOutlierTextInput[j] = false
                }
              }
              this.getBoxPlotData(this.clusteredStocksSymbols, 'portfolio')
              this.getComparison()
              this.OutlierStockProfile()
            })
            .catch(error => {
              console.log(error)
            })
        })
        .catch(error => {
          console.log(error)
        })

    },
    async getComparison() {
      await axios
        .post('api/comparison', {
          "portfolio_list": this.clusteredStocksSymbols,
          "outlier_list": this.outlierStocksSymbols,
          "initial_date": "2023-01-03",
          "final_date": "2023-03-17"
        })
        .then(response => {
          this.ClusterCapitalGainLoss = response.data.Portfolio
          this.OutlierCapitalGainLoss = response.data.Outlier
          console.log(this.ClusterCapitalGainLoss)
        })
        .catch(error => {
          console.log(error)
        }
        )
    },
    async getBoxPlotData(data, type) {
      console.log("data", data)

      await axios
        .post('api/portfolio/box-plot-data', {
          "portfolio_list": data,
          "Category": this.category
        })
        .then(response => {
          if (type == 'portfolio') {
            this.boxPlotData = response.data
            this.boxPlotData = this.groupBoxPlotData(this.boxPlotData)
          }
          else {
            this.outlierBoxPlotData = response.data
            this.outlierBoxPlotData = this.groupBoxPlotData(this.outlierBoxPlotData)
            console.log("this.outlierBoxPlotData", this.outlierBoxPlotData)
          }
        })
        .catch(error => {
          console.log(error)
        }
        )
    },
    groupBoxPlotData(arrOfObjects) {
      return arrOfObjects.reduce((result, value, index, array) => {
        if (index % 6 === 0) {
          result.push(array.slice(index, index + 6))
        }
        return result
      }, [])
    },
    async OutlierStockProfile() {
      const sortedArray = this.stockTypeOptions.sort();// sort the array in ascending order
      this.outlierTitle = [...new Set(sortedArray)];
      console.log("sortedArray", sortedArray)
      console.log("this.outlierTitle", this.outlierTitle)
      const indexMap = this.stockTypeOptions.reduce((acc, value, index) => {
        if (acc[value]) {
          acc[value].push(index);
        } else {
          acc[value] = [index];
        }
        return acc;
      }, {});
      console.log("indexMap", indexMap)
      const indexArray = Object.values(indexMap); // convert object values to an array
      console.log("indexArray", indexArray)
      const result = indexArray.map((sublist) =>
        sublist.map((index) => this.outlierStocksSymbols[index])
      );
      this.getBoxPlotData(result, 'outlier')
      this.outlierStockProfile = true
    },
     async updateResult() {
      await axios.put(`api/history/${this.id}`, {
        portfolioTypeOptions: this.portfolioTypeOptions,
        stockTypeOptions: this.stockTypeOptions
      }).then(response => {
        toast({
          message: 'Record updated',
          type: 'is-success',
          dismissible: true,
          pauseOnHover: true,
          duration: 4000,
          position: 'bottom-right',
        })
        console.log(response);
      });
    }
  }
}
</script>