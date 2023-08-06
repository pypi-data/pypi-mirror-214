import json
import os
import pickle
import sys
import warnings
from datetime import datetime
from typing import Dict, List, Optional, Set, Tuple

from tqdm import tqdm

warnings.filterwarnings("ignore")

import gensim
import nltk
import openai
import pymongo
import spacy
from gensim.corpora import Dictionary
from gensim.models import HdpModel
from pymongo import MongoClient

from monito_tools import general_config, init_mongodb, init_nlp, load_general_config, log, preprocess

MODEL = None
INSTRUCTIONS = None
DEBUG = True


def init_openai():
    global MODEL, INSTRUCTIONS

    openai_api_key: Optional[str] = os.getenv("OPENAI_API_KEY")

    if openai_api_key is None:
        """
        Try reading from file
        """
        openai_filename = ".openai_api_key"
        log.info(f"Attempting to read OpenAI Key from {openai_filename} ...")
        try:
            with open(openai_filename, "r") as api_file:
                openai_api_key = api_file.read()[:-1]
        except FileNotFoundError as FNFE:
            log.warning(f"OpenAI Key must be provided at {openai_filename} if you want to use the topics feature.")
            # raise FNFE
        else:
            log.info(f"Successfully read OpenAI Key from {openai_filename}.")

    openai.api_key = openai_api_key

    MODEL = "gpt-3.5-turbo"
    # MODEL = "gpt-4"

    INSTRUCTIONS = [
        {
            "role": "system",
            "content": "Usted es TopicGPT, una IA que genera un título corto para un tema compuesto por varias palabras.",
        },
        {
            "role": "system",
            "content": "Las palabras son devueltas por un modelo de Proceso Dirichlet Jerárquico.",
        },
        {
            "role": "system",
            "content": "Los títulos deben ser de una sola palabra o sustantivo compuesto. Sea lo más breve posible.",
        },
        {
            "role": "system",
            "content": "Encuentre la mejor palabra que se relacione con todas las palabras clave dadas.",
        },
        {
            "role": "system",
            "content": "Nunca debe emitir más de una palabra o sustantivo compuesto.",
        },
    ]


def get_topic_title(ps_and_ws: List[Tuple[float, str]]) -> str:
    """
    Use GPT to get topic title
    :param ps_and_ws: The words and associated probabilities of one topic returned by hdp_pipeline
    """

    init_openai()

    words = " ".join([w for (p, w) in ps_and_ws])

    input_ = {"role": "user", "content": words}

    try:
        response = openai.ChatCompletion.create(
            model=MODEL,
            messages=INSTRUCTIONS + [input_],
        )

        response = response["choices"][0]["message"]["content"]

        response = response.replace(".", "")
        response = response.replace("'", "")
        response = response.replace('"', "")

        # get last word of response
        response = response.split(" ")[-1]
    except openai.error.RateLimitError:
        response = ""

    return response


def remove_common_words(corpus: List[List[str]], remove_fraction=0.1):
    """
    Remove most frequent words (across documents)
    Does not double count words in the same doc
    :param corpus: List of List of tokens; output of preprocess
    """

    dictionary: Dict[str, int] = {}  # holds wordcounts
    unique_tokens = []

    for doc in corpus:
        seen_in_this_doc: Set[str] = set()
        for token in doc:
            if token not in seen_in_this_doc:
                seen_in_this_doc.add(token)
                if token not in dictionary:
                    dictionary[token] = 1
                    unique_tokens.append(token)
                else:
                    dictionary[token] += 1

    sorted_tokens = sorted(unique_tokens, key=lambda t: dictionary[t], reverse=True)
    remove_n = int(remove_fraction * len(dictionary))
    keep_tokens = set(sorted_tokens[remove_n:])

    cleaned_corpus = []
    for doc in corpus:
        cleaned_corpus.append([])
        for token in doc:
            if token in keep_tokens:
                cleaned_corpus[:-1].append(token)

    return cleaned_corpus


def do_hdp(texts: List[List[str]], **kwargs) -> gensim.models.hdpmodel.HdpModel:
    """
    Build a HDP Model using gensim.
    :param texts: Corpus, i.e. list of list of strings.
    :return hdp_model: The HDP Model
    """
    dictionary = Dictionary(texts)
    corpus = [dictionary.doc2bow(doc) for doc in texts]

    hdp_model = HdpModel(corpus, dictionary, **kwargs)
    return hdp_model


def hdp_pipeline(
    cursor: pymongo.cursor.Cursor,
    num_topics: int = 10,
    num_words: int = 10,
    output_file: Optional[str] = None,
    remove_fraction: float = 0.1,
    **kwargs,
) -> List[Tuple[int, List[Tuple[float, str]]]]:
    """
    Build Topic Model (using gensim's Hierarchical Dirichlet Process)
    from a mongo cursor of a monito article collection
    Example usage:
    >>> from monito import general_config, init_mongodb, load_general_config
    >>> from monito import hdp_pipeline
    >>> load_general_config("monito_config.toml")
    >>> db = init_mongodb()
    >>> cursor = db.find() # add criteria here
    >>> topics = hdp_pipeline(cursor)
    :param cursor: the excerpt of the monito database to analyze
    :param num_topics: the number of most important topics to output
    :param num_words: the number of most important words per topic to output
    :param output_file: if given, path where to save the hdp model
    :param kwargs: keyword arguments of gensim.models.HdpModel
    :return topics: List of topics, numbered and for each a list of words with probability
    """

    nlp = init_nlp()

    # lang_model = general_config["lang_model"]
    # nlp = spacy.load(lang_model)

    corpus = []
    for i, c in tqdm(enumerate(cursor), desc="Preprocessing articles"):
        if DEBUG and i > 100:
            break
        preprocessed = preprocess(nlp, c["title"] + "\n" + c["subtitle"] + "\n" + c["text"])
        corpus.append(preprocessed)

    cleaned_corpus = remove_common_words(corpus, remove_fraction=remove_fraction)

    hdp_model = do_hdp(corpus, **kwargs)

    # print(f"HDP Model methods:")
    # print(dir(hdp_model))

    numbered_topics = hdp_model.print_topics(num_topics, num_words)

    topics = get_topics(numbered_topics)

    if output_file is not None:
        hdp_model.save(output_file)

    return topics


def get_topics(numbered_topics):
    """
    Post process the output of gensim.models.HdpModel.print_topics
    """
    topics = []
    for i, topical in numbered_topics:
        probs_and_words = topical.split(" + ")
        ps_and_ws = []
        for p_w in probs_and_words:
            star = p_w.find("*")
            prob = float(p_w[:star])
            word = p_w[star + 1 :]
            ps_and_ws.append((prob, word))

        topics.append((i, ps_and_ws))
    return topics


def run():
    log_msgs = load_general_config("monito_config.toml")

    # init data base
    articles_db = init_mongodb()

    start = "2023-04-03"
    end = "2023-04-04"

    num_topics = 20
    num_words = 10

    # make corpus
    output_file = "data/topic_model.gensim"

    cursor = articles_db.find({"published": {"$gte": start, "$lte": end}})

    if not os.path.isfile(output_file):
        topics = hdp_pipeline(
            cursor=cursor,
            num_topics=num_topics,
            num_words=num_words,
            output_file=output_file,
        )
    else:
        hdp_model = HdpModel.load(output_file)
        topics = get_topics(hdp_model.print_topics(num_topics, num_words))

    for topic in topics:
        print()
        print(topic)

    # top_p = max([max([p for (p, w) in topic]) for i, topic in topics])


if __name__ == "__main__":
    run()
