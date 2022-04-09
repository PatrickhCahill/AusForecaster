var svg = d3.select("#australiasenatemap")
.append("svg")
.attr("preserveAspectRatio", "xMinYMin meet")
.attr("viewBox", "0 0 220 260");
const labor = "#a62621";
const liberal = "#2d45a6";
const green = "#32CD32";
const ind = "#909090";
const notup = "#262626";

const nsw = { first: labor, second: green, third: labor, fourth: labor, fifth: liberal, sixth: liberal };
const vic = { first: liberal, second: green, third: liberal, fourth: labor, fifth: labor, sixth: labor };
const qld = { first: liberal, second: liberal, third: liberal, fourth: labor, fifth: labor, sixth: green };
const tas = { first: labor, second: labor, third: labor, fourth: liberal, fifth: liberal, sixth: green };
const wa = { first: labor, second: labor, third: labor, fourth: green, fifth: liberal, sixth: liberal };
const sa = { first: labor, second: liberal, third: liberal, fourth: labor, fifth: green, sixth: ind };
const nt = { first: notup, second: notup };
const act = { first: notup, second: notup };


function makecircle(cx,cy,col){
    svg.append('circle')
    .attr('cx', cx)
    .attr('cy', cy)
    .attr('r', 7)
    .attr('fill', col)
    .transition()
    .duration(1000);
};
function outline(x1,y1,x2,y2){
    svg.append('line')
    .attr('x1', x1)
    .attr('y1', y1)
    .attr('x2', x2)
    .attr('y2', y2)
    .attr('stroke', 'black')
    .attr('stroke-width','0.2px')
}
//TASMANIA
makecircle(180,240,tas.first);
makecircle(160,240,tas.second);
makecircle(140,240,tas.third);
makecircle(180,220,tas.fourth);
makecircle(160,220,tas.fifth);
makecircle(140,220,tas.sixth);

svg.append('rect')
    .attr('x', 130)
    .attr('y', 210)
    .attr('width', 60)
    .attr('height', 40)
    .attr('stroke', 'black')
    .attr('stroke-width','0.2px')
    .attr('fill', 'rgba(0,0,0,0)');
//VICTORIA
makecircle(160,180,vic.first);
makecircle(180,160,vic.second);
makecircle(160,160,vic.third);
makecircle(140,160,vic.fourth);
makecircle(140,140,vic.fifth);
makecircle(180,140,vic.sixth);

outline(130,170,150,170);
outline(150,170,150,190);
outline(150,190,170,190);
outline(170,190,170,170);
outline(170,170,190,170);
outline(190,170,190,90);
outline(190,130,170,130);
outline(170,130,170,150);
outline(130,170,130,130);
outline(130,170,130,130);
outline(130,130,150,130);
//ACT
makecircle(160,140,act.first);
makecircle(160,120,act.second);

svg.append('rect')
    .attr('x', 150)
    .attr('y', 110)
    .attr('width', 20)
    .attr('height', 40)
    .attr('stroke', 'black')
    .attr('stroke-width','0.2px')
    .attr('fill', 'rgba(0,0,0,0)');
//NSW
makecircle(180,120,nsw.first);
makecircle(120,100,nsw.second);
makecircle(140,120,nsw.third);
makecircle(180,100,nsw.fourth);
makecircle(160,100,nsw.fifth);
makecircle(140,100,nsw.sixth);

outline(110,110,110,90);
outline(110,110,130,110);
outline(130,110,130,130);
//QUEENSLAND
makecircle(160,80,qld.first);
makecircle(160,60,qld.second);
makecircle(140,80,qld.third);
makecircle(140,60,qld.fourth);
makecircle(140,40,qld.fifth);
makecircle(120,80,qld.sixth);


outline(130,30,150,30);
outline(150,30,150,50);
outline(150,50,170,50);
outline(170,50,170,90);
outline(130,30,130,70);
outline(130,70,110,70);
outline(110,70,110,90);
outline(190,90,110,90);
//SA
makecircle(120,120,sa.first);
makecircle(100,120,sa.second);
makecircle(80,120,sa.third);
makecircle(120,140,sa.fourth);
makecircle(100,100,sa.fifth);
makecircle(80,100,sa.sixth);

outline(70,130,70,90);
outline(70,90,90,90);
outline(70,130,110,130);
outline(110,130,110,150);
outline(110,150,130,150);
//NT
makecircle(100,80,nt.first)
makecircle(100,60,nt.second)

svg.append('rect')
    .attr('x', 90)
    .attr('y', 50)
    .attr('width', 20)
    .attr('height', 40)
    .attr('stroke', 'black')
    .attr('stroke-width','0.2px')
    .attr('fill', 'rgba(0,0,0,0)');
//WA
makecircle(60,80,wa.first)
makecircle(60,100,wa.second)
makecircle(60,120,wa.third)
makecircle(60,140,wa.fourth)
makecircle(40,100,wa.fifth)
makecircle(40,120,wa.sixth)

outline(50,150,70,150);
outline(70,150,70,70);
outline(50,70,70,70);
outline(50,70,50,90);
outline(50,90,30,90);
outline(30,90,30,130);
outline(30,130,50,130);
outline(50,130,50,150);


