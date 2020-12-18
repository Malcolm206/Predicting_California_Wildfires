# Predicting California Wildfires
**Authors** <br>
[Malcolm Katzenbach](https://github.com/malcolm206)<br>

![forest_fire](https://unsplash.com/photos/nVYEechGqqM)

## Repository Structure

```
├── data                                <- Gathered externally
├── Images                              <- Generated from code
├── Models                              <- pickled models
├── Notebooks                           <- All modeling, data collection, data prep, and EDA notebooks
├── Source                              <- Custom Library .py file with functions
├── California_Wildfires.ipynb          <- Final Notebook
├── presentation.pdf                    <- Slide Deck
└── README.md                           <- The high-level overview of this project
```

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

## Exploratory Data Analysis

We first check to see the number of weeks that have wildfires started and those that don't.

image

As expected, there is a large class imbalance between the number of weeks that have a wildfire starting and the weeks that don't.

Next we checked the number wildfires through the year. We use only one year to get a clearer idea of possible high points.

image

There are more wildfires starting in the summer months than the rest of the year. This makes sense as the summer months are drier and with less rain.

We create a month feature to take a closer look at the number of wildfires started based on month.

image

As seen in the year 2013, over the course of 2013-2018 the majority of wildfires start in the summer months. July is the month that has the most wildfires started.

Next we check if there are certain years that have more wildfires than others.

image

After the decrease after 2013, there seems to be an increasing trend of wildfires that Calfire managed the containment of.

There are certain counties that are more likely to have more wildfires than others. The county of Riverside has had the highest number of wilfires started.

image

## Model Evaluation

We tried several model: a logistic regression model, a K Nearest Neighbor (KNN) model, a Decision Tree classifier, and a Random Forest Classifier. To validate the models, we used cross validation using `cross_val_scores` with the logistic regression model and the knn model. The Decision Tree classifier and the Random Forest classifier had parameters tuned and validated using GridSearchCV.

The best model is the logistic regression. While all the models had very close recall scores, the logistic regression model was slightly higher with a score of ~80%.

image

From the confusion matrix, we can see that while the number of false negatives was smaller, the number of false positives was very large.

image


## Conclusion

With a recall score of nearly 80%, it means that this model should not be used on its own. While the model does well at catching which observations will result in wildfires, the model should ideally have a higher score. A possible reason for the false negatives could be from missing connections. A large number of wildfires are caused by humans, which is something that is unaccounted for in this model. The large number of false positives could be from missing connections or it might be due to the nature of CalFire Wildfire Incidents only record wildfires that burn more than 10 acres. A portion of the false positives could be from wildfires that burned close to 10 acres but did not reach the cutoff.

## Future Steps

Possible future improvements to this project are: 

    - More feature engineering
    - Gathering human relevant data such as population or population density
    - New models such as XG Boost and Neural Nets
    
Further study could model the probability of fire sizes using the number of acres burned.

## Sources

[California Land Use and Ownership Portal by the University of California](https://callands.ucanr.edu/data.html#)
[California Irrigation Management Information System (CIMIS)](https://cimis.water.ca.gov/)
[Weather Underground](https://www.wunderground.com/)
[Kaggle California Wildfire Incidents](https://www.kaggle.com/ananthu017/california-wildfire-incidents-20132020)
[CalFire](https://www.fire.ca.gov/)
[Anyplace America](https://www.anyplaceamerica.com/directory/ca/)
