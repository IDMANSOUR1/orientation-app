import streamlit as st
import openai
import base64
from io import BytesIO
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt

# Configuration
st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Questionnaire d’Orientation Scolaire")

# Clé API
openai.api_key = "sk-...VOTRE_CLÉ_ICI..."

# Navigation
page = st.sidebar.selectbox("📂 Choisir une section", [
    "🧠 Personnalité", "💪 Compétences", "❤️ Préférences", "📊 Résumé"
])

# ========== SECTION 1 : Personnalité ==========
if page == "🧠 Personnalité":
    st.header("🧠 Profil de personnalité")

    st.text_input("Prénom de l'élève :", key="prenom")

    options1 = ["-- Sélectionne --", "Seul(e)", "En groupe", "Les deux"]
    g = st.radio("Préféres-tu travailler seul(e) ou en groupe ?", options1, key="groupe")
    if g != "-- Sélectionne --":
        st.session_state["groupe"] = g

    options2 = ["-- Sélectionne --", "Organisé(e)", "Spontané(e)"]
    o = st.radio("Es-tu plutôt organisé(e) ou spontané(e) ?", options2, key="organisation")
    if o != "-- Sélectionne --":
        st.session_state["organisation"] = o

    options3 = ["-- Sélectionne --", "Essaies de comprendre", "Te décourages", "Cherches de l’aide"]
    e = st.radio("Quand tu fais une erreur, tu :", options3, key="erreur")
    if e != "-- Sélectionne --":
        st.session_state["erreur"] = e

    options4 = ["-- Sélectionne --", "Suivre les consignes", "Inventer ta méthode", "Un peu des deux"]
    c = st.radio("Tu préfères :", options4, key="consignes")
    if c != "-- Sélectionne --":
        st.session_state["consignes"] = c

    options5 = ["-- Sélectionne --", "Oui", "Non", "Parfois"]
    cu = st.radio("Te décris-tu comme quelqu’un de curieux(se) ?", options5, key="curiosite")
    if cu != "-- Sélectionne --":
        st.session_state["curiosite"] = cu

# ========== SECTION 2 : Compétences ==========
elif page == "💪 Compétences":
    st.header("💪 Tes compétences")

    options6 = ["-- Sélectionne --", "À l’écrit", "À l’oral", "Les deux"]
    exp = st.radio("Es-tu plus à l’aise à l’écrit ou à l’oral ?", options6, key="expression")
    if exp != "-- Sélectionne --":
        st.session_state["expression"] = exp

    options7 = ["-- Sélectionne --", "Oui", "Non", "Parfois"]
    expl = st.radio("Sais-tu expliquer facilement une idée aux autres ?", options7, key="expliquer")
    if expl != "-- Sélectionne --":
        st.session_state["expliquer"] = expl

    options8 = ["-- Sélectionne --", "Oui", "Non", "Un peu"]
    num = st.radio("Es-tu à l’aise avec les outils numériques ?", options8, key="numerique")
    if num != "-- Sélectionne --":
        st.session_state["numerique"] = num

    prob = st.radio("Aimes-tu résoudre des problèmes complexes ?", options7, key="probleme")
    if prob != "-- Sélectionne --":
        st.session_state["probleme"] = prob

# ========== SECTION 3 : Préférences ==========
elif page == "❤️ Préférences":
    st.header("❤️ Tes préférences")

    options9 = ["-- Sélectionne --", "Maths", "Français", "SVT", "Histoire", "Physique", "Langues", "Arts", "Sport", "Autre"]
    mat = st.selectbox("Quelle matière préfères-tu à l’école ?", options9, key="matiere")
    if mat != "-- Sélectionne --":
        st.session_state["matiere"] = mat

    options10 = ["-- Sélectionne --", "Lire", "Dessiner", "Bricoler", "Jouer", "Écouter de la musique", "Autre"]
    act = st.radio("Chez toi, tu préfères :", options10, key="activite")
    if act != "-- Sélectionne --":
        st.session_state["activite"] = act

    crea = st.radio("Aimes-tu les activités créatives ?", options7, key="creativite")
    if crea != "-- Sélectionne --":
        st.session_state["creativite"] = crea

    rep = st.radio("Tu t’ennuies vite quand une activité est répétitive ?", options7, key="repetition")
    if rep != "-- Sélectionne --":
        st.session_state["repetition"] = rep

    options11 = ["-- Sélectionne --", "L’histoire", "Les images/effets", "Le message profond"]
    film = st.radio("Dans un film, tu préfères :", options11, key="film")
    if film != "-- Sélectionne --":
        st.session_state["film"] = film

# ========== SECTION 4 : Résumé ==========
elif page == "📊 Résumé":
    st.header("📊 Résumé de tes réponses")
    prenom = st.session_state.get("prenom", "")
    if prenom:
        st.markdown(f"👤 **Élève : {prenom}**")

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

    for question, reponse in reponses.items():
        if reponse and reponse != "-- Sélectionne --":
            st.write(f"**{question}** : {reponse}")

    if st.button("🔎 Analyser mon profil"):
        with st.spinner("Analyse en cours..."):
            try:
                prompt = f"Prénom de l'élève : {prenom}\n\nVoici ses réponses :\n"
                for q, r in reponses.items():
                    if r and r != "-- Sélectionne --":
                        prompt += f"- {q} : {r}\n"
                prompt += """
Analyse ces réponses. Donne une orientation (scientifique, littéraire ou mixte), une justification et un score sur 10 pour :
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

                # PDF
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, f"Orientation scolaire pour : {prenom}")
                for q, r in reponses.items():
                    if r and r != "-- Sélectionne --":
                        pdf.multi_cell(0, 10, f"{q} : {r}")
                pdf.multi_cell(0, 10, "\nRésultat IA :")
                pdf.multi_cell(0, 10, result_text)
                buffer = BytesIO()
                buffer.write(pdf.output(dest='S').encode("latin-1"))
                b64 = base64.b64encode(buffer.getvalue()).decode()
                href = f'<a href="data:application/octet-stream;base64,{b64}" download="orientation_resultat.pdf">📄 Télécharger le PDF</a>'
                st.markdown(href, unsafe_allow_html=True)

            except Exception as e:
                st.error("❌ Erreur : " + str(e))
