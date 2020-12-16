# Predicting California Wildfires

## Overview

This project's aim is to build a classification model that will predict if there will be a fire in given county over the course of that week. This will be done by using wildfire incidents from Kaggle, and combining it with data about fuel sources by using ground cover data, topography by using elevation data and weather data from CIMIS and Weather Underground. Predicting the weekly probability of wildfires can provide early warning to government groups like CalFire in fighting the spread of wildfires.

## Business Problem

As of early December, there have been more than 9,500 wildfires that have burned more than 4 million acres of California land. California has about 100 million acres, so nearly 4% of California's land has burned from wildfires in the year 2020. This makes 2020 the most destructive year of wildfires recorded in California. Right now the government group CalFire has a Red Flag and Fire Watch Warning system which is issued during forecasted weather events 24-72 hours in advance, which may result in wildfire behavior. The model in this project would predict the probabilities of a wildfire occuring in a county of California during a specific week based on the three main factors that affect wildfire behavior: weather, topography, and fuels. CalFire could use this model in addition to their warning system to better allocate funds and personnel to counties in more danger of wildfire incidents, and thus better control the spread of wildfires that do start.

## Data Understanding

The data set used in the modeling is gathered from muliple sources. The original wildfire data comes from a Kaggle data set that had over 1600 different incidents between 2013 and 2020 that the government group CalFire managed the containment of. From this data set, the `acres_burned`, `county`, and `Start` date were used in the final data set. From the `Start` and `county` columns we regrouped the data based on a weekly basis per county and `acres_burned` gave our target variable if there was an indicent in that county and week or not. To help predict the probability of wildfire, we used the features that affect wildfire behavior: Fuel, Topography, and Weather.

The Fuel data was gathered from the California Land Use and Ownership Portal by the University of California. Between the years of 2013-2018, each county has a Summary Land Use Statistics csv file for each year. There are 26 different types of land cover, like agriculture use, type of forest, or even barren. All these different files were combined into one dataset that that had number of acres and percentage of county land for each tyoe of landcover. 

The Topography data used the min and max elevations of the counties from the Anyplace America topographic maps.

The Weather Data was gathered from the California Irrigation Management Information System (CIMIS) by the California Department of Water Resources and from the Weather Underground Website. The daily measurements for the following features were grabbed:

- `Avg Air Temp (F)`
- `Max Air Temp (F)`
- `Min Air Temp (F)`
- `Max Rel Hum (%)`
- `Avg Rel Hum (%)`
- `Min Rel Hum (%)`
- `Dew Point (F)`
- `Avg Wind Speed (mph)`
- `Precip (in)`

For each of the features, the previous week's and previous month's averages were created for the final data set.

