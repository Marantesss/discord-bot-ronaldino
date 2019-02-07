# defining the command handler class

class CommandHandler:

    # Creating a command handler
    def __init__(self, client):
        self.client = client
        # Creating an empty list of commands
        self.commands = []

    # Adding a command to the command list
    def addCommand(self, command):
        self.commands.append(command)

    # Handling a command
    def handler(self, message):
        # loop through the command list and answer accordingly
        for command in self.commands:

            if message.content.startswith(command["trigger"]):
                
