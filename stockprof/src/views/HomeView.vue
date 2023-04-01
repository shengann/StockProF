<template>
  <div class="home">
    <div class="field has-addons">
      <div class="control">
        <input class="input" type="text" placeholder="Find a repository">
      </div>
      <div class="control">
        <a class="button is-info">
          Search
        </a>
    </div>
    </div>
     <div class="dropdown">
      <button
        class="btn btn-primary dropdown-toggle"
        type="button" id="dropdownMenuButton1"
        data-bs-toggle="dropdown"
        aria-expanded="false">
        Category : {{ value }}
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1" role="menu">
        <li v-for="option in options" :key="option">
          <a class="dropdown-item"   @click="value = option; filterStock()" href="javascript:void(0)">{{ option }}</a>
        </li>
      </ul>
    </div>
    <button to="portfolio" @click="navigateToPortfolio" type="button"  class="btn btn-primary">Generate Portfolio</button> 

    <div class="box">
    <div>
      <table class="table table-striped table-bordered table-sm">
        <thead>
          <tr>
            <th class="text-center" scope="col">Name</th>
            <th class="text-center" scope="col">Code</th>
            <th class="text-center" scope="col">Category</th>
            <th class="text-center" scope="col">Total asset turnover</th>
            <th class="text-center" scope="col">Cash ratio</th>
            <th class="text-center" scope="col">Debt ratio</th>
            <th class="text-center" scope="col">Return on equity </th>
            <th class="text-center" scope="col">Dividend yield</th>
            <th class="text-center" scope="col">Price earnings ratio </th>
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
            <td scope="row"><router-link v-bind:to="this.stocks[index].get_absolute_url" class="button is-dark mt-4">View Chart</router-link></td>
          </tr>
        </tbody>
      </table>
      <nav class="pagination" role="navigation" aria-label="pagination">
    <a class="pagination-previous" @click="loadPrevious()">Previous</a>
    <a class="pagination-next" @click="loadNext()">Next page</a>
    <ul class="pagination-list">
      <li>
        <a class="pagination-link" aria-label="Goto page 1">1</a>
      </li>
      <li>
        <span class="pagination-ellipsis">&hellip;</span>
      </li>
      <li>
        <a class="pagination-link" aria-label="Goto page 45">45</a>
      </li>
      <li>
        <a class="pagination-link is-current" aria-label="Page 46" aria-current="page">46</a>
      </li>
      <li>
        <a class="pagination-link" aria-label="Goto page 47">47</a>
      </li>
      <li>
        <span class="pagination-ellipsis">&hellip;</span>
      </li>
      <li>
        <a class="pagination-link" aria-label="Goto page 86">86</a>
      </li>
    </ul>
  </nav>
    </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
export default {
  name: 'Home',
  data() {
    return {
      stocks: [],
      financialRatio:[],
      selectedStocks: [],
      options: new Set([""]),
      value: '',
      currentPage:  1,
    }
  },
  components: {
      // Vuetable
  },
  mounted() {
    this.getStocks()

    document.title = 'Home' + ' | Djacket'
  },
  methods: {
    loadNext(){
      this.currentPage +=1
      if (this.value){
        this.filterStock()
      }
      else
        this.getStocks()
    },
    loadPrevious(){
      if (this.currentPage<=1){
        this.currentPage =1
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
            const symbols = response1.data.result.map(symbol => symbol.Symbol);
            this.selectedStocks = symbols
          })
        })
        .catch(error => {
          console.log(error)
        }
        )
    },
    async filterStock(){
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
            })
        })
        .catch(error => {
          console.log(error)
        }
        )
    },
    async navigateToPortfolio(){
      console.log("navigateToPortfolio",this.selectedStocks)
      this.$router.push({
        name: 'Portfolio',
        query: {
          selectedStocks : this.selectedStocks
        }
      })
    },

  }
}
</script>

<style scoped>

</style>