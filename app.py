import streamlit as st
import openai
import base64
from io import BytesIO
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt

# Configuration générale
st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Questionnaire d’Orientation Scolaire")

# Clé API
openai.api_key = "sk-...VOTRE_CLÉ_ICI..."  # Remplace par ta vraie clé

# Navigation entre pages
page = st.sidebar.selectbox("📂 Choisir une section", [
    "🧠 Personnalité", "💪 Compétences", "❤️ Préférences", "📊 Résumé"
], key="page")

# 🔹 SECTION 1 : Personnalité
if page == "🧠 Personnalité":
    st.header("🧠 Profil de personnalité")

    st.text_input("Prénom de l'élève :", key="prenom")
    st.radio("Préféres-tu travailler seul(e) ou en groupe ?", ["Seul(e)", "En groupe", "Les deux"], key="groupe")
    st.radio("Es-tu plutôt organisé(e) ou spontané(e) ?", ["Organisé(e)", "Spontané(e)"], key="organisation")
    st.radio("Quand tu fais une erreur, tu :", ["Essaies de comprendre", "Te décourages", "Cherches de l’aide"], key="erreur")
    st.radio("Tu préfères :", ["Suivre les consignes", "Inventer ta méthode", "Un peu des deux"], key="consignes")
    st.radio("Te décris-tu comme quelqu’un de curieux(se) ?", ["Oui", "Non", "Parfois"], key="curiosite")

# 🔹 SECTION 2 : Compétences
elif page == "💪 Compétences":
    st.header("💪 Tes compétences")

    st.radio("Es-tu plus à l’aise à l’écrit ou à l’oral ?", ["À l’écrit", "À l’oral", "Les deux"], key="expression")
    st.radio("Sais-tu expliquer facilement une idée aux autres ?", ["Oui", "Non", "Parfois"], key="expliquer")
    st.radio("Es-tu à l’aise avec les outils numériques ?", ["Oui", "Non", "Un peu"], key="numerique")
    st.radio("Aimes-tu résoudre des problèmes complexes ?", ["Oui", "Non", "Parfois"], key="probleme")

# 🔹 SECTION 3 : Préférences
elif page == "❤️ Préférences":
    st.header("❤️ Tes préférences")

    st.selectbox("Quelle matière préfères-tu à l’école ?", ["Maths", "Français", "SVT", "Histoire", "Physique", "Langues", "Arts", "Sport", "Autre"], key="matiere")
    st.radio("Chez toi, tu préfères :", ["Lire", "Dessiner", "Bricoler", "Jouer", "Écouter de la musique", "Autre"], key="activite")
    st.radio("Aimes-tu les activités créatives ?", ["Oui", "Non", "Un peu"], key="creativite")
    st.radio("Tu t’ennuies vite quand une activité est répétitive ?", ["Oui", "Non", "Parfois"], key="repetition")
    st.radio("Dans un film, tu préfères :", ["L’histoire", "Les images/effets", "Le message profond"], key="film")

# 🔹 SECTION 4 : Résumé & Analyse
elif page == "📊 Résumé":
    st.header("📊 Résumé de tes réponses")
    prenom = st.session_state.get("prenom", "")

    if prenom:
        st.markdown(f"👤 **Élève : {prenom}**")

    # Construction des réponses à partir de session_state
    reponses = {
        "Travail en groupe": st.session_state.get("groupe", ""),
        "Organisation": st.session_state.get("organisation", ""),
        "Face à l’erreur": st.session_state.get("erreur", ""),
        "Respect des consignes": st.session_state.get("consignes", ""),
        "Curiosité": st.session_state.get("curiosite", ""),
        "Expression préférée": st.session_state.get("expression", ""),
        "Expliquer une idée": st.session_state.get("expliquer", ""),
        "Compétences numériques": st.session_state.get("numerique", ""),
        "Résolution de problème": st.session_state.get("probleme", ""),
        "Matière préférée": st.session_state.get("matiere", ""),
        "Activité à la maison": st.session_state.get("activite", ""),
        "Créativité": st.session_state.get("creativite", ""),
        "Répétition": st.session_state.get("repetition", ""),
        "Film préféré": st.session_state.get("film", "")
    }

    # Affichage
    for question, reponse in reponses.items():
        st.write(f"**{question}** : {reponse}")

    # 🔎 Analyse IA
    if st.button("🔎 Analyser mon profil"):
        with st.spinner("Analyse en cours..."):
            try:
                prompt = f"Prénom de l'élève : {prenom}\n\nVoici ses réponses :\n"
                for q, r in reponses.items():
                    prompt += f"- {q} : {r}\n"
                prompt += """
Analyse ces réponses. Si certaines sont absurdes ou vides, donne un score bas ou 'non mesurable'.

Donne ensuite :
1. L’orientation recommandée (scientifique, littéraire ou mixte)
2. Une justification
3. Un score sur 10 pour :
   - Logique
   - Créativité
   - Communication
   - Curiosité scientifique
   - Expression artistique
"""

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                result_text = response.choices[0].message["content"]
                st.success("🎯 Résultat")
                st.markdown(result_text)

                # Graphe radar
                scores = {}
                for line in result_text.splitlines():
                    if ":" in line and any(k in line.lower() for k in ["logique", "créativité", "communication", "curiosité", "artistique"]):
                        key, val = line.split(":")
                        try:
                            scores[key.strip().capitalize()] = float(val.strip().replace("/10", "").replace(",", "."))
                        except:
                            pass

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

                # PDF export
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, f"Orientation scolaire pour : {prenom}")
                for q, r in reponses.items():
                    pdf.multi_cell(0, 10, f"{q} : {r}")
                pdf.multi_cell(0, 10, "\nRésultat IA :")
                pdf.multi_cell(_
