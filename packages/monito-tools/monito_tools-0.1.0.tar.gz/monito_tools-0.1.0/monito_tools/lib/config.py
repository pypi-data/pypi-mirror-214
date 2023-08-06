"""The general configuration"""

import os

import toml

general_config = {
    "_MONITO_DEBUG_MODE": False,
    "_MONITO_QUIET_MODE": False,
}


def load_general_config(args_general_config: str) -> list:
    """load the general configuration"""

    log_msgs = []
    if os.path.isfile(args_general_config):
        log_msgs.append(("DEBUG", f"loading general config file {args_general_config}"))
        # g_config = toml.load(args_general_config)

        try:
            g_config = toml.load(args_general_config)
        except Exception as e:
            log_msgs.append(("ERROR", f"Error loading {args_general_config}:\n{str(e)}"))
            g_config = {
                "log_to_file": "monito_$DATE.log",
                "log_to_file_width": 120,
                "lang_model": "es_core_news_lg",
                "db": "mongodb://localhost:27017",
            }
            general_config.update(g_config)
            return log_msgs
    else:
        g_config = {
            "log_to_file": "monito_$DATE.log",
            "log_to_file_width": 120,
            "lang_model": "es_core_news_lg",
            "db": "mongodb://localhost:27017",
        }
        log_msgs.append(
            (
                "WARNING",
                f"general config file {args_general_config} not found. Falling back to defaults.",
            )
        )

    g_config["hide_progress"] = False

    general_config.update(g_config)

    return log_msgs
