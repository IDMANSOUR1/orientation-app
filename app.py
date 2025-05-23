import streamlit as st
import os
import base64
from io import BytesIO
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt
import re
from openai import OpenAI

# Configuration
st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Questionnaire d’Orientation Scolaire")

# Clé API
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Navigation
page = st.sidebar.selectbox("📂 Choisir une section", [
    "🧠 Personnalité", "💪 Compétences", "❤️ Préférences", "📊 Résumé"
])

# Fonctions questions persistantes
def question_radio(label, options, key):
    valeur = st.session_state.get(key)
    index = options.index(valeur) if valeur in options else 0
    choix = st.radio(label, options, index=index)
    if choix != options[0]:
        st.session_state[key] = choix

def question_selectbox(label, options, key):
    valeur = st.session_state.get(key)
    index = options.index(valeur) if valeur in options else 0
    choix = st.selectbox(label, options, index=index)
    if choix != options[0]:
        st.session_state[key] = choix

# 🔹 PAGE 1 : Personnalité
if page == "🧠 Personnalité":
    st.header("🧠 Profil de personnalité")
    st.text_input("Prénom de l'élève :", key="prenom")

    question_radio("Préféres-tu travailler seul(e) ou en groupe ?", ["-- Sélectionne --", "Seul(e)", "En groupe", "Les deux"], "groupe")
    question_radio("Es-tu plutôt organisé(e) ou spontané(e) ?", ["-- Sélectionne --", "Organisé(e)", "Spontané(e)"], "organisation")
    question_radio("Quand tu fais une erreur, tu :", ["-- Sélectionne --", "Essaies de comprendre", "Te décourages", "Cherches de l’aide"], "erreur")
    question_radio("Tu préfères :", ["-- Sélectionne --", "Suivre les consignes", "Inventer ta méthode", "Un peu des deux"], "consignes")
    question_radio("Te décris-tu comme quelqu’un de curieux(se) ?", ["-- Sélectionne --", "Oui", "Non", "Parfois"], "curiosite")

# 🔹 PAGE 2 : Compétences
elif page == "💪 Compétences":
    st.header("💪 Tes compétences")
    question_radio("Es-tu plus à l’aise à l’écrit ou à l’oral ?", ["-- Sélectionne --", "À l’écrit", "À l’oral", "Les deux"], "expression")
    question_radio("Sais-tu expliquer facilement une idée aux autres ?", ["-- Sélectionne --", "Oui", "Non", "Parfois"], "expliquer")
    question_radio("Es-tu à l’aise avec les outils numériques ?", ["-- Sélectionne --", "Oui", "Non", "Un peu"], "numerique")
    question_radio("Aimes-tu résoudre des problèmes complexes ?", ["-- Sélectionne --", "Oui", "Non", "Parfois"], "probleme")

# 🔹 PAGE 3 : Préférences
elif page == "❤️ Préférences":
    st.header("❤️ Tes préférences")
    question_selectbox("Quelle matière préfères-tu à l’école ?", ["-- Sélectionne --", "Maths", "Français", "SVT", "Histoire", "Physique", "Langues", "Arts", "Sport", "Autre"], "matiere")
    question_radio("Chez toi, tu préfères :", ["-- Sélectionne --", "Lire", "Dessiner", "Bricoler", "Jouer", "Écouter de la musique", "Autre"], "activite")
    question_radio("Aimes-tu les activités créatives ?", ["-- Sélectionne --", "Oui", "Non", "Parfois"], "creativite")
    question_radio("Tu t’ennuies vite quand une activité est répétitive ?", ["-- Sélectionne --", "Oui", "Non", "Parfois"], "repetition")
    question_radio("Dans un film, tu préfères :", ["-- Sélectionne --", "L’histoire", "Les images/effets", "Le message profond"], "film")

# 🔹 PAGE 4 : Résumé et Analyse
elif page == "📊 Résumé":
    st.header("📊 Résumé de tes réponses")
    prenom = st.session_state.get("prenom", "")
    if prenom:
        st.markdown(f"👤 **Élève : {prenom}**")

    reponses = {
        k: v for k, v in st.session_state.items()
        if k not in ["page", "prenom"] and v != "-- Sélectionne --"
    }

    for question, reponse in reponses.items():
        st.write(f"**{question}** : {reponse}")

    if st.button("🔎 Analyser mon profil"):
        with st.spinner("Analyse en cours..."):
            try:
                # 🧠 Construction du prompt
                prompt = f"Prénom de l'élève : {prenom}\nVoici ses réponses :\n"
                for q, r in reponses.items():
                    prompt += f"- {q} : {r}\n"
                prompt += """
Analyse ces réponses. Donne une orientation (scientifique, littéraire ou mixte), une justification et un score sur 10 pour :
- Logique
- Créativité
- Communication
- Curiosité scientifique
- Expression artistique
"""

                response = client.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )

                result_text = response.choices[0].message.content
                st.success("🎯 Résultat")
                st.markdown(result_text)

                # 📊 Extraction des scores
                scores = {}
                for line in result_text.splitlines():
                    match = re.search(r"([\w\séèàçïÉÊÈ]+)\s*:\s*(\d+(?:[\.,]\d+)?)\s*/\s*10", line)
                    if match:
                        key = match.group(1).strip().capitalize()
                        val = match.group(2).replace(",", ".")
                        try:
                            scores[key] = float(val)
                        except:
                            pass

                st.write("✅ Scores extraits :", scores)

                # ✅ Graphe radar
                if scores:
                    st.markdown("### 📊 Visualisation du profil")
                    labels = list(scores.keys())
                    values = list(scores.values())
                    angles = np.linspace(0, 2 * np.pi, len(labels), endpoint=False).tolist()
                    values += values[:1]
                    angles += angles[:1]
                    fig, ax = plt.subplots(figsize=(6, 6), subplot_kw=dict(polar=True))
                    ax.plot(angles, values, color='blue', linewidth=2)
                    ax.fill(angles, values, color='skyblue', alpha=0.4)
                    ax.set_yticklabels([])
                    ax.set_xticks(angles[:-1])
                    ax.set_xticklabels(labels)
                    st.pyplot(fig)

                # 📄 Génération PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, f"Orientation scolaire pour : {prenom}")
                for q, r in reponses.items():
                    pdf.multi_cell(0, 10, f"{q} : {r}")
                pdf.multi_cell(0, 10, "\nRésultat IA :")
                pdf.multi_cell(0, 10, result_text.encode('latin-1', 'ignore').decode('latin-1'))
                buffer = BytesIO()
                buffer.write(pdf.output(dest='S').encode("latin-1"))
                b64 = base64.b64encode(buffer.getvalue()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="orientation_resultat.pdf">📄 Télécharger le PDF</a>'
                st.markdown(href, unsafe_allow_html=True)

            except Exception as e:
                st.error("❌ Erreur : " + str(e))
