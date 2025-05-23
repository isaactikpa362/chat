import re
import string
import streamlit as st

# 🔽 Fonction pour découper le texte en phrases
def split_sentences(text):
    return re.split(r'(?<=[.!?])\s+', text.strip())

# 🔽 Fonction pour prétraiter une phrase
def preprocess(sentence):
    # Convertir en minuscules, enlever la ponctuation
    sentence = sentence.lower().translate(str.maketrans('', '', string.punctuation))
    words = sentence.split()
    stopwords = set([
        "i", "me", "my", "myself", "we", "our", "ours", "ourselves",
        "you", "your", "yours", "yourself", "yourselves", "he", "him",
        "his", "himself", "she", "her", "hers", "herself", "it", "its",
        "itself", "they", "them", "their", "theirs", "themselves",
        "what", "which", "who", "whom", "this", "that", "these", "those",
        "am", "is", "are", "was", "were", "be", "been", "being", "have",
        "has", "had", "having", "do", "does", "did", "doing", "a", "an",
        "the", "and", "but", "if", "or", "because", "as", "until", "while",
        "of", "at", "by", "for", "with", "about", "against", "between",
        "into", "through", "during", "before", "after", "above", "below",
        "to", "from", "up", "down", "in", "out", "on", "off", "over",
        "under", "again", "further", "then", "once", "here", "there",
        "when", "where", "why", "how", "all", "any", "both", "each",
        "few", "more", "most", "other", "some", "such", "no", "nor",
        "not", "only", "own", "same", "so", "than", "too", "very",
        "can", "will", "just", "don", "should", "now"
    ])
    words = [word for word in words if word not in stopwords]
    return words

# 🔽 Charger et prétraiter le corpus
try:
    with open("corpus.txt", "r", encoding="utf-8") as f:
        data = f.read().replace("\n", " ")
except FileNotFoundError:
    data = ""

sentences = split_sentences(data)
corpus = [preprocess(sentence) for sentence in sentences]

# 🔽 Fonction pour trouver la phrase la plus pertinente
def get_most_relevant_sentence(query):
    query = preprocess(query)
    max_similarity = 0
    best_sentence = "Je ne trouve rien de pertinent dans le texte."
    for i, sentence in enumerate(corpus):
        union = set(query).union(sentence)
        if not union:
            continue
        similarity = len(set(query).intersection(sentence)) / len(union)
        if similarity > max_similarity:
            max_similarity = similarity
            best_sentence = sentences[i]
    return best_sentence

# 🔽 Fonction principale du chatbot
def chatbot(question):
    return get_most_relevant_sentence(question)

# 🔽 Interface utilisateur avec Streamlit
def main():
    st.title("🤖 Chatbot basé sur un fichier texte")
    st.write("Pose une question sur le contenu de `corpus.txt`.")

    question = st.text_input("Vous :")

    if st.button("Envoyer"):
        if not question.strip():
            st.warning("Veuillez entrer une question.")
        else:
            response = chatbot(question)
            st.markdown(f"**Chatbot :** {response}")

# 🔽 Lancement de l'app
if __name__ == "__main__":
    main()
