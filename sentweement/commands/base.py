class BaseCommand(object):
    def __init__(self, prog_name, args):
        self.__prog_name = prog_name
        self.__args = args

    def get_prog_name(self):
        return self.__prog_name

    def get_arguments(self):
        return self.__args

    def run(self):
        raise NotImplementedError("run() is not implemented for %s" % self.__class__)


def run_command(prog_name, command, args):
    try:
        klass = get_commands()[command.lower()]["module"]
    except KeyError:
        return

    instance = klass(prog_name, args)
    return instance.run()

def get_commands():
    from sentweement import commands
    valid_commands = {}
    for command, item in commands.VALID_COMMANDS.copy().items():
        if item is not None:
            valid_commands.update({command: item})
    return valid_commands
