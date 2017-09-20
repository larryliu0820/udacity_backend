import os
import re
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class Handler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))


class MainPage(Handler):
    def get(self):
        items = self.request.get_all("food")
        self.render("shopping_list.html", items=items)


class FizzBuzzHandler(Handler):
    def get(self):
        n = self.request.get('n', 0)
        n = n and int(n)
        self.render('fizzbuzz.html', n=n)


class WelcomeHandler(Handler):
    def get(self):
        username = self.request.get('username')
        self.render('welcome.html', username=username)


class Rot13Handler(Handler):
    def write_textarea(self, text=""):
        self.response.out.write(text)

    def get(self):
        self.render("rot13.html", x="")

    def post(self):
        user_text = self.request.get("text")
        text = user_text.encode('rot13')
        self.render("rot13.html", x=text)

class SignupHandler(Handler):
    def get(self):
        self.render("signup.html")

    def valid_input(self, type, value):
        RE_DICT = {
            "username": re.compile(r"^[a-zA-Z0-9_-]{3,20}$"),
            "password": re.compile(r"^.{3,20}$"),
            "email": re.compile(r"^[\S]+@[\S]+.[\S]+$")
        }
        return RE_DICT[type].match(value) and value

    def post(self):
        input_dict = {"username": "", "password": "", "verify_pass": "", "email": ""}
        error_dict = {
            "username_error": "That's not a valid username.",
            "password_error": "That wasn't a valid password.",
            "verify_pass_error": "Your passwords didn't match.",
            "email_error": "That's not a valid email."
        }
        for key in input_dict:
            input_dict[key] = self.request.get(key)
            if key is "email" and not input_dict["email"]:
                input_dict[key] = ""
                error_dict["email_error"] = ""
                continue
            if key is not "verify_pass":
                input_dict[key] = self.valid_input(key, input_dict[key])

        if input_dict["password"] and input_dict["password"] != input_dict["verify_pass"]:
            input_dict["verify_pass"] = ""
        for key in error_dict:
            if key != "email" and input_dict[key[:-6]]:
                if key[:-6] in ["password", "verify_pass"]:
                    input_dict[key[:-6]] = ""
                error_dict[key] = ""
        if any(error_dict.itervalues()):
            self.render("signup.html", **{k: v for d in (input_dict, error_dict) for k, v in d.items()})
        else:
            self.redirect("/welcome?username=%s" % input_dict["username"])

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/fizzbuzz', FizzBuzzHandler),
                               ('/rot13', Rot13Handler),
                               ('/signup', SignupHandler),
                               ('/welcome', WelcomeHandler)],
                              debug=True)