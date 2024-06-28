import streamlit as st
import requests

st.title('Formulaire de fidélité')

col1, col2 = st.columns(2)

with col1:
    CreditScore = st.number_input('Score de Crédit', min_value=0, max_value=1000, step=1, value=567)
    Tenure = st.number_input('Durée (en années)', min_value=0, max_value=50, step=1, value=3)
    NumOfProducts = st.number_input('Nombre de Produits', min_value=1, max_value=10, step=1, value=2)
    IsActiveMember = st.selectbox('Membre Actif', ['Oui', 'Non'])
    Geography = st.radio('Pays', ['France', 'Germany', 'Spain'], horizontal=True)

with col2:
    Age = st.number_input('Âge', min_value=18, max_value=100, step=1)
    Balance = st.number_input('Solde', min_value=0, step=1000, value=10000)
    HasCrCard = st.selectbox('Possède une Carte de Crédit', ['Oui', 'Non'])
    EstimatedSalary = st.number_input('Salaire Estimé', min_value=0, step=1000, value=1000)
    Gender = st.radio('Genre', ['Homme', 'Femme'], horizontal=True)

# Transformez les valeurs en 1 ou 0 selon les conditions
Geography_Germany = 1 if Geography == "Germany" else 0
Geography_Spain = 1 if Geography == "Spain" else 0
Gender_Male = 1 if Gender == "Homme" else 0

# Ajoutez un bouton de soumission
submitted = st.button('Soumettre')

# Fonction pour traiter la soumission
if submitted:
    # Envoyez les données au backend
    if (CreditScore and Age and Tenure and Balance and NumOfProducts and EstimatedSalary and
        (HasCrCard in ['Oui', 'Non']) and (IsActiveMember in ['Oui', 'Non']) and 
        (Geography in ['France', 'Germany', 'Spain']) and (Gender in ['Homme', 'Femme'])):
        
        # Envoyez les données au backend
        data = {
            'CreditScore': CreditScore,
            'Age': Age,
            'Tenure': Tenure,
            'Balance': Balance,
            'NumOfProducts': NumOfProducts,
            'HasCrCard': 1 if HasCrCard == 'Oui' else 0,
            'IsActiveMember': 1 if IsActiveMember == 'Oui' else 0,
            'EstimatedSalary': EstimatedSalary,
            'Geography_Germany': Geography_Germany,
            'Geography_Spain': Geography_Spain,
            'Gender_Male': Gender_Male
        }
        # Envoie des données au backend 
        st.write('Données envoyées au backend:')

        response = requests.post("https://tp-fidelite-api-knrxbt4qfq-uc.a.run.app/predict", data=data)
        result = response.json()
        # st.write(result)

        if 'prediction' in result:
            rec = result["prediction"]
            probability = rec * 100
            st.write(f"Le pourcentage de fidélité de ce client est de : {probability:.2f}%")
        else:
            st.error(f"Erreur de prédiction: {result.get('error', 'Réponse inattendue du serveur.')}")
    else:
        st.error("Tous les champs doivent être remplis avant de soumettre le formulaire.")