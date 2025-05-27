import streamlit as st
import os
from openai import OpenAI
import json

# Configuration
st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Test d'Orientation Implicite")

# API OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.header("🧐 Réponds aux 15 situations")
prenom = st.text_input("Prénom de l'élève :", key="prenom")

# Questions implicites (Q1 à Q15)
questions = {
    "Q1": ("Ton professeur te donne un exposé sur un sujet inconnu. Tu as 3 jours. Tu :", [
        "Organises tes idées en plan avant de chercher",
        "Commences par écrire pour voir ce que tu penses",
        "Dessines une carte mentale pour explorer le sujet"
    ]),
    # ... autres questions Q2 à Q15 (identiques)
    "Q15": ("On te demande de résumer un texte. Tu :", [
        "Identifies les idées principales",
        "Reformules avec tes mots",
        "Fais une carte mentale"
    ])
}

reponses = {}
for key, (question, options) in questions.items():
    choix = st.radio(question, options, key=key)
    if choix:
        reponses[key] = choix

if st.button("🔎 Analyser mon profil"):
    if len(reponses) < 15 or not prenom:
        st.warning("Merci de répondre à toutes les questions et d’entrer ton prénom.")
    else:
        with st.spinner("Analyse en cours..."):
            try:
                prompt = f"""
Tu es un conseiller en orientation scolaire. Voici les réponses d’un élève marocain à 15 scénarios implicites. 
Analyse-les pour déterminer :
- Les tendances cognitives dominantes (logique, verbal, visuel, créatif…)
- L’orientation probable (scientifique, littéraire, mixte…)
- Le niveau de clarté du profil
- Un résumé personnalisé

Prénom : {prenom}
Réponses :
"""
                for q, r in reponses.items():
                    prompt += f"- {q} : {r}\n"

                prompt += """
Réponds en JSON :
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
                result_json = json.loads(response.choices[0].message.content)

                st.success("🌟 Résultat")
                st.markdown(f"**🧑 Prénom :** {prenom}")
                st.markdown(f"**📚 Orientation recommandée :** `{result_json['orientation']}`")
                st.markdown(f"**🗭 Tendances cognitives :** {', '.join(result_json['tendances'])}")
                st.markdown(f"**📊 Niveau de clarté :** {result_json['niveau_certitude']}")
                st.markdown("**📝 Résumé :**")
                st.markdown(f"> {result_json['resume']}" )

                st.session_state["profil"] = result_json['orientation']

            except Exception as e:
                st.error(f"❌ Une erreur est survenue : {str(e)}")

if "profil" in st.session_state:
    if st.button("➕ Générer des questions ciblées (Q16–Q30)"):
        profil = st.session_state["profil"]
        with st.spinner(f"Génération de questions pour le profil {profil.upper()}..."):
            try:
                adaptation_prompt = f"""
Tu es un pédagogue expert. En te basant sur le profil {profil}, génère 15 nouvelles questions (Q16 à Q30).
Pour chaque question, donne 3 options de réponses implicites (sans réponses évidentes). Structure ta réponse en JSON ainsi :
{
  "Q16": {"question": "...", "options": ["...", "...", "..."]},
  ...
  "Q30": {"question": "...", "options": ["...", "...", "..."]}
}
"""
                followup = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": adaptation_prompt}],
                    temperature=0.7
                )
                data = json.loads(followup.choices[0].message.content)
                st.markdown("### 🌟 Questions ciblées (Q16–Q30) :")
                for qid, qdata in data.items():
                    st.radio(qdata["question"], qdata["options"], key=qid)
            except Exception as e:
                st.error(f"❌ Erreur lors de la génération des questions : {str(e)}")
