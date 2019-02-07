# defining the command handler class

class CommandHandler:
    """A class used to handle events"""
    # Creating a command handler
    def __init__(self, client):
        """Regular constructor"""
        self.client = client
        # Creating an empty list of commands
        self.commands = []

    # Adding a command to the command list
    def add_command(self, command):
        """Class method that adds a command dictionary to the command list"""
        self.commands.append(command)

    # Handling a command
    def command_handler(self, message):
        """
        Class method that handles events based on messages sent by other clients
        
        Messages sent by other users may contain keywords that the script
        picks up and acts accordingly
        """
        # loop through the command list and answer accordingly
        for command in self.commands:
            # first word in the message is the trigger
            if message.content.startswith(command["trigger"]):
                # collecting all the arguments in the message
                args = message.content.split(" ")
                # Making sure the trigger is valid
                if args[0] == command["trigger"]:
                    # Removing the trigger
                    args.pop(0)
                    # command has no arguments
                    if command["args_num"] == 0:
                        # returns the results of the function
                        return self.client.send_message(message.channel, str(command["function"](message, self, args)))
                    # command has one or more arguments
                    elif len(args) >= command["args_num"]:
                        # return the results of the function
                        return self.client.send_message(message.channel, str(command["function"](message, self, args)))
                    # command has less arguments than expected
                    else:
                        # return argument error
                        return self.client.send_message(message.channel, ":no_entry: **ERROR** :no_entry: : command \"{}\" requires {} argument(s): \"{}\"".format(command["trigger"], command["args_num"], ', '.join(command["args_name"])))
                else:
                    break
