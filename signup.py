import os
import webapp2
import jinja2
import re
import codecs

template_dir = os.path.join(os.path.dirname(__file__),'signup')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)
                                


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a,**kw)

        
    def render_str(self, template, **params):
        t=jinja_env.get_template(template)
        return t.render(params)

    def render(self,template, **kw):
        self.write(self.render_str(template, **kw))

class MainPage(Handler):
    	def get(self):
     		self.render("rot13.html")
     	def post(self):
     		text = self.request.get("text")
     		rot13 = codecs.encode(text,'rot_13')
     		self.render("rot13.html",text = rot13)
        

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_password(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+.[\S]+$')
def valid_email(email):
    return not email or EMAIL_RE.match(email)

class Signup(Handler):
    def get(self):
        self.render("signup.html")
      
     
    def post(self):
         have_error= False
         username = self.request.get("username")
         password = self.request.get("password")
         verify = self.request.get("verify")
         email = self.request.get("email")

         params= dict(username = username,
                      email = email)
         
         if not valid_username(username):
             params['error_username']= "that is not a valid user name"
             have_error = True
         if not valid_password(password):
             params['error_password'] = "that wasn't a valid password"
             have_erro = True
         elif password != verify:
             params['error_verify']= "password doesn't match"
             have_error= True

         if not valid_email(email):
            params['error_email'] = "that is not a valid email"
            have_error= True

         if have_error:
             self.render("signup.html",**params)

         else:
             self.redirect('/welcome?username='+username)
         
         
class Welcome(Handler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render("welcome.html",username = username)
        else:
            self.redirect('/signup')
       
       

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/signup',Signup),
                               ('/welcome',Welcome),],
                               debug=True)  
        

