from sentweement.commands import helpcmd
from sentweement.commands import model

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
    "twitter-search": None,
    "twitter-gen-dataset": None,
}
