import streamlit as st
import os
from openai import OpenAI
import json

# Configuration
st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Test d'Orientation Implicite")

# API OpenAI
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.header("🧠 Réponds aux 15 situations")
prenom = st.text_input("Prénom de l'élève :", key="prenom")

# Questions et options spécifiques
questions = {
    "Q1": ("Ton professeur te donne un exposé sur un sujet inconnu. Tu as 3 jours. Tu :", [
        "Organises tes idées en plan avant de chercher",
        "Commences par écrire pour voir ce que tu penses",
        "Dessines une carte mentale pour explorer le sujet"
    ]),
    "Q2": ("Un camarade bloque sur un exercice. Il te demande de l’aide. Tu :", [
        "Réexplique la règle ou méthode",
        "Reformules le problème avec tes mots",
        "Inventes une métaphore pour l’aider"
    ]),
    "Q3": ("Ton professeur corrige un devoir en silence au tableau. Tu préfères :", [
        "Une correction structurée étape par étape",
        "Une explication orale avec des exemples",
        "Plusieurs méthodes comparées"
    ]),
    "Q4": ("Tu dois faire un devoir noté. Tu choisis :", [
        "Un problème avec une seule solution",
        "Une rédaction libre",
        "Un projet créatif"
    ]),
    "Q5": ("Ton prof pose une question difficile. Tu :", [
        "Tentes ta chance",
        "Attends d’être certain(e)",
        "Notes la question pour plus tard"
    ]),
    "Q6": ("Un devoir est noté \"méthode originale mais pas rapide\". Tu te dis :", [
        "Chercher une méthode plus logique",
        "Être fier(e) d’avoir réfléchi autrement",
        "Se questionner sur son style"
    ]),
    "Q7": ("Une heure libre au CDI avec Internet. Tu :", [
        "Cherches un tuto sur un sujet qui te passionne",
        "Lis un article, un blog ou regarde une vidéo d’analyse",
        "Dessines, écris ou développes un projet"
    ]),
    "Q8": ("Un adulte te dit : \"Tu es méthodique\". Tu penses :", [
        "Oui, j’aime que tout soit structuré",
        "Non, je laisse venir les idées",
        "Je suis les deux selon les moments"
    ]),
    "Q9": ("Tu trouves un sujet difficile. Tu préfères :", [
        "Faire un exercice pour tester ta compréhension",
        "Relire le cours plusieurs fois",
        "Discuter avec quelqu’un"
    ]),
    "Q10": ("On te propose un atelier libre. Tu choisis :", [
        "Construire une maquette",
        "Écrire un scénario ou un article",
        "Résoudre des énigmes en équipe"
    ]),
    "Q11": ("Tu dois corriger un devoir. Tu regardes surtout :", [
        "Si le raisonnement est juste",
        "Si c’est bien écrit",
        "Si l’idée est originale"
    ]),
    "Q12": ("Pendant un exposé en groupe, tu préfères :", [
        "Faire les recherches et organiser le contenu",
        "Écrire le texte ou le présenter",
        "Créer un support visuel"
    ]),
    "Q13": ("Un prof donne une consigne floue. Tu :", [
        "Demande plus de détails",
        "Proposes une idée originale",
        "Hésites puis improvises"
    ]),
    "Q14": ("Un débat entre deux élèves. Tu observes :", [
        "Qui a les meilleurs arguments",
        "Qui s’exprime le plus clairement",
        "Qui est le plus surprenant"
    ]),
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

                st.success("🎯 Résultat")
                st.markdown(f"**🧑 Prénom :** {prenom}")
                st.markdown(f"**📚 Orientation recommandée :** `{result_json['orientation']}`")
                st.markdown(f"**🧭 Tendances cognitives :** {', '.join(result_json['tendances'])}")
                st.markdown(f"**📊 Niveau de clarté :** {result_json['niveau_certitude']}")
                st.markdown("**📝 Résumé :**")
                st.markdown(f"> {result_json['resume']}")

                if st.button("➕ Générer des questions ciblées (Q16–Q30)"):
                    profil = result_json['orientation']
                    st.info(f"Questions adaptées pour un profil {profil.upper()} en cours de génération...")

                    adaptation_prompt = f"""
Tu es un créateur de tests d’orientation. En te basant sur le profil suivant : {profil}, génère 15 nouvelles questions ciblées Q16 à Q30. Chaque question doit être implicite, contextuelle, et liée aux compétences de ce profil.
Réponds sous ce format :
- Q16 : [question]
- Q17 : [question]
...
- Q30 : [question]
"""
                    followup = client.chat.completions.create(
                        model="gpt-4",
                        messages=[{"role": "user", "content": adaptation_prompt}],
                        temperature=0.7
                    )
                    st.markdown("### 🎯 Questions ciblées :")
                    st.markdown(followup.choices[0].message.content)

            except Exception as e:
                st.error("Erreur : " + str(e))
