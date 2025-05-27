import streamlit as st
import os
from openai import OpenAI
import json

st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Test d'Orientation Implicite")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.header("🧠 Réponds aux 15 situations")
prenom = st.text_input("Prénom de l'élève :", key="prenom")

questions = {
    "Q1": ("Ton professeur te donne un exposé sur un sujet inconnu. Tu as 3 jours. Tu :", [
        "Organises tes idées en plan avant de chercher",
        "Commences par écrire pour voir ce que tu penses",
        "Dessines une carte mentale pour explorer le sujet"
    ]),
    "Q15": ("On te demande de résumer un texte. Tu :", [
        "Identifies les idées principales",
        "Reformules avec tes mots",
        "Fais une carte mentale"
    ])
    # (raccourci pour l'exemple)
}

reponses = {}
for key, (question, options) in questions.items():
    choix = st.radio(question, options, key=key)
    if choix:
        reponses[key] = choix

if st.button("🔎 Analyser mon profil"):
    if len(reponses) < len(questions) or not prenom.strip():
        st.warning("Merci de répondre à toutes les questions et d’entrer ton prénom.")
    else:
        with st.spinner("Analyse en cours..."):
            try:
                prompt = f"""
Voici les réponses d’un élève marocain à un test d’orientation implicite. Déduis son profil dominant (scientifique, littéraire ou mixte), et propose une synthèse.

Prénom : {prenom.strip()}
Réponses :
"""
                for q, r in reponses.items():
                    prompt += f"- {q} : {r}\n"

                prompt += """
Réponds en JSON :
{
  "orientation": "scientifique/littéraire/mixte",
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
                st.markdown(f"**🧑 Prénom :** {prenom.strip()}")
                st.markdown(f"**📚 Orientation recommandée :** `{result_json['orientation']}`")
                st.markdown("**📝 Résumé :**")
                st.markdown(f"> {result_json['resume']}" )

                st.session_state["profil"] = result_json['orientation']

            except Exception as e:
                st.error(f"❌ Une erreur est survenue : {str(e)}")

if "profil" in st.session_state:
    if st.button("🧩 Voir les 15 questions ciblées selon mon profil"):
        st.subheader("🔎 Bloc 2 : Questions ciblées")

        literaire_questions = [
            "Tu dois écrire un discours pour convaincre : que fais-tu en premier ?",
            "Dans un débat, tu préfères :",
            "Tu écris une lettre à un ami pour exprimer une idée : comment tu t’y prends ?",
            # ... jusqu'à 15
        ]

        scientifique_questions = [
            "Tu rencontres un problème avec ton vélo. Quelle est ta première réaction ?",
            "On te donne un puzzle logique. Que fais-tu ?",
            "Tu dois organiser une expérience. Quelle étape passes-tu en premier ?",
            # ... jusqu'à 15
        ]

        profil = st.session_state["profil"].lower()
        ciblees = literaire_questions if profil == "littéraire" else scientifique_questions if profil == "scientifique" else literaire_questions[:7] + scientifique_questions[:8]

        for idx, q in enumerate(ciblees):
            st.radio(f"Q{16 + idx} : {q}", ["Option A", "Option B", "Option C"], key=f"Q{16 + idx}")
