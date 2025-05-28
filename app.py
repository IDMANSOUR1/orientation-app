import streamlit as st
import os
from openai import OpenAI
import json

st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Test d'Orientation Implicite")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "etape" not in st.session_state:
    st.session_state["etape"] = "bloc1"

# === Bloc 1 ===
if st.session_state["etape"] == "bloc1":
    st.header("🧠 Bloc 1 : Situations générales")
    prenom = st.text_input("Prénom de l'élève :", key="prenom")

    questions_bloc1 = {
        "Q1": ("Ton professeur te donne un exposé à faire sur un sujet que tu ne connais pas du tout. Tu as 3 jours. Tu :", [
            "Organises les idées en plan avant de commencer à chercher",
            "Commences par écrire des phrases pour voir ce que tu en penses",
            "Dessines un schéma ou une carte mentale pour explorer le sujet"
        ]),
        "Q2": ("Un camarade bloque sur un exercice. Il te demande de l’aide. Tu :", [
            "Réexplique la règle ou la méthode",
            "Reformules le problème avec tes propres mots",
            "Inventes une analogie ou une métaphore pour l’aider"
        ]),
        # ... ajoute jusqu'à Q15 comme tu l'avais déjà fait ...
    }

    reponses_bloc1 = {}
    for key, (question, options) in questions_bloc1.items():
        choix = st.radio(question, options, key=key)
        if choix:
            reponses_bloc1[key] = choix

    if st.button("➡️ Suivant"):
        if len(reponses_bloc1) < len(questions_bloc1) or not prenom.strip():
            st.warning("Merci de répondre à toutes les questions et d’entrer ton prénom.")
        else:
            prompt = f"Voici les réponses d’un élève marocain. Déduis son profil dominant : scientifique, littéraire ou mixte.\nPrénom : {prenom.strip()}\n"
            for q, r in reponses_bloc1.items():
                prompt += f"- {q} : {r}\n"
            prompt += "Réponds en JSON : { \"orientation\": \"...\", \"resume\": \"...\" }"

            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.7
            )
            result_json = json.loads(response.choices[0].message.content)
            st.session_state["orientation"] = result_json["orientation"]
            st.session_state["resume"] = result_json["resume"]
            st.session_state["prenom_resultat"] = prenom.strip()
            st.session_state["etape"] = "bloc2"
            st.rerun()

# === Bloc 2 ===
elif st.session_state["etape"] == "bloc2":
    st.header("📘 Bloc 2 : Questions ciblées")

    profil = st.session_state["orientation"]
    st.success(f"📚 Profil détecté : {profil}")
    st.markdown(f"**Résumé Bloc 1 :** _{st.session_state['resume']}_")

    questions = []
    if profil == "scientifique":
        questions = [
            ("Tu découvres un nouveau concept en physique. Tu préfères :", ["Lire des explications", "Regarder des expériences", "Tester par toi-même"]),
            # ... jusqu’à 10 questions scientifiques ...
        ]
    elif profil == "littéraire":
        questions = [
            ("Tu dois écrire une lettre à un personnage historique. Tu :", ["Imagines le contexte", "Utilises un style soutenu", "Racontes une fiction"]),
            # ... jusqu’à 10 questions littéraires ...
        ]

    reponses_bloc2 = {}
    for idx, (question, options) in enumerate(questions):
        qkey = f"B2_Q{idx+1}"
        choix = st.radio(question, options, key=qkey)
        reponses_bloc2[qkey] = choix

    if st.button("➡️ Suivant (Analyse + Bloc 3)"):
        try:
            synthese_prompt = f"Profil : {profil}\nPrénom : {st.session_state['prenom_resultat']}\nRéponses Bloc 2 :\n"
            for q, r in reponses_bloc2.items():
                synthese_prompt += f"- {q} : {r}\n"
            synthese_prompt += "Analyse les points forts et prépare l’élève au Bloc 3."

            synthese = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": synthese_prompt}],
                temperature=0.7
            ).choices[0].message.content

            st.session_state["synthese_bloc2"] = synthese
            st.session_state["etape"] = "bloc3"
            st.rerun()
        except Exception as e:
            st.error(f"Erreur GPT : {str(e)}")

# === Bloc 3 ===
elif st.session_state["etape"] == "bloc3":
    st.header("🔍 Bloc 3 : Confirmation par situation complexe")

    profil = st.session_state["orientation"]
    st.markdown(f"**📚 Profil prédit :** {profil}")
    st.markdown(f"**📝 Synthèse Bloc 2 :** {st.session_state['synthese_bloc2']}")

    try:
        prompt_situation = f"Génère une situation complexe pour confirmer un profil {profil} d’orientation scolaire. La situation doit :\n- être réaliste\n- contenir deux dimensions (émotionnelle, logique...)\n- se terminer par 3 questions ouvertes"

        situation = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt_situation}],
            temperature=0.7
        ).choices[0].message.content

        st.markdown("### 📘 Situation complexe à résoudre")
        st.markdown(situation)

        rep1 = st.text_area("Réponse 1")
        rep2 = st.text_area("Réponse 2")
        rep3 = st.text_area("Réponse 3")

        if st.button("📍 Analyse finale et profil confirmé"):
            prompt_final = f"""Voici les réponses à une situation complexe pour un élève au profil {profil} :
1. {rep1}
2. {rep2}
3. {rep3}

Analyse-les pour confirmer ou ajuster le profil (scientifique/littéraire/mixte) et donne une recommandation claire et motivante."""

            final = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt_final}],
                temperature=0.7
            ).choices[0].message.content

            st.markdown("## ✅ Résultat final")
            st.markdown(final)

    except Exception as e:
        st.error(f"Erreur lors de la génération de la situation complexe : {str(e)}")
