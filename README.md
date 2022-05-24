# Weather Forecasting in Singapore: Predicting the Occurrence of Rainfall Using Classification Techniques on Scraped Meteorological Data

This originally personal project was adapted for submission as SMU IS424-Data Mining and Business Analytics Project<br>
Grade: A-

## Executive Summary:
In Singapore, many people lead a fast-paced life, with some who often travel from places to places for work or for leisure. Although Singapore is said to be geographically small compared to other countries, there have been numerous times where the weather predictions are inaccurate: within the same town or estate, it can be both sunny and rainy, depending on your exact location. As a result, we may be affected during our travels due to the unexpected weather conditions and our insufficient preparation. Furthermore, there are a limited number of sources for people in Singapore to get their information about the weather. The most common sources of information where people obtain weather forecasts are from The National Environmental Agency (NEA)’s website– which fundamentally uses Meteorological Services Singapore (MSS)– to provide generally reliable and responsive weather and climate information (Note that there are also other online sources of weather forecast information available, such as AccuWeather and The Weather Channel, but the aforementioned NEA and MSS websites are the more popular sites where weather information is usually taken). With these two reasons in mind, we will, in this project, attempt to make an alternative model that learns a set of historical weather data and predicts the future local weather condition based on a user’s location, so that Singaporeans can have another source of weather forecast they can turn to and be better informed.

In this project, we will go about modelling our weather datasets using a number of different classifiers. The reason for doing this is to have a general feel of how the various classifiers perform when trying to classify our data. Some classifiers may be better (have higher accuracy) than others when predicting binary outputs. In our project, we will use data mining techniques– specifically, classification techniques– to predict the occurrence of rainfall. These techniques will take in the existing data available and explore hidden patterns that may be overlooked by traditional data analysis techniques, allowing us to discover novel insights
and make well-informed decisions based on the trends found. 

Using datasets scraped and consolidated from the NEA’s weather forecast websites, we will transform some fields for the purpose of classifying whether conditions at a certain area, at that particular date and time, whether there is rainfall or not (More details can be found under the Dataset section). Then, we will model these historical weather data, using techniques such as k-th Nearest Neighbours (kNN), Naive Bayes(NB), Decision Tree, Artificial Neural Network(ANN) as well as the Support Vector Machine(SVM) to get our output, which will produce a binary output as an indication of the presence of rainfall. We also use ensemble methods, such as AdaBoost and CatBoost, as well as perform hyperparameter tuning to improve the performance of our classifiers. As we are mainly interested in predicting instances of rainfall,
we place greater emphasis on the true positives. 

In this project, we use F1 score as our yardstick to compare model performances. Due to our limited data mining knowledge and time given for this project, we only used classifiers that we are rather familiar with. It is to be noted that in the future, if anyone were to be interested in attempting to forecast the weather
in Singapore, more sophisticated data mining and machine learning techniques can be considered as plausible approaches to our topic.

## Dataset

Meteorological data of Singapore was obtained from publicly available Application Programmable Interfaces (APIs) published by the National Environment Agency (NEA) of
Singapore on the public data repository data.gov.sg (data.gov.sg, n.d.). Data.gov.sg hosts 5 different weather-related APIs including:

1. Air temperature
2. Humidity
3. Wind Speeds
4. Wind Direction
5. Rainfall

As the APIs were published mid-2016, the dataset for 2016 would be incomplete. Hence, data collected would be from 2017 to 2021. Data was scraped using Python to make API calls using the <code>request</code> package for every hour from “2017-01-01 00:00:00” to “2021-12-31 23:59:59”. The data is returned as a json file that is first processed as a table in Python using pandas, numpy and datetime before being stored in a MySQL database using the <code>pymysql</code> package. A SQL database is used to store records due to the large number of records that necessitated scraping over a few days. Hence, an easily updatable database was used.

A glimpse of a single variable's (temperature) raw data looks like this:

![image](https://user-images.githubusercontent.com/88301287/169970721-c4cd65ae-b5c6-45d3-9808-c6cb9326f95e.png)

Therefore, to merge the weather variables into a single dataframe, the readings of the data were aggregated by the locations of the weather stations. More specifically, the readings of weather stations within the same region of Singapore were aggregated using their mean values. This was done as for each particular timestamp, different weather variables had different numbers of active weather stations. Additionally, if the location of weather stations was used as is in the model, forecast predictions would need to take in latitudes and longitudes as an input. An average Singaporean would be unlikely to know which weather
station is their closest one, meanwhile they are more likely to know which region they would like to forecast the weather for instead.

## Exploratory Data Analysis

To get a feel of how the data should be prepared, boxplots and pairplots of the numerical attributes were drawn. The results are shown below:

![image](https://user-images.githubusercontent.com/88301287/169971318-78bbbd0e-fe4c-4eef-ada8-ed9e5de99424.png)

We can tell that the median temperature for periods with rainfall is lower than on periods without rainfall. The median humidity is higher for periods with
rainfall compared to periods without rainfall. The median wind speed did not differ much on both instances, though on periods with rainfall, there is a slightly higher wind speed than on days without. The large differences in scaling between these attributes also meant that standardisation of values was required.

![image](https://user-images.githubusercontent.com/88301287/169971449-ff24fe04-7447-4a65-b6a7-0d8713465cf4.png)

Also, we can see that temperature is normally distributed, while humidity and wind speed are negatively and positively skewed respectively. Hence, in addition to standardisation normalisation of the attributes is also required. By adding labels to increase the visibility of points where rainfall is present, we can also see that there seems to be a consistent pattern of lower temperature and humidity close to 100% on days with rain.

![image](https://user-images.githubusercontent.com/88301287/169971619-7afddebf-3dd0-4740-bacc-ce334460135c.png)

Next, correlation matrix shows that the correlation of humidity, temperature and wind speed values have an almost negligible impact on the probability of rainfall in the current state. Hence, further feature engineering would be required to create a model that performs well. At the same time, variables like temperature and humidity being very highly correlated could suggest a need for PCA decomposition.

![image](https://user-images.githubusercontent.com/88301287/169971941-6dbc27cb-ac3d-4096-a55a-8e821c5d9ad0.png)

Furthermore, the idea that within a year, there are consistent periods of higher rainfall was also floated in preliminary discussions. For example, drier months tend to be the June - August period, while ‘wetter’ months would be from Nov - Jan. Such a trend would affect how the classification model was created and might be useful.

![image](https://user-images.githubusercontent.com/88301287/169972073-6394e851-4f75-4426-a760-19bd18fe34b0.png)

Lastly, it was found that there is a large class imbalance for the ‘rainfall’ attribute. Any classification models created thus would have to account for this and be adjusted accordingly

## Feature Engineering
Some transformations were made to make the data more intuitively understandable. Firstly, rainfall was converted into a binary indicator variable, indicating ‘1’ for the presence of rain and ‘0’ for its absence whenever the reading exceeded 0 mm of rain. This allowed the use of classification techniques for the prediction of rain. 

We decomposed wind speed and direction into wind speeds in the easting and northing directions using simple trigonometry (windspeed_x and windspeed_y) as wind direction has no meaning if wind speeds are 0.

Since the goal of the project is to predict future occurrences of rain using historical data, columns of past_x where x are the other weather variables were created by shifting the dataset by 1 period. For example, past_temperature for the row representing “2017-01-01 02:00:00” would take on the temperature value from the row representing “2017-01-01 01:00:00”. 

Next, we thought that instead of the absolute values it was the changes in the weather conditions experienced in the past hour that gave important signals to the model and hence delta_x was created.

Lastly, since the nature of the dataset is a time-series data, datetime variables including year, month, date, quarter, and hour were also created.

## Preprocessing
Given the time-series nature of the data, the dataset would be split into training and test sets in a chronological manner; data from the first 80% of the timeline would go into the training set and data from the last 20% of the timestamps would be the test set. A random split was not used here as training using later data points would lead to data leakage, a situation in which later data points are used to train and test for earlier data points.

Since the dataset is naturally imbalanced with only 9% positive when aggregated at the regional level, the resampling algorithms found in the <code>imblearn</code> package was used to resample the data points to make the dataset more balanced for classification. In total, a oversampling variation of SMOTE called SMOTE-NC, an undersampling algorithm called Edited Nearest Neighbours and the hybridisation of the 2, SMOTE-ENN were tried.

Lastly, as mentioned before, normalization was done using <code>sklearn</code>'s <code>StandardScaler()</code> and PCA to reduce the dimensionality of the data was also attempted.

## Results and Discussion
The following are the results from the best attempt at each classification method:

![image](https://user-images.githubusercontent.com/88301287/169973881-c23107cb-9473-4e95-b222-a3842830ca17.png)

We conclude that weather prediction is not easy as can be seen from how our best attempts only got a f1 score of 0.48. 

Limitations in our project that are present in our methodology include:

1. Inadequate signals from the APIs: More variables could have the potential to give more information
2. Computational limitations resulted in hyperparameter tuning being conducted in a greedy fashion that finds a locally optimal but not globally optimal solution.

Some suggestions for future works to improve on our methodology include:

1. Using a different scaling function such as Box-Cox
2. Using other powerful variants of dealing with class imbalances such as Generative Adversarial Networks (GANs) (An attempt was made using <code>tabgans</code> however as we have little experience using GANs, the implementation did not actually improve the performance of the classification)
3. Using actual time series classification methods available in <code>sktime</code> for example
4. Rephrasing the problem as a regression or anomaly detection problem rather than a classification one.












