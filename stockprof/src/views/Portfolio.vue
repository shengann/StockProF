<template>
    <div class="page-portfolio">
        <h1 class="title">Sector : {{ category }}</h1>
        <div v-if="outlierStocks.length > 1" class="box mt-6 box has-background-white border border-primary border-2 my-5">
            <h2 class="title">Outlier Stocks</h2>

            <div class="columns is-multiline" v-if="outlierStockProfile">
                <div class="column is-half" v-for="(outlierBoxPlotData, index) in outlierBoxPlotData"
                    :key="outlierBoxPlotData.id" :class="{ 'is-12-mobile': (index % 2 === 0) }">
                    <h2 class="title">{{ this.outlierTitle[index] }}</h2>
                    <box-plot :box-plot-data="outlierBoxPlotData" :id="'box-plot-' + index"></box-plot>
                    <div>
                        <table class="table table-striped table-bordered table-sm my-6">
                            <thead>
                                <tr>
                                    <th class="text-center" scope="col">Fianncial Ratio</th>
                                    <th class="text-center" scope="col">Q1</th>
                                    <th class="text-center" scope="col">Median</th>
                                    <th class="text-center" scope="col">Q3</th>
                                    <th class="text-center" scope="col">Min</th>
                                    <th class="text-center" scope="col">Max</th>
                                </tr>
                            </thead>
                            <tbody v-for="(data, index) in outlierBoxPlotData" v-bind:key="data.id">
                                <td scope="row">{{ financial_ratios[index] }}</td>
                                <td scope="row">{{ parseFloat(data.q1).toFixed(2) }}</td>
                                <td scope="row">{{ parseFloat(data.q2).toFixed(2) }}</td>
                                <td scope="row">{{ parseFloat(data.q3).toFixed(2) }}</td>
                                <td scope="row">{{ parseFloat(data.min).toFixed(2) }}</td>
                                <td scope="row">{{ parseFloat(data.max).toFixed(2) }}</td>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>

            <table class="table table-striped table-bordered table-sm ">
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
                        <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">{{ this.outlierStocks[index].Name }}</td>
                        <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">{{ this.outlierStocks[index].Symbol }}</td>
                        <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">{{ financialRatio[0].assetturnover }}</td>
                        <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">{{ financialRatio[0].quickratio }}</td>
                        <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">{{ financialRatio[0].debttoequity }}</td>
                        <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">{{ financialRatio[0].roe }}</td>
                        <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">{{ financialRatio[0].dividendyield }}</td>
                        <td scope="row" style="cursor: pointer;" @click="showChartDialog(this.outlierStocks[index].Symbol)">{{ financialRatio[0].pricetoearnings }}</td>
                        <td scope="row" v-if="OutlierCapitalGainLoss.length > 0">{{
                            OutlierCapitalGainLoss[index].toFixed(2) }}%</td>
                        <td scope="row">
                            <div class="select is-small mb-3 mr-3">
                                <select v-model="stockTypeOptions[index]" @change="showOutlierInput(index)">
                                    <option value="Outperforming">Outpeforming</option>
                                    <option value="Underperforming">Underperforming</option>
                                    <option value="custom">Custom</option>
                                </select>
                            </div>
                            <input v-if="showOutlierTextInput[index]" class="input is-small" type="text"
                                placeholder="Stock type" style="width:120px;" v-model="stockTypeOptions[index]" />
                        </td>
                    </tr>
                </tbody>
            </table>
            <button type="button" @click="OutlierStockProfile()" class="btn btn-primary mt-3">Outlier Stock Profile</button>
        </div>

        <div class="columns is-multiline box has-background-white border border-primary border-2 my-6">
             <div class="column is-full">
                <h3 class="title my-5 has-text-centered">Portfolio For Non-outlier stocks</h3>
            </div>
            <div class="column is-half" v-for="(boxPlotData, index) in boxPlotData" v-bind:key="boxPlotData.id">
                <div>
                    <h2 class="title">Portfolio {{ index + 1 }}</h2>
                    <box-plot :box-plot-data="boxPlotData" :id="'box-plot-' + index"></box-plot>
                    <div>
                        <table class="table table-striped table-bordered table-sm my-6">
                            <thead>
                                <tr>
                                    <th class="text-center" scope="col">Fianncial Ratio</th>
                                    <th class="text-center" scope="col">Q1</th>
                                    <th class="text-center" scope="col">Median</th>
                                    <th class="text-center" scope="col">Q3</th>
                                    <th class="text-center" scope="col">Min</th>
                                    <th class="text-center" scope="col">Max</th>
                                </tr>
                            </thead>
                            <tbody v-for="(data, index) in boxPlotData" v-bind:key="data.id">
                                <td scope="row">{{ financial_ratios[index] }}</td>
                                <td scope="row">{{ parseFloat(data.q1).toFixed(2) }}</td>
                                <td scope="row">{{ parseFloat(data.q2).toFixed(2) }}</td>
                                <td scope="row">{{ parseFloat(data.q3).toFixed(2) }}</td>
                                <td scope="row">{{ parseFloat(data.min).toFixed(2) }}</td>
                                <td scope="row">{{ parseFloat(data.max).toFixed(2) }}</td>
                            </tbody>
                        </table>
                    </div>
                    <table class="table table-striped table-bordered table-sm">
                        <thead>
                            <tr>
                                <th class="text-center" scope="col">Name</th>
                                <th class="text-center" scope="col">Code</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-for="stock in clusteredStocks[index]" v-bind:key="stock.id">
                                <td scope="row" style="cursor: pointer;" @click="showChartDialog(stock.Symbol)">{{ stock.Name }}</td>
                                <td scope="row" style="cursor: pointer;" @click="showChartDialog(stock.Symbol)">{{ stock.Symbol }}</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
                <div class="label" v-if="ClusterCapitalGainLoss.length > 0">Capital Gain & Loss :
                    {{ ClusterCapitalGainLoss[index].toFixed(2) }}%</div>
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
                <input v-if="showTextInput[index]" v-model="portfolioTypeOptions[index]" class="input my-4" type="text"
                    placeholder="Portfolio type">
            </div>
        </div>
        <div>
            <button @click="saveResult_showModal = true" class="btn btn-primary mt-4">Save Results</button>
            <div class="modal" v-if="isAuthenticated" :class="{ 'is-active': saveResult_showModal }">
                <div class="modal-background" @click="saveResult_showModal = false"></div>
                <div class="modal-card">
                    <header class="modal-card-head">
                        <p class="modal-card-title">Sector : {{ category }}</p>
                        <button class="delete" aria-label="close" @click="saveResult_showModal = false"></button>
                    </header>
                    <section class="modal-card-body">
                        <label>Remarks For The Portfolio Generated</label>
                        <input v-model="remark" class="input my-4" type="text" placeholder="Remarks">
                    </section>
                    <footer class="modal-card-foot">
                        <button class="button is-success" @click="saveResult()">Save Results</button>
                        <button class="button" @click="saveResult_showModal = false">Cancel</button>
                    </footer>
                </div>
            </div>

            <div class="modal" v-else :class="{ 'is-active': saveResult_showModal }">
                <div class="modal-background" @click="saveResult_showModal = false"></div>
                <div class="modal-card">
                    <header class="modal-card-head">
                        <p class="modal-card-title">Sector : {{ category }}</p>
                        <button class="delete" aria-label="close" @click="saveResult_showModal = false"></button>
                    </header>
                    <section class="modal-card-body">
                        <label>Please Login to save result</label>
                    </section>
                    <footer class="modal-card-foot">
                        <button class="button is-warning" @click="saveResult()">Login</button>
                        <button class="button" @click="saveResult_showModal = false">Cancel</button>
                    </footer>
                </div>
            </div>
        </div>
        <div v-if="chartId != ''">
                <stock-chart :show-modal="this.showModal" :ticker="this.chartId" @modal-closed="handleModalClosed"></stock-chart>
        </div>

    </div>
</template>

<script>
import axios from "axios"
import BoxPlot from '@/components/BoxPlot'
import StockChart from '@/components/StockChart'
import { mapGetters } from 'vuex'
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
            outlierBoxPlotData: [],
            portfolioTypeOptions: [],
            showTextInput: [],
            showOutlierTextInput: [],
            stockTypeOptions: [],
            ClusterCapitalGainLoss: [],
            OutlierCapitalGainLoss: [],
            outlierStockProfile: false,
            outlierTitle: [],
            saveResult_showModal: false,
            remark: '',
            financial_ratios: ['Total asset turnover', 'Cash ratio', 'Debt ratio', 'Return on equity', 'Dividend yield', 'Price earnings ratio'],
            showModal: false,
            chartId: '',
        }
    },
    components: {
        BoxPlot,
        StockChart
    },
    computed: {
        ...mapGetters(['isAuthenticated'])
    },
    mounted() {
        this.getPortfolio()

        document.title = 'Portfolio' + ' | StockProF'
    },
    methods: {
        handleModalClosed() {
            this.chartId = "";
        },
        showChartDialog(index) {
            this.showModal = true
            this.chartId = index
        },
        async saveResult() {
            console.log("this.portfolioTypeOptions", this.portfolioTypeOptions)
            const data = {
                'clusteredStocksSymbols': this.clusteredStocksSymbols,
                'outlierStocksSymbols': this.outlierStocksSymbols,
                'portfolioTypeOptions': this.portfolioTypeOptions,
                'category': this.category,
                'stockTypeOptions': this.stockTypeOptions,
                'remarks': this.remark
            }
            await axios
                .post('api/save-result', { data })
                .then(response => {
                    console.log(response)
                    this.$router.push({
                        name: 'PersonalProfile'
                    })
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
            if (this.stockTypeOptions[index] !== 'Outperforming' && this.stockTypeOptions[index] !== 'Underperforming') {
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
                    this.getBoxPlotData(this.clusteredStocksSymbols, 'portfolio')
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
                    "initial_date": "2023-01-03",
                    "final_date": "2023-03-17"
                })
                .then(response => {
                    this.ClusterCapitalGainLoss = response.data.Portfolio
                    this.OutlierCapitalGainLoss = response.data.Outlier
                    console.log(this.ClusterCapitalGainLoss)
                })
                .catch(error => {
                    console.log(error)
                }
                )
        },
        async getBoxPlotData(data, type) {
            console.log(data)
            await axios
                .post('api/portfolio/box-plot-data', {
                    "portfolio_list": data,
                    "Category": this.category
                })
                .then(response => {
                    if (type == 'portfolio') {
                        this.boxPlotData = response.data
                        this.boxPlotData = this.groupBoxPlotData(this.boxPlotData)
                    }
                    else {
                        this.outlierBoxPlotData = response.data
                        this.outlierBoxPlotData = this.groupBoxPlotData(this.outlierBoxPlotData)
                    }
                })
                .catch(error => {
                    console.log(error)
                }
                )
        },
        groupBoxPlotData(arrOfObjects) {
            return arrOfObjects.reduce((result, value, index, array) => {
                if (index % 6 === 0) {
                    result.push(array.slice(index, index + 6))
                }
                return result
            }, [])
        },
        async OutlierStockProfile() {
            const sortedArray = this.stockTypeOptions.sort();// sort the array in ascending order
            this.outlierTitle = [...new Set(sortedArray)];
            console.log("sortedArray", sortedArray)
            console.log("this.outlierTitle", this.outlierTitle)
            const indexMap = this.stockTypeOptions.reduce((acc, value, index) => {
                if (acc[value]) {
                    acc[value].push(index);
                } else {
                    acc[value] = [index];
                }
                return acc;
            }, {});
            console.log("indexMap", indexMap)
            const indexArray = Object.values(indexMap); // convert object values to an array
            console.log("indexArray", indexArray)
            const result = indexArray.map((sublist) =>
                sublist.map((index) => this.outlierStocksSymbols[index])
            );
            this.getBoxPlotData(result, 'outlier')
            this.outlierStockProfile = true
        }
    }
}
</script>

<style scoped></style>