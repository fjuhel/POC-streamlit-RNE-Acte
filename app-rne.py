import streamlit as st
import requests

# Fonctions pour obtenir le token et les documents
def get_token():
    url = "https://registre-national-entreprises.inpi.fr/api/sso/login"
    payload = {
        "username": "kmameri@scores-decisions.com",
        "password": "Intesciarne2022!"
    }
    response = requests.post(url, json=payload)
    if response.status_code == 200:
        return response.json().get("token")
    else:
        return None

def get_documents(siren, token):
    url = f"https://registre-national-entreprises.inpi.fr/api/companies/{siren}/attachments"
    headers = {
        "Authorization": f"Bearer {token}"
    }
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json().get("actes")
    else:
        return None

# Configuration Streamlit
st.set_page_config(
    page_title="Consultation des Actes d'Entreprises",
    layout='wide',
    page_icon="📑",
    menu_items={
         'About': 'Call Kevin MAMERI',
     }
)

# Titre de la page
st.header("Consultation des Actes d'Entreprises via SIREN")
st.caption("App développée par Kevin MAMERI")

# Entrée du SIREN
siren = st.text_input("Veuillez entrer le SIREN de l'entreprise:")

# Obtenir le token
token = get_token()

import pandas as pd

if token and siren:
    documents = get_documents(siren, token)
    if documents:
        data = []
        for doc in documents:
            date_depot = doc.get('dateDepot')
            nom_document = doc.get('nomDocument')
            id_doc = doc.get('idDoc') # Obtenez l'id_doc à partir des données du document
            type_rdds = doc.get('typeRdd', [])
            for type_rdd in type_rdds:
                type_acte = type_rdd.get('typeActe')
                decision = type_rdd.get('decision')
                doc_url = f"https://registre-national-entreprises.inpi.fr/api/companies/{siren}/attachments/{id_doc}" # Construisez l'URL du document
                data.append([date_depot, nom_document, type_acte, decision, doc_url])
        
        df = pd.DataFrame(data, columns=['Date de dépôt', 'Nom du document', 'Type d\'acte', 'Décision', 'Lien du document'])
        st.write(df.to_html(escape=False, render_links=True), unsafe_allow_html=True) # Affichez le DataFrame avec les liens actifs
    else:
        st.warning("Aucun document trouvé pour ce SIREN.")
else:
    if not token:
        st.error("Impossible d'obtenir le token.")
