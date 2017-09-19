import os
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


class Rot13Handler(Handler):
    def write_textarea(self, text=""):
        self.response.out.write(text)

    def rot13(self, text):
        output = ''
        for char in text:
            if char.isalpha():
                begin = 'A' if char.isupper() else 'a'
                output += chr((ord(char) - ord(begin) + 13) % 26 + ord(begin))
        return output

    def get(self):
        self.render("rot13.html", x="")

    def post(self):
        user_text = self.request.get("text")
        text = self.rot13(user_text)
        self.render("rot13.html", x=text)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/fizzbuzz', FizzBuzzHandler),
                               ('/rot13', Rot13Handler)],
                              debug=True)