import cgi

from google.appengine.api import users
from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template

import link
games = {}
gametexts = {}

class MainPage(webapp.RequestHandler):

  def get(self):
    user = users.get_current_user()
    if not user:
      url = users.create_login_url(self.request.uri)
      self.redirect(url)
      return
    else:
      url = users.create_logout_url(self.request.uri)
      url_linktext = user.email()+ ' logout'
      name = user.email()

    global games, gametexts
    if not name in games:
        games[name]=link.link()
        gametexts[name]=games[name].next().replace('\n','<br>')
        
    template_values = {
      'user':user.email(),
      'url': url,
      'url_linktext': url_linktext,
      'text':gametexts[name]
      }

    path = os.path.join(os.path.dirname(__file__), 'index.html')
    self.response.out.write(template.render(path, template_values))

class Command(webapp.RequestHandler):
  def post(self):
    global games,gametexts
    user = users.get_current_user()
    if not user:
      url = users.create_login_url(self.request.uri)
      self.redirect(url)
      return
    else:
      name = user.email()

    cmd = self.request.get('content')[:80]

    if cmd == "restart":
        games[name] = link.link()
        gametexts[name] = games[name].next().replace('\n','<br>')
    else:
        gametexts[name] = games[name].send(cmd).replace('\n','<br>').replace(" ","&nbsp;")
    self.redirect('/')

application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      ('/cmd', Command)],
                                     debug=True)

def main():
  run_wsgi_app(application)


if __name__ == "__main__":
  main()
