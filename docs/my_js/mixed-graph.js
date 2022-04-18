d3.csv("page_data/mixed-graphdata.csv").then(makeChart);
function makeChart(unparseddata) {
    let labels = []
    let data   = []
    let colors = []
    let hovercolors = []
    for (let index = 0; index < unparseddata.length; index++) {
        labels.push(unparseddata[index].nLabor)
        data.push(+unparseddata[index].frequency)
        if(unparseddata[index].nLabor<=69){colors.push( "rgba(45, 69, 166,0.7)");hovercolors.push( "rgba(45, 69, 166,1)")}   
    else if(unparseddata[index].nLabor>=76){colors.push( "rgba(166, 38, 33,0.7)");hovercolors.push( "rgba(166, 38, 33,1)")}
    else {colors.push("rgba(133, 133, 133,0.7)");hovercolors.push( "rgba(133, 133, 133,1)")}
    }
    const config = {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                label: "Europe",
                type: "line",
                borderColor: "#858585",
                data: data,
                fill: false
            }, {
                label: "Europe",
                type: "bar",
                backgroundColor: colors,
                data: data,
                pointHoverBackgroundColor: hovercolors
            }
            ]
        },
        options: {
            title: {display: true,},
            plugins: {legend: { display: false }},
            tension: 0.6,
            scales:{x:{
                        grid: { color: 'rgba(0,0,0,0)' },
                        ticks:{font:{family:'sans-serif',size:21}}
                    },
                    y:{
                        grid: { color: 'rgba(0,0,0,0)' },
                        ticks:{font:{family:'sans-serif',size:21}},
                        position: 'none',
                    }                }
        }
    }
    new Chart(document.getElementById("mixed-chart"),config);
};