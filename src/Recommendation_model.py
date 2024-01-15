#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


data = "data_project/nomadlist_travel_info.csv"


# In[3]:


df = pd.read_csv(data)


# In[4]:


df1=df.iloc[:,[1,2]]


# In[5]:


df1.head


# In[6]:


def extract_countries(city_country_list):
    countries = [city_country.split(', ')[-1] for city_country in city_country_list]
    return countries

df1['visited_countries'] = df1['visited'].apply(lambda x: extract_countries(eval(x)))
df1['nomadlist_countries'] = df1['nomadlist_recommends'].apply(lambda x: extract_countries(eval(x)))
#eval wandelt die Liste von Zeichen in Strings um 

print(df1[['visited_countries', 'nomadlist_countries']].head())


# In[7]:


df2=df1.iloc[:,[2,3]]


# In[8]:


df2.head


# In[9]:


from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# In[10]:


X_train, X_test, y_train, y_test = train_test_split(df2['visited_countries'], df2['nomadlist_countries'], test_size=0.2, random_state=42)


# In[11]:


mlb = MultiLabelBinarizer()
y_train_bin = mlb.fit_transform(y_train)
model = make_pipeline(CountVectorizer(), MultiOutputClassifier(RandomForestClassifier()))
model.fit(X_train.apply(lambda x: ' '.join(x)), y_train_bin)


# In[12]:


predictions_bin = model.predict(X_test.apply(lambda x: ' '.join(x)))


# In[13]:


predictions = mlb.inverse_transform(predictions_bin)


# In[14]:


predictions


# In[15]:


accuracies = []

for true_labels, predicted_labels in zip(y_test, predictions):
    accuracy = sum(label in predicted_labels for label in true_labels) / max(len(true_labels), 1)
    accuracies.append(accuracy)

average_accuracy = sum(accuracies) / len(accuracies)

print(f"Average Accuracy: {average_accuracy}")


# In[17]:


# Function to recommend countries based on user input
def recommend_countries():
    while True:
        # Get user input
        user_input = input("Enter the countries you have visited (comma-separated): ")
        user_countries = [country.strip() for country in user_input.split(',')]

        # Check if all input countries are known
        unknown_countries = set(user_countries) - known_countries

        if not unknown_countries:
            # All input countries are known, proceed with recommendations

            # Predict based on user input
            input_str = ' '.join(user_countries)
            prediction_bin = model.predict([input_str])
            prediction = mlb.inverse_transform(prediction_bin)

            # Print the recommended countries
            print("Recommended countries to visit:")
            for country in prediction[0][:3]:
                print(country)

            break  # Exit the loop if valid input is received
        else:
            print("Some input countries are not known:")
            print(', '.join(unknown_countries))
            print("Please enter valid countries.")


# Get all known countries
known_countries = set(country for countries_list in pd.concat([X_train, X_test, y_train, y_test]) for country in countries_list)

# Make recommendations based on user input
recommend_countries()

