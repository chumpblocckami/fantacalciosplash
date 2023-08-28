import pandas as pd
import plotly.express as px
import streamlit as st
import os

from utility import filter_dataframe

if "edizione" not in st.session_state:
    st.session_state["edizione"] = ""

st.title(f"Fantacalciosplash {st.session_state['edizione']}")

FIELDS = ["giocatori", "fantasquadre", "punteggi", "classifica"]


def load_data():
    if st.session_state["edizione"] not in st.session_state:
        st.session_state[st.session_state["edizione"]] = {}

    for name, source in zip(FIELDS,
                            [f'{st.session_state["edizione"]}/{field}.xlsx' for field in FIELDS]):
        try:
            data = pd.read_excel(source)#.fillna(value="")
            st.session_state[st.session_state["edizione"]][name] = data
        except Exception as e:
            st.error(f"{e}")
            st.session_state[st.session_state["edizione"]][name] = pd.DataFrame()


with st.sidebar:
    st.session_state["edizione"] = st.radio("Edizione", [x for x in os.listdir() if x.isdigit()])

with st.spinner("Caricamento..."):
    load_data()

for name in FIELDS:
    with st.expander(name.capitalize()):
        st.subheader(name.capitalize())
        dataframe = filter_dataframe(st.session_state[st.session_state["edizione"]][name], key=name)
        st.dataframe(dataframe)
        if name == "classifica":
            graph = st.checkbox("Visualizza grafico", key=f"checkbox_{name}")
            if graph:
                progression = dataframe.set_index("FANTALLENATORE").drop(columns=["TOTALE"]).T.cumsum()
                fig = px.line(progression, title="Progressione classifica").update_layout(
                    xaxis_title="Gironi torneo", yaxis_title="Punteggio fanta",
                )
                st.write(fig)
        elif name == "punteggi":
            graph = st.checkbox("Visualizza grafico", key=f"checkbox_{name}")
            if graph:
                progression = dataframe.set_index("NOME").sort_values(by="TOTALE", ascending=False).drop(
                    columns=["TOTALE"]).T.cumsum()
                fig = px.line(progression, title="Progressione punteggio").update_layout(
                    xaxis_title="Gironi torneo", yaxis_title="Punteggio fanta",
                )
                st.write(fig)
        else:
            st.checkbox("Visualizza grafico", value=False, key=f"checkbox_{name}", disabled=True)
