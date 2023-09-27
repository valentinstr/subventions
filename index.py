import streamlit as st
import requests
import pandas as pd

def api_siret(siret):
    url = f'https://api-subvention-asso-prod.osc-secnum-fr1.scalingo.io/open-data/subventions/etablissement/{siret}'
    response = requests.get(url)
    return response.status_code, response.json()

def api_siren_ou_rna(siren_ou_rna):
    url = f'https://api-subvention-asso-prod.osc-secnum-fr1.scalingo.io/open-data/subventions/association/{siren_ou_rna}'
    response = requests.get(url)
    return response.status_code, response.json()

st.title("Subventions aux associations et structures")
st.markdown('API des subventions mise en place par [beta.gouv](https://github.com/betagouv/api-subventions-asso).')

type_subvention = st.radio("Établissement ou association", ("Établissement (SIRET)", "Association (SIREN ou RNA)"))

if type_subvention == "Établissement (SIRET)":
    siret = st.text_input("SIRET", key="siret")
    sub_siret = st.button("Rechercher", key="sub_siret")
    if siret:
        if sub_siret:
            with st.spinner('Recherche en cours...'):
                code, subventions_etablissement = api_siret(siret)
            if code!=200:
                st.error("Erreur lors de la recherche.")
            else:
                df_siret = pd.DataFrame(subventions_etablissement)
                if df_siret.empty:
                    st.write("Aucune subvention trouvée.")
                else :
                    st.dataframe(df_siret)
        
if type_subvention == "Association (SIREN ou RNA)":
    siren_ou_rna = st.text_input("SIREN ou RNA", key="siren_ou_rna")
    sub_siren = st.button("Rechercher")
    if siren_ou_rna:
        if sub_siren:
            with st.spinner('Recherche en cours...'):
                code, subventions_association = api_siren_ou_rna(siren_ou_rna)
            if code!=200:
                st.error("Erreur lors de la recherche.")
            else:
                df_siren = pd.DataFrame(subventions_association)
                if df_siren.empty:
                    st.write("Aucune subvention trouvée.")
                else :
                    st.dataframe(df_siren)