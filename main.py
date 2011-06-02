import os

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

import link
games = {}
gametexts = {}

class MainPage(webapp.RequestHandler):

  def get(self):
    ip =  self.request.remote_addr
    global games, gametexts
    if not ip in games:
        games[ip]=link.link()
        gametexts[ip]=games[ip].next().replace('\n','<br>')
        
    template_values = {
      'text':gametexts[ip]
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class Command(webapp.RequestHandler):
  def post(self):
    ip =  self.request.remote_addr
    global games,gametexts
    cmd = self.request.get('content')[:80]

    if cmd == "restart":
        games[ip] = link.link()
        gametexts[ip] = games[name].next().replace('\n','<br>')
    else:
        try:
            gametexts[ip] = games[ip].send(cmd).replace('\n','<br>').replace(" ","&nbsp;")
            gametexts[ip] = gametexts[ip].replace("@@img@@","img src").replace("@@width@@"," width")
        except StopIteration:
            del games[ip]
    self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/cmd', Command)],
                                     debug=True)

def main():
  run_wsgi_app(application)


if __name__ == "__main__":
  main()
