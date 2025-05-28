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
        "Q1": ("Tu dois faire un exposé. Tu :", [
            "Organises tes idées en plan",
            "Commences par écrire",
            "Dessines une carte mentale"
        ]),
        "Q2": ("Un ami bloque sur un exercice. Tu :", [
            "Réexplique la méthode",
            "Reformules avec tes mots",
            "Inventes une métaphore"
        ]),
        "Q3": ("Tu préfères :", [
            "Correction structurée",
            "Explication orale",
            "Méthodes comparées"
        ]),
        "Q4": ("Tu choisis :", [
            "Problème à solution unique",
            "Rédaction libre",
            "Projet créatif"
        ]),
        "Q5": ("Face à une question difficile, tu :", [
            "Tentes ta chance",
            "Attends d’être sûr",
            "Notes pour plus tard"
        ]),
        "Q6": ("On dit : 'méthode originale mais lente'. Tu :", [
            "Cherches logique",
            "Es fier(e)",
            "T'interroges sur ton style"
        ]),
        "Q7": ("Au CDI, tu :", [
            "Cherches un tuto",
            "Lis un blog ou vidéo d’analyse",
            "Crées un projet"
        ]),
        "Q8": ("Tu es méthodique ?", [
            "Oui, j’aime structurer",
            "Non, idées spontanées",
            "Les deux selon les cas"
        ]),
        "Q9": ("Sujet difficile. Tu :", [
            "Fais un exercice",
            "Relis ton cours",
            "Discutes avec quelqu’un"
        ]),
        "Q10": ("Atelier libre. Tu choisis :", [
            "Construire une maquette",
            "Écrire une histoire",
            "Résoudre des énigmes"
        ]),
        "Q11": ("Corriger un devoir. Tu regardes :", [
            "Le raisonnement",
            "La qualité d’écriture",
            "L’originalité"
        ]),
        "Q12": ("En exposé, tu préfères :", [
            "Rechercher et organiser",
            "Écrire ou présenter",
            "Créer le support"
        ]),
        "Q13": ("Consigne floue. Tu :", [
            "Demande plus de détails",
            "Proposes une idée originale",
            "Improvises"
        ]),
        "Q14": ("Débat. Tu observes :", [
            "Les arguments",
            "La clarté",
            "La surprise"
        ]),
        "Q15": ("Pour résumer un texte :", [
            "Idées principales",
            "Tes mots",
            "Carte mentale"
        ])
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
            with st.spinner("Analyse du profil..."):
                try:
                    prompt = f"Voici les réponses d’un élève marocain. Déduis son profil dominant : scientifique, littéraire ou mixte. Prénom : {prenom.strip()}\n"
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
                    st.session_state["prenom"] = prenom.strip()
                    st.session_state["etape"] = "bloc2"
                    st.rerun()
                except Exception as e:
                    st.error(f"Erreur GPT : {str(e)}")

# === Bloc 2 ===
elif st.session_state["etape"] == "bloc2":
    st.header("📘 Bloc 2 : Questions ciblées")

    profil = st.session_state["orientation"]
    st.success(f"📚 Profil détecté : {profil}")
    st.markdown(f"**Résumé Bloc 1 :** _{st.session_state['resume']}_")

    literaire_qs = [
        ("Tu dois écrire un discours. Tu :", ["Note idées", "Cherche citations", "Rédige directement"]),
        ("Dans un débat, tu :", ["Arguments logiques", "Émotion", "Jeux de mots"]),
        ("Lettre à un ami :", ["J’écris comme je parle", "Je structure", "Je fais un plan détaillé"]),
    ]
    scientifique_qs = [
        ("Ton vélo a un problème. Tu :", ["Observe", "Cherche en ligne", "Demande à quelqu’un"]),
        ("Puzzle logique. Tu :", ["Cherche les règles", "Teste au hasard", "Regarde un exemple"]),
        ("Organiser une expérience. Tu :", ["Liste matériel", "Définit l’objectif", "Note les variables"]),
    ]

    if profil == "scientifique":
        questions = scientifique_qs
    elif profil == "littéraire":
        questions = literaire_qs
    else:
        questions = scientifique_qs[:2] + literaire_qs[:1]

    reponses_bloc2 = {}
    for idx, (question, options) in enumerate(questions):
        qkey = f"B2_Q{idx+1}"
        choix = st.radio(f"{question}", options, key=qkey)
        reponses_bloc2[qkey] = choix

    if st.button("📊 Analyse finale"):
        with st.spinner("Analyse des réponses ciblées..."):
            try:
                synthese_prompt = f"Profil : {profil}\nPrénom : {st.session_state['prenom']}\nRéponses Bloc 2 :\n"
                for q, r in reponses_bloc2.items():
                    synthese_prompt += f"- {q} : {r}\n"

                synthese_prompt += "Analyse le fonctionnement cognitif de l’élève et propose un conseil d’orientation adapté."

                completion = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": synthese_prompt}],
                    temperature=0.7
                )
                st.markdown("### 🧠 Synthèse finale")
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Erreur GPT : {str(e)}")
