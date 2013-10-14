import botlib
import urllib
import pytumblr 
from bs4 import BeautifulSoup
from random import choice

# Create a new class for our bot, extending the Bot class from botlib
class JohnPyBot(botlib.Bot):
    def __init__(self, server, channel, nick, password=None):
        botlib.Bot.__init__(self, server, 6667, channel, nick)

        # Send nickserv password if available
        if password != None:
            self.protocol.privmsg("nickserv", "identify" % password)

        self.masters = []
        self.masters.append("Garnavis")

        self.client = pytumblr.TumblrRestClient( \
                'sSMRBoKp2ognfANViuUGt6V4CfNDhTIVSC8agmORVGH5VDXTon')

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

if __name__== "__main__":
    # Create a new instance of our bot and run it
    JohnPyBot("irc.freenode.net", "#oswegocsa", "Lucien").run()
