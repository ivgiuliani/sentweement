from sentweement.commands.base import BaseCommand, get_commands

import textwrap

class HelpCommand(BaseCommand):
    """
    Show the command list or help about a specific command
    """

    def command_list(self):
        commands = get_commands()
        command_list = sorted(commands.keys())
        longest_command = max(commands)
        command_width = len(longest_command) + 2

        print("Commands:")
        for command in commands:
            help_text = commands[command]["help"]
            parameters = commands[command]["params"]

            print("{0:>{width}}  {1}".format(command, help_text, width=command_width))
            if parameters:
                print("{0:{width}}  Parameters: {1}".format("", parameters, width=command_width))

    def run(self):
        arguments = self.get_arguments()
        try:
            command = arguments[0]
            module = get_commands()[command]
        except (IndexError, KeyError):
            self.command_list()
            return False
        
        print("Command: %s %s %s" % (self.get_prog_name(), command, module["params"]))

        docstring = module["module"].__doc__
        long_help = docstring or "\nNo further help for %s\n" % command
        for line in textwrap.dedent(long_help).split("\n"):
            print("         %s" % line)

        return False
