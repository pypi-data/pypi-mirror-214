"""Analysis tools for monito data files"""

__version__ = "0.1.0"

import argparse
import json
import logging
from collections import Counter
from datetime import date, datetime, timedelta
from glob import glob

from fs import open_fs
from fs.path import basename
from rich import box, print

# from rich.color import Color
from rich.columns import Columns

# from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.progress import track
from rich.table import Table
from rich.text import Text

from monito_tools import console, init_mongodb, load_general_config, log, sanitize_article, set_log_level

# from uniplot import plot

logging.basicConfig(
    level="INFO",
    format="%(message)s",
    datefmt="[%F %T]",
    # handlers=[RichHandler(console=Console(highlighter=IsoformatDateHighlighter(),
    #                                       theme=Theme({"monito.isodate": "bold magenta"})),
    #                       rich_tracebacks=True)],
    handlers=[RichHandler(rich_tracebacks=True, console=console, show_path=False, show_time=False)],
)


colors = [
    "yellow",
    "cyan",
    "magenta",
    "green",
    "red",
    "blue",
]

_MONITO_DEBUG_MODE = False
_MONITO_QUIET_MODE = False
_MONITO_VERBOSE_MODE = False


def _parse_arguments(argv=None):
    # parse the command line options
    argparser = argparse.ArgumentParser(
        description="monito_analysis: a tool for analysing news feeds downloaded by monito. "
        "Please have a look at the documentation (https://monito.readthedocs.io/en/latest/) "
        "for further information on how tho use this software.",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    argparser.add_argument(
        "-i",
        "--input-directory",
        type=str,
        nargs="+",
        help="The input directory or directories where the articles are read from. "
        "If absent, the program will connect to mongodb.",
    )
    argparser.add_argument(
        "-o",
        "--output-file",
        type=str,
        default="out.txt",
        help="The output file for results.",
    )
    argparser.add_argument(
        "--outlet",
        type=str,
        nargs="+",
        help="Filter articles by outlets.",
    )
    argparser.add_argument(
        "-s",
        "--save",
        type=str,
        nargs="+",
        help="Which parts of the data to write to the output file.",
    )
    argparser.add_argument(
        "--category",
        type=str,
        nargs="+",
        help="Filter articles by categories.",
    )
    argparser.add_argument(
        "--keyword",
        type=str,
        nargs="+",
        help="Filter articles by keywords.",
    )
    argparser.add_argument(
        "--author",
        type=str,
        nargs="+",
        help="Filter articles by authors.",
    )
    argparser.add_argument(
        "--place",
        type=str,
        nargs="+",
        help="Filter articles by places.",
    )
    argparser.add_argument(
        "--people",
        type=str,
        nargs="+",
        help="Filter articles by people.",
    )
    argparser.add_argument(
        "--org",
        type=str,
        nargs="+",
        help="Filter articles by orgs.",
    )
    argparser.add_argument(
        "--full-text",
        type=str,
        default=None,
        help="Filter articles by full text search.",
    )
    argparser.add_argument(
        "-l",
        "--last",
        type=str,
        metavar="TIME",
        help="Filter articles published since TIME. Specify the TIME in the form n[n...]{h,d,w}, e.g., "
        "'24h', or '1w'",
    )
    argparser.add_argument(
        "-p",
        "--print",
        type=str,
        nargs="+",
        metavar="TOPIC",
        default=["stats"],
        help="Print individual articles. Can be 'stats, 'title', 'text' or 'fulltext'. "
        "'text' and 'fulltext' include 'title'.",
    )
    argparser.add_argument(
        "-q",
        "--quiet",
        action="store_true",
        help="Switch off text output except for error messages. This will overwrite -v.",
    )
    argparser.add_argument("-v", "--verbose", action="store_true", help="More verbose text output")
    argparser.add_argument(
        "-d",
        "--debug",
        action="store_true",
        help="Switch on debug mode. This will show intermediate results and plots, as well as "
        "log a lot of debugging information.",
    )
    argparser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {__version__}",
        help="show the version of this software",
    )
    return argparser.parse_args(argv)


def bar(fraction: float, total: int) -> str:
    """return a string containing a bar of the fraction ([0.0, 1.0])
    of the total width using unicode block characters"""

    blocks = (" ", "▏", "▎", "▍", "▌", "▋", "▊", "▉")
    blocks_to_fill = total * fraction
    residual = (blocks_to_fill - int(blocks_to_fill)) * 8
    result = "█" * int(blocks_to_fill) + blocks[int(residual)]
    return result.strip()


def filter_by_outlet(article_dict: dict, args_outlet: list) -> bool:
    if args_outlet:
        for outlet in args_outlet:
            if outlet.lower() in article_dict["outlet"].lower():
                break
        else:
            return True
    return False


def prefilter_by_date(article_filename: str, args_last: str) -> bool:
    """Filter by the date in the filename, rounded up one day"""

    if args_last:
        last_val = int(args_last[:-1])
        last_unit = args_last[-1]
        if last_unit not in ["h", "d", "w"]:
            log.error("valid units for time differences are 'h', 'd', and 'w'")
        article_date = datetime.fromisoformat(article_filename[:10])

        if last_unit == "h":
            td = timedelta(hours=last_val, days=1)
        elif last_unit == "d":
            td = timedelta(days=last_val + 1)
        elif last_unit == "w":
            td = timedelta(weeks=last_val, days=1)

        if article_date < datetime.now() - td:
            return True

    return False


def get_timedelta_from_last_string(last_str: str) -> timedelta:
    last_val = int(last_str[:-1])
    last_unit = last_str[-1]
    if last_unit not in ["h", "d", "w"]:
        log.error("valid units for time differences are 'h', 'd', and 'w'")
        return

    if last_unit == "h":
        td = timedelta(hours=last_val)
    elif last_unit == "d":
        td = timedelta(days=last_val)
    elif last_unit == "w":
        td = timedelta(weeks=last_val)
    return td


def filter_by_date(article_dict: dict, args_last: str) -> bool:
    if len(article_dict["published"]) == 0:
        log.warning(f"empty field 'published' \n {article_dict}")
        return True

    if args_last:
        article_date = datetime.fromisoformat(article_dict["published"][:16])
        td = get_timedelta_from_last_string(args_last)

        if article_date < datetime.now() - td:
            return True

    return False


def filter_by_category(article_dict: dict, args_category: list):
    if args_category:
        for category in args_category:
            if any(category.lower() in cat.lower() for cat in article_dict["category"]):
                break
        else:
            return True
    return False


def filter_by_keyword(article_dict: dict, args_keyword: list):
    if args_keyword:
        for keyword in args_keyword:
            if any(keyword.lower() in art.lower() for art in article_dict["keywords"]):
                break
        else:
            return True
    return False


def filter_by_author(article_dict: dict, args_author: list):
    if args_author:
        for author in args_author:
            if any(author.lower() in aut.lower() for aut in article_dict["authors"]):
                break
        else:
            return True
    return False


def filter_by_place(article_dict: dict, args_place: list):
    if args_place:
        for place in args_place:
            if any(place.lower() in pl.lower() for pl in article_dict["places"]):
                break
        else:
            return True
    return False


def filter_by_people(article_dict: dict, args_people: list):
    if args_people:
        for person in args_people:
            if any(person.lower() in per.lower() for per in article_dict["people"]):
                break
        else:
            return True
    return False


def filter_by_org(article_dict: dict, args_org: list):
    if args_org:
        for org in args_org:
            if any(org.lower() in o.lower() for o in article_dict["orgs"]):
                break
        else:
            return True
    return False


def filter_by_full_text_search(article_dict: dict, args_full_text: list):
    if args_full_text:
        for text in args_full_text:
            if text.lower() in article_dict["text"].lower():
                break
        else:
            return True
    return False


def display_size(size: int) -> str:
    dir_size_KB = round(size / 1024, 1)
    dir_size_MB = round(dir_size_KB / 1024, 1)
    if dir_size_MB > 1:
        display_size = f"{dir_size_MB} MB"
    else:
        display_size = f"{dir_size_KB} KB"

    return display_size


def run(argv: list = None):
    """the command line tool. Please use the ``--help`` option to get help."""

    global _MONITO_QUIET_MODE
    global _MONITO_DEBUG_MODE
    global _MONITO_VERBOSE_MODE

    # parse the command line options
    args = _parse_arguments(argv)

    # print the logo and version
    if args.quiet is False:  # pragma: no cover
        console.print(
            Panel(
                Text(f"monito_analysis {__version__}", justify="center", style="bold red"),
                box=box.DOUBLE_EDGE,
                highlight=True,
            )
        )

    # set quiet mode
    _MONITO_QUIET_MODE = args.quiet

    # set debug mode
    _MONITO_DEBUG_MODE = args.debug

    # set verbose mode
    _MONITO_VERBOSE_MODE = args.verbose

    # set verbosity level
    set_log_level(args.quiet, args.verbose, args.debug)

    if _MONITO_VERBOSE_MODE or _MONITO_DEBUG_MODE:
        log.info(args)

    files = []
    total_size = 0
    total_n = 0

    if args.input_directory:
        for directory in args.input_directory:
            if _MONITO_VERBOSE_MODE:
                log.info(f"processing directory {directory}")
            files_dir = glob(f"{directory}/*.json")
            if _MONITO_VERBOSE_MODE:
                log.info(f"found {len(files_dir)} files.")

            article_fs = open_fs(directory)
            dir_size = sum(info.size for info in list(article_fs.scandir("/", namespaces=["details"])))
            if _MONITO_VERBOSE_MODE:
                log.info(f"size of files in directory: {display_size(dir_size)}")

            total_size += dir_size
            total_n += len(files_dir)
            files.extend(files_dir)

        log.info(f"total number of files {total_n}")

        log.info(f"size of all files: {display_size(total_size)}")

        log.info("processing articles")

        found_articles = []

        for f in track(files, description="reading article files…", transient=True):
            if prefilter_by_date(basename(f), args.last):
                continue

            try:
                article_dict = json.load(open(f))
            except Exception as e:
                logging.error(f"failed to decode file {f}")
                logging.error(e)
                continue

            # filters
            if filter_by_outlet(article_dict, args.outlet):
                continue
            if filter_by_date(article_dict, args.last):
                continue
            if filter_by_category(article_dict, args.category):
                continue
            if filter_by_keyword(article_dict, args.keyword):
                continue
            if filter_by_author(article_dict, args.author):
                continue
            if filter_by_place(article_dict, args.place):
                continue
            if filter_by_people(article_dict, args.people):
                continue
            if filter_by_org(article_dict, args.org):
                continue
            if filter_by_full_text_search(article_dict, args.full_text):
                continue

            found_articles.append(article_dict)

    else:
        log.info("Connecting to MongoDB.")
        # init data base
        load_general_config("monito_config.toml")
        articles_db = init_mongodb()
        and_arr = []
        if args.outlet:
            and_arr.append({"outlet": {"$in": args.outlet}})
        if args.last:
            td = get_timedelta_from_last_string(args.last)
            start_date = (date.today() - td).isoformat()
            and_arr.append({"published": {"$gte": start_date}})
        if args.full_text:
            and_arr.append({"$text": {"$search": args.full_text}})

        query = {"$and": and_arr}
        found_articles = list(articles_db.find(query))

    # checks and extract data
    data = {
        "outlet": [],
        "authors": [],
        "keywords": [],
        "places": [],
        "people": [],
        "orgs": [],
        "category": [],
        "published": [],
    }

    article_count = 0
    for article_dict in found_articles:
        # sanitize
        sanitize_article(article_dict)

        # checks
        if "saved" in article_dict and article_dict["published"] > article_dict["saved"]:
            log.debug(f"'published' is in the future \n {article_dict}")

        # extract data
        for k in data:
            if isinstance(article_dict[k], list):
                data[k].extend(article_dict[k])
            else:
                data[k].append(article_dict[k])

        article_count += 1

    log.info(f"number of articles: {article_count}")

    if article_count == 0:
        return

    data["weekday"] = []
    data["month"] = []
    data["hour"] = []
    data["monthday"] = []
    # data["week"] = []
    data["date"] = []
    data["datemonth"] = []

    weekdays = [
        "Monday",
        "Tuesday",
        "Wednesday",
        "Thursday",
        "Friday",
        "Saturday",
        "Sunday",
    ]

    earliest_pub = "9"
    latest_pub = "0"
    for pub in data["published"]:
        if pub < earliest_pub:
            earliest_pub = pub
        if pub > latest_pub:
            latest_pub = pub
        pub_dt = datetime.fromisoformat(pub)
        data["weekday"].append(weekdays[pub_dt.weekday()])
        data["month"].append(pub_dt.month)
        data["hour"].append(pub_dt.hour)
        data["monthday"].append(pub_dt.day)
        # data["week"].append(pub_dt.isocalendar().week)
        data["date"].append(pub_dt.date().isoformat())
        data["datemonth"].append(pub_dt.date().isoformat()[:-3])

    data.pop("published")

    logging.info(f"Dates range from {earliest_pub} to {latest_pub}")

    if "stats" in args.print:
        tables = []
        for k, v in data.items():
            t = Table(title=k)
            t.add_column("name", style="green")
            t.add_column("#", style="cyan")
            t.add_column("", style="blue")
            c = Counter(v)
            if k in ["month", "hour", "monthday", "week", "date", "datemonth"]:
                to_be_shown = sorted(c.items())
            elif k == "weekday":
                to_be_shown = [(k, c[k]) for k in weekdays]
            else:
                to_be_shown = c.most_common(30)

            for item in to_be_shown:
                if (
                    k not in ["date", "datemonth"]
                    or (k == "date" and item[0] >= "2021-12")
                    or (k == "datemonth" and item[0] >= "2021")
                ):
                    t.add_row(*map(str, item), bar(item[1] / c.most_common(1)[0][1], 20))

            tables.append(t)

        console.rule("[bold orange1]Statistics[/]", style="white")
        print(Columns(tables))

    if args.print:
        console.rule("[bold orange1]Articles[/]", style="white")
        if "title" in args.print and "text" not in args.print and "fulltext" not in args.print:
            for art in found_articles:
                category = art["category"][0] if art["category"] else None
                print(
                    f'{datetime.fromisoformat(art["published"]).ctime()} | {art["outlet"]} '
                    f'| {category} | {", ".join(art["authors"])}'
                )
                print(art["url"])
                print(f'[bold]{art["title"]}[/]\n')
        if "text" in args.print or "fulltext" in args.print:
            panels = []
            h = None if "fulltext" in args.print else 20
            for art in found_articles:
                text = Text(art["text"], style="default")
                for i, key in enumerate(args.full_text):
                    text.highlight_words([key], colors[i], case_sensitive=False)
                content = Text.assemble(
                    (f'{art["title"]}\n', "bold white"),
                    (f'({art["url"]})\n\n', f'dim link {art["url"]}'),
                    text,
                )
                panels.append(
                    Panel(
                        content,
                        width=100,
                        height=h,
                        padding=1,
                        title=f'{datetime.fromisoformat(art["published"]).ctime()} '
                        f'| {art["outlet"]} | {art["category"][0]} | {", ".join(art["authors"])}',
                    )
                )

            print(Columns(panels))

    if args.save:
        logging.info(f"Saving data {args.save} from {len(found_articles)} articles to {args.output_file}")
        try:
            f = open(args.output_file, "w")
        except Exception as e:
            raise e

        for art in found_articles:
            logging.info(f"{art['published']}\t{art['title']}")
            if "title" in args.save:
                f.write(art["title"] + "\n")
            if "text" in args.save:
                f.write(art["text"] + "\n")
        f.close()


if __name__ == "__main__":
    run()
