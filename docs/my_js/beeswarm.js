//Creates the svg and id that stores the chart
//Edit The height,width and change the relative sizes. The graph will dynamically change its size to fit the div it's contained in.

let bee__height = 400;
let bee__width = 1000;
let bee__margin = ({ top: 0, right: 40, bottom: 40, left: 40 });
let bee = d3.select("#bee")
    .append("svg")
    .attr("preserveAspectRatio", "xMinYMin meet")
    .attr("viewBox", "0 0 1000 400");




//Here we define the colors that will be used to fill the circles.
let colors = d3.scaleOrdinal()
    .domain(["Labor", "Coalition", "Hung"])
    .range(['#a62621', '#2d45a6', '#858585']);

d3.select("#laborColor").style("color", colors("nLabor"));
d3.select("#coalitionColor").style("color", colors("nLib"));
d3.select("#hungParliament").style("color", colors("nThird"));

// We append "g" which is a group that will contain the x-axis
bee.append("g")
    .attr("class", "x axis")
    .attr("transform", "translate(0," + (bee__height - bee__margin.bottom) + ")");


// The line that goes from axis to the tooltip is created.
let xLine = bee.append("line")
    .attr("stroke", "rgb(96,125,139)")

// Create tooltip div and make it invisible
let tooltip = d3.select("#bee").append("div")
    .attr("class", "bee-tooltip")
    .style("opacity", 0);

// Load and process data
d3.csv("page_data/beedata.csv").then(function (data) {
    let dataSet = data;
    redraw();

    function redraw() {

        // Defines the domain and the range: range() represents the pixels on the screens and domain represents the values of the data.
        xScale = d3.scaleLinear().range([bee__margin.left, bee__width - bee__margin.right])
            .domain([0, 151]);
        
        // xAxis is the xAxis which is created from the xScale function.
        let xAxis = d3.axisBottom(xScale)
            .ticks(11)
            .tickSizeOuter(0);

        //We the then attach the class="x axis" to the xAxis which renders our axis.
        d3.transition(bee).select(".x.axis")
            .transition()
            .duration(1000)
            .call(xAxis);

        // At this stage we have defined the "canvas" and placed an x-axis on it. We now want to distribute the data we loaded onto the canvas
        // To do this we will use a forceSimulation()




        // Create simulation with specified dataset
        let simulation = d3.forceSimulation(dataSet)
            // This creates a force in the x direction that places the data points in the CORRECT POSITION
            .force("x", d3.forceX(function (d) {
                // Mapping of values from total column of dataset to range of SVG chart (<bee__margin.left, bee__margin.right>)
                return xScale(+d["nLabor"]);  // This is the desired position
            }).strength(2))  // Increases the strength of the force, bubbles will converge faster.
            .force("y", d3.forceY((bee__height / 2) - bee__margin.bottom / 2))  // // Apply positioning force to push nodes towards center along Y axis
            .force("collide", d3.forceCollide(12)) // Apply collision force with radius of 9 - keeps nodes centers 9 pixels apart
            .stop();  // Stop simulation from starting automatically

        // Manually run simulation
        for (let i = 0; i < dataSet.length; ++i) {
            simulation.tick(10);
        }

        // Create circles
        let winnersCircles = bee.selectAll(".winners")
            .data(dataSet, function (d) { return d.Winner });

        winnersCircles.exit()
            .transition()
            .duration(1000)
            .attr("cx", 0)
            .attr("cy", (bee__height / 2) - bee__margin.bottom / 2)
            .remove();

        winnersCircles.enter()
            .append("circle")
            .attr("class", "winners")
            .attr("cx", 0)
            .attr("cy", (bee__height / 2) - bee__margin.bottom / 2)
            .attr("r", 12)
            .attr("fill", function (d) { return colors(d.Winner) })
            .merge(winnersCircles)
            .transition()
            .duration(2000)
            .attr("cx", function (d) { return d.x; })
            .attr("cy", function (d) { return d.y; })
            .style("stroke-width", 3)   
            .style("stroke", "white");

        // Defining Tooltip
        d3.selectAll(".winners").on("mousemove", function (d) {
            tooltip.html(`Winner: <strong>${d.Winner}</strong><br>
                          ${"No. Of Labor Seats ".slice(0, "No. Of Labor Seats ".indexOf(","))}: 
                          <strong>${d3.format(",")(d["nLabor"])}</strong>
                          ${"No. Of Labor Seats ".slice("No. Of Labor Seats ".lastIndexOf(" "))}`)
                .style('top', d3.event.pageY - 12 + 'px')
                .style('left', d3.event.pageX + 25 + 'px')
                .style("opacity", 0.9);

            xLine.attr("x1", d3.select(this).attr("cx"))
                .attr("y1", d3.select(this).attr("cy"))
                .attr("y2", (bee__height - bee__margin.bottom))
                .attr("x2", d3.select(this).attr("cx"))
                .attr("opacity", 1);

        }).on("mouseout", function (_) {
            tooltip.style("opacity", 0);
            xLine.attr("opacity", 0);
        });

    }

}).catch(function (error) {
    if (error) throw error;
});