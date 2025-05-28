import streamlit as st
import os
from openai import OpenAI
import json

st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Test d'Orientation Implicite")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Navigation
if "page" not in st.session_state:
    st.session_state.page = "bloc1"

if st.session_state.page == "bloc1":
    st.header("🧠 Réponds aux 15 situations")
    prenom = st.text_input("Prénom de l'élève :", key="prenom")

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
        "Q6": ("Un devoir est noté 'méthode originale mais pas rapide'. Tu te dis :", [
            "Chercher une méthode plus logique",
            "Être fier(e) d’avoir réfléchi autrement",
            "Se questionner sur son style"
        ]),
        "Q7": ("Une heure libre au CDI avec Internet. Tu :", [
            "Cherches un tuto sur un sujet qui te passionne",
            "Lis un article, un blog ou regarde une vidéo d’analyse",
            "Dessines, écris ou développes un projet"
        ]),
        "Q8": ("Un adulte te dit : 'Tu es méthodique'. Tu penses :", [
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
        # Ajoutez les 13 autres questions similaires ici (raccourci pour la clarté)
    }
    reponses = {}
    for key, (question, options) in questions.items():
        choix = st.radio(question, options, key=key)
        if choix:
            reponses[key] = choix

    if st.button("➡️ Suivant : Analyser le profil"):
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

                    st.session_state["profil"] = result_json['orientation']
                    st.session_state["resume"] = result_json['resume']
                    st.session_state.page = "bloc2"
                    st.experimental_rerun()

                except Exception as e:
                    st.error(f"❌ Une erreur est survenue : {str(e)}")

elif st.session_state.page == "bloc2":
    st.header("📘 Bloc 2 : Questions selon ton profil")

    profil = st.session_state["profil"].lower()
    resume = st.session_state.get("resume", "")

    st.markdown(f"**🧑 Prénom :** {st.session_state.get('prenom', '')}")
    st.markdown(f"**📚 Orientation recommandée :** `{profil}`")
    st.markdown("**📝 Résumé :**")
    st.markdown(f"> {resume}")

    literaire_questions = [
        ("Tu dois écrire un discours pour convaincre : que fais-tu en premier ?", ["Je note mes idées clés", "Je cherche des citations", "Je rédige directement"]),
        ("Dans un débat, tu préfères :", ["Présenter des arguments logiques", "Toucher les émotions", "Jouer avec les mots"])
    ]

    scientifique_questions = [
        ("Tu rencontres un problème avec ton vélo. Quelle est ta première réaction ?", ["Observer et identifier le problème", "Chercher une solution sur Internet", "Demander à quelqu’un"]),
        ("On te donne un puzzle logique. Que fais-tu ?", ["Je cherche les règles du jeu", "Je commence au hasard pour tester", "Je regarde un exemple"])
    ]

    if profil == "littéraire":
        questions_bloc2 = literaire_questions
    elif profil == "scientifique":
        questions_bloc2 = scientifique_questions
    else:
        questions_bloc2 = literaire_questions[:1] + scientifique_questions[:1]

    reponses_bloc2 = {}
    for idx, (question, options) in enumerate(questions_bloc2):
        choix = st.radio(f"Q{16 + idx} : {question}", options, key=f"Q{16 + idx}")
        reponses_bloc2[f"Q{16 + idx}"] = choix

    if st.button("📊 Analyser Bloc 2"):
        with st.spinner("Analyse complémentaire..."):
            try:
                summary_prompt = f"""
Voici les réponses d’un élève à un bloc de questions ciblées pour l’orientation scolaire. Analyse ces réponses pour détecter des traits cognitifs, des préférences ou des comportements liés à l’apprentissage, en lien avec le profil estimé ({profil}).

Réponses Bloc 2 :
"""
                for q, r in reponses_bloc2.items():
                    summary_prompt += f"- {q} : {r}\n"

                summary_prompt += """
Rédige une brève synthèse sur son fonctionnement cognitif et donne un conseil adapté.
"""

                completion = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": summary_prompt}],
                    temperature=0.7
                )
                synthese = completion.choices[0].message.content
                st.markdown("### 🧠 Analyse Bloc 2")
                st.markdown(synthese)

            except Exception as e:
                st.error(f"Erreur GPT : {str(e)}")
