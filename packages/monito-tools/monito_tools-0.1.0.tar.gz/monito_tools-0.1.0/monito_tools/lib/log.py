"""Tools for logging and text output
"""

import functools
import inspect
import logging
from datetime import datetime
from time import perf_counter

from rich.box import DOUBLE_EDGE
from rich.console import Console
from rich.logging import RichHandler
from rich.panel import Panel
from rich.text import Text
from rich.traceback import install

console = Console(record=True)

install(show_locals=True)

# from rich.table import Table
# from rich.highlighter import RegexHighlighter, Highlighter
# from rich.theme import Theme

# class IsoformatDateHighlighter(RegexHighlighter):
#     """Apply style to anything that looks like an email."""

#     base_style = "monito."
#     highlights = [r"?P<isodate>config"]
#     # highlights = [r'^(?P<isodate>-?(?:[1-9][0-9]*)?[0-9]{4})-(1[0-2]|0[1-9])-(3[01]|0[1-9]|[12][0-9])'
#           'T(2[0-3]|[01][0-9]):([0-5][0-9]):([0-5][0-9])(\.[0-9]+)?(Z|[+-](?:2[0-3]|[01][0-9]):[0-5][0-9])?$']

# class RainbowHighlighter(Highlighter):
#     def highlight(self, text):
#         for index in range(len(text)):
#             text.stylize(f"color({randint(16, 255)})", index, index + 1)


# rainbow = RainbowHighlighter()


log = logging.getLogger("rich")

logging.getLogger("selenium").setLevel(logging.WARNING)
logging.getLogger("urllib3.connectionpool").setLevel(logging.ERROR)

_timers = {}


def logging_set_up(log_to_stdout: bool = True):
    from monito_tools import general_config

    if general_config.get("log_to_file_width", 0) > 0:
        console.width = general_config["log_to_file_width"]
    if log_to_stdout:
        general_config["log_to_file"] = ""
        general_config["log_filename"] = "log"
    if general_config["log_to_file"]:
        general_config["log_filename"] = general_config["log_to_file"].replace(
            "$DATE", datetime.today().strftime("%Y-%m-%d_%H-%M-%S")
        )
        try:
            console.file = open(general_config["log_filename"], "w")
        except Exception as e:
            log.error(f"Error opening {general_config['log_filename']} for writing. Falling back to stdout")
            log.error(e)
        else:
            general_config["hide_progress"] = True

    logging.basicConfig(
        level="INFO",
        format="%(message)s",
        datefmt="[%F %T]",
        # handlers=[RichHandler(console=Console(highlighter=IsoformatDateHighlighter(),
        #                                       theme=Theme({"monito.isodate": "bold magenta"})),
        #                       rich_tracebacks=True)],
        handlers=[RichHandler(rich_tracebacks=True, console=console, show_path=False, show_time=False)],
    )


def set_log_level(quiet: bool = False, verbose: bool = False, debug: bool = False) -> None:  # pragma: no cover
    if debug is True:
        log.setLevel(logging.DEBUG)
        log.info("debug mode engaged")
    if verbose is True:
        log.setLevel(logging.INFO)
    if quiet is True:
        log.setLevel(logging.ERROR)


def print_logo(version: str):
    """print the logo and version"""
    console.print(
        Panel(
            Text(f"monito {version}", justify="center", style="bold red"),
            box=DOUBLE_EDGE,
            highlight=True,
        )
    )


def profile(func):
    """profiling and logging decorator"""
    stk = inspect.stack()[1]
    mod = inspect.getmodulename(stk.filename)

    # print(mod)
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        t0 = perf_counter()
        log.debug(f"Entering {mod}.{func.__name__}")
        ret = func(*args, **kwargs)
        log.info(f"Exiting {mod}.{func.__name__}; {perf_counter() - t0:.2f} s")
        return ret

    return wrapper


def debug(func):
    """Print the function signature and return value"""

    @functools.wraps(func)
    def wrapper_debug(*args, **kwargs):
        args_repr = [repr(a) for a in args]
        kwargs_repr = [f"{k}={v!r}" for k, v in kwargs.items()]
        signature = ", ".join(args_repr + kwargs_repr)
        log.debug(f"Calling {func.__name__}({signature})")
        value = func(*args, **kwargs)
        log.debug(f"{func.__name__!r} returned {value!r}")
        return value

    return wrapper_debug


def timer_start(name: str = "default"):
    """start a named timer"""
    _timers[name] = perf_counter()


def timer_stop(name: str = "default"):
    """print the time of a named timer"""
    if name not in _timers:
        log.warning(f"timer {name} has not bee started")
    log.info(f"timer '{name}': {perf_counter() - _timers[name]:.3f} s")
