var svg = d3.select("#australiasenatemap").append("svg").attr("width", 200).attr("height", 260)

const labor = "#a62621";
const liberal = "#2d45a6";
const green = "#32CD32";
const ind = "#909090";
const notup = "#262626"

const nsw = { first: labor, second: labor, third: liberal, fourth: green, fifth: liberal, sixth: labor };
const vic = { first: liberal, second: liberal, third: green, fourth: labor, fifth: labor, sixth: labor };
const qld = { first: liberal, second: liberal, third: liberal, fourth: labor, fifth: labor, sixth: green };
const tas = { first: labor, second: labor, third: labor, fourth: liberal, fifth: liberal, sixth: green };
const wa = { first: liberal, second: liberal, third: green, fourth: labor, fifth: labor, sixth: labor };
const sa = { first: liberal, second: liberal, third: labor, fourth: labor, fifth: green, sixth: ind };
const nt = { first: notup, second: notup };
const act = { first: notup, second: notup };




//TASMANIA
svg.append('circle')
    .attr('cx', 160)
    .attr('cy', 240)
    .attr('r', 7)
    .attr('fill', tas.first);
svg.append('circle')
    .attr('cx', 140)
    .attr('cy', 240)
    .attr('r', 7)
    .attr('fill', tas.fifth);
svg.append('circle')
    .attr('cx', 160)
    .attr('cy', 220)
    .attr('r', 7)
    .attr('fill', tas.third);
svg.append('circle')
    .attr('cx', 140)
    .attr('cy', 220)
    .attr('r', 7)
    .attr('fill', tas.fourth);
svg.append('circle')
    .attr('cx', 160)
    .attr('cy', 200)
    .attr('r', 7)
    .attr('fill', tas.second);
svg.append('circle')
    .attr('cx', 140)
    .attr('cy', 200)
    .attr('r', 7)
    .attr('fill', tas.sixth);
svg.append('rect')
    .attr('x', 130)
    .attr('y', 190)
    .attr('width', 40)
    .attr('height', 60)
    .attr('stroke', 'black')
    .attr('border-radius', 20)
    .attr('fill', 'rgba(0,0,0,0)')


//VICTORIA
svg.append('circle')
    .attr('cx', 160)
    .attr('cy', 160)
    .attr('r', 7)
    .attr('fill', vic.first);
svg.append('circle')
    .attr('cx', 140)
    .attr('cy', 160)
    .attr('r', 7)
    .attr('fill', vic.second);
svg.append('circle')
    .attr('cx', 120)
    .attr('cy', 160)
    .attr('r', 7)
    .attr('fill', vic.third);
svg.append('circle')
    .attr('cx', 160)
    .attr('cy', 140)
    .attr('r', 7)
    .attr('fill', vic.fourth);
svg.append('circle')
    .attr('cx', 140)
    .attr('cy', 140)
    .attr('r', 7)
    .attr('fill', vic.fifth);
svg.append('circle')
    .attr('cx', 120)
    .attr('cy', 140)
    .attr('r', 7)
    .attr('fill', vic.sixth);
svg.append('rect')
    .attr('x', 110)
    .attr('y', 130)
    .attr('width', 60)
    .attr('height', 40)
    .attr('stroke', 'black')
    .attr('border-radius', 20)
    .attr('fill', 'rgba(0,0,0,0)')



//NSW
svg.append('circle')
    .attr('cx', 160)
    .attr('cy', 120)
    .attr('r', 7)
    .attr('fill', nsw.first);
svg.append('circle')
    .attr('cx', 140)
    .attr('cy', 120)
    .attr('r', 7)
    .attr('fill', nsw.second);
svg.append('circle')
    .attr('cx', 120)
    .attr('cy', 120)
    .attr('r', 7)
    .attr('fill', nsw.sixth);
svg.append('circle')
    .attr('cx', 160)
    .attr('cy', 100)
    .attr('r', 7)
    .attr('fill', nsw.fourth);
svg.append('circle')
    .attr('cx', 140)
    .attr('cy', 100)
    .attr('r', 7)
    .attr('fill', nsw.fifth);
svg.append('circle')
    .attr('cx', 120)
    .attr('cy', 100)
    .attr('r', 7)
    .attr('fill', nsw.third);

svg.append('rect')
    .attr('x', 110)
    .attr('y', 90)
    .attr('width', 60)
    .attr('height', 40)
    .attr('stroke', 'black')
    .attr('border-radius', 20)
    .attr('fill', 'rgba(0,0,0,0)')
//QLD
svg.append('circle')
    .attr('cx', 120)
    .attr('cy', 80)
    .attr('r', 7)
    .attr('fill', qld.first);
svg.append('circle')
    .attr('cx', 100)
    .attr('cy', 80)
    .attr('r', 7)
    .attr('fill', qld.second);
svg.append('circle')
    .attr('cx', 100)
    .attr('cy', 60)
    .attr('r', 7)
    .attr('fill', qld.third);
svg.append('circle')
    .attr('cx', 100)
    .attr('cy', 40)
    .attr('r', 7)
    .attr('fill', qld.sixth);
svg.append('circle')
    .attr('cx', 80)
    .attr('cy', 80)
    .attr('r', 7)
    .attr('fill', qld.fifth);
svg.append('circle')
    .attr('cx', 80)
    .attr('cy', 60)
    .attr('r', 7)
    .attr('fill', qld.fourth);

svg.append('line')
    .attr('x1', 90)
    .attr('y1', 30)
    .attr('x2', 110)
    .attr('y2', 30)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 110)
    .attr('y1', 30)
    .attr('x2', 110)
    .attr('y2', 70)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 110)
    .attr('y1', 70)
    .attr('x2', 130)
    .attr('y2', 70)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 130)
    .attr('y1', 70)
    .attr('x2', 130)
    .attr('y2', 90)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 130)
    .attr('y1', 90)
    .attr('x2', 70)
    .attr('y2', 90)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 70)
    .attr('y1', 90)
    .attr('x2', 70)
    .attr('y2', 50)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 70)
    .attr('y1', 50)
    .attr('x2', 90)
    .attr('y2', 50)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 90)
    .attr('y1', 50)
    .attr('x2', 90)
    .attr('y2', 30)
    .attr('stroke', 'black')

//NT
svg.append('circle')
    .attr('cx', 60)
    .attr('cy', 80)
    .attr('r', 7)
    .attr('fill', nt.first);
svg.append('circle')
    .attr('cx', 60)
    .attr('cy', 60)
    .attr('r', 7)
    .attr('fill', nt.second);

svg.append('rect')
    .attr('x', 50)
    .attr('y', 50)
    .attr('width', 20)
    .attr('height', 40)
    .attr('stroke', 'black')
    .attr('border-radius', 20)
    .attr('fill', 'rgba(0,0,0,0)')


//SA
svg.append('circle')
    .attr('cx', 80)
    .attr('cy', 140)
    .attr('r', 7)
    .attr('fill', sa.first);
svg.append('circle')
    .attr('cx', 80)
    .attr('cy', 120)
    .attr('r', 7)
    .attr('fill', sa.second);
svg.append('circle')
    .attr('cx', 60)
    .attr('cy', 120)
    .attr('r', 7)
    .attr('fill', sa.fifth);
svg.append('circle')
    .attr('cx', 100)
    .attr('cy', 100)
    .attr('r', 7)
    .attr('fill', sa.fourth);
svg.append('circle')
    .attr('cx', 80)
    .attr('cy', 100)
    .attr('r', 7)

    .attr('fill', sa.third);
svg.append('circle')
    .attr('cx', 60)
    .attr('cy', 100)
    .attr('r', 7)
    .attr('fill', sa.sixth);

svg.append('line')
    .attr('x1', 70)
    .attr('y1', 150)
    .attr('x2', 90)
    .attr('y2', 150)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 70)
    .attr('y1', 150)
    .attr('x2', 70)
    .attr('y2', 130)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 70)
    .attr('y1', 130)
    .attr('x2', 50)
    .attr('y2', 130)
    .attr('stroke', 'black')
//ACT
svg.append('circle')
    .attr('cx', 100)
    .attr('cy', 120)
    .attr('r', 7)

    .attr('fill', act.first);
svg.append('circle')
    .attr('cx', 100)
    .attr('cy', 140)
    .attr('r', 7)
    .attr('fill', act.second);

svg.append('rect')
    .attr('x', 90)
    .attr('y', 110)
    .attr('width', 20)
    .attr('height', 40)
    .attr('stroke', 'black')
    .attr('border-radius', 20)
    .attr('fill', 'rgba(0,0,0,0)')
//WA
svg.append('circle')
    .attr('cx', 40)
    .attr('cy', 80)
    .attr('r', 7)
    .attr('fill', wa.first);
svg.append('circle')
    .attr('cx', 40)
    .attr('cy', 100)
    .attr('r', 7)

    .attr('fill', wa.second);
svg.append('circle')
    .attr('cx', 40)
    .attr('cy', 120)
    .attr('r', 7)
    .attr('fill', wa.third);
svg.append('circle')
    .attr('cx', 20)
    .attr('cy', 100)
    .attr('r', 7)
    .attr('fill', wa.fourth);
svg.append('circle')
    .attr('cx', 20)
    .attr('cy', 120)
    .attr('r', 7)
    .attr('fill', wa.fifth);
svg.append('circle')
    .attr('cx', 20)
    .attr('cy', 140)
    .attr('r', 7)
    .attr('fill', wa.sixth);

svg.append('line')
    .attr('x1', 10)
    .attr('y1', 150)
    .attr('x2', 10)
    .attr('y2', 90)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 10)
    .attr('y1', 90)
    .attr('x2', 30)
    .attr('y2', 90)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 30)
    .attr('y1', 90)
    .attr('x2', 30)
    .attr('y2', 70)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 30)
    .attr('y1', 70)
    .attr('x2', 50)
    .attr('y2', 70)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 50)
    .attr('y1', 70)
    .attr('x2', 50)
    .attr('y2', 130)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 50)
    .attr('y1', 130)
    .attr('x2', 30)
    .attr('y2', 130)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 30)
    .attr('y1', 130)
    .attr('x2', 30)
    .attr('y2', 150)
    .attr('stroke', 'black')
svg.append('line')
    .attr('x1', 30)
    .attr('y1', 150)
    .attr('x2', 10)
    .attr('y2', 150)
    .attr('stroke', 'black')