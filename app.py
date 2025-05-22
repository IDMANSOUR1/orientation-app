import streamlit as st
import openai
import base64
from io import BytesIO
from fpdf import FPDF
import numpy as np
import matplotlib.pyplot as plt

# Clé API
openai.api_key = "sk-...VOTRE_CLÉ_ICI..."  # Remplace par ta vraie clé

st.set_page_config(page_title="Orientation Collège Maroc", layout="centered")
st.title("🎓 Questionnaire d’Orientation Scolaire")

# Navigation
page = st.sidebar.selectbox("📂 Choisir une section", [
    "🧠 Personnalité", "💪 Compétences", "❤️ Préférences", "📊 Résumé"
], key="page")

# 🔹 SECTION 1 : Personnalité
if page == "🧠 Personnalité":
    st.header("🧠 Profil de personnalité")

    st.text_input("Prénom de l'élève :", key="prenom")

    options1 = ["Seul(e)", "En groupe", "Les deux"]
    st.radio("Préféres-tu travailler seul(e) ou en groupe ?", options1, key="groupe", index=options1.index(st.session_state.get("groupe", options1[0])))

    options2 = ["Organisé(e)", "Spontané(e)"]
    st.radio("Es-tu plutôt organisé(e) ou spontané(e) ?", options2, key="organisation", index=options2.index(st.session_state.get("organisation", options2[0])))

    options3 = ["Essaies de comprendre", "Te décourages", "Cherches de l’aide"]
    st.radio("Quand tu fais une erreur, tu :", options3, key="erreur", index=options3.index(st.session_state.get("erreur", options3[0])))

    options4 = ["Suivre les consignes", "Inventer ta méthode", "Un peu des deux"]
    st.radio("Tu préfères :", options4, key="consignes", index=options4.index(st.session_state.get("consignes", options4[0])))

    options5 = ["Oui", "Non", "Parfois"]
    st.radio("Te décris-tu comme quelqu’un de curieux(se) ?", options5, key="curiosite", index=options5.index(st.session_state.get("curiosite", options5[0])))

# 🔹 SECTION 2 : Compétences
elif page == "💪 Compétences":
    st.header("💪 Tes compétences")

    options6 = ["À l’écrit", "À l’oral", "Les deux"]
    st.radio("Es-tu plus à l’aise à l’écrit ou à l’oral ?", options6, key="expression", index=options6.index(st.session_state.get("expression", options6[0])))

    options7 = ["Oui", "Non", "Parfois"]
    st.radio("Sais-tu expliquer facilement une idée aux autres ?", options7, key="expliquer", index=options7.index(st.session_state.get("expliquer", options7[0])))

    options8 = ["Oui", "Non", "Un peu"]
    st.radio("Es-tu à l’aise avec les outils numériques ?", options8, key="numerique", index=options8.index(st.session_state.get("numerique", options8[0])))

    st.radio("Aimes-tu résoudre des problèmes complexes ?", options7, key="probleme", index=options7.index(st.session_state.get("probleme", options7[0])))

# 🔹 SECTION 3 : Préférences
elif page == "❤️ Préférences":
    st.header("❤️ Tes préférences")

    options9 = ["Maths", "Français", "SVT", "Histoire", "Physique", "Langues", "Arts", "Sport", "Autre"]
    st.selectbox("Quelle matière préfères-tu à l’école ?", options9, key="matiere", index=options9.index(st.session_state.get("matiere", options9[0])))

    options10 = ["Lire", "Dessiner", "Bricoler", "Jouer", "Écouter de la musique", "Autre"]
    st.radio("Chez toi, tu préfères :", options10, key="activite", index=options10.index(st.session_state.get("activite", options10[0])))

    st.radio("Aimes-tu les activités créatives ?", options7, key="creativite", index=options7.index(st.session_state.get("creativite", options7[0])))

    st.radio("Tu t’ennuies vite quand une activité est répétitive ?", options7, key="repetition", index=options7.index(st.session_state.get("repetition", options7[0])))

    options11 = ["L’histoire", "Les images/effets", "Le message profond"]
    st.radio("Dans un film, tu préfères :", options11, key="film", index=options11.index(st.session_state.get("film", options11[0])))

# 🔹 SECTION 4 : Résumé
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
        st.write(f"**{question}** : {reponse}")

    if st.button("🔎 Analyser mon profil"):
        with st.spinner("Analyse en cours..."):
            try:
                prompt = f"Prénom de l'élève : {prenom}\n\nVoici ses réponses :\n"
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

                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    temperature=0.7
                )
                result_text = response.choices[0].message["content"]
                st.success("🎯 Résultat")
                st.markdown(result_text)

                # 🔢 Extraction et graphe radar
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

                # 📄 PDF export
                pdf = FPDF()
                pdf.add_page()
                pdf.set_font("Arial", size=12)
                pdf.multi_cell(0, 10, f"Orientation scolaire pour : {prenom}")
                for q, r in reponses.items():
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
