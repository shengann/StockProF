<template>

    <div class="page-portfolio">
         <!-- <div class="box"> -->
            <p>{{ this.stocks }}</p>
        <!-- </div> -->
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
            
        }
    },
    mounted() {
        // this.getPortfolio()
        console.log(this.data); // Outputs 'Hello World'

        document.title = 'Portfolio' + ' | Djacket'
    },
    methods: {
        async getStocks() {
            await axios
                .post('api/stockprof',{
                    
                })
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
    }
}
</script>

<style scoped></style>