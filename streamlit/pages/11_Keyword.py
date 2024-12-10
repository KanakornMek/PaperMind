import streamlit as st
from pymongo import MongoClient
import pandas as pd
import json
import plotly.express as px
# connect to MongoDB
client = MongoClient("mongodb://datasci:scopus888@datascidb.kanakornmek.dev:27017/?authSource=admin")
db = client["datasci"]
collection = db["papers"]
# fetch data
data = []
for doc in collection.find({"authkeywords.author-keyword":{"$exists": True}},{"authkeywords":1,"subject-areas":1}):
    # Extract subject areas and keywords
     subject_areas = doc.get("subject-areas",{}).get("subject-area",[])
     if not isinstance(subject_areas,list):
        subject_areas = [subject_areas]
     subjects = [subj.get("$") for subj in subject_areas if subj]
     keywords = doc.get("authkeywords",{}).get("author-keyword",[])
     if not isinstance(keywords,list):
         keywords = [keywords]
     keywords = [kw.get("$") for kw in keywords if kw]
     # Append data
     for subject in subjects:
         for keyword in keywords:
             data.append({"subject":subject,"keyword":keyword})
# convert to DataFrame
df = pd.DataFrame(data)
# do the bar chart thing    
keyword_count = df.groupby(["subject","keyword"]).size().reset_index(name="frequency")
st.title("Popular Keywords by Subject Area")
# dopdown to select subject area
subject_areas = keyword_count["subject"].unique()
selected_subject = st.selectbox("Select Subject Area",subject_areas)
filtered_data = keyword_count[keyword_count["subject"] == selected_subject]
filtered_data = filtered_data.sort_values("frequency",ascending=False)
top_keywords = filtered_data.head(10)
fig = px.bar(
    top_keywords,
    x="keyword",
    y="frequency",
    labels={"frequency": "Keyword Frequency", "keyword": "Keyword"},
    title=f"Top 10 Keyword and their frequencies for Subject Area: {selected_subject}"
)
fig.update_layout(
    bargap=0.3  
)
st.plotly_chart(fig)
