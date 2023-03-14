<template>

    <div class="page-portfolio">   
        
        <div
            v-for="stockList in clusteredStocks"
            v-bind:key="stockList.id"
        >
            <div class="card">
                <div class="card-header">
                    Portfolio
                </div>
                <ul class="list-group list-group-flush">
                    <div
                        v-for="stock in stockList"
                        v-bind:key="stock.id"
                    >   
                        <li  class="list-group-item">{{ stock.Symbol }}</li>
                    </div>
                </ul>
            </div>
        </div>    
    </div>
</template>

<script>
import axios from "axios"
export default {
    name: 'Portfolio',
    props: ['selectedStocks'],
    data() {
        return {
            stocks: this.$route.query.selectedStocks,
            clusteredStocks: []
        }
    },
    mounted() {
        this.getPortfolio()

        document.title = 'Portfolio' + ' | Djacket'
    },
    methods: {
        async getPortfolio() {
            await axios
                .post('api/stockprof',{
                    "ticker_list":this.stocks,
                    "date":"2022-09-30"
                })
                .then(response => {
                    this.clusteredStocks = response.data.data
                })
                .catch(error => {
                    console.log(error)
                }
                )
        },
    }
}
</script>

<style scoped></style>