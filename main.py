import os
import random

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import link
games = {}
gametexts = {}

class MainPage(webapp.RequestHandler):

  def post(self):
      self.get()

  def get(self):
    userid = self.request.get('userid')[:80]
    if userid == None or userid == "":
        userid = str(random.randint(1,10**10))
        
    global games, gametexts

    if userid in games:
        cmd = self.request.get('content')[:80]

        if cmd == "restart":
            del games[userid]
        else:
            try:
                gametexts[userid] = games[userid].send(cmd).replace('\n','<br>').replace(" ","&nbsp;")
                gametexts[userid] = gametexts[userid].replace("@@img@@","img src").replace("@@width@@"," width")
            except StopIteration:
                del games[userid]

    if not userid in games:
        games[userid]=link.link()
        gametexts[userid]=games[userid].next().replace('\n','<br>')

    template_path = os.path.join(os.path.dirname(__file__), 'index.html')
    html = template.render(template_path, dict(text=gametexts[userid],userid=userid))
    self.response.out.write(html)

application = webapp.WSGIApplication([('/', MainPage)], debug=True)

def main():
  run_wsgi_app(application)


if __name__ == "__main__":
  main()
