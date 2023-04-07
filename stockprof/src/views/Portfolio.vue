<template>    
    <div class="page-portfolio">
        <h1 class="title">Sector : {{ category }}</h1>
        <div v-if="outlierStocks.length > 1" class="box mt-6">
            <h2 class="title">Outlier Stocks</h2>

            <table class="table table-striped table-bordered table-sm">
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
                        <td scope="row">{{ this.outlierStocks[index].Name }}</td>
                        <td scope="row">{{ this.outlierStocks[index].Symbol }}</td>
                        <td scope="row">{{ financialRatio[0].assetturnover }}</td>
                        <td scope="row">{{ financialRatio[0].quickratio }}</td>
                        <td scope="row">{{ financialRatio[0].debttoequity }}</td>
                        <td scope="row">{{ financialRatio[0].roe }}</td>
                        <td scope="row">{{ financialRatio[0].dividendyield }}</td>
                        <td scope="row">{{ financialRatio[0].pricetoearnings }}</td>
                        <td scope="row">test</td>
                        <td scope="row">
                            <div class="select is-small mb-3 mr-3">
                                <select v-model="stockTypeOptions[index]" @change="showOutlierInput(index)">
                                    <option value="outperforming">Outpeforming</option>
                                    <option value="underperforming">Underperforming</option>
                                    <option value="custom">Custom</option>
                                </select>
                            </div>
                            <input v-if="showOutlierTextInput[index]" class="input is-small" type="text"
                                style="width:120px;" v-model="stockTypeOptions[index]" />
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>


        <div class="columns is-multiline box">
            <div class="column is-half" v-for="(boxPlotData, index) in boxPlotData" v-bind:key="boxPlotData.id">
                <div>
                    <h2 class="title">Portfolio {{ index + 1 }}</h2>
                    <box-plot
                        :box-plot-data="boxPlotData"
                        :id="'box-plot-' + index"
                    ></box-plot>
                    <table class="table table-striped table-bordered table-sm" >
                        <thead>
                            <tr>
                                <th class="text-center" scope="col">Name</th>
                                <th class="text-center" scope="col">Code</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="stock in clusteredStocks[index]" v-bind:key="stock.id">
                                <td scope="row">{{ stock.Name }}</td>
                                <td scope="row">{{ stock.Symbol }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="field">
                    <label class="label">Portfolio Type</label>
                    <div class="control">
                        <div class="select is-rounded">
                            <select v-model="portfolioTypeOptions[index]" @change="showInput(index)">
                                <option value="Aggressive">Aggressive</option>
                                <option value="Average">Average</option>
                                <option value="Defensive">Defensive</option>
                                <option value=Custom>Custom</option>
                            </select>
                        </div>
                    </div>
                </div>
                <input v-if="showTextInput[index]" v-model="portfolioTypeOptions[index]" class="input my-4" type="text" placeholder="Portfolio type">            </div>
        </div>
        <button type="button" @click="saveResult()" class="btn btn-primary mt-6">Save Results</button>

    </div>
</template>

<script>
import axios from "axios"
import BoxPlot from '@/components/BoxPlot'
export default {
    name: 'Portfolio',
    data() {
        return {
            stocks: this.$route.query.selectedStocks,
            category: this.$route.query.category,
            clusteredStocks: [],
            outlierStocks: [],
            outlierFinancialratio: [],
            clusteredStocksSymbols: [],
            outlierStocksSymbols: [],
            boxPlotData: [],
            portfolioTypeOptions: [],
            showTextInput: [],
            showOutlierTextInput: [],
            stockTypeOptions: []
        }
    },
    components: {
        BoxPlot
    },
    mounted() {
        this.getPortfolio()

        document.title = 'Portfolio' + ' | StockProF'
    },
    methods: {
        async saveResult() {
            console.log("this.portfolioTypeOptions", this.portfolioTypeOptions)
            const data = {
                'clusteredStocksSymbols': this.clusteredStocksSymbols,
                'outlierStocksSymbols': this.outlierStocksSymbols,
                'portfolioTypeOptions': this.portfolioTypeOptions,
                'category': this.category
            }
            await axios
                .post('api/save-result', { data })
                .then(response => {
                    conosle.log(response)
                    this.$router.push('/profile')
                })
                .catch(error => {
                    console.log("error", error)
                })
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
        showOutlierInput(index) {
            if (this.stockTypeOptions[index] !== 'outperforming' && this.stockTypeOptions[index] !== 'underperforming') {
                this.showOutlierTextInput[index] = true;
                if (this.stockTypeOptions[index] == 'custom') {
                    this.stockTypeOptions[index] = ''
                }
            }
            else {
                this.showOutlierTextInput[index] = false;
            }
        },
        async getPortfolio() {
            await axios
                .post('api/stockprof', {
                    "ticker_list": this.stocks,
                })
                .then(response => {
                    this.clusteredStocks = response.data.portfolio
                    this.outlierStocks = response.data.outlier
                    const outlierFinancialratio = response.data.outlier.map(financial_ratios => financial_ratios.financial_ratios);
                    this.outlierFinancialratio = outlierFinancialratio
                    for (let i = 0; i < response.data.portfolio.length; i++) {
                        const clustered_symbols = response.data.portfolio[i].map(symbol => symbol.Symbol);
                        this.clusteredStocksSymbols.push(clustered_symbols)
                        this.showTextInput.push(false)
                    }
                    for (let j = 0; j < response.data.outlier.length; j++) {
                        this.showOutlierTextInput.push(false)
                    }
                    const outlier_symbols = response.data.outlier.map(symbol => symbol.Symbol);
                    this.outlierStocksSymbols = outlier_symbols
                    this.getBoxPlotData()
                    this.getComparison()

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
        async getBoxPlotData() {
            await axios
                .post('api/portfolio/box-plot-data', {
                    "portfolio_list": this.clusteredStocksSymbols
                })
                .then(response => {
                    this.boxPlotData = response.data
                    this.boxPlotData = this.groupBoxPlotData(this.boxPlotData)
                })
                .catch(error => {
                    console.log(error)
                }
                )
        },
        groupBoxPlotData(arrOfObjects) {
            return arrOfObjects.reduce((result, value, index, array) => {
                if (index %6 === 0) {
                    result.push(array.slice(index, index + 6))
                }
                return result
            }, [])
        }
    }
}
</script>

<style scoped></style>