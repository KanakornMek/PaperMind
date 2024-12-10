import streamlit as st
from pymongo.mongo_client import MongoClient
import networkx as nx
from pyvis import network as net
from stvis import pv_static

uri = "mongodb://datasci:scopus888@datascidb.kanakornmek.dev:27017/?authSource=admin"

# Create a new client and connect to the server
client = MongoClient(uri)
db = client['datasci']
collection = db['papers']

state = st.session_state
if 'dir' not in state:
    state.dir = ''

st.sidebar.text_input('Search Author (Please Enter Full Name ex. Frodo Baggins)' ,value = state.dir, key='dir')
author = state.dir

st.write("## Search Author in Sidebar")

# @st.cache_data
# def main():
if author.strip().count(' ') == 1:
    firstname, surname = author.strip().split()
    firstname = firstname.capitalize()
    surname = surname.capitalize()
    cursor = collection.find({'authors.author.preferred-name.ce:given-name':firstname ,'authors.author.preferred-name.ce:surname':surname}, limit=10)
    if cursor != None:
        graph = nx.empty_graph()
        for doc in cursor:
            doc_dict = dict(doc)
            authors_list = []
            authors = doc_dict['authors']['author']
            for a in authors:
                try:
                    obj = f'{a['preferred-name']['ce:given-name']} {a['preferred-name']['ce:surname']} {a['@auid']}'
                    authors_list.append(obj)
                    if len(authors_list) > 20:
                        break
                except:
                    print('no author')
            
            to_add = nx.complete_graph(authors_list)
            graph = nx.compose(graph,to_add)
        # st.write(graph.nodes)
        pynet = net.Network(height='600px', width='600px',notebook=True)
        pynet.repulsion()
        pynet.from_nx(graph)
        pv_static(pynet)

        st.sidebar.write('Successful')
    else:
        st.sidebar.write('This person does not exist in database')
elif author.strip() == '':
    st.sidebar.write('')
else:
    st.sidebar.write('Wrong Format')

# main()
