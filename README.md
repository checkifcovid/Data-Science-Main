# CheckIfCovid Data Science

Aim: This is an overview of the data approach to modelling COVID-19 positivity.

# Get survey data
Utilizing internally developed API
1. Could be per period of time
2. Are there multiple records per individuals?

If someone later reports a diagnosis or worsening of symptoms, how is that reconciled?
- Exclude fraudulent or invalid responses
- Select most recent entry
- Or, build a linear profile

# Get local covid data
From an outside source. Should be as granular and localized as possible. 

Used kaggle database (https://www.kaggle.com/sudalairajkumar/novel-corona-virus-2019-dataset) as our main dataset to train the ML algorithm. We also used web-scrapping python code to gather information from Twitter and Bing about province-by-province level data in China for a later iteration of the survey data.

A major step was to clean the data on the .csv file and index together symptoms that were on the same category as others. We consulted MD and Infectious Disease fellow at Johns Hopkins University, Diana Zhong, who advised us on current trends in the infectious, comorbidities, research field and how they have changed how physicians diagnose patients for COVID-19. An example of how we indexed symptoms with similar characteristics is on anhelation, respiratory stress, severe dyspnea, emesis, respiratory complaints and wheezing which can all be indexed as in the shortness of breath variable.

In order to merge different databases we used the longitude and latitude geo-location whenever provided in the datasets as the common identifier of the samples to merge across. 
To generate .csv file we utlized the API to update the schema, change the lambda, shape the data to match adjacent sample with the survey data symptom design. 

# Model likelihood of surveyees being covid positive
Utilize local data to generalize and approximate covid positive cases. Normalize sampling of data based on population data → use to match severity with covid positivity.
1. Build a reward function for covid positivity
Tree based, ensemble, or deep learning method.
2. Utilize self reported covid positive individuals to cluster symptoms
Could be done globally. This will be especially powerful if individuals check in after their first response if they’ve been tested. Use this to build a classifier – could be knn, ensemble, or ltsm.
3. Miscellaneous models
We like the following but aren’t sure how to proceed:
- Cox-Hazard
- The Cox-Hazard model 
4. Select best model
Many ways to do this. Probably f-score will be most useful. We ended up selecting unsupervised cluster SVM non-linear Kernel specification for our model. Due to lack of large sample data on patients who have not tested positive but demonstrate symptoms and the need to train the ML model on both samples of negatively and positively tested patients, we run the non-linear Kernel model to also reduce within-cluster variation.The algorithms also gives an accuracy estimator which we assess with Doctor Zhong. It learns a decision function for novelty detection: classifying new data as similar or different to the training set.

The output of the algorithm gives for a scale of susceptibility of symptoms out of 100 and if surveyed participant with specific tracked ID in specific location and in proximity to hotspots scores an x>= 75% in the scale of symptoms then our output predicts how likely they be infected by COVID-19. 

# Update database with predictions
Create a new table and store user ids (or anonymized location) and the day’s predicted likelihood of covid positivity. Database is updated daily. 

# Human validation
Before commiting the day’s changes to the model, it’ll be helpful for a human to investigate predicted likelihood. (We don’t want a bad model to scare the hell out of people, that they’re all going to die.)

# Push to front-end
Front end platform will request or cache updated results. 
Database call.
K-Means clustering model


Shows province-by-province of China the susceptibility of populations by clusters (feature that we run with the K-mean algorithms was ID, symptoms, gender, geo-location). It demonstrates the different clusters using centroids and plots them. 
Output:  Northern part of China is more susceptible more at risk to COVID-19 spread since the earlier hotspot already happened in the Southern provinces (Wuhan) or the centroids plotted lower on y-axis of graph. 


Additional graphs:





Unsupervised cluster SVM non-linear Kernel model



# Additional Stuff
1. What are the data sources?
  - Survey data
  - Localized covid testing data

2. What are the predictions?
Likelihood of covid positivity based on self reported symptom
Localized likelihood of covid positivity based on symptom threshold.

3. Addition research questions:
- How are we going to account for people who were asymptomatic (did not exhibit symptoms) but got tested positive after the 14 day incubation period?
- Determine probability of recovery or severity


# Required next steps
1. Get sample of survey data
Could be fake, but need the structure to begin modelling
- Connect to database
- Sample test data available at https://docs.google.com/spreadsheets/d/1lyPuMoolIvbJQjZkETHA-y1fCXRIBZbCstr_NH9Q5TQ/htmlview can be used for initial modeling. Specially the Kaggle data with demographic information.


-----

# Actual next steps
- Knn for physical distance
  * Iterate n_kernels → until some max error occurs
  * Use each kernel as a feature whose value is distance from center of kernel
  * Create new features for above namely min distance, 75th percentile, median, and average distance.
Symptoms + Covid Positive


Here are your symptoms + likelihood of covid.
Headache + cough → Need negative people to make prediction

Feature importance.
