# An Australian Election Forecaster 
By _Patrick Cahill_
### Code in this repositry will generate simulations, probabilities and visualisations for the upcoming Australian Election

### A Brief

In the 2019 Federal Australian Election polling missed badly. The main pollster for the election, the traditionally reliable **Newspoll**, showed a TPP preferred final polling of 52 for the ALP - predicting a change in government. In reality, the coalition achieved a half point swing in their direction, and restored their majority.

There were a combination of major errors that led to flawed consensus of Australian media, that Bill Shortern was likely to become the next Australian Prime Minister. Chief among them was the common statistically illeterate belief that if something is probable, then it is guaranteed. The goal of this forecaster is to take the polling data, combine it with correlations between seats and other indicators for the upcoming election to generate a probability of a particular party winning the next election.

### Plan: (IN PROGRESS)
1. Polling Data Wrangling
2. Historical Data Wrangling
3. Simulate Elections
4. Visualise and Express Simulations

## 1. Polling Data Wrangling
Unlike in other countries, polling in Australia is relatively rare. With the exception of the two major pollsters - **Newspoll** (Owned by **YouGov**) and **Roy Morgan**, there are relatively few polls. This odd lack of polls compared to other countries means that the polling averages have larger uncertainties than usual.

-Poll Breakdowns Occur State-by-State and Federally.
-Most polls report primary vote data and TPP. 2019 data suggests that much of the polling error was in assumptions about preference distribution (especially with minor parties such as the UAP). To account for this the model performs a regression analysis based off previous elections and current polling to calculate our own preference distribution. This is then applied to the primary vote data of the polls in order to generate TPP.
-A weighted average of the generated TPP data is taken, determined by sample size and time since poll - weights are calculated by a regression of the 2019 election data.

From inputted polling data, the model then outputs an average TPP for the ALP in each state and federally - each with associated uncertainties.

## 2. Historical Data Wrangling
A common feature in elections across the world is that certain "types" of seats tend to vote together. Wealthy City Seats tend to vote Liberal with a high Greens primary vote, while metropolitan seats are overwhelmingly Labor (again with high Greens primary vote). Meanwhile, suburban seats tend to be the most marginal - up for grabs between the Coalition or Labor, while rural seats are a competition between Labor and the Nationals.

Every seat's TPP result for the past 3 elections is used and compared to produce a correlation matrix - which weakly quantifies the above heuristics. Also, the regionality of a seat is stored because trends for the past twenty years suggest swings are much larger (approx. 2x) in urban areas than in rural areas. This data is stored along with the 2019 election results.

## 3. Simulate Elections
The weighted TPP swing in each seat is calculated by a combination of state and federal polling. A unified (accounting for regionality) swing across the country is initially assumed to generate average TPP values in each seat. The list of seats is then randomised. The first seat is then simulated with the average value and uncertainty (found in 1.) assuming a normal outcome. The difference between the actual result and the expected outcome is then used to update the remaining 150 seats via the correlation matrix. This process is then repeated throughout all the seats until a final outcome is simulate.

This election simulation is then repeated thousands of times in order to calculate the final results - and a then a simple probability is calculated.

## 4. Visualisation
WIP
