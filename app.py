import streamlit as st
import openai
import pandas as pd
from io import BytesIO
from fpdf import FPDF
import base64
import matplotlib.pyplot as plt
import numpy as np

# Clé API
openai.api_key = "sk-...VOTRE_CLÉ_ICI..."

# Configuration
st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Questionnaire d’Orientation Scolaire")

# Navigation
page = st.sidebar.selectbox("📂 Choisir une section", [
    "🧠 Personnalité", "💪 Compétences", "❤️ Préférences", "📊 Résumé"
])

# Dictionnaire global de réponses
reponses = {}

# 🔹 PAGE 1 : PERSONNALITÉ
if page == "🧠 Personnalité":
    st.header("🧠 Profil de personnalité")
    reponses["Travail en groupe"] = st.radio("Préféres-tu travailler seul(e) ou en groupe ?", ["Seul(e)", "En groupe", "Les deux"])
    reponses["Organisation"] = st.radio("Es-tu plutôt organisé(e) ou spontané(e) ?", ["Organisé(e)", "Spontané(e)"])
    reponses["Face à l’erreur"] = st.radio("Quand tu fais une erreur, tu :", ["Essaies de comprendre", "Te décourages", "Cherches de l’aide"])
    reponses["Respect des consignes"] = st.radio("Tu préfères :", ["Suivre les consignes", "Inventer ta méthode", "Un peu des deux"])
    reponses["Curiosité"] = st.radio("Te décris-tu comme quelqu’un de curieux(se) ?", ["Oui", "Non", "Parfois"])

# 🔹 PAGE 2 : COMPÉTENCES
elif page == "💪 Compétences":
    st.header("💪 Tes compétences")
    reponses["Expression préférée"] = st.radio("Es-tu plus à l’aise à l’écrit ou à l’oral ?", ["À l’écrit", "À l’oral", "Les deux"])
    reponses["Expliquer une idée"] = st.radio("Sais-tu expliquer facilement une idée aux autres ?", ["Oui", "Non", "Parfois"])
    reponses["Compétences numériques"] = st.radio("Es-tu à l’aise avec les outils numériques (ordinateur, tablette) ?", ["Oui", "Non", "Un peu"])
    reponses["Résolution de problème"] = st.radio("Aimes-tu résoudre des problèmes complexes ?", ["Oui", "Non", "Parfois"])

# 🔹 PAGE 3 : PRÉFÉRENCES
elif page == "❤️ Préférences":
    st.header("❤️ Tes préférences")
    reponses["Matière préférée"] = st.selectbox("Quelle matière préfères-tu à l’école ?", ["Maths", "Français", "SVT", "Histoire", "Physique", "Langues", "Arts", "Sport", "Autre"])
    reponses["Activité à la maison"] = st.radio("Chez toi, tu préfères :", ["Lire", "Dessiner", "Bricoler", "Jouer", "Écouter de la musique", "Autre"])
    reponses["Créativité"] = st.radio("Aimes-tu les activités créatives (écrire, peindre, imaginer) ?", ["Oui", "Non", "Un peu"])
    reponses["Répétition"] = st.radio("Tu t’ennuies vite quand une activité est répétitive ?", ["Oui", "Non", "Parfois"])
    reponses["Film préféré"] = st.radio("Dans un film, tu préfères :", ["L’histoire", "Les images/effets", "Le message profond"])

# 🔹 PAGE 4 : RÉSUMÉ + GPT
elif page == "📊 Résumé":
    st.header("📊 Résumé de tes réponses")
    if reponses:
        for question, reponse in reponses.items():
            st.write(f"**{question}** : {reponse}")
        st.success("✅ Tu peux maintenant analyser ton profil.")

        if st.button("🔎 Analyser mon profil"):
            with st.spinner("Analyse IA en cours..."):
                try:
                    prompt = "Voici les réponses d’un élève à un questionnaire d’orientation scolaire :\n\n"
                    for question, reponse in reponses.items():
                        prompt += f"- {question} : {reponse}\n"
                    prompt += """
Analyse ces réponses. Si certaines sont courtes, absurdes ou vides, donne des scores très faibles ou indique 'non mesurable'.

Donne ensuite :
1. L’orientation scolaire recommandée (scientifique, littéraire ou mixte) avec justification
2. Un score sur 10 pour :
   - Logique
   - Créativité
   - Communication
   - Curiosité scientifique
   - Expression artistique
"""

                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.7,
                        max_tokens=500
                    )
                    result_text = response.choices[0].message["content"]
                    st.success("🎯 Résultat")
                    st.markdown(result_text)

                    # Extraction des scores
                    scores = {}
                    for line in result_text.splitlines():
                        if ":" in line and any(key in line.lower() for key in ["logique", "créativité", "communication", "curiosité", "artistique"]):
                            key, val = line.split(":")
                            key = key.strip().capitalize()
                            try:
                                scores[key] = float(val.strip().replace("/10", "").replace(",", "."))
                            except:
                                pass

                    if scores:
                        st.markdown("### 📊 Visualisation du profil")
                        show_radar_chart(scores)

                    # PDF
                    pdf_bytes = generate_pdf(reponses, result_text)
                    b64 = base64.b64encode(pdf_bytes).decode()
                    href = f'<a href="data:application/octet-stream;base64,{b64}" download="orientation_resultat.pdf">📄 Télécharger le PDF</a>'
                    st.markdown(href, unsafe_allow_html=True)

                except Exception as e:
                    st.error("❌ Erreur : " + str(e))
    else:
        st.warning("⚠️ Tu n’as encore rempli aucune réponse. Commence par la première section.")

# 📄 Génération PDF
def generate_pdf(responses_dict, result_text):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.set_text_color(40, 40, 40)
    pdf.multi_cell(0, 10, "Résultat d'Orientation Scolaire", align='C')
    pdf.ln(5)
    for question, answer in responses_dict.items():
        q = question.encode("latin-1", "ignore").decode("latin-1")
        a = answer.encode("latin-1", "ignore").decode("latin-1")
        pdf.multi_cell(0, 10, f"{q} : {a}")
    pdf.ln(5)
    pdf.set_text_color(0, 102, 204)
    pdf.multi_cell(0, 10, "Orientation Recommandée :", align='L')
    pdf.set_text_color(0, 0, 0)
    result = result_text.encode("latin-1", "ignore").decode("latin-1")
    pdf.multi_cell(0, 10, result)
    buffer = BytesIO()
    pdf_bytes = pdf.output(dest='S').encode("latin-1")
    buffer.write(pdf_bytes)
    return buffer.getvalue()

# 📊 Graphe radar
def show_radar_chart(scores):
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
