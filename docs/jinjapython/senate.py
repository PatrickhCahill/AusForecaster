
from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader("docs/templates")

env = Environment(loader=file_loader)

stylesheets=["css/bootstrap.css","my_css/navbar.css","my_css/senategraph.css","my_css/frame.css"]
scripts = ["js/bootstrap.js",
"https://d3js.org/d3.v4.min.js",
"js/d3-parliament.min.js",
"my_js/senategraph.js",
"https://d3js.org/d3.v5.min.js",
"my_js/cartogram.js"]
active="senate"


template = env.get_template('senate/senate.jinja')
output = template.render(stylesheets=stylesheets,active=active,scripts=scripts)
with open('docs/senate.html','w') as f:
    f.write(output)