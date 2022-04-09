# Readme To Understand The Code
The code is divided into two categories:

1. Simulation (Python - runs once)
2. html generators (R - runs concurrently for interactive graphs)

## Simulations
This code is written in python and is designed to run once for each update of the model.

There are two python files of concern - a) regression_model.py and b) model.py. The regression_model is used to calculate weights and to handle polling data, while the model is used to run the total simulations and write the results to a csv.

## html generators
The csv's produced by the simulation code is then handled in two ways. An R markdown code is used to generate histogram and seat changes as html. This only runs once. There is also an interactive shinyapp written in R that runs continuosly and in hosted on shinyapp.io.