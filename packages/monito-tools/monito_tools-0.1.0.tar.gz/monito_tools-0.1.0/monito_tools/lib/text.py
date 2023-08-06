"""Tools for accessing text metrics, sanitize text etc.
"""

import os
import re
import unicodedata
from datetime import datetime, timedelta
from glob import glob
from typing import List
from urllib.parse import quote, quote_plus, urlsplit, urlunsplit
from zoneinfo import ZoneInfo

import numpy as np
import spacy
from spacy_syllables import SpacySyllables  # noqa: ignore

from monito_tools import general_config, log


def preprocess(nlp, text: str) -> List[str]:
    """
    preprocess text using spacy
    """

    text: spacy.tokens.doc.Doc = nlp(text)
    bow, _, _, _ = get_bag_of_words(text)
    bow = [replace_accented_letters(tok) for tok in bow]

    return bow


def med(str1, str2):
    """minimum edit distance."""
    n = len(str1)
    m = len(str2)

    matrix = [[i + j for j in range(m + 1)] for i in range(n + 1)]

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            if str1[i - 1] == str2[j - 1]:
                d = 0
            else:
                d = 1

            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + d)

    distance_score = matrix[n][m]

    return distance_score


def url_fix(s: str, encoding: str = "utf-8", remove_fragment: bool = True, remove_query: bool = True) -> str:
    r"""
    Inspired by https://github.com/pallets/werkzeug/blob/main/src/werkzeug/urls.py

    Sometimes you get an URL by a user that just isn't a real URL because
    it contains unsafe characters like ' ' and so on. This function can fix
    some of the problems in a similar way browsers handle data entered by the
    user:
    >>> url_fix('http://de.wikipedia.org/wiki/Elf (Begriffskl\xe4rung)')
    'http://de.wikipedia.org/wiki/Elf%20(Begriffskl%C3%A4rung)'
    :param s: the string with the URL to fix.
    :param encoding: The target encoding for the URL if the url was given
        as a string.
    :param remove_fragment: whether to remove the fragment of the url (the part after '#')
    :return: the fixed urls as a str
    """

    # First step is to switch to text processing and to convert
    # backslashes (which are invalid in URLs anyways) to slashes.  This is
    # consistent with what Chrome does.
    s = str(s).replace("\\", "/")

    url = urlsplit(s)
    path = quote(url.path, safe="/%+$!*'(),", encoding=encoding)
    if remove_fragment:
        fragment = ""
    else:
        fragment = quote_plus(url.fragment, safe=":&%=+$!*'(),", encoding=encoding)

    if remove_query:
        query = ""
    else:
        query = quote_plus(url.query, safe=":&%=+$!*'(),", encoding=encoding)

    return urlunsplit((url.scheme, url.netloc, path, query, fragment))


def replace_quotes(s: str) -> str:
    """replace dificult characters"""
    return s.translate(str.maketrans("‘’“”", "''\"\""))


def replace_accented_letters(s: str) -> str:
    """replace accented letters with their ascii counterpart"""
    return unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode("utf-8")


def init_nlp():
    """Initialize the NLP pipeline"""

    # check whether any language model is installed
    if len(spacy.util.get_installed_models()) == 0:
        log.error("No language model found. Install with ´python -m spacy download es_core_news_sm´")
        raise RuntimeError

    # find closest match to model in cfg
    # via minimum edit distance to installed models
    m_cfg = general_config["lang_model"]

    model_match = sorted([(m, med(m_cfg, m)) for m in spacy.util.get_installed_models()], key=lambda t: t[1])[0][0]

    log.info(f"Chosing {model_match}")
    if model_match[:2] != general_config["lang_model"][:2]:
        log.warning(f"language mismatch: {model_match} != {general_config['lang_model']}1")
    _nlp = spacy.load(model_match)
    language = general_config["lang_model"][:2]
    _nlp.add_pipe("syllables", after="morphologizer", config={"lang": language})

    return _nlp


def init_language_tool(locale):
    """Initializs Languagetool"""
    import language_tool_python

    language_tool = language_tool_python.LanguageTool(locale[:2])
    return language_tool


def get_bag_of_words(doc: spacy.tokens.doc.Doc) -> tuple[set]:
    """generate a bag of normalized words from text"""

    # without_stopwords = {word.text for word in doc if word.is_alpha and not word.is_stop}
    normalized_bow = sorted(
        {word.lemma_.lower() for word in doc if word.is_alpha and not word.is_stop and len(word) > 1}
    )
    places = sorted({word.text.title().strip() for word in doc.ents if word.label_ in ["GPE", "LOC"]})
    people = sorted({word.text.title().strip() for word in doc.ents if word.label_ == "PER"})
    orgs = sorted({word.text.strip() for word in doc.ents if word.label_ == "ORG"})

    # add GPEs from files
    gpes_from_files = []
    for f in glob(os.path.join(general_config["gpe_directory"], "gpe_*.txt")):
        with open(f) as fp:
            gpes_from_files += [line.strip() for line in fp.readlines()]

    gpes_from_files = set(gpes_from_files)

    found_gpes = [word.title() for word in normalized_bow if word.lower() in map(str.lower, gpes_from_files)]
    places = sorted(set(places + found_gpes))

    # fix some frequent errors
    if "Mich." in people:
        people.remove("Mich.")
        places = sorted(set(places + ["Michoacán"]))

    if "MORELIA" in orgs:
        orgs.remove("MORELIA")
        places = sorted(set(places + ["Morelia"]))

    orgs_dict = {
        "Instituto Mexicano del Seguro Social": "IMSS",
        "Secretaría de Seguridad Pública": "SSP",
        "Universidad Michoacana de San Nicolás de Hidalgo": "UMSNH",
    }

    for k, v in orgs_dict.items():
        if k in orgs:
            orgs.remove(k)
            places = sorted(set(places + [v]))

    for p in people.copy():
        if "\n" in p:
            people.remove(p)
            people = sorted(set(people + [p.split("\n")[0]]))

    for p1 in people.copy():
        for p2 in people.copy():
            if p1 != p2 and (p2.startswith(p1) or p2.endswith(p1)) and p1 in people:
                people.remove(p1)

    for p in places.copy():
        if "\n" in p:
            places.remove(p)
            places = sorted(set(places + [p.split("\n")[0]]))

    # print(text)
    # print(without_stopwords)
    # print(normalized_bow)
    # print(places)
    # print(people)
    # for ent in doc.ents:
    #     print(ent.text, ent.label_)
    # sys.exit(999)

    return normalized_bow, places, people, orgs


def process_article_text(
    article_dict: dict,
    config: dict,
    nlp,
    language_tool=None,
    i: int = None,
) -> None:
    """analyse the article text and add the information to the article dict"""

    if len(article_dict["text"]) < 100:
        log.warning(f"{i} found very short text")
        return

    for field in ["text", "subtitle", "title"]:
        if article_dict[field]:
            article_dict[field] = re.sub("\xa0", " ", article_dict[field])
            article_dict[field] = re.sub(r" +", " ", article_dict[field])
            article_dict[field] = re.sub(r"\n\n+", "\n", article_dict[field])
            article_dict[field] = re.sub(r"( *\n *)+", "\n", article_dict[field])

    text_doc = nlp(article_dict["text"])

    # get bag of words
    (
        article_dict["bag_of_words"],
        article_dict["places"],
        article_dict["people"],
        article_dict["orgs"],
    ) = get_bag_of_words(text_doc)

    # get legibility and stats
    article_dict["legibility"] = legibility_es(text_doc)

    article_dict["stats"] = {}
    article_dict["stats"]["n_characters"] = len(article_dict["text"])
    article_dict["stats"]["n_letters"] = count_letters(text_doc)
    article_dict["stats"]["n_syllables"] = count_syllables(text_doc)
    article_dict["stats"]["n_words"] = count_words(text_doc)
    article_dict["stats"]["n_sentences"] = count_sentences(text_doc)
    article_dict["stats"]["n_bag_of_words"] = len(article_dict["bag_of_words"])

    if language_tool is not None:
        matches = language_tool.check(article_dict["text"])
        article_dict["n_errors"] = len(matches)
    else:
        article_dict["n_errors"] = None

    sanitize_article(article_dict)


def sanitize_article(article_dict: dict) -> None:
    """sanitize (i.e., normalize) the keywords, people, categories, etc."""

    # create missing fields
    if "category" not in article_dict:
        article_dict["category"] = []
    if "places" not in article_dict:
        article_dict["places"] = []
    if "authors" not in article_dict:
        article_dict["authors"] = []
    if "keywords" not in article_dict:
        article_dict["keywords"] = []
    if "orgs" not in article_dict:
        article_dict["orgs"] = []
    if "people" not in article_dict:
        article_dict["people"] = []

    # sanitize dates
    # if article_dict["published"].endswith("Z"):
    #     article_dict["published"] = article_dict["published"][:-1]

    tz_correction = timedelta(0)
    if article_dict["outlet"] in ["urbistv", "ultranoticias", "Ecos de La Meseta", "Acueducto Online"]:
        tz_correction = timedelta(hours=-6)

    if article_dict["url"].startswith("https://www.debate.com.mx/policiacas"):
        if not re.search(r"[+-]0\d:00$", article_dict["published"]):
            article_dict["published"] = article_dict["published"] + "+00:00"

    article_dict["published"] = (
        (datetime.fromtimestamp(datetime.fromisoformat(article_dict["published"]).timestamp()) + tz_correction)
        .astimezone(tz=ZoneInfo("America/Mexico_City"))
        .isoformat(timespec="minutes")
    )

    # sanitize authors
    article_dict["authors"] = [key.strip() for key in article_dict["authors"]]
    article_dict["authors"] = [key for key in article_dict["authors"] if len(key) < 100]

    if "Europa Press, Afp" in article_dict["authors"]:
        article_dict["authors"].remove("Europa Press, Afp")
        article_dict["authors"].append("Europa Press")
        article_dict["authors"].append("AFP")

    for key in ["Afp", "AFp", "afp"]:
        if key in article_dict["authors"]:
            article_dict["authors"].remove(key)
            article_dict["authors"] = sorted(set(article_dict["authors"] + ["AFP"]))

    # sanitize categories
    article_dict["category"] = [key.lower() for key in article_dict["category"]]

    # sanitize keywords
    if len(article_dict["keywords"]) == 1 and "," in article_dict["keywords"]:
        article_dict["keywords"] = [key.strip() for key in article_dict["keywords"][0].split(",")]
    article_dict["keywords"] = [key.lower() for key in article_dict["keywords"]]
    for key in ["amlo-presidente", "lopez-obrador", "noticias-amlo"]:
        if key in article_dict["keywords"]:
            article_dict["keywords"].remove(key)
            article_dict["keywords"] = sorted(set(article_dict["keywords"] + ["amlo"]))
    for key in ["corona", "coronavirus", "covid 19"]:
        if key in article_dict["keywords"]:
            article_dict["keywords"].remove(key)
            article_dict["keywords"] = sorted(set(article_dict["keywords"] + ["covid-19"]))
    for key in ["Covid-19", "COVID-19", "COVID-19.", "Covid", "COVID"]:
        if key in article_dict["places"]:
            article_dict["places"].remove(key)
            article_dict["keywords"] = sorted(set(article_dict["keywords"] + ["covid-19"]))
        if key in article_dict["people"]:
            article_dict["people"].remove(key)
            article_dict["keywords"] = sorted(set(article_dict["keywords"] + ["covid-19"]))
        if key in article_dict["orgs"]:
            article_dict["orgs"].remove(key)
            article_dict["keywords"] = sorted(set(article_dict["keywords"] + ["covid-19"]))

    # sanitize people
    for key in article_dict["people"].copy():
        if "   " in key:
            article_dict["people"].remove(key)
            article_dict["people"] = sorted(set(article_dict["people"] + [k.strip() for k in key.split("   ")]))

    article_dict["people"] = [key.title() for key in article_dict["people"]]
    article_dict["people"] = [key.strip(".") for key in article_dict["people"]]
    article_dict["people"] = [key.split(":")[0] for key in article_dict["people"]]
    for key in ["Amlo", "López Obrador"]:
        if key in article_dict["people"]:
            article_dict["people"].remove(key)
            article_dict["people"] = sorted(set(article_dict["people"] + ["Andrés Manuel López Obrador"]))
    for key in ["Silvano Aureoles"]:
        if key in article_dict["people"]:
            article_dict["people"].remove(key)
            article_dict["people"] = sorted(set(article_dict["people"] + ["Silvano Aureoles Conejo"]))
    for key in ["Ramírez Bedolla"]:
        if key in article_dict["people"]:
            article_dict["people"].remove(key)
            article_dict["people"] = sorted(set(article_dict["people"] + ["Alfredo Ramírez Bedolla"]))
    for key in ["Recomendamos El Podcast", "Él", "Instagram"]:
        if key in article_dict["people"]:
            article_dict["people"].remove(key)

    # sanitize places
    article_dict["places"] = [key.strip(".") for key in article_dict["places"]]
    for key in ["Mexico"]:
        if key in article_dict["places"]:
            article_dict["places"].remove(key)
            article_dict["places"] = sorted(set(article_dict["places"] + ["México"]))
    for key in ["En Estados Unidos"]:
        if key in article_dict["places"]:
            article_dict["places"].remove(key)
            article_dict["places"] = sorted(set(article_dict["places"] + ["Estados Unidos"]))
    for key in ["Mich", "Michoacana", "Michoacan"]:
        if key in article_dict["places"]:
            article_dict["places"].remove(key)
            article_dict["places"] = sorted(set(article_dict["places"] + ["Michoacán"]))

    for key in ["Escucha El Podcast ⬇️", "Ver", "Changoonga.Com", "Mascota"]:
        if key in article_dict["places"]:
            article_dict["places"].remove(key)

    # sanitize orgs
    article_dict["orgs"] = [key.strip(".-") for key in article_dict["orgs"]]
    for key in ["Michoacán"]:
        if key in article_dict["orgs"]:
            article_dict["orgs"].remove(key)
    for key in ["Morena"]:
        if key in article_dict["people"]:
            article_dict["people"].remove(key)
            article_dict["orgs"] = sorted(set(article_dict["orgs"] + ["Morena"]))

    for long_name, short_name in (
        ("Secretaría de Salud de Michoacán", "SSM"),
        ("Instituto Nacional Electoral", "INE"),
        ("Organización Mundial de la Salud", "OMS"),
        ("Comisión Federal de Electricidad", "CFE"),
        ("Fiscalía General de la República", "FGR"),
        ("Fiscalía General del Estado", "FGE"),
        ("Partido del Trabajo", "PT"),
    ):
        if long_name in article_dict["orgs"]:
            article_dict["orgs"].remove(long_name)
            article_dict["orgs"] = sorted(set(article_dict["orgs"] + [short_name]))


def sanitize_filename(s: str) -> str:
    """replace characters that should not be in a filename"""

    result = s.translate(str.maketrans("áéíóúñÁÉÍÓÚÑü", "aeiounAEIOUNu", ",\"'“”|.;/‘’?¿!¡&#\t\r\b\n"))

    if len(result) > 100:
        print(result)
        while "___" in result:
            result = result.replace("___", "__")

    return result


def count_syllables(doc: spacy.tokens.doc.Doc) -> int:
    """Count syllables in text"""
    # logging.debug(str([(token.text, token._.syllables_count) for token in doc if not token.is_punct]))
    return sum(token._.syllables_count for token in doc if not token.is_punct and token._.syllables_count is not None)


def count_letters(doc: spacy.tokens.doc.Doc) -> int:
    """Count letters in text"""
    return sum(len(word) for word in doc if not word.is_punct)


def count_words(doc: spacy.tokens.doc.Doc) -> int:
    """Count words in text"""
    return len(list(word for word in doc if not word.is_punct))


def count_sentences(doc: spacy.tokens.doc.Doc) -> int:
    """Count sentences in text"""
    return len(list(doc.sents))


def legibility_es(doc: spacy.tokens.doc.Doc) -> dict:
    """Get legibility measures for Spanish text"""
    result = {}

    n_letters = count_letters(doc)
    n_syllables = count_syllables(doc)
    n_words = count_words(doc)
    n_sentences = count_sentences(doc)
    result["FH"] = result["Fernández Huerta"] = round(
        206.84 - 60 * n_syllables / n_words - 102 * n_sentences / n_words, 1
    )
    result["SP"] = result["Szigriszt-Pazos"] = round(206.835 - 62.3 * n_syllables / n_words - n_words / n_sentences, 1)
    letters_per_word = [len(word) for word in doc if not word.is_punct]
    result["mu"] = round(
        n_words / (n_words - 1) * (n_letters / n_words) / np.var(letters_per_word) * 100,
        1,
    )

    return result


if __name__ == "__main__":
    nlp = spacy.load("es_core_news_lg")
    nlp.add_pipe("syllables", after="morphologizer", config={"lang": "es"})

    assert count_letters(nlp("Esto es un texto.")) == 13
    assert count_syllables(nlp("Esto es un texto.")) == 6
    assert count_words(nlp("Esto es un texto.")) == 4
    assert count_sentences(nlp("Esto es un texto. Y esto es otro.")) == 2

    print(legibility_es(nlp("Esto es un texto muy simple.")))

    long_text = nlp(
        "Tomando en cuenta la complejidad del vocabulario,"
        " esto se podría considerar un texto más complicado y menos legible."
    )

    print(
        count_letters(long_text),
        count_syllables(long_text),
        count_words(long_text),
        count_sentences(long_text),
    )
    print(legibility_es(nlp(long_text)))
