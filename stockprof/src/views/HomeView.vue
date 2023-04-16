<template>
  <div class="home">
    <head><link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css" integrity="sha512-..." crossorigin="anonymous" />
  </head>
    <div class="field has-addons columns is-flex justify-content-center">
      <div class="column is-half">
        <div class="dropdown">
          <button class="btn btn-primary dropdown-toggle" type="button" id="dropdownMenuButton1" data-bs-toggle="dropdown"
            aria-expanded="false">
            Category : {{ value }}
          </button>
          <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1" role="menu">
            <li v-for="option in options" :key="option">
              <a class="dropdown-item" @click="value = option; filterStock()" href="javascript:void(0)">{{ option }}</a>
            </li>
          </ul>
        </div>
        <button v-if="this.value != ''" to="portfolio" @click="navigateToPortfolio" type="button"
          class="btn btn-primary">GeneratePortfolio</button>
      </div>
    </div>
    <label class="text-centered label">*The generation of the portfolio based the category selected</label>
    <div class="box">
      <div class="columns">
        <div class="column  is-flex ">
          <div class="control">
            <input class="input" type="text" placeholder="Find the stocks">
          </div>
          <div>
            <a class="button is-info">
              Search
            </a>
          </div>
        </div>
        <h2 class="subtitle column is-one-third has-text-right">{{ this.total_stocks }} stocks found.</h2>
      </div>
      <div>
        <table class="table table-striped table-bordered table-sm">
          <thead>
            <tr>
                    <th class="text-center" scope="col">
          Name
          <span class="float-right">
            <i class="fa fa-sort-amount-down"></i>
          </span>
        </th>
        <th class="text-center" scope="col">
          Code
          <span class="float-right">
            <i class="fa fa-sort-amount-down"></i>
          </span>
        </th>
        <th class="text-center" scope="col">
          Category
          <span class="float-right">
            <i class="fa fa-sort-amount-down"></i> 
          </span>
        </th>
        <th class="text-center" scope="col">
          Total asset turnover
          <span class="float-right">
            <i class="fa fa-sort-amount-down"></i> 
          </span>
        </th>
        <th class="text-center" scope="col">
          Cash ratio
          <span class="float-right">
            <i class="fa fa-sort-amount-down"></i>
          </span>
        </th>
        <th class="text-center" scope="col">
          Debt ratio
          <span class="float-right">
            <i class="fa fa-sort-amount-down"></i>
          </span>
        </th>
        <th class="text-center" scope="col">
          Return on equity
          <span class="float-right">
            <i class="fa fa-sort-amount-down"></i>
          </span>
        </th>
        <th class="text-center" scope="col">
          Dividend yield
          <span class="float-right">
            <i class="fas fa-sort-amount-down"></i>
          </span>
        </th>
        <th class="text-center" scope="col">
          Price earnings ratio
          <span class="float-right">
            <i class="fas fa-sort-amount-down"></i>
          </span>
        </th>
              <th class="text-center" scope="col"></th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(financialRatio, index) in financialRatio" :key="index">
              <td scope="row">{{ this.stocks[index].Name }}</td>
              <td scope="row">{{ this.stocks[index].Symbol }}</td>
              <td scope="row">{{ this.stocks[index].Category }}</td>
              <td scope="row">{{ financialRatio[0].assetturnover }}</td>
              <td scope="row">{{ financialRatio[0].quickratio }}</td>
              <td scope="row">{{ financialRatio[0].debttoequity }}</td>
              <td scope="row">{{ financialRatio[0].roe }}</td>
              <td scope="row">{{ financialRatio[0].dividendyield }}</td>
              <td scope="row">{{ financialRatio[0].pricetoearnings }}</td>
              <div>
                <td scope="row"><div
                    class="button is-dark mt-4" @click="showChartDialog(index)">View Chart</div>
                </td>    
              </div>
              
            </tr>           
          </tbody>
        </table>
        <nav class="pagination is-flex justify-content-between" role="navigation" aria-label="pagination">
          <div>
            <a v-if="currentPage > 1" class="pagination-previous" @click="loadPrevious()">Previous</a>
          </div>
          <div>
            <a class="pagination-next" @click="loadNext()">Next page</a>
          </div>
        </nav>
      </div>
    </div>
      <div v-if="chartId!=''">
            <stock-chart :show-modal="this.showModal" :ticker="this.chartId" @modal-closed="handleModalClosed"></stock-chart>
      </div>
  </div>
</template>

<script>
import axios from "axios"
import StockChart from '@/components/StockChart'
export default {
  name: 'Home',
  data() {
    return {
      stocks: [],
      financialRatio: [],
      selectedStocks: [],
      options: new Set([""]),
      value: '',
      currentPage: 1,
      total_stocks: 0,
      showModal : false,
      chartId:'',
    }
  },
  components: {
    StockChart
  },
  mounted() {
    this.getStocks()

    document.title = 'Home' + ' | StockProF'
  },
  methods: {
    handleModalClosed() {
      this.chartId = "";
    },
    showChartDialog(index){
      this.showModal = true
      this.chartId= this.stocks[index].Symbol
    },
    loadNext() {
      this.currentPage += 1
      if (this.value) {
        this.filterStock()
      }
      else
        this.getStocks()
    },
    loadPrevious() {
      if (this.currentPage <= 1) {
        this.currentPage = 1
      }
      else
        this.currentPage -= 1
      if (this.value) {
        this.filterStock()
      }
      else
        this.getStocks()
    },
    async getStocks() {
      await axios
        .get(`api/stocks/?page=${this.currentPage}`)
        .then(response => {
          return axios.get(`api/stocks/?disable_pagination=true`)
            .then(response1 => {
              this.stocks = response.data.results
              const financialRatio = response.data.results.map(financial_ratios => financial_ratios.financial_ratios);
              this.financialRatio = financialRatio
              const Category = response1.data.map(Category => Category.Category.split(',')[0].trim());
              Category.forEach(Category => this.options.add(Category));
              // const symbols = response1.data.result.map(symbol => symbol.Symbol);
              // this.selectedStocks = symbols
              this.total_stocks = response1.data.length
            })
        })
        .catch(error => {
          console.log(error)
        }
        )
    },
    async filterStock() {
      this.currentPage = 1
      await axios
        .get(`api/stocks/?page=${this.currentPage}&search=${this.value}`)
        .then(response => {
          return axios.get(`api/stocks/?disable_pagination=true&search=${this.value}`)
            .then(response1 => {
              this.stocks = response.data.results
              const financialRatio = response.data.results.map(financial_ratios => financial_ratios.financial_ratios);
              this.financialRatio = financialRatio
              const symbols = response1.data.map(symbol => symbol.Symbol);
              this.selectedStocks = symbols
              this.total_stocks = response1.data.length
            })
        })
        .catch(error => {
          console.log(error)
        }
        )
    },
    async navigateToPortfolio() {
      console.log("navigateToPortfolio", this.selectedStocks)
      this.$router.push({
        name: 'Portfolio',
        query: {
          selectedStocks: this.selectedStocks,
          category: this.value
        }
      })
    },

  }
}
</script>

<style scoped></style>