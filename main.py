#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import re
import os
import cgi
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), "templates") #___file___ uses most current file
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape = True)

def render_str(self, template, **params):
    t = jinja_env.get_template(template)
    return t.render(params)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.write(*a, **kw)

    def render(self, template, **kw):
        self.response.write(render_str(template, **kw))



USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
def valid_username(username):
    return username and USER_RE.match(username)

PASS_RE = re.compile(r"^.{3,20}$")
def valid_pw(password):
    return password and PASS_RE.match(password)

EMAIL_RE = re.compile(r'^[\S]+@[\S]+.[\S]+$')
def valid_email(email):
    return email and EMAIL_RE.match(email)





class MainHandler(Handler):
    #def write_form(self, error="", username="", email=""):
    #    self.response.write("sign-up.html", error = error, username = username, email = email)

    def get(self, error="", username="", email=""):
        self.render("signup.html")

    def post(self):
        hasError = False
        username = self.request.get('username')
        password = self.request.get('password')
        verify = self.request.get('verify')
        email = self.request.get('email')

        params = dict(username= username, email = email)

        #username = valid_name(user_name)
        #password = valid_pw(user_pw)
        #email = valid_email(user_email)
        #confirm_password = valid_pw2(user_pw2)

        if not valid_username(username):
            params['error_username'] = "Try again friend - that wasn't a valid username."
            hasError= True

        if not valid_pw(password):
            params['error_password'] = "Try again friend - that wasn't a valid password."
            hasError= True

        elif password != confirm_password:
            params['error_verify'] = "Try again friend - your passwords didn't match"
            hasError= True

        if not valid_email(email):
            params['error_email'] = "Try again friend - that wasn't a valid email."
            hasError= True

        if hasError:
            self.render('signup.html', **params)
        else:
            self.redirect('/thanks?username=' + username)
            #print("Hello")


class ThanksHandler(Handler):
    def get(self):
        username = self.request.get('username')
        if valid_username(username):
            self.render("welcome.html", username = username)
        else:
            self.redirect('/')



app = webapp2.WSGIApplication([
    ('/', MainHandler), ('/thanks', ThanksHandler)
], debug=True)
