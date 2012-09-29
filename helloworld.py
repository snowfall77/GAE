import webapp2

import os

from google.appengine.ext.webapp import template

from google.appengine.ext import db
from google.appengine.api import users

class UserInfo(db.Model):
    nickname = db.StringProperty()
    username = db.StringProperty()
    prev_username = db.StringProperty()

class MainPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()

        if user:
            self.response.headers['Content-Type'] = 'text/plain'

            userinfo = db.GqlQuery("SELECT * FROM UserInfo WHERE nickname IN :1", [user.nickname()])
	    if userinfo.count() == 0:
	        u = UserInfo(nickname=user.nickname())
		u.put()
            else:
	        u = userinfo.get()

	    template_values = {
                'nickname': u.nickname,
		'username': u.username,
		'prev_username': u.prev_username,
	    }
	    
	    path = os.path.join(os.path.dirname(__file__), 'templates/index.html')
	    self.response.headers["Content-Type"] = 'text/html'
	    self.response.out.write(template.render(path, template_values))
	else:
	    self.redirect(users.create_login_url(self.request.uri))

class Update_username(webapp2.RequestHandler):
    def get(self):
        username = self.request.get('username')
        nickname = self.request.get('nickname')
	userinfo = db.GqlQuery("SELECT * FROM UserInfo WHERE nickname IN :1", [nickname])
        u = userinfo.get()
	prev_username = u.username
	u.prev_username = u.username
	u.username = username
        u.put()

	self.response.out.write(prev_username)
	
app = webapp2.WSGIApplication([('/', MainPage),
                               ('/update_username', Update_username)
			      ],
                             debug=True)
