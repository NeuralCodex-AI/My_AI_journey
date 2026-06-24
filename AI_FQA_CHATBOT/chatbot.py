import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt')
nltk.download('stopwords')

questions = [
    "What is Artificial Intelligence?",
    "What does AI stand for?",
    "How does AI work?",
    "Where is AI used?",
    "What is Machine Learning?",
    "What is Deep Learning?",
    "What is a neural network?",
    "What is Generative AI?",
    "What is ChatGPT?",
    "Who developed ChatGPT?",
    "Can AI think like humans?",
    "Can AI replace humans?",
    "What are the advantages of AI?",
    "What are the disadvantages of AI?",
    "What is Natural Language Processing?",
    "What is Computer Vision?",
    "What is a chatbot?",
    "Is ChatGPT a chatbot?",
    "What is supervised learning?",
    "What is unsupervised learning?",
    "What is reinforcement learning?",
    "What is data in AI?",
    "Why is data important for AI?",
    "Can AI make mistakes?",
    "Is AI dangerous?",
    "What is the future of AI?",
    "Can AI create images?",
    "Can AI write code?",
    "What skills are needed to learn AI?",
    "Who is known as the father of AI?"
]

answers = [
    "Artificial Intelligence is a field of computer science that enables machines to perform tasks that normally require human intelligence.",
    "AI stands for Artificial Intelligence.",
    "AI works by using algorithms and data to learn patterns and make decisions.",
    "AI is used in healthcare, education, finance, transportation, and many other industries.",
    "Machine Learning is a branch of AI that allows computers to learn from data without being explicitly programmed.",
    "Deep Learning is a subset of Machine Learning that uses neural networks to process large amounts of data.",
    "A neural network is a system inspired by the human brain that helps computers recognize patterns and make predictions.",
    "Generative AI creates new content such as text, images, audio, or videos based on learned patterns.",
    "ChatGPT is an AI chatbot that can understand and generate human-like text responses.",
    "ChatGPT was developed by OpenAI.",
    "AI can perform certain tasks intelligently, but it does not think or understand exactly like humans.",
    "AI can automate some tasks, but many jobs still require human creativity, judgment, and emotions.",
    "AI can improve efficiency, reduce errors, and automate repetitive tasks.",
    "AI can be expensive, may produce incorrect results, and can raise privacy concerns.",
    "Natural Language Processing is a branch of AI that helps computers understand and process human language.",
    "Computer Vision enables computers to interpret and analyze images and videos.",
    "A chatbot is a software application that interacts with users through text or voice conversations.",
    "Yes, ChatGPT is an AI-powered chatbot.",
    "Supervised learning is a Machine Learning method that learns from labeled data.",
    "Unsupervised learning is a Machine Learning method that finds patterns in unlabeled data.",
    "Reinforcement learning is a method where an AI agent learns through rewards and penalties.",
    "Data is the information used to train and improve AI systems.",
    "AI systems learn from data, so high-quality data improves performance and accuracy.",
    "Yes, AI can make mistakes if the data is incomplete, biased, or incorrect.",
    "AI can pose risks if used irresponsibly, but it can also provide many benefits when properly managed.",
    "The future of AI includes more advanced automation, smarter systems, and new innovations across industries.",
    "Yes, many AI systems can generate images from text descriptions.",
    "Yes, AI tools can assist with writing, explaining, and debugging code.",
    "Programming, mathematics, statistics, and problem-solving skills are useful for learning AI.",
    "John McCarthy is often called the father of Artificial Intelligence."
]

print("=============Artificial Intelligence===============")

stop_words = set(stopwords.words('english'))

def preprocess(text):
    text = text.lower()

    words = word_tokenize(text)

    filtered_words = []

    for word in words:
        if word.isalnum() and word not in stop_words:
            filtered_words.append(word)

    return " ".join(filtered_words)

# Preprocess FAQ Questions
clean_questions = []

for question in questions:
    clean_questions.append(preprocess(question))

# TF-IDF Vectorization
vectorizer = TfidfVectorizer()

tfidf_matrix = vectorizer.fit_transform(clean_questions)

print("===== AI FAQ Chatbot =====")
print("Type 'exit' to quit.\n")

while True:

    user_question = input("You: ")

    if user_question.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    clean_user_question = preprocess(user_question)

    user_vector = vectorizer.transform([clean_user_question])

    scores = cosine_similarity(user_vector, tfidf_matrix)

    best_index = scores.argmax()

    best_score = scores[0][best_index]

    print("Similarity Score:", round(best_score, 2))

    if best_score < 0.30:
        print("Chatbot: Sorry, I don't understand your question.\n")
    else:
        print("Chatbot:", answers[best_index], "\n")