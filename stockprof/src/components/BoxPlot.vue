<template>
        <div class="box-plot">
        <div ref="boxplot" :id="'boxplot-' + id"></div>
      </div>
</template>

<script>
import * as d3 from 'd3';
export default {
    name: 'BoxPlot',
    props: {
        boxPlotData: Array,
        id: String // new prop to pass a unique ID
    },
    mounted() {
        if (this.boxPlotData.length) {
            this.showBoxPlot()
        }

    },
    methods: {
        showBoxPlot() {
            const margin = { top: 10, right: 30, bottom: 30, left: 40 };
            const width = 500 - margin.left - margin.right;
            const height = 400 - margin.top - margin.bottom;

            // Create a unique id for the SVG element using the component's id

            // Remove the SVG element if it exists
            d3.select(`.plot-${this.id}`)
            // append the svg object to the selected DOM element
            const svg = d3.select(`#boxplot-${this.id}`).append('svg')
                
                .attr('width', width + margin.left + margin.right)
                .attr('height', height + margin.top + margin.bottom)
                .append('g')
                .attr('transform', `translate(${margin.left},${margin.top})`);

            // Compute quartiles, median, inter quantile range min and max
            const sumstat = this.boxPlotData.map((d) => {
                const q1 = d.q1;
                const median = d.q2;
                const q3 = d.q3;
                const interQuantileRange = d.iqr;
                const min = q1 - 1.5 * interQuantileRange;
                const max = q3 + 1.5 * interQuantileRange;
                return ({ name: d.name, q1, median, q3, interQuantileRange, min, max });
            });

            // Show the X scale
            const x = d3.scaleBand()
                .range([0, width])
                .domain(this.boxPlotData.map((d) => d.name))
                .paddingInner(1)
                .paddingOuter(0.5);
            svg.append('g')
                .attr('transform', `translate(0,${height})`)
                .call(d3.axisBottom(x));

            // Show the Y scale
            const y = d3.scaleLinear()
                .domain([-0.5, 1])
                .range([height, 0]);
            svg.append('g').call(d3.axisLeft(y));

            // Show the main vertical line
            svg
                .selectAll('vertLines')
                .data(sumstat)
                .enter()
                .append('line')
                .attr('x1', (d) => x(d.name))
                .attr('x2', (d) => x(d.name))
                .attr('y1', (d) => y(d.min))
                .attr('y2', (d) => y(d.max))
                .attr('stroke', 'black')
                .style('width', 40);

            // rectangle for the main box
            const boxWidth = 50;
            svg
                .selectAll('boxes')
                .data(sumstat)
                .enter()
                .append('rect')
                .attr('x', (d) => x(d.name) - boxWidth / 2)
                .attr('y', (d) => y(d.q3))
                .attr('height', (d) => y(d.q1) - y(d.q3))
                .attr('width', boxWidth)
                .attr('stroke', 'black')
                .style('fill', '#69b3a2');

            // Show the median
            svg
                .selectAll('medianLines')
                .data(sumstat)
                .enter()
                .append('line')
                .attr('x1', (d) => x(d.name) - boxWidth / 2)
                .attr('x2', (d) => x(d.name) + boxWidth / 2)
                .attr("y1", function (d) { return (y(d.median)) })
                .attr("y2", function (d) { return (y(d.median)) })
                .attr("stroke", "black")
                .style("width", 80)
        }
    }
}
</script>