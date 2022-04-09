// set the dimensions and margins of the graph
const margin = { top: 0, right: 40, bottom: 34, left: 40 },
    width = 960 - margin.left - margin.right,
    height = 500 - margin.top - margin.bottom;

// append the svg object to the body of the page
const svg = d3.select("#timegraph")
    .append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", "-50 0 960 500");

//Read the data
d3.csv("https://raw.githubusercontent.com/Hades98765/AusForecaster/main/polling_data/timegraphdata.csv",
    // When reading the csv, I must format variables:
    function (d) {
        return { date: d3.timeParse("%Y-%m-%d")(d.date), party: d.party, seatNum: d.seatNum }
    }).then(
        function (data) {
            // group the data: I want to draw one line per group
            const sumstat = d3.group(data, d => d.party); // nest function allows to group the calculation per level of a factor

            // Add X axis --> it is a date format
            const x = d3.scaleTime()
                .domain(d3.extent(data, function (d) { return d.date; }))
                .range([0, width]);
            svg.append("g")
                .attr("class", "x axis")
                .attr("transform", `translate(0, ${height})`)
                .call(d3.axisBottom(x).ticks(5));
            // Add Y axis
            const y = d3.scaleLinear()
                .domain([0, d3.max(data, function (d) { return +d.seatNum + 10; })])
                .range([height, 0]);
            svg.append("g")
                .attr("class", "x axis")
                .call(d3.axisLeft(y));

            // color palette
            const color = d3.scaleOrdinal()
                .domain(["Labor", "Coalition", "Others"])
                .range(['#a62621', '#2d45a6', '#858585']);

            // Draw the line
            svg.selectAll(".line")
                .data(sumstat)
                .join("path")
                .attr("fill", "none")
                .attr("stroke", function (d) {return color(d[0]) })
                .attr("stroke-width", 1.5)
                .attr("d", function (d) {
                    return d3.line()
                        .x(function (d) { return x(d.date) })
                        .y(function (d) { return y(d.seatNum) })
                        (d[1])
                })

        })