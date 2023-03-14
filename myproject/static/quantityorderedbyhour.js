d3.csv("{% url 'csv_data' %}", function(data) {
    // Create a nested array of order counts by hour
    var ordersByHour = d3.nest()
        .key(function(d) { return d.hour; })
        .rollup(function(v) { return v.length; })
        .entries(data);

    // Set up the dimensions of the chart
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    // Set up the scales for the x and y axes
    var x = d3.scaleLinear()
        .range([0, width])
        .domain([0, 24]);

    var y = d3.scaleLinear()
        .range([height, 0])
        .domain([0, d3.max(ordersByHour, function(d) { return d.value; })]);

    // Create a new SVG element for the chart
    var svg = d3.select("#chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Add the x axis to the chart
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x).ticks(24));

    // Add the y axis to the chart
    svg.append("g")
        .call(d3.axisLeft(y))
      .append("text")
        .attr("fill", "#000")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", "0.71em")
        .attr("text-anchor", "end")
        .text("Number of Orders");

    // Add the bars to the chart
    svg.selectAll(".bar")
        .data(ordersByHour)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d.key); })
        .attr("y", function(d) { return y(d.value); })
        .attr("width", x(1) - x(0))
        .attr("height", function(d) { return height - y(d.value); });
});
