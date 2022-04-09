var parliament = d3v4.parliament().width(300).innerRadiusCoef(0.4);
parliament.enter.fromCenter(true).smallToBig(true);
parliament.exit.toCenter(true).bigToSmall(true);
parliament.on("click", function(e) { console.log(e); });

var setData = function(d) {
    d3v4.select("#parliament").datum(d).call(parliament);
};

d3v4.json("page_data/senate.json", setData);
