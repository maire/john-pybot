# -*- coding: utf-8 -*-

__author__ = 'herschel'

import requests, threading, leaf, re
from time import sleep
from random import choice, random

thread_url = 'http://forums.somethingawful.com/showthread.php?threadid=3032497&goto=newpost'
get_new_post_number = re.compile('pti([0-9]*)')
user_adjectives = ['troll', 'superstar', 'token conservative', 'scapegoat', 'fyad reject', 'anime avatar']
post_adjectives = ['a stunning', 'a rage-inducing', 'a bombshell', 'a misogynistic', 'a chic', 'an informative',
                   'a bannable']
dead_threshold = 2
poll_sleep = 10
change_of_using_a_funny_adjective = .15

class nyc(threading.Thread):

  def __init__(self, callback, channel):

    threading.Thread.__init__(self)

    self.daemon = True

    self.callback = callback
    self.channel = channel

    self.dead = 0

    creds = open('login.cfg').readlines()

    self.session = requests.session()

    payload = { 'action' : 'login',
                'username': creds[0].replace('\n', ''),
                'password': creds[1].replace('\n', ''),
                'next': '/'
    }

    login = self.session.post('http://forums.somethingawful.com/account.php?action=loginform', data=payload)

    if 'Clicking here makes all your wildest dreams come true.' in login.text:
      print 'Successfully logged in to the forums.'
    else:
      raise Exception('¡Ay no!')

  def ping(self, data):

    if 'PRIVMSG {0}'.format(self.channel) in data:
      self.dead = 0

  def run(self):

    self.session.get(thread_url)

    while True:
      try:
        sleep(10)
        poll = self.session.get(thread_url)

        if '#lastpost' in poll.url:
          continue

        if self.dead >= dead_threshold - 1:
          continue
        else:
          self.dead += 1

        new_index = int(get_new_post_number.findall(poll.url)[0]) - 1

        page = leaf.parse(poll.text)

        self.callback(self.channel, 'Forums {0} {1} made {2} new post in the NYC thread! {3}'.format(
          choice(user_adjectives) if random() < change_of_using_a_funny_adjective else 'poster',
          page('.author')[new_index].text,
          choice(post_adjectives) if random() < change_of_using_a_funny_adjective else 'a',
          poll.url
        ))

      except Exception as e:
        print e
