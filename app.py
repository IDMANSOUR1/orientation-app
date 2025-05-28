import streamlit as st
import os
from openai import OpenAI
import json

st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Test d'Orientation Scolaire - Collégien")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "etape" not in st.session_state:
    st.session_state["etape"] = "bloc1"

# === Bloc 1 ===
if st.session_state["etape"] == "bloc1":
    st.header("🧠 Bloc 1 : Réponds aux 15 situations")
    prenom = st.text_input("Ton prénom :", key="prenom")
    
    questions_bloc1 = {
        "Q1": ("Tu fais face à un nouveau sujet inconnu. Tu :", [
            "Organises tes idées en plan",
            "Commences à écrire directement",
            "Fais une carte mentale"
        ]),
        "Q2": ("Un camarade te demande de l’aide sur un exercice. Tu :", [
            "Réexplique la méthode",
            "Reformules le problème",
            "Inventes une métaphore"
        ]),
        # ➕ Ajoute ici Q3 à Q15
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
            st.session_state["prenom"] = prenom.strip()
            st.session_state["reponses_bloc1"] = reponses_bloc1
            prompt = f"Voici les réponses d’un élève. Donne son profil dominant : scientifique, littéraire ou mixte.\n"
            for q, r in reponses_bloc1.items():
                prompt += f"- {q} : {r}\n"
            prompt += "Réponds uniquement en JSON : { \"profil\": \"...\" }"
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                data = json.loads(response.choices[0].message.content)
                st.session_state["profil"] = data["profil"]
                st.session_state["etape"] = "bloc2"
                st.rerun()
            except Exception as e:
                st.error(f"Erreur GPT : {str(e)}")

# === Bloc 2 ===
elif st.session_state["etape"] == "bloc2":
    st.header("📘 Bloc 2 : Questions ciblées")
    profil = st.session_state["profil"]

    scientifique_qs = [
        ("Tu découvres un nouveau concept scientifique. Tu :", ["Lis une explication", "Cherches une vidéo", "Fais une expérience"]),
        # ➕ Ajoute 9 autres questions ici
    ]
    literaire_qs = [
        ("Tu dois écrire une lettre à un personnage historique. Tu :", ["Imagines son époque", "Utilises un beau style", "Racontes une histoire"]),
        # ➕ Ajoute 9 autres questions ici
    ]

    if profil == "scientifique":
        questions = scientifique_qs
    elif profil == "littéraire":
        questions = literaire_qs
    else:
        questions = scientifique_qs[:5] + literaire_qs[:5]

    reponses_bloc2 = {}
    for idx, (question, options) in enumerate(questions):
        qkey = f"B2_Q{idx+1}"
        choix = st.radio(f"{question}", options, key=qkey)
        reponses_bloc2[qkey] = choix

    if st.button("➡️ Suivant (Bloc 3)"):
        st.session_state["reponses_bloc2"] = reponses_bloc2
        st.session_state["etape"] = "bloc3"
        st.rerun()

# === Bloc 3 ===
elif st.session_state["etape"] == "bloc3":
    st.header("🧪 Bloc 3 : Situation complexe de confirmation")
    profil = st.session_state["profil"]

    if "situation" not in st.session_state:
        situation_prompt = f"""Crée une situation complexe pour un élève de collège marocain au profil {profil}.
Donne :
- Un court scénario crédible et engageant
- 3 à 5 questions ouvertes qui explorent sa logique, sa créativité et son raisonnement.
Langage simple. But : confirmer le profil."""
        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": situation_prompt}],
                temperature=0.7
            )
            st.session_state["situation"] = response.choices[0].message.content
        except Exception as e:
            st.error(f"Erreur GPT : {str(e)}")

    st.markdown(st.session_state["situation"])
    reponse_libre = st.text_area("📝 Tes réponses libres :", key="bloc3_reponse")

    if st.button("🎯 Résultat final"):
        analyse_finale_prompt = f"""
Voici toutes les réponses d’un élève :
- Bloc 1 : {st.session_state['reponses_bloc1']}
- Bloc 2 : {st.session_state['reponses_bloc2']}
- Bloc 3 : {st.session_state['situation']} \nRéponses : {reponse_libre}

Fais une synthèse finale de 4 à 6 phrases :
1. Indique clairement son profil
2. Souligne ses points forts
3. Donne 2 ou 3 pistes d'orientation
4. Termine par un conseil positif

Langage adapté à un élève, direct, chaleureux et clair.
"""
        try:
            final = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": analyse_finale_prompt}],
                temperature=0.7
            )
            st.markdown("### 🧠 Résultat final")
            st.markdown(final.choices[0].message.content)
        except Exception as e:
            st.error(f"Erreur GPT : {str(e)}")
