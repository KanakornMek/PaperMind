import streamlit as st
from pymongo.mongo_client import MongoClient
import plotly.express as px
import pandas as pd

uri = "mongodb://datasci:scopus888@datascidb.kanakornmek.dev:27017/?authSource=admin"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client['datasci']
collection = db['papers']

subject = ['AGRI - Agricultural and Biological Sciences', 'ARTS - Arts and Humanities', 'BIOC - Biochemistry, Genetics and Molecular Biology', 'BUSI - Business, Management and Accounting', 'CENG - Chemical Engineering', 'CHEM - Chemistry', 'COMP - Computer Science', 'DECI - Decision Sciences', 'DENT - Dentistry', 'EART - Earth and Planetary Sciences', 'ECON - Economics, Econometrics and Finance', 'ENER - Energy', 'ENGI - Engineering', 'ENVI - Environmental Science', 'HEAL - Health Professions', 'IMMU - Immunology and Microbiology', 'MATE - Materials Science', 'MATH - Mathematics', 'MEDI - Medicine', 'NEUR - Neuroscience', 'NURS - Nursing', 'PHAR - Pharmacology, Toxicology and Pharmaceutics', 'PHYS - Physics and Astronomy', 'PSYC - Psychology', 'SOCI - Social Sciences', 'VETE - Veterinary', 'MULT - Multidisciplinary']

st.write("# Top Organization")

option = st.selectbox('Filter by subject area', subject, index=None, placeholder='All')
num = st.number_input('Pick amount to show (between 10 and 20 included)',min_value=10, max_value=20, value=10)

if option is not None:
    option_text = option[0:4]
    cursor = collection.find({'subject-areas.subject-area.@abbrev':option_text},projection={'affiliation':True})
else:
    cursor = collection.find(projection={'affiliation':True})

u_dict = dict()
for doc in cursor:
    try:
        doc_dict = dict(doc)
        aff = doc_dict['affiliation']
        if type(aff).__name__ == 'dict':
            if aff['affilname'] not in u_dict:
                u_dict[aff['affilname']] = 1
            else:
                u_dict[aff['affilname']] += 1
        else:
            u_set = set()
            for u in aff:
                u_set.add(u['affilname'])
            for us in u_set:
                if us not in u_dict:
                    u_dict[us] = 1
                else:
                    u_dict[us] += 1
    except:
        print('omit error')
df = pd.Series(u_dict)
df = df.sort_values(ascending=False)
df = df.head(num)
fig = px.bar(df)
fig.update_layout(showlegend=False,xaxis_title="Country", yaxis_title="Amount of Papers")
# st.write(df)
st.plotly_chart(fig)
