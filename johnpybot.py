import botlib
import urllib
import pytumblr
import csv
from nyc import nyc
from bs4 import BeautifulSoup
from random import choice

# Create a new class for our bot, extending the Bot class from botlib
class JohnPyBot(botlib.Bot):
    def __init__(self, server, channel, nick, password=None):
        botlib.Bot.__init__(self, server, 6667, channel, nick)

        try:
          self.nyc_thread = nyc(self.protocol.privmsg, channel)
          self.nyc_thread.start()
        except Exception as e:
          print 'Couldn\'t start the nyc thread poll cause:\n' + e

        # Send nickserv password if available
        if password != None:
            self.protocol.privmsg("nickserv", "identify" % password)

        self.commands = ["!hello",
                         "!leave",
                         "!tumblr",
                         "!insult"]

        self.url_monitoring = []

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

        self.nyc_thread.ping(self.data)

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
           self.get_username() in self.url_monitoring:
            url = "http://" + self.data.partition("http://")[2]
            soup = BeautifulSoup(urllib.urlopen(url))
            self.protocol.privmsg(self.channel, \
                    soup.title.string.encode("utf-8", "ignore"))

        # Add a user to the URL check list.
        if botlib.check_found(self.data, "!add"):
            nicks = self.get_args()
            for nick in nicks:
                self.url_monitoring.append(nick)
                self.protocol.privmsg(self.channel, \
                        "Checking URLs for %s." % nick)

        # Show the users whose URLs Lucien checks.
        if botlib.check_found(self.data, "!list"):
            self.protocol.privmsg(self.channel, self.url_monitoring)

        # Find a recent text post with the given tag.
        if botlib.check_found(self.data, "!tumblr"):
            tag = " ".join(self.get_args())
            posts = self.client.tagged(tag, filter="text")
            text_posts = filter(lambda x: "title" in x, posts)
            if len(text_posts) > 0:
                post = choice(text_posts)
                title = post.get("title").encode("utf-8", "ignore")
                if "body" in post:
                    body = post.get("body").encode("utf-8", "ignore")
                else:
                    body = post.get("url").encode("utf-8", "ignore")
                self.protocol.privmsg(self.channel, title)
                self.protocol.privmsg(self.channel, body)
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
    # Create a new instance of the bot and run it
    JohnPyBot("irc.synirc.net", "#nyc", "Lucien").run()
