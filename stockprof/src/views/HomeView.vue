<template>
  <div class="home">
  <div
    v-for="stock in stocks"
    v-bind:key="stock.id"
  >
    <div class="is-size-4">{{stock.Symbol}}</div>

  </div>
  </div>
</template>

<script>
import axios from "axios"
export default {
  name: 'Home',
  data() {
    return {
      stocks: []
    }
  },
  mounted() {
    this.getStocks()

    document.title = 'Home' + ' | Djacket'
  },
  methods: {
    async getStocks() {
      await axios
        .get('/stockprof/stocks')
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