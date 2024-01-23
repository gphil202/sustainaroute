#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# In[2]:


data = "data_project/nomadlist_travel_info_separated.csv"


# In[4]:


df = pd.read_csv(data)


# In[5]:


df.head


# In[8]:


df1=df.iloc[:,[1,3]]


# In[9]:


df1.head


# In[15]:


df1['visited'] = df1['cities_visited'].apply(lambda x: eval(x))
df1['nomadlist_recommends'] = df1['recommended_cities'].apply(lambda x: eval(x))
#eval wandelt die Liste von Zeichen in Strings um 

print(df1[['visited', 'nomadlist_recommends']].head())


# In[17]:


df1.head


# In[11]:


from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.multioutput import MultiOutputClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.pipeline import make_pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


# In[25]:


X_train, X_test, y_train, y_test = train_test_split(df1['visited'], df1['nomadlist_recommends'], test_size=0.2, random_state=42)


# In[26]:


X_train


# In[27]:


mlb = MultiLabelBinarizer()
y_train_bin = mlb.fit_transform(y_train)
model = make_pipeline(CountVectorizer(), MultiOutputClassifier(RandomForestClassifier()))
model.fit(X_train.apply(lambda x: ' '.join(x)), y_train_bin)


# In[28]:


predictions_bin = model.predict(X_test.apply(lambda x: ' '.join(x)))


# In[29]:


predictions = mlb.inverse_transform(predictions_bin)


# In[30]:


predictions


# In[31]:


accuracies = []

for true_labels, predicted_labels in zip(y_test, predictions):
    accuracy = sum(label in predicted_labels for label in true_labels) / max(len(true_labels), 1)
    accuracies.append(accuracy)

average_accuracy = sum(accuracies) / len(accuracies)

print(f"Average Accuracy: {average_accuracy}")


# In[39]:


# Function to recommend countries based on user input
def recommend_cities():
    while True:
        # Get user input
        user_input = input("Enter the cities you have visited (comma-separated): ")
        user_cities = [city.strip() for city in user_input.split(',')]

        # Check if all input cities are known
        unknown_cities = set(user_cities) - known_cities

        if not unknown_cities:
            # All input cities are known, proceed with recommendations

            # Predict based on user input
            input_str = ' '.join(user_cities)
            prediction_bin = model.predict([input_str])
            prediction = mlb.inverse_transform(prediction_bin)

            # Print the recommended countries
            print("Recommended cities to visit:")
            for city in prediction[0][:5]:
                print(city)

            break  # Exit the loop if valid input is received
        else:
            print("Some input cities are not known:")
            print(', '.join(unknown_cities))
            print("Please enter valid cities.")


# Get all known countries
known_cities = set(city for cities_list in pd.concat([X_train, X_test, y_train, y_test]) for city in cities_list)

# Make recommendations based on user input
recommend_cities()

