import streamlit as st
import plotly.graph_objs as go
import pandas as pd
from util.normalize_entries import normalize_entries
from util.plot_graph import plot_graph
from db.entries import get_entry_by_name

if "name" not in st.query_params:
    st.query_params["name"] = []

name = st.query_params["name"]

get_entries = get_entry_by_name(name)
entries = normalize_entries(get_entries, ref_electrode="SHE", c_ref=None, ion=None, ref_scan_rate=None)

st.set_page_config(layout="wide")
st.title(f"Detail view for {name}")
col1, col2 = st.columns([3, 2])

with col1:
    plot_graph(entries, "Detail Entries")

with col2:
    tab1, tab2, tab3 = st.tabs(["ELECTROCHEMICAL SYSTEM", "ENTRY SOURCE", "BIBLIOGRAPHY"])
    with tab1:
        st.header("ELECTROCHEMICAL SYSTEM")
        electrochemical_system = get_entries[0].system
        
        for electrode in electrochemical_system["electrodes"]:
            st.subheader(f"{electrode['function'].capitalize()} ({electrode['name']}):")
            if hasattr(electrode, 'material'):
                st.text(f"Material: {electrode['material']}")
            if hasattr(electrode, 'type'):
                st.text(f"Type: {electrode['type']}")
            if hasattr(electrode, 'shape'):
                st.text(f"Shape: {electrode['shape']['type']}")
            if hasattr(electrode, 'crystallographic orientation'):
                st.text(f"Crystallographic orientation: {electrode['crystallographic orientation']}")
            if hasattr(electrode, 'preparation procedure'):
                st.text(f"Preparation procedure: {','.join(electrode['preparation procedure']['description'])}")

        st.subheader("Electrolyte:")
        electrolyte = electrochemical_system['electrolyte']
        
        st.text(f"Components:")
        for component in electrolyte['components']:
            st.text(f"- Name: {component['name']}")
            st.text(f"- Type: {component['type']}")
            if hasattr(component, 'concentration'):
                st.text('Concentration:')
                st.text(f"Unit: {component['concentration']['unit']}")
                st.text(f"Value: {component['concentration']['value']}")
        
        
        temp_unit=electrochemical_system["electrolyte"]["temperature"]["unit"]
        temp_value=electrochemical_system["electrolyte"]["temperature"]["value"]
        st.text(f"Temperature:")
        st.text(f"Unit: {temp_unit}")
        st.text(f"Value: {temp_value}")
                
    with tab2:
        st.header("ENTRY SOURCE")
        entry_source = get_entries[0].source
        st.text(f"Citation key: {entry_source.citation_key}")
        st.text(f"URL: {entry_source.url}")
        st.text(f"Techniques: {','.join(entry_source.techniques)}")
        st.text(f"Figure: {entry_source.figure}")
        st.text(f"Curve: {entry_source.curve}")

    with tab3:
        st.header("BIBLIOGRAPHY")
        bibliography = get_entries[0].bibliography
        st.text(f"Type: {bibliography.type}")

        fields_dict = dict(bibliography.fields)
        for field, value in fields_dict.items():
            st.text(f"{field.capitalize()}: {value}")
        
        persons = bibliography.persons.get("author")
        person_names = [f"{person}" for person in persons]
        st.text("Authors: " + '; '.join(person_names))
    