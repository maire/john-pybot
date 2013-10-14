import botlib
import urllib
import pytumblr
import csv
from bs4 import BeautifulSoup
from random import choice

# Create a new class for our bot, extending the Bot class from botlib
class JohnPyBot(botlib.Bot):
    def __init__(self, server, channel, nick, password=None):
        botlib.Bot.__init__(self, server, 6667, channel, nick)

        # Send nickserv password if available
        if password != None:
            self.protocol.privmsg("nickserv", "identify" % password)

        self.commands = ["!hello",
                         "!leave",
                         "!tumblr",
                         "!insult"]

        self.masters = []
        self.masters.append("Garnavis")

        self.client = pytumblr.TumblrRestClient( \
                "sSMRBoKp2ognfANViuUGt6V4CfNDhTIVSC8agmORVGH5VDXTon")

        self.insults_a = []
        self.insults_b = []
        self.insults_c = []

        with open("insults.txt", "rb") as tabfile:
            self.insult_reader = csv.reader(tabfile, delimiter='\t')
            for row in self.insult_reader:
                self.insults_a.append(row[0])
                self.insults_b.append(row[1])
                self.insults_c.append(row[2])

    def __actions__(self):
        botlib.Bot.__actions__(self)

        # List all commands.
        if botlib.check_found(self.data, "!commands"):
            self.protocol.privmsg(self.channel, ", ".join(self.commands))

        # Say hello to the prompting user.
        if botlib.check_found(self.data, "!hello"):
            username = self.get_username()
            self.protocol.privmsg(self.channel, "Hello %s!" % username)

        # Leave the network upon command.
        if botlib.check_found(self.data, "!leave") or \
           botlib.check_found(self.data, "!getout"):
            self.protocol.disconnect("If I must.")

        # Get the title from the web page linked.
        if botlib.check_found(self.data, "http://") and \
           self.get_username() in self.masters:
            url = "http://" + self.data.partition("http://")[2]
            soup = BeautifulSoup(urllib.urlopen(url))
            self.protocol.privmsg(self.channel, \
                    soup.title.string.encode("utf-8", "ignore"))

        # Add a user to the URL check list.
        if botlib.check_found(self.data, "!add"):
            self.masters.append(self.get_args()[0])

        # Show the users whose URLs Lucien checks.
        if botlib.check_found(self.data, "!list"):
            self.protocol.privmsg(self.channel, self.masters)

        # Find a recent text post with the given tag.
        if botlib.check_found(self.data, "!tumblr"):
            self.tag = " ".join(self.get_args())
            self.posts = self.client.tagged(self.tag, filter="text")
            self.text_posts = filter(lambda x: "title" in x, self.posts)
            if len(self.text_posts) > 0:
                self.post = choice(self.text_posts)
                self.title = self.post.get("title").encode("utf-8", "ignore")
                if "body" in self.post:
                    self.body = self.post.get("body").encode("utf-8", "ignore")
                else:
                    self.body = self.post.get("url").encode("utf-8", "ignore")
                self.protocol.privmsg(self.channel, self.title)
                self.protocol.privmsg(self.channel, self.body)
            else:
                self.protocol.privmsg(self.channel, \
                        "Sorry, I can't find anything for that tag.")

        # Say a Shakespearean insult.
        if botlib.check_found(self.data, "!insult"):
            self.protocol.privmsg(self.channel, \
                    "Thou %s, %s %s!" % \
                    (choice(self.insults_a), \
                     choice(self.insults_b), \
                     choice(self.insults_c)))

if __name__== "__main__":
    # Create a new instance of our bot and run it
    JohnPyBot("irc.freenode.net", "#oswegocsa", "Lucien").run()
