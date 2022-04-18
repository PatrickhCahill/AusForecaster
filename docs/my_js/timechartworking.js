const margin = { top: 20, right: 60, bottom: 60, left: 120 },
    width = 920 - margin.left - margin.right,
    height = 800 - margin.top - margin.bottom;

const timechart = d3.select("#my_dataviz")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", `translate(${margin.left},${margin.top})`);

    
d3.csv("page_data/testing.csv",
    //Parse the data as neeeded here
    function (d) {
        return {
            date: d3.timeParse("%Y-%m-%d")(d.date),
            party: d.party,
            tpp: +d.tpp,
            tppError: +d.tppError
        };
    }).then(function (data) {
        const formatDate = d3.timeFormat("%d %B %Y");
        //Group data according to label. In the case by political party
        const sumstat = d3.group(data, d => d.party);
        //Create x-axis. Change the domain arguments to change the x-axis
        const x = d3.scaleTime()
            .domain(d3.extent(data, function (d) { return d.date; }))
            .range([0, width]);
        timechart.append("g")
            .attr("transform", `translate(0, ${height})`)
            .call(d3.axisBottom(x).tickFormat(function(d){return  d3.timeFormat("%d %B")(d)}));

        //Create the y-axis. Change the domain arguments to change the y-axis
        const y = d3.scaleLinear()
            .domain([0, 100])
            .range([height, 0]);
        timechart.append("g")
            .call(d3.axisLeft(y));

        //Create color functions. colorArea is for d3.area() and colorLine is for d3.line
        const colorArea = d3.scaleOrdinal()
            .range(["rgba(140, 22, 9, 0.48)", 'rgba(50, 53, 197, 0.48)']);

        const colorLine = d3.scaleOrdinal()
            .range(["rgba(140, 22, 9, 0.9)", 'rgba(50, 53, 197, 0.9)']);

        //Create the confidence intervals
        timechart.selectAll(".line")
            .data(sumstat)
            .join("path")
            .attr("fill", function (d) { return colorArea(d[0]) })
            .attr("stroke", "none")
            .attr("stroke-width", 1.5)
            .attr("d", function (d) {
                return d3.area()
                    .x(function (d) { return x(d.date) })
                    .y0(function (d) { return y(d.tpp + d.tppError) })
                    .y1(function (d) { return y(d.tpp - d.tppError) })
                    (d[1])
            });

        //Create the lines
        timechart.selectAll(".line")
            .data(sumstat)
            .join("path")
            .attr("fill", "none")
            .attr("stroke", function (d) { return colorLine(d[0]) })
            .attr("stroke-width", 1.5)
            .attr("background-color","rgba(0,0,0,1)")
            .attr("d", function (d) {
                return d3.line()
                    .x(function (d) { return x(d.date); })
                    .y(function (d) { return y(+d.tpp); })
                    (d[1])
            });


        // Tooltip.
        //bisect() is a function that will retrieve the nearest date in the data to a given date.
        const bisect = d3.bisector(function (d) { return d.date; }).center;
        //We then create these empty arrays which will hold our tooltip info
        const numLines = 2; //This is the number of different elements our tooltip will track
        let focus = [];
        let focusText = [];
        for (let index = 0; index < numLines; index++) {
            focus.push(timechart.append('g')
                .append('circle')
                .style("fill", "none")
                .attr("stroke", "black")
                .attr('r', 6)
                .style("opacity", 0))
            focusText.push(timechart.append('g')
                .append('text')
                .style("opacity", 0)
                .attr("text-anchor", "left")
                .attr("alignment-baseline", "middle"))
        };
        const initialX = d3.extent(data, function (d) { return d.date; })[1];
        const maxY = 80;
        const LineTextOffset = 2;
        const tooltipLine = timechart.append("line")
                .attr("x1", x(initialX))
                .attr("y1", y(0))
                .attr("x2", x(initialX))
                .attr("y2", y(maxY))
                .style("stroke-width", 1)
                .style("stroke-dasharray", ("2, 3"))
                .style("stroke", "black")
                .style("fill", "none");
        const tooltipLineText = timechart.append('g')
            .append('text')
            .style("opacity", 0)
            .attr("text-anchor", "middle")
            .attr("alignment-baseline", "middle")
            .attr("y",y(maxY+LineTextOffset))
        // Create the text that travels along the curve of chart



        // Create a rect on top of the svg area: this rectangle recovers mouse position
        timechart.append('rect')
            .style("fill", "none")
            .style("pointer-events", "all")
            .attr('width', width)
            .attr('height', height)
            .on('mouseover', mouseover)
            .on('mousemove', mousemove)
            .on('mouseout', mouseout);


        function mouseover() {
            for (let index = 0; index < focus.length; index++) {
                focus[index].style("opacity", 1);
                focusText[index].style("opacity", 1);
                tooltipLine.style("opacity",1);
                tooltipLineText.style("opacity",1);
            }
        };

        function mousemove(event) {
            // recover coordinate we need
            const x0 = x.invert(d3.pointer(event)[0]);
            const i = bisect(data, x0, 1);
            const nearestDateTime = data[i].date.getTime();
            const selectedData = []
            for (let index = 0; index < data.length; index++) {
                if (data[index].date.getTime() === nearestDateTime) {
                    selectedData.push(data[index]);
                }
            }
            for (let i = 0; i < numLines; i++) {
                focus[i]
                    .attr("cx", x(selectedData[i].date))
                    .attr("cy", y(selectedData[i].tpp));
                focusText[i]
                    .html("y:" + selectedData[i].tpp)
                    .attr("x", x(selectedData[i].date) + 15)
                    .attr("y", y(selectedData[i].tpp));

            }
            tooltipLine.attr("x1", x(nearestDateTime))
                        .attr("x2", x(nearestDateTime));  //<<== change your code here
            tooltipLineText
                    .html("Date: "+formatDate(selectedData[0].date))
                    .attr("x", x(selectedData[0].date));
        };
        function mouseout() {
            for (let index = 0; index < focus.length; index++) {
                focus[index].style("opacity", 0);
                focusText[index].style("opacity", 0);
                tooltipLine.style("opacity",0);        
                tooltipLineText.style("opacity",0);
          
            }
        };

    })
