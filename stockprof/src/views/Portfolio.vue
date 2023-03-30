<template>

    <div class="page-portfolio">   
        <button  @click="getComparison" type="button"  class="btn btn-primary">Capital Gain/Lose</button> 

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
            clusteredStocks: [],
            outlierStocks: [],
            clusteredStocksSymbols :[], 
            outlierStocksSymbols : []
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
                    // "date":"2022-09-30"
                })
                .then(response => {
                    this.clusteredStocks = response.data.portfolio
                    this.outlierStocks = response.data.outlier
                    console.log(this.clusteredStocks)
                    for (let i=0;i< response.data.portfolio.length;i++) {
                        const clustered_symbols = response.data.portfolio[i].map(symbol => symbol.Symbol);
                        this.clusteredStocksSymbols.push(clustered_symbols)

                    }
                    // this.clusteredStocksSymbols = clustered_symbols
                    const outlier_symbols = response.data.outlier.map(symbol => symbol.Symbol);
                    this.outlierStocksSymbols = outlier_symbols
                })
                .catch(error => {
                    console.log(error)
                }
                )
        },
        async getComparison() {
            await axios
                .post('api/comparison', {
                    "portfolio_list": this.clusteredStocksSymbols,
                    "outlier_list": this.outlierStocksSymbols,
                    "initial_date": "2022-01-05",
                    "final_date": "2023-01-05"
                })
                .then(response => {
                    console.log(response)
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