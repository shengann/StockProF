<template>
  <div ref="chart"></div>
</template>

<script>
import * as d3 from 'd3';
import axios from "axios"
export default {
  mounted() {
    this.showChart();
  },
  methods: {
        async showChart() {
      const data = await this.getStockPrice(); // assume you have a method to fetch data from an API
      const margin = { top: 50, right: 50, bottom: 50, left: 50 };
      const width = 800 - margin.left - margin.right;
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
        .text("Price ($)");

    },
    async getStockPrice() {
      // assume you have a method to fetch data from an API
      
         const ticker = this.$route.params.ticker;
      try {
        const response = await axios.get(`/api/stock/${ticker}`);
        const data = response.data;
        document.title = `${ticker} | StockProf`;
        return data;
      } catch (error) {
        console.log(error);
      }

      
    },
  },
};
</script>
