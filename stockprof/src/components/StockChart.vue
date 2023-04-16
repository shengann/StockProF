<template>
        <div>
                  <div class="modal"  :class="{ 'is-active': showModal }">
                      <div class="modal-background" @click="closeModal"></div>
                      <div class="modal-card">
                          <header class="modal-card-head">
                              <p class="modal-card-title">Stock Price for {{ticker}}</p>
                              <button class="delete" aria-label="close" @click="showModal = false;closeModal()"></button>
                          </header>
                          <section class="modal-card-body">
                              <div ref="chart"></div>
                              <!-- <input v-model="remark" class="input my-4" type="text" placeholder="Remarks"> -->
                          </section>
                      </div>
                  </div>

              </div>
      
</template>

<script>
import axios from "axios"
import * as d3 from 'd3';
export default {
    name: 'StcokChart',
    data(){
        return{
        }
    },
    props: {
        ticker : String,
        showModal : Boolean,
    },
    mounted() {
        this.showChart()
    },
      methods: {
        closeModal() {
            this.$emit("modal-closed");
        },
        async showChart() {
            const data = await this.getStockPrice(); 
            console.log("showchart",data)
            const margin = { top: 50, right: 50, bottom: 50, left: 50 };
            const width = 600 - margin.left - margin.right;
            const height = 500 - margin.top - margin.bottom;

            const svg = d3.select(this.$refs.chart)
                .append("svg")
                .attr("width", width + margin.left + margin.right)
                .attr("height", height + margin.top + margin.bottom)
                .append("g")
                .attr("transform", `translate(${margin.left},${margin.top})`);

            const x = d3.scaleTime()
                .range([0, width])
                .domain(d3.extent(data, d => new Date(d.Date)));

            const y = d3.scaleLinear()
                .range([height, 0])
                .domain([0, d3.max(data, d => parseFloat(d.High))]);

            const line = d3.line()
                .x(d => x(new Date(d.Date)))
                .y(d => y(parseFloat(d.High)));

            svg.append("path")
                .datum(data)
                .attr("fill", "none")
                .attr("stroke", "steelblue")
                .attr("stroke-width", 1.5)
                .attr("d", line);

            const xAxis = d3.axisBottom(x);
            const yAxis = d3.axisLeft(y);

            svg.append("g")
                .attr("transform", `translate(0,${height})`)
                .call(xAxis);

            svg.append("g")
                .call(yAxis);

            svg.append("g")
                .attr("class", "grid")
                .call(d3.axisLeft(y)
                    .tickSize(-width)
                    .tickFormat("")
                )

            svg.append("text")
                .attr("transform", `translate(${width / 2},${height + margin.top - 10})`)
                .style("text-anchor", "middle")
                .style("font-weight", "bold")
                .text("Date");

            svg.append("text")
                .attr("transform", `rotate(-90)`)
                .attr("y", 0 - margin.left)
                .attr("x", 0 - (height / 2))
                .attr("dy", "1em")
                .style("text-anchor", "middle")
                .style("font-weight", "bold")
                .text("Price (RM)");
            
                this.stock_ticker= ''


        },
        async getStockPrice() {
            // assume you have a method to fetch data from an API

            const ticker = this.ticker;
            try {
                const response = await axios.get(`/api/stock/${ticker}`);
                const data = response.data;
                console.log(data)
                if (data.length>0){
                    console.log(data.length)
                    this.chartData = true
                    console.log(this.showModal)
                }
                document.title = `${ticker} | StockProf`;
                return data;
            } catch (error) {
                console.log(error);
            }


        },
    }
}
</script>