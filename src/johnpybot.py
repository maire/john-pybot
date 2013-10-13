import botlib
import urllib
from bs4 import BeautifulSoup

# Create a new class for our bot, extending the Bot class from botlib
class JohnPyBot(botlib.Bot):
    masters = []
    def __init__(self, server, channel, nick, password=None):
        botlib.Bot.__init__(self, server, 6667, channel, nick)

        # Send nickserv password if available
        if password != None:
            self.protocol.privmsg("nickserv", "identify" % password)

        self.masters.append("Garnavis")
        

    def __actions__(self):
        botlib.Bot.__actions__(self)

        # Say hello to the prompting user.
        if botlib.check_found(self.data, "!hello"):
            username = self.get_username()
            self.protocol.privmsg(self.channel, "Hello %s!" % username)

        # Leave the network upon command.
        if botlib.check_found(self.data, "!leave"):
            self.protocol.disconnect("If I must.")

        # Get the title from the web page linked.
        if botlib.check_found(self.data, "http://") and \
           self.get_username() in self.masters:
            url = "http://" + self.data.partition("http://")[2]
            soup = BeautifulSoup(urllib.urlopen(url))
            self.protocol.privmsg(self.channel, soup.title.string)

        if botlib.check_found(self.data, "!add"):
            self.masters.append(self.get_args()[0])

        if botlib.check_found(self.data, "!list"):
            self.protocol.privmsg(self.channel, self.masters)

if __name__== "__main__":
    # Create a nwe instance of our bot and run it
    JohnPyBot("irc.synirc.net", "#rhirc", "Lucien").run()
