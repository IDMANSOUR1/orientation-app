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
    "Q3": ("En classe, ton professeur corrige un devoir en silence au tableau. Tu préfères :", [
        "Que ce soit bien structuré, étape par étape",
        "Que ce soit expliqué à voix haute avec des exemples",
        "Qu’il donne plusieurs façons de résoudre pour comparer"
    ]),
    "Q4": ("Tu dois préparer un devoir noté. Tu as le choix :", [
        "Un problème complexe avec une seule bonne solution",
        "Une dissertation ou un texte à rédiger librement",
        "Un projet créatif à construire ou présenter"
    ]),
    "Q5": ("Pendant un cours, ton prof pose une question difficile. Tu :", [
        "Lances-toi, même si tu n’es pas sûr",
        "Attends d’être vraiment certain(e) pour répondre",
        "Préféres noter la question pour la revoir chez toi"
    ]),
    "Q6": ("Tu reçois un devoir corrigé avec cette remarque : 'Ta méthode n’était pas la plus rapide, mais elle est originale.' Tu te dis :", [
        "Je vais chercher la méthode la plus logique la prochaine fois",
        "Je suis fier(e), ça veut dire que j’ai réfléchi autrement",
        "Je me demande si mon style d’approche est un atout ou une faiblesse"
    ]),
    "Q7": ("Tu as une heure de liberté dans un CDI avec Internet. Tu fais quoi ?", [
        "Cherches un tuto sur un sujet qui te fascine (sciences, tech, etc.)",
        "Lis un article, un blog, ou regardes une vidéo d’analyse",
        "Dessines, écris ou prépares un projet personnel"
    ]),
    "Q8": ("Un adulte te dit : 'Tu es quelqu’un de très méthodique.' Tu penses :", [
        "Oui, j’aime bien que tout soit structuré",
        "Non, je préfère laisser venir les idées naturellement",
        "Je suis un peu des deux, selon les moments"
    ]),
    "Q9": ("Un nouveau sujet te paraît difficile à comprendre. Tu préfères :", [
        "Faire un exercice ou un exemple tout de suite pour tester ta compréhension",
        "Lire plusieurs fois le cours pour bien assimiler",
        "En discuter avec quelqu’un pour clarifier tes idées"
    ]),
    "Q10": ("On te propose de participer à un atelier pendant une semaine. Tu choisis :", [
        "Construire un objet ou une maquette",
        "Écrire un scénario, un article ou une histoire",
        "Résoudre des énigmes ou défis logiques en équipe"
    ]),
    "Q11": ("Tu dois corriger un travail. Tu es plus attentif(ve) à :", [
        "Si le raisonnement est juste, même si c’est mal présenté",
        "Si le texte est clair et agréable à lire",
        "Si l’idée est originale ou différente des autres"
    ]),
    "Q12": ("Pendant un exposé en groupe, tu préfères :", [
        "Faire les recherches et organiser le contenu",
        "Écrire le texte ou faire la présentation orale",
        "Concevoir un support visuel ou interactif"
    ]),
    "Q13": ("Un prof te donne une consigne volontairement vague pour un projet libre. Tu ressens :", [
        "Le besoin de lui demander des précisions",
        "Une envie de proposer quelque chose d’original",
        "De l’hésitation, mais tu finis par improviser"
    ]),
    "Q14": ("Tu assistes à un débat entre deux élèves. Tu observes surtout :", [
        "Qui a les meilleurs arguments logiques",
        "Qui s’exprime le plus clairement",
        "Qui a des idées différentes et surprenantes"
    ]),
    "Q15": ("Ton professeur te demande de résumer un texte long. Tu commences par :", [
        "Identifier les idées principales et les structurer",
        "Reformuler phrase par phrase avec tes mots",
        "Créer un plan visuel ou une carte mentale"
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
            prenom_nettoye = prenom.strip()
            with st.spinner("Analyse du profil..."):
                try:
                    prompt = f"Voici les réponses d’un élève marocain. Déduis son profil dominant : scientifique, littéraire ou mixte. Prénom : {prenom_nettoye}\n"
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
                    st.session_state["prenom_resultat"] = prenom_nettoye
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
    st.markdown(f"**Prénom :** {st.session_state['prenom_resultat']}")

  
    scientifique_qs = [
    ("Tu découvres un nouveau concept en physique. Tu préfères :", ["Lire des explications théoriques", "Regarder une vidéo avec des expériences", "Faire toi-même une petite expérience"]),
    ("On te demande de créer une affiche sur un phénomène scientifique. Tu commences par :", ["Rechercher des données fiables", "Imaginer une expérience à montrer", "Faire un schéma clair"]),
    ("Tu dois résoudre un problème de maths inconnu. Tu :", ["Appliques une méthode connue", "Essaies plusieurs pistes logiques", "Demandes un exemple similaire"]),
    ("En sciences, ce qui t’intéresse le plus c’est :", ["Comprendre les lois naturelles", "Trouver des applications concrètes", "Imaginer comment améliorer les choses"]),
    ("Quand tu lis un problème scientifique, tu :", ["Détaille chaque donnée", "Visualises le problème dans ta tête", "Te l’expliques à haute voix"]),
    ("Tu dois créer un projet en sciences. Tu préfères :", ["Un modèle réduit d’un phénomène", "Une recherche documentaire précise", "Un exposé oral avec données chiffrées"]),
    ("On te propose un stage en laboratoire. Tu es surtout attiré par :", ["Manipuler des instruments", "Observer et noter les résultats", "Émettre des hypothèses à tester"]),
    ("En mathématiques, tu ressens le plus de satisfaction quand :", ["Tu trouves le bon raisonnement", "Tu expliques la solution à d'autres", "Tu découvres une méthode nouvelle"]),
    ("Tu es face à un système complexe. Tu :", ["Le décomposes en sous-éléments", "Cherches les relations entre les parties", "Simules son fonctionnement"]),
    ("Tu dois organiser une sortie éducative. Tu proposes :", ["Une visite à un musée scientifique", "Un atelier de robotique", "Une expérience encadrée en classe"])
]



    literaire_qs = [
    ("Tu dois écrire une lettre à un personnage historique. Tu :", ["Imagines son contexte", "Utilises un langage soutenu", "Racontes une situation fictive"]),
    ("On te demande de créer un article de blog. Tu préfères :", ["Argumenter sur un sujet d’actualité", "Témoigner d’une expérience personnelle", "Raconter une histoire touchante"]),
    ("En classe de français, tu préfères :", ["Les débats", "L’analyse de texte", "L’écriture d’invention"]),
    ("Tu lis un texte ancien. Tu es curieux de :", ["L’époque et son contexte", "Le style de l’auteur", "La manière dont on peut l’adapter aujourd’hui"]),
    ("Tu dois défendre une idée à l’écrit. Tu commences par :", ["Structurer tes arguments", "Trouver des exemples forts", "Choisir un ton percutant"]),
    ("En cours de langue, tu aimes :", ["Traduire avec précision", "Jouer avec les mots et expressions", "Écrire des dialogues ou des récits"]),
    ("Un film ou un livre t’a touché. Tu en parles en mettant en avant :", ["Le message profond", "Les émotions vécues", "Le style de narration"]),
    ("Tu dois créer un podcast. Tu veux :", ["Partager une idée originale", "Interviewer des gens", "Lire un texte de ta création"]),
    ("À la bibliothèque, tu cherches plutôt :", ["Des romans classiques", "Des livres d’analyse ou de critique", "Des recueils de poésie ou nouvelles"]),
    ("Tu dois créer un spectacle de fin d’année. Tu veux :", ["Écrire le scénario", "Jouer un rôle marquant", "Créer la mise en scène"])
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
                synthese_prompt = f"Profil : {profil}\nPrénom : {st.session_state['prenom_resultat']}\nRéponses Bloc 2 :\n"
                for q, r in reponses_bloc2.items():
                    synthese_prompt += f"- {q} : {r}\n"

                synthese_prompt += """Analyse le fonctionnement cognitif de l’élève et propose un conseil d’orientation adapté.Ta mission est de rédiger une **réponse brève, claire et motivante** qui :
1. Indique explicitement à l'élève quel est son profil (ex: « Ton profil est plutôt scientifique… »)
2. Met en valeur 2 ou 3 de ses forces principales (en lien avec les réponses)
3. Suggère 2 à 3 pistes ou domaines adaptés à ce profil
4. Termine par un conseil simple, personnalisé et encourageant

⚠️ Format attendu :
- 4 à 6 phrases max
- Style fluide, chaleureux, sans jargon scolaire
- Parle directement à l’élève (avec « tu » ou son prénom)

Objectif : lui donner confiance, clarté et envie de s’investir dans les domaines proposés."""

                completion = client.chat.completions.create(
                    model="gpt-4",
                    messages=[{"role": "user", "content": synthese_prompt}],
                    temperature=0.7
                )
                st.markdown("### 🧠 Synthèse finale")
                st.markdown(completion.choices[0].message.content)
            except Exception as e:
                st.error(f"Erreur GPT : {str(e)}")
