from sentweement.commands import helpcmd
from sentweement.commands import model
from sentweement.commands import twitter

__all__ = [ "run_command", "get_commands" ]

VALID_COMMANDS = {
    "help": {
        "help": "Show help",
        "params": "[command]",
        "module": helpcmd.HelpCommand,
    },
    "model-create": {
        "help": "Creates a new learning model",
        "params": "<output model> <input dataset 1> [... <input dataset N>]",
        "module": model.CreateModelCommand,
    },
    "model-update": {
        "help": "Updates an existing learning model",
        "params": "<input model> <input dataset 1> [... <input dataset N>]",
        "module": model.UpdateModelCommand,
    },
    "predict": None,
    "predict-batch": None,
    "twitter-search": {
        "help": "Show the current stream of tweets that matches the search terms",
        "params": "<language code> [<search term 1> ... <search term N>]",
        "module": twitter.SearchTweetsCommand,
    },
    "twitter-gen-dataset": {
        "help": "Save a twitter dataset sample",
        "params": "<language code> <tweet count> <output file>",
        "module": twitter.SaveSampleCommand,
    },
}