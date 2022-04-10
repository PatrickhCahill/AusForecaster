const getOrCreateTooltip = (chart) => {
    let tooltipEl = chart.canvas.parentNode.querySelector('div');
  
    if (!tooltipEl) {
      tooltipEl = document.createElement('div');
      tooltipEl.style.background = 'rgba(0, 0, 0, 0.7)';
      tooltipEl.style.borderRadius = '3px';
      tooltipEl.style.color = 'white';
      tooltipEl.style.opacity = 1;
      tooltipEl.style.pointerEvents = 'none';
      tooltipEl.style.position = 'absolute';
      tooltipEl.style.transform = 'translate(-50%, 0)';
      tooltipEl.style.transition = 'all .1s ease';
  
      const table = document.createElement('table');
      table.style.margin = '0px';
  
      tooltipEl.appendChild(table);
      chart.canvas.parentNode.appendChild(tooltipEl);
    }
  
    return tooltipEl;
  };
  
  const externalTooltipHandler = (context) => {
    // Tooltip Element
    const {chart, tooltip} = context;
    const tooltipEl = getOrCreateTooltip(chart);
    // Hide if no tooltip
    if (tooltip.opacity === 0) {
      tooltipEl.style.opacity = 0;
      return;
    }
  
    // Set Text
    if (tooltip.body) {
      let titleunparsed = tooltip.title[0]
      titleunparsed = titleunparsed.slice(0,titleunparsed.length-15)
      parseTime = d3.timeParse("%b %d, %Y")
      const parsedTitle =d3.timeFormat("%d/%m/%y")(parseTime(titleunparsed));
      const title = document.createTextNode(parsedTitle+"");
      const bodyLines = tooltip.body.map(b => b.lines);
  
      const tableHead = document.createElement('thead');
      const spanhead = document.createElement('span');
      spanhead.style.background = colors.backgroundColor;
      spanhead.style.borderColor = colors.borderColor;
      spanhead.style.borderWidth = '2px';
      spanhead.style.marginRight = '10px';
      spanhead.style.height = '10px';
      spanhead.style.width = '10px';
      spanhead.style.display = 'inline-block';
      const trhead = document.createElement('tr');
      trhead.style.backgroundColor = 'inherit';
      trhead.style.borderWidth = 0;

      const tdhead = document.createElement('td');
      tdhead.style.borderWidth = 0;
      tdhead.appendChild(spanhead);
      tdhead.appendChild(title);
      trhead.appendChild(tdhead);
      tableHead.appendChild(trhead);


      const tableBody = document.createElement('tbody');
      bodyLines.forEach((body, i) => {
        const colors = tooltip.labelColors[i];
  
        const span = document.createElement('span');
        span.style.background = colors.backgroundColor;
        span.style.borderColor = colors.borderColor;
        span.style.borderWidth = '2px';
        span.style.marginRight = '10px';
        span.style.height = '10px';
        span.style.width = '10px';
        span.style.display = 'inline-block';
  
        const tr = document.createElement('tr');
        tr.style.backgroundColor = 'inherit';
        tr.style.borderWidth = 0;
  
        const td = document.createElement('td');
        td.style.borderWidth = 0;
        body = body+"";
        if (body.slice(0,1)=="L") {
            var outtext = "Labor: "+body.slice(body.length-2,body.length)+"%";
        } else if (body.slice(0,1)=="C"){
            var outtext = "Coalition: "+body.slice(body.length-2,body.length)+"%";
        } else if (body.slice(0,1)=="H"){
            var outtext = "Hung Parliament: "+body.slice(body.length-2,body.length)+"%";
        } else if (body.slice(0,8)=="No. of L"){
          var outtext = "Labor: "+body.slice(body.length-2,body.length);
        }else if (body.slice(0,8)=="No. of C"){
          var outtext = "Coalition: "+body.slice(body.length-2,body.length);
        }else if (body.slice(0,8)=="No. of O"){
          var outtext = "Others: "+body.slice(body.length-2,body.length);
        }
        else{var outtext = body}

        const text = document.createTextNode(outtext);
        td.appendChild(span);
        td.appendChild(text);
        tr.appendChild(td);
        tableBody.appendChild(tr);
      });
  
      const tableRoot = tooltipEl.querySelector('table');
  
      // Remove old children
      while (tableRoot.firstChild) {
        tableRoot.firstChild.remove();
      }
  
      // Add new children
      tableRoot.appendChild(tableHead);
      tableRoot.appendChild(tableBody);
    }
  
    const {offsetLeft: positionX, offsetTop: positionY} = chart.canvas;
  
    // Display, position, and set styles for font
    tooltipEl.style.opacity = 1;
    tooltipEl.style.left = positionX + tooltip.caretX + 'px';
    tooltipEl.style.top = positionY + tooltip.caretY + 'px';
    tooltipEl.style.font = tooltip.options.bodyFont.string;
    tooltipEl.style.padding = tooltip.options.padding + 'px ' + tooltip.options.padding + 'px';
  };

  const externalTooltipHandler3 = (context) => {
    // Tooltip Element
    const {chart, tooltip} = context;
    const tooltipEl = getOrCreateTooltip(chart);
  
    // Hide if no tooltip
    if (tooltip.opacity === 0) {
      tooltipEl.style.opacity = 0;
      return;
    }
  
    // Set Text
    if (tooltip.body) {
      let titleunparsed = tooltip.title[0]
      titleunparsed = titleunparsed.slice(0,titleunparsed.length-15)
      parseTime = d3.timeParse("%b %d, %Y")
      const parsedTitle =d3.timeFormat("%d/%m/%y")(parseTime(titleunparsed));
      const title = document.createTextNode(parsedTitle+"");
      const bodyLines = tooltip.body.map(b => b.lines);
  
      const tableHead = document.createElement('thead');
      const spanhead = document.createElement('span');
      spanhead.style.background = colors.backgroundColor;
      spanhead.style.borderColor = colors.borderColor;
      spanhead.style.borderWidth = '2px';
      spanhead.style.marginRight = '10px';
      spanhead.style.height = '10px';
      spanhead.style.width = '10px';
      spanhead.style.display = 'inline-block';
      const trhead = document.createElement('tr');
      trhead.style.backgroundColor = 'inherit';
      trhead.style.borderWidth = 0;

      const tdhead = document.createElement('td');
      tdhead.style.borderWidth = 0;
      tdhead.appendChild(spanhead);
      tdhead.appendChild(title);
      trhead.appendChild(tdhead);
      tableHead.appendChild(trhead);

      const tableBody = document.createElement('tbody');
      bodyLines.forEach((body, i) => {
        const colors = tooltip.labelColors[i];
  
        const span = document.createElement('span');
        span.style.background = colors.backgroundColor;
        span.style.borderColor = colors.borderColor;
        span.style.borderWidth = '2px';
        span.style.marginRight = '10px';
        span.style.height = '10px';
        span.style.width = '10px';
        span.style.display = 'inline-block';
  
        const tr = document.createElement('tr');
        tr.style.backgroundColor = 'inherit';
        tr.style.borderWidth = 0;
  
        const td = document.createElement('td');
        td.style.borderWidth = 0;
        body = body+"";

        if (body.slice(0,1)=="L") {
            var outtext = "Labor: "+body.slice(body.length-4,body.length)+"%";
        } else if (body.slice(0,1)=="C"){
            var outtext = "Coalition: "+body.slice(body.length-4,body.length)+"%";
        } else if (body.slice(0,1)=="H"){
            var outtext = "Hung Parliament: "+body.slice(body.length-4,body.length)+"%";
        }
        else{var outtext = body}

        const text = document.createTextNode(outtext);
  
        td.appendChild(span);
        td.appendChild(text);
        tr.appendChild(td);
        tableBody.appendChild(tr);
      });
  
      const tableRoot = tooltipEl.querySelector('table');
  
      // Remove old children
      while (tableRoot.firstChild) {
        tableRoot.firstChild.remove();
      }
  
      // Add new children
      tableRoot.appendChild(tableHead);
      tableRoot.appendChild(tableBody);
    }
  
    const {offsetLeft: positionX, offsetTop: positionY} = chart.canvas;
  
    // Display, position, and set styles for font
    tooltipEl.style.opacity = 1;
    tooltipEl.style.left = positionX + tooltip.caretX + 'px';
    tooltipEl.style.top = positionY + tooltip.caretY + 'px';
    tooltipEl.style.font = tooltip.options.bodyFont.string;
    tooltipEl.style.padding = tooltip.options.padding + 'px ' + tooltip.options.padding + 'px';
  };


