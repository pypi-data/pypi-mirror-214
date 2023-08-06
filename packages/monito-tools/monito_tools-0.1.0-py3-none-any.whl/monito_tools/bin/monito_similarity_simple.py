"""Find articles similar to a given text file
"""
import pickle
from datetime import datetime

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from monito_tools import init_mongodb, load_general_config

# client = MongoClient("mongodb://localhost:27017")
# database = client["monite"]
# articles_db = database["articles"]

# load the general configuration
log_msgs = load_general_config("monito_config.toml")

# init data base
articles_db = init_mongodb()


start = "2023-04-01"
end = "2023-04-08"
vectorizer_file = "data/vectorizer_2023-01-06_35087.pk"
vectorizer = None
sensitivity = 0.99

create_vectorizer = False
compare = True

if create_vectorizer:
    print(articles_db)
    cursor = articles_db.find({"published": {"$gte": "2023-03", "$lte": "2023-04"}})
    corpus = [c["title"] + "\n" + c["text"] for c in cursor]

    # print(corpus[:2])

    vectorizer = TfidfVectorizer()  # TODO: add options stop_words, ngram_range, max_features
    vectorizer.fit(corpus)
    filename = f"vectorizer_{datetime.today().strftime('%Y-%m-%d')}_{len(corpus)}.pk"
    with open(filename, "wb") as f:
        pickle.dump(vectorizer, f)

        print(f"{datetime.today().strftime('[%Y-%m-%d %H:%M:%S]')} saved the vectorizer as {filename}")
        vectorizer_file = filename
    print(f"Saved vectorizer as {filename}.")
    exit()

if compare:
    # print("article:")
    # article = sys.stdin.read()

    published = []
    outlets = []
    titles = []
    texts = []
    urls = []

    cursor = articles_db.find({"published": {"$gte": start, "$lte": end}})

    for i, c in enumerate(cursor):
        # print(i, "\t", c["published"], c["title"])

        published.append(c["published"])
        outlets.append(c["outlet"])
        titles.append(c["title"])
        texts.append(c["text"])
        urls.append(c["url"])

    if vectorizer is None:
        with open(vectorizer_file, "rb") as f:
            vectorizer = pickle.load(f)

    matrix_text = vectorizer.transform(texts)
    sim_matrix = cosine_similarity(matrix_text, matrix_text)

    print(sim_matrix)

    count = len(texts)
    count_groups = 0
    already_processed = set()
    for i in range(count):
        printed_first = False
        if i in already_processed:
            continue
        for j in range(count):
            if i == j:
                continue
            if j in already_processed:
                continue
            if sim_matrix[i][j] > sensitivity:
                if not printed_first:
                    print(f"\n{i}\t{outlets[i]:30} {titles[i]} {urls[i]}")
                    count_groups += 1
                    printed_first = True
                # print(round(sim_matrix[i][j], 3), i, j)
                print(f"{j}\t{outlets[j]:30} {titles[j]} {urls[j]}")
                already_processed.add(j)
        already_processed.add(i)

    print("\n", count_groups)
