"""Tools for saving articles to a database"""

import os
from datetime import datetime, timedelta
from typing import Optional

import pandas as pd
from pymongo import DESCENDING, MongoClient
from pymongo.errors import ServerSelectionTimeoutError

from monito_tools import general_config, log, profile

_DB = None

columns = [
    "outlet",
    "url",
    "title",
    "subtitle",
    "text",
    "published",
    "published_iso",
    "saved",
    "saved_iso",
    "authors",
    "bag_of_words",
    "category",
]
articles_cache = None
last_update_articles_cache = None


@profile
def get_articles_cache(n_articles: int = 20000, dt: Optional[timedelta] = timedelta(seconds=60)) -> pd.DataFrame:
    """fill the global variable articles_cache with the last n articles"""

    global articles_cache, last_update_articles_cache
    if articles_cache is not None and dt is not None and last_update_articles_cache > datetime.now() - dt:
        return articles_cache

    articles_db = init_mongodb()

    if articles_cache is None:
        print("hier?")
        cursor = articles_db.find().sort("published", DESCENDING).limit(n_articles)
        print("dazwischen")
        df = pd.DataFrame(list(cursor), columns=columns)[columns]
        print("hä?")
        articles_cache = df
        print("echt?")
    else:
        print("before")
        cursor = articles_db.find({"saved_iso": {"$gt": last_update_articles_cache}})
        df = pd.DataFrame(list(cursor), columns=columns)[columns]
        articles_cache = pd.concat([df, articles_cache]).sort_values("published")
        print("after")

    last_update_articles_cache = datetime.now()

    first_date = df.loc[len(df) - 1, "published"]
    last_date = df.loc[0, "published"]
    log.debug(f"cached articles from {first_date} to {last_date}")

    print(df.loc[:5][["title", "published", "authors"]])
    print(df.loc[len(df) - 5 :][["title", "published", "authors"]])
    return df


def init_mongodb():
    """initialise the mongodb"""
    global _DB

    # log.debug("Getting database handle")
    if _DB is not None:
        return _DB

    # patch_all()

    if "MONITO_DB_URI" in os.environ:
        db_uri = os.environ["MONITO_DB_URI"]
        log.info("Found environment variable MONITO_DB_URI")
    else:
        db_uri = general_config["db"]
        log.info("Using db from general config")

    try:
        client = MongoClient(db_uri)
        database = client["monite"]
        articles_db = database["articles"]
    except ServerSelectionTimeoutError as e:
        log.error(f"ServerSelectionTimeoutError:\n{str(e)}")

    _DB = articles_db
    return articles_db


@profile
def save_article_to_mongodb(article_dict, config, articles_db, i: int = 0, n: int = 0, overwrite: bool = False) -> bool:
    """save an article to mongodb"""

    if art := articles_db.find_one(
        {
            "$and": [
                {"published": article_dict["published"]},
                {"outlet": article_dict["outlet"]},
                {"title": article_dict["title"]},
            ]
        }
    ):
        if overwrite:
            log.warning("The article already exists in the data base. Overwriting.\n\t" f"{art['url']}")
            articles_db.update_one({"_id": art["_id"]}, {"$set": article_dict})
            return True
        log.info("The article already exists in the data base. Not overwriting.\n\t" f"{art['url']}")
        return False

    try:
        articles_db.insert_one(article_dict)
        log.info(f"published: {article_dict['published']}")
        return True
    except Exception as e:
        log.error("Exception occurred during db insert: ")
        log.error(str(e))
        return False


# def get_urls_in_db(config: dict, articles_db) -> list:
#    """get urls that have already been processed"""
#    return articles_db.distinct("url")

# urls_in_db = []
# with open_fs(config["output_directory"]) as articles_fs:
#     urls_in_db = [
#         json.load(articles_fs.open(path))["url"]
#         for path in articles_fs.walk.files(filter=["*.json"])
#     ]
# return urls_in_db
