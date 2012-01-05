from sentweement.commands.base import BaseCommand, get_commands

class HelpCommand(BaseCommand):
    def run(self):
        commands = get_commands()
        command_list = sorted(commands.keys())
        longest_command = max(commands)
        command_width = len(longest_command) + 2

        for command in commands:
            help_text = commands[command]["help"]
            parameters = commands[command]["params"]

            print("{0:>{width}}  {1}".format(command, help_text, width=command_width))
            if parameters:
                print("{0:{width}}  Parameters: {1}".format("", parameters, width=command_width))
