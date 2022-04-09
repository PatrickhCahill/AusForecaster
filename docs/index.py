from jinja2 import Environment, FileSystemLoader

file_loader = FileSystemLoader("docs/templates")

env = Environment(loader=file_loader)


page_dict = {
  "title": "House Forecast"
}
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


template = env.get_template('index-main.html')
output = template.render(page=page_dict,data=data_dict)
with open('docs/index.html','w') as f:
    f.write(output)