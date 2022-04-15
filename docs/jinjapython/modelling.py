from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader("docs/templates")

env = Environment(loader=file_loader)

stylesheets=["css/bootstrap.css","my_css/navbar.css","my_css/frame.css"]
scripts = ["js/bootstrap.js"]
active="about"


template = env.get_template('modelling/modelling.jinja')
output = template.render(stylesheets=stylesheets,active=active,scripts=scripts)
with open('docs/modelling.html','w') as f:
    f.write(output)