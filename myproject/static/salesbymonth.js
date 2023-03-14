d3.csv("{% url 'csv_data' %}", function(data) {
    // Parse the dates in the data set
    var parseDate = d3.timeParse("%Y-%m-%d %H:%M:%S");
    data.forEach(function(d) {
        d.date = parseDate(d.month);
    });

    // Create a nested array of sales data by month
    var salesByMonth = d3.nest()
        .key(function(d) { return d3.timeMonth(d.date); })
        .rollup(function(v) { return d3.sum(v, function(d) { return d.sales; }); })
        .entries(data);

    // Set up the dimensions of the chart
    var margin = {top: 20, right: 20, bottom: 30, left: 40},
        width = 960 - margin.left - margin.right,
        height = 500 - margin.top - margin.bottom;

    // Set up the scales for the x and y axes
    var x = d3.scaleTime()
        .range([0, width]);

    var y = d3.scaleLinear()
        .range([height, 0]);

    // Create a new SVG element for the chart
    var svg = d3.select("#chart").append("svg")
        .attr("width", width + margin.left + margin.right)
        .attr("height", height + margin.top + margin.bottom)
      .append("g")
        .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

    // Set the domains of the x and y scales
    x.domain(d3.extent(salesByMonth, function(d) { return d3.timeMonth(d.key); }));
    y.domain([0, d3.max(salesByMonth, function(d) { return d.value; })]);

    // Add the x axis to the chart
    svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

    // Add the y axis to the chart
    svg.append("g")
        .call(d3.axisLeft(y))
      .append("text")
        .attr("fill", "#000")
        .attr("transform", "rotate(-90)")
        .attr("y", 6)
        .attr("dy", "0.71em")
        .attr("text-anchor", "end")
        .text("Sales");

    // Add the bars to the chart
    svg.selectAll(".bar")
        .data(salesByMonth)
      .enter().append("rect")
        .attr("class", "bar")
        .attr("x", function(d) { return x(d3.timeMonth(d.key)); })
        .attr("y", function(d) { return y(d.value); })
        .attr("width", x(d3.timeMonth.offset(d3.timeMonth(d.key), 1)) - x(d3.timeMonth(d.key)))
        .attr("height", function(d) { return height - y(d.value); });
});
