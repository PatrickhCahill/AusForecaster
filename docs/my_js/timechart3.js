d3.csv("page_data/timechart3data.csv").then(makeChart);
function makeChart(untreatedData) {
  const unparsedlabels = untreatedData.map(function (d) { return d.labels; });
  var labels = [];
  const parseTime = d3.timeParse("%Y-%m-%d");
  for(var i = 0; i<unparsedlabels.length;i++){labels.push(parseTime(unparsedlabels[i]))};
  const labor = untreatedData.map(function (d) { return d.labor; });
  const laborset = { label: "Labor's TPP", data: labor, backgroundColor: '#a62621', borderColor: '#a62621', };
  const liberal = untreatedData.map(function (d) { return d.coalition; });
  const liberalset = { label: "Coalition's TPP", data: liberal, backgroundColor: '#2d45a6', borderColor: '#2d45a6', };
  const chartdata = { dates: labels, labor: laborset, liberal: liberalset};

  const data = {
    labels: chartdata.dates,
    datasets: [chartdata.labor, chartdata.liberal]
  };

  const config = {
    type: 'line',
    data: data,
    options: {
      tension:0.5,
      borderWidth:2,
      responsive: true,
      maintainAspectRatio:false,
      interaction: {
        mode: 'index',
        intersect: false,
      },
      stacked: false,
      scales: {
        y: {
          type: 'linear',
          display: true,
          position: 'left',
          suggestedMin: 40,
          suggestedMax: 60,
          ticks:{          
            stepSize: 10,
            font:{family:'sans-serif',size:15}}
         
        },
        x: {
          type: 'time',
          time: {unit:'day'},
          grid: { color: 'rgba(0,0,0,0)' },
          ticks:{font:{family:'sans-serif',size:15}}
        },

      },
      plugins: {
        tooltip: {
          enabled: false,
          position: 'nearest',
          external: externalTooltipHandler3
        }
      },
      datasets: { line: { pointRadius: 0 } }
    },
  };

  const myChart = new Chart(
    document.getElementById('timechart3'),
    config
  );


};

