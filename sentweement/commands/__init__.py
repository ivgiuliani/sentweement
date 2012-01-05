from sentweement.commands import helpcmd
from sentweement.commands import model

__all__ = [ "run_command", "get_commands" ]

VALID_COMMANDS = {
    "help": {
        "help": "Show help",
        "module": helpcmd.HelpCommand,
    },
    "model-create": {
        "help": "Creates a new learning model",
        "module": model.CreateModelCommand,
    },
    "model-update": {
        "help": "Updates an existing learning model",
        "module": model.UpdateModelCommand,
    },
    "predict": None,
    "predict-batch": None,
    "twitter-search": None,
    "twitter-gen-dataset": None,
}
