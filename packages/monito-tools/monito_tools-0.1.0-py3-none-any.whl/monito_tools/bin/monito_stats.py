"""Monito tool for printing general stats"""

from datetime import datetime, timedelta

from rich import print
from rich.panel import Panel
from rich.pretty import Pretty
from rich.table import Table
from rich.text import Text

from monito_tools import init_mongodb, logging_set_up, timer_start, timer_stop


def get_pretty_article(article: dict):
    output_str = Text()
    output_str.append(f"{article['title']:<120}", style="bold")
    output_str.append(f"   {article['outlet']}")
    output_str.append("\n")
    output_str.append(
        f"{article['published']} (saved: {article['saved']} | {article['download_hostname']})\n", style="dim"
    )

    return output_str


class PrettyArticleShort(Pretty):
    def __init__(self):
        super().__init__(self)


if __name__ == "__main__":
    db_articles = init_mongodb()
    logging_set_up()

    timer_start("stats")
    proj = {"title": True, "url": True, "published": True, "saved": True, "outlet": True, "download_hostname": True}

    now = datetime.now()
    now_24h = now - timedelta(seconds=86400)
    now_1w = now - timedelta(days=7)

    cursor = db_articles.find({}, proj, sort=[("published", -1)]).limit(1)
    last_published = list(cursor)[0]

    cursor = db_articles.find({}, proj, sort=[("saved_iso", -1)]).limit(1)
    last_saved = list(cursor)[0]

    general_stats = Table("key", "value", title="General Statistics", width=50)

    general_stats.add_row("total articles", str(db_articles.estimated_document_count()))
    general_stats.add_row("last 24h", str(db_articles.count_documents({"published": {"$gte": now_24h.isoformat()}})))
    general_stats.add_row("last week", str(db_articles.count_documents({"published": {"$gte": now_1w.isoformat()}})))
    print(general_stats)

    print(Panel(get_pretty_article(last_published), title="last published", title_align="left"))
    print(Panel(get_pretty_article(last_saved), title="last saved", title_align="left"))
    timer_stop("stats")
