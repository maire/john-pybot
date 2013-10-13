import botlib

# Create a new class for our bot, extending the Bot class from botlib
class HelloWorldBot(botlib.Bot):
    def __init__(self, server, channel, nick, password=None):
        botlib.Bot.__init__(self, server, 6667, channel, nick)

        # Send nickserv password if available
        if password != None:
            self.protocol.privmsg("nickserv", "identify" % password)

    def __actions__(self):
        botlib.Bot.__actions__(self)

        # Say hello to the prompting user.
        if botlib.check_found(self.data, "!hello"):
            username = self.get_username()
            self.protocol.privmsg(self.channel, "Hello %s!" % username)

        # Leave the network upon command.
        if botlib.check_found(self.data, "!leave"):
            self.protocol.disconnect("If I must.")

if __name__== "__main__":
    # Create a nwe instance of our bot and run it
    HelloWorldBot("irc.synirc.net", "#rhirc", "Lucien").run()
