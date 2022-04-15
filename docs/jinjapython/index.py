from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader("docs/templates")

env = Environment(loader=file_loader)

stylesheets=["css/bootstrap.css","my_css/navbar.css","my_css/bubble.css","my_css/frame.css","my_css/beegraph.css"]
scripts = ["js/bootstrap.js",
"https://d3js.org/d3.v5.min.js",
"https://cdn.jsdelivr.net/npm/chart.js",
"https://cdn.jsdelivr.net/npm/chartjs-adapter-date-fns/dist/chartjs-adapter-date-fns.bundle.min.js",
"https://ajax.googleapis.com/ajax/libs/jquery/3.6.0/jquery.min.js",
"my_js/bubblebackground.js",
"my_js/beeswarm.js",
"my_js/timecharttooltip.js",
"my_js/timechartmanager.js",
"my_js/timechart1.js",
"my_js/timechart2.js",
"my_js/timechart3.js"]

active="index"

data_dict = {
    "winner":"Labor",
    "loser":"Coalition",
    "winnerWith":"Labor",
    "favouredStatus":"very favoured",
    "winnerColour":"rgba(136, 31, 31, 0.82)",
    "winnerSeats":"82",
    "updateTime":"Today",
    "winnerChance":"a 91",
    "coalitionChance":"3",
    "laborChance":"91",
    "hungChance":"7",
    "chanceExample":"one in twenty"
}



template = env.get_template('index/index.jinja')
output = template.render(stylesheets=stylesheets,active=active,data=data_dict,scripts=scripts)
with open('docs/index.html','w') as f:
    f.write(output)