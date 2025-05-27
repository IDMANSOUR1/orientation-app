import streamlit as st
import os
import base64
from io import BytesIO
from fpdf import FPDF
import matplotlib.pyplot as plt
import numpy as np
from openai import OpenAI

# Configuration
st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Test d'Orientation Implicite")

# Clé API (à ajouter dans les secrets Streamlit)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Questions implicites
questions = {
    "Q1": "Ton professeur te donne un exposé à faire sur un sujet que tu ne connais pas. Tu as 3 jours. Tu :",
    "Q2": "Un camarade bloque sur un exercice. Il te demande de l’aide. Tu :",
    "Q3": "En classe, ton professeur corrige un devoir en silence au tableau. Tu préfères :",
    "Q4": "Tu dois préparer un devoir noté. Tu as le choix :",
    "Q5": "Pendant un cours, ton prof pose une question difficile. Tu :",
    "Q6": "Tu reçois un devoir corrigé avec cette remarque : \"Ta méthode n’était pas la plus rapide, mais elle est originale.\" Tu te dis :",
    "Q7": "Tu as une heure de liberté dans un CDI avec Internet. Tu fais quoi ?",
    "Q8": "Un adulte te dit : \"Tu es quelqu’un de très méthodique.\" Tu penses :",
    "Q9": "Un nouveau sujet te paraît difficile à comprendre. Tu préfères :",
    "Q10": "On te propose de participer à un atelier pendant une semaine. Tu choisis :",
    "Q11": "Tu dois corriger un travail. Tu es plus attentif(ve) à :",
    "Q12": "Pendant un exposé en groupe, tu préfères :",
    "Q13": "Un prof te donne une consigne vague pour un projet libre. Tu ressens :",
    "Q14": "Tu assistes à un débat entre deux élèves. Tu observes surtout :",
    "Q15": "Ton professeur te demande de résumer un texte long. Tu commences par :"
}

# Réponses disponibles (exemple générique à adapter pour chaque question)
reponse_options = [
    "-- Sélectionne --",
    "Option A",
    "Option B",
    "Option C"
]

# Interface questions
st.header("🧠 Réponds aux 15 situations")
prenom = st.text_input("Prénom de l'élève :", key="prenom")

reponses = {}
for key, question in questions.items():
    choix = st.radio(question, reponse_options, key=key)
    if choix != reponse_options[0]:
        reponses[key] = choix

# Bouton analyse
if st.button("🔎 Analyser mon profil"):
    if len(reponses) < 15 or not prenom:
        st.warning("Merci de répondre à toutes les questions et d’entrer ton prénom.")
    else:
        with st.spinner("Analyse en cours..."):
            try:
                prompt = f"""
Tu es un expert en orientation scolaire. Voici les réponses d’un élève à 15 scénarios projectifs. Analyse-les pour détecter :
1. Les tendances cognitives dominantes (logique, verbal, visuel, créatif…)
2. L’orientation potentielle (scientifique, littéraire, mixte…)
3. Si le profil est clair ou contradictoire
4. Une phrase de résumé personnalisée

Réponses de l'élève {prenom} :
"""
                for q, r in reponses.items():
                    prompt += f"- {q} : {r}\n"

                prompt += """
Réponds au format JSON :
{
  "tendances": [...],
  "orientation": "...",
  "niveau_certitude": "...",
  "resume": "..."
}
"""

                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                result_text = response.choices[0].message.content
                st.success("🎯 Résultat")
                st.markdown(result_text)

            except Exception as e:
                st.error("Erreur : " + str(e))
