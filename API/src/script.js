// Dimensions and margins.
var margin = {top: 20, right: 20, bottom: 30, left: 50},
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// SVG element.
var svg = d3.select("#chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

// Scales.
var xScale = d3.scaleTime().range([0, width]),
    yScale = d3.scaleLinear().range([height, 0]);

// Line generator.
var line = d3.line()
    .x(function(d) { return xScale(d.date); })
    .y(function(d) { return yScale(d.value); });

// Test data.
var data = [
    {date: "2023-01-01", value: 10},
    {date: "2023-02-01", value: 20},
    {date: "2023-03-01", value: 15},
    {date: "2023-04-01", value: 25}
];

// Parse dates and set scale domains.
data.forEach(function(d) {
    d.date = d3.timeParse("%Y-%m-%d")(d.date);
    d.value = +d.value;
});

xScale.domain(d3.extent(data, function(d) { return d.date; }));
yScale.domain(d3.extent(data, function(d) { return d.value; }));

// Add line, x-axis, and y-axis.
svg.append("path")
    .datum(data)
    .attr("class", "line")
    .attr("d", line);

svg.append("g")
    .attr("transform", "translate(0," + height + ")")
    .call(d3.axisBottom(xScale));

svg.append("g")
    .call(d3.axisLeft(yScale));

// Brush.
var brush = d3.brushX()
    .extent([[0, 0], [width, height]])
    .on("end", brushed);

svg.append("g")
    .attr("class", "brush")
    .call(brush);

// Brushed function.
function brushed() {
    var selection = d3.event.selection;
    var selectedData = data.filter(function(d) {
        return (xScale(d.date) >= selection[0]) && (xScale(d.date) <= selection[1]);
    });
    console.log(selectedData); // Output the selected data to the console.
}
