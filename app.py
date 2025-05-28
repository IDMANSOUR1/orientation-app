import streamlit as st
import os
import json
from openai import OpenAI

st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Test d'Orientation Implicite")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

if "etape" not in st.session_state:
    st.session_state["etape"] = "bloc1"

if "prenom" not in st.session_state:
    st.session_state["prenom"] = ""

# === Bloc 1 ===
if st.session_state["etape"] == "bloc1":
    st.header("🧠 Bloc 1 : Situations générales")
    st.session_state["prenom"] = st.text_input("Prénom de l'élève :", value=st.session_state["prenom"])

    questions_bloc1 = { f"Q{i+1}": question for i, question in enumerate([
        ("Ton professeur te donne un exposé...", ["Organises les idées...", "Commences par écrire...", "Dessines un schéma..."]),
        ("Un camarade bloque sur un exercice...", ["Réexplique...", "Reformules...", "Inventes..."]),
        ("En classe, ton professeur corrige...", ["Structuré", "Expliqué à voix haute", "Plusieurs méthodes"]),
        ("Tu dois préparer un devoir...", ["Problème", "Dissertation", "Projet créatif"]),
        ("Pendant un cours, ton prof pose...", ["Lances-toi", "Attends", "Note la question"]),
        ("Tu reçois un devoir corrigé...", ["Plus logique", "Fier", "Se questionner"]),
        ("Tu as une heure au CDI...", ["Cherches un tuto", "Lis un article", "Crées un projet"]),
        ("Un adulte dit : 'Tu es méthodique'", ["Oui", "Non", "Un peu des deux"]),
        ("Un nouveau sujet te paraît difficile...", ["Exercice", "Lire", "Discuter"]),
        ("On te propose un atelier...", ["Construire", "Ecrire", "Résoudre"]),
        ("Tu dois corriger un travail...", ["Raisonnement", "Texte clair", "Idée originale"]),
        ("Exposé en groupe...", ["Recherches", "Texte/Oral", "Support visuel"]),
        ("Consigne floue...", ["Demander", "Proposer", "Improviser"]),
        ("Un débat...", ["Arguments", "Clarté", "Idées surprenantes"]),
        ("Résumer un texte...", ["Idées principales", "Reformuler", "Carte mentale"]),
    ])}

    reponses_bloc1 = {}
    for key, (question, options) in questions_bloc1.items():
        choix = st.radio(f"{key} : {question}", options, key=key)
        if choix:
            reponses_bloc1[key] = choix

    if st.button("➡️ Suivant"):
        if len(reponses_bloc1) < 15 or not st.session_state["prenom"].strip():
            st.warning("Merci de répondre à toutes les questions.")
        else:
            prompt = f"""
Voici les réponses de l'élève :
{json.dumps(reponses_bloc1, indent=2)}

Estime son profil : scientifique, littéraire ou mixte. Réponds uniquement avec :
{{"profil": "..."}}
            """
            try:
                response = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                profil = json.loads(response.choices[0].message.content)["profil"]
                st.session_state["profil"] = profil
                st.session_state["etape"] = "bloc2"
                st.rerun()
            except Exception as e:
                st.error(str(e))

# === Bloc 2 ===
elif st.session_state["etape"] == "bloc2":
    st.header("📘 Bloc 2 : Questions ciblées")
    profil = st.session_state["profil"]
    st.info(f"Profil estimé : {profil}")

    questions_sci = [
        ("Tu découvres un concept scientifique...", ["Lire", "Vidéo", "Expérience"]),
        ("Créer une affiche scientifique...", ["Données", "Expérience", "Schéma"]),
        ("Problème de maths...", ["Méthode connue", "Tester", "Exemple"]),
        ("Ce que tu préfères en sciences...", ["Lois", "Applications", "Idées"]),
        ("Lire un problème...", ["Détails", "Visualiser", "Oral"]),
        ("Projet en sciences...", ["Maquette", "Recherche", "Exposé"]),
        ("Stage en labo...", ["Manipuler", "Observer", "Hypothèse"]),
        ("Maths : satisfaction...", ["Raisonnement", "Expliquer", "Nouvelle méthode"]),
        ("Système complexe...", ["Décomposer", "Relations", "Simulation"]),
        ("Sortie éducative...", ["Musée", "Atelier", "Expérience"])
    ]

    questions_lit = [
        ("Lettre à un personnage historique...", ["Contexte", "Langage", "Fiction"]),
        ("Créer un blog...", ["Argumenter", "Témoigner", "Toucher"]),
        ("Français : préféré...", ["Débat", "Analyse", "Invention"]),
        ("Texte ancien...", ["Contexte", "Style", "Adapter"]),
        ("Défendre une idée...", ["Arguments", "Exemples", "Ton"]),
        ("Langue...", ["Traduire", "Jouer", "Dialogues"]),
        ("Livre ou film...", ["Message", "Émotions", "Narration"]),
        ("Podcast...", ["Idée", "Interview", "Lecture"]),
        ("Bibliothèque...", ["Romans", "Analyse", "Poésie"]),
        ("Spectacle...", ["Scénario", "Rôle", "Scène"])
    ]

    questions_bloc2 = questions_sci if profil == "scientifique" else questions_lit

    reponses_bloc2 = {}
    for i, (q, opts) in enumerate(questions_bloc2):
        choix = st.radio(f"Q{i+1} : {q}", opts, key=f"b2q{i+1}")
        reponses_bloc2[f"Q{i+1}"] = choix

    if st.button("➡️ Suivant"):
        st.session_state["bloc2_reponses"] = reponses_bloc2
        st.session_state["etape"] = "bloc3"
        st.rerun()

# === Bloc 3 ===
elif st.session_state["etape"] == "bloc3":
    st.header("🧪 Bloc 3 : Confirmation par situation complexe")
    profil = st.session_state["profil"]
    prompt = f"""
Génère une situation complexe et réaliste pour un collégien marocain, spécifique au profil suivant : {profil}.

Inclue une histoire ou un contexte impliquant une décision, un problème ou une initiative personnelle.
Puis pose 3  questions ouvertes qui permettent de vérifier ses compétences, son raisonnement, ses valeurs, sa personnalité.

Objectif : valider ou ajuster le profil avec une analyse finale.
"""
    try:
        rep = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        st.markdown(rep.choices[0].message.content)

        st.text_area("📝 Tes réponses ici (copie-colle si besoin) :", key="bloc3_text")

        if st.button("📈 Analyse finale"):
            analyse_prompt = f"Voici toutes les réponses des blocs 1, 2 et 3 pour {st.session_state['prenom']} :\n"
            analyse_prompt += json.dumps(st.session_state.get("bloc2_reponses", {}), indent=2)
            analyse_prompt += f"\nEt voici ses réflexions ouvertes : {st.session_state['bloc3_text']}\n"
            analyse_prompt += "Déduis son profil final (scientifique/littéraire/mixte), ses qualités et conseille-le."

            completion = client.chat.completions.create(
                model="gpt-4",
                messages=[{"role": "user", "content": analyse_prompt}],
                temperature=0.7
            )
            st.success("🎓 Profil Final")
            st.markdown(completion.choices[0].message.content)
    except Exception as e:
        st.error(str(e))
