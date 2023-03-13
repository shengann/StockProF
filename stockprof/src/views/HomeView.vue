<template>
  <div class="home">

     <div class="dropdown">
      <button
        class="btn btn-primary dropdown-toggle"
        type="button" id="dropdownMenuButton1"
        data-bs-toggle="dropdown"
        aria-expanded="false">
        Dropdown button: {{ value }}
      </button>
      <ul class="dropdown-menu" aria-labelledby="dropdownMenuButton1" role="menu">
        <li v-for="option in options" :key="option">
          <a class="dropdown-item" @click="value = option; filterStock()" href="javascript:void(0)">{{ option }}</a>
        </li>
      </ul>
    </div>

    <div class="box">
      <div
        v-for="stock in stocks"
        v-bind:key="stock.id"
      >
        <div class="is-size-4">{{stock.Symbol}} {{ stock.Sector }}</div>
        <router-link v-bind:to="stock.get_absolute_url" class="button is-dark mt-4">View details</router-link>
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
        .then(response => {
          this.stocks = response.data,
            console.log(response.data)
            const symbols = response.data.map(symbol => symbol.Symbol);
            console.log(symbols)
            const sectors = response.data.map(sector => sector.Sector);
            sectors.forEach(sector => this.options.add(sector));
        })
        .catch(error => {
          console.log(error)
        }
        )
    },
    async filterStock(){
      await axios
        .get(`api/stocks/${this.value}`)
        .then(response => {
          this.stocks = response.data,
            console.log("this.stocks", this.stocks)
        })
        .catch(error => {
          console.log(error)
        }
        )
    }
  }
}
</script>

<style scoped>

</style>