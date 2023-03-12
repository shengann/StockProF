<template>
  <div class="page-stock">
     <div class="box">
      <div
        v-for="stockDeatail in stock"
        v-bind:key="stockDeatail.id"
      >
        <div class="is-size-4">{{ stockDeatail.ticker }} {{ stockDeatail.date }} {{ stockDeatail.assetturnover }} {{ stockDeatail.debttoequity }}</div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios"
export default {
  name: 'StockDetail',
  data() {
    return {
      stock: []
    }
  },
  mounted() {
    this.getFinancialRatios()
    document.title = 'Home' + ' | Djacket'
  },
  methods: {
    async getFinancialRatios() {
      const ticker = this.$route.params.ticker


      await axios
        .get(`/api/stock/${ticker}`)
        .then(response => {
          this.stock = response.data

          document.title = ticker + ' | StockProf'
        })
        .catch(error => {
          console.log(error)
        })

    }
  }
}
</script>

<style scoped></style>