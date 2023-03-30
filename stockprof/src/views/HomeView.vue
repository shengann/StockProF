<template>
  <div class="home">

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
          <a class="dropdown-item" @click="value = option; filterStock()" href="javascript:void(0)">{{ option }}</a>
        </li>
      </ul>
    </div>
    <button to="portfolio" @click="navigateToPortfolio" type="button"  class="btn btn-primary">Generate Portfolio</button> 

    <div class="box">
      <!-- <div
        v-for="stock in stocks"
        v-bind:key="stock.id"
      >
        <div class="is-size-4">{{stock.Symbol}} {{ stock.Category }}</div>
        <router-link v-bind:to="stock.get_absolute_url" class="button is-dark mt-4">View details</router-link>
      </div> -->
    <div>
        <table class="table">
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
          <tr v-for="(stock, index) in stocks" :key="index">
            <td scope="row">{{ stock.Name }}</td>
            <td scope="row">{{ stock.Symbol }}</td>
            <td scope="row">{{ stock.Category }}</td>
            <td scope="row">{{ financialRatio[index].assetturnover }}</td>
            <td scope="row">{{ financialRatio[index].quickratio }}</td>
            <td scope="row">{{ financialRatio[index].debttoequity }}</td>
            <td scope="row">{{ financialRatio[index].roe }}</td>
            <td scope="row">{{ financialRatio[index].dividendyield }}</td>
            <td scope="row">{{ financialRatio[index].pricetoearnings }}</td>
            <td scope="row"><router-link v-bind:to="stock.get_absolute_url" class="button is-dark mt-4">View Chart</router-link></td>
          </tr>
        </tbody>
      </table>
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
      value: ''
    }
  },
  mounted() {
    this.getStocks()

    document.title = 'Home' + ' | Djacket'
  },
  methods: {
    async getStocks() {
      await axios
        .get('api/stocks')
        .then(response1 => {
          return axios.get('api/financial-ratio')
          .then(response2 => {
            this.stocks = response1.data,
            this.financialRatio = response2.data
            const Category = response1.data.map(Category => Category.Category);
            Category.forEach(Category => this.options.add(Category));
            })
        })
        .catch(error => {
          console.log(error)
        }
        )
    },
    async filterStock(){
      await axios
        .get(`api/stocks/${this.value}`)
        .then(response1 => {
          return axios.get(`api/stocks/${this.value}/financial-ratio`)
            .then(response2 => {
              this.stocks = response1.data,
              this.financialRatio = response2.data
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