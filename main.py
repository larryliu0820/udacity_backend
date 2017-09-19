import webapp2
import cgi
form = """
    <form  method="post">
        What is your birthday?
        <br>
        <label>Month <input type="text" name="month"></label>
        <label>Day <input type="text" name="day"></label>
        <label>Year <input type="text" name="year"></label>
        <div style="color: red">%(error)s</div>
        <br>
        <br>
        <input type="submit">
    </form>
"""


def valid_day(day):
    if day.isdigit():
        day = int(day)
        if 1 <= day <= 31:
            return day


def valid_year(year):
    if year.isdigit():
        year = int(year)
        if 1900 <= year <= 2020:
            return year

months = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']


def valid_month(month):
    month_dict = dict((mon.lower()[:3], mon) for mon in months)
    if month.lower()[:3] in month_dict:
        return month_dict[month.lower()[:3]]


def escape_html(s):
    return cgi.escape(s, quote=True)


class MainPage(webapp2.RequestHandler):
    def write_form(self, error="", month="", day="", year=""):
        self.response.out.write(form % {"error": error,
                                        "month": escape_html(month),
                                        "day": escape_html(day),
                                        "year": escape_html(year)})

    def get(self):
        # self.response.headers['Content-Type'] = 'text/plain'
        self.write_form()

    def post(self):
        user_month = self.request.get('month')
        user_day = self.request.get('day')
        user_year = self.request.get('year')

        month = valid_month(user_month)
        day = valid_day(user_day)
        year = valid_year(user_year)

        if not (month and day and year):
            self.write_form("That doesn't look valid to me, friend. %s, %s, %s" % (month, day, year), user_month, user_day, user_year)
        else:
            self.redirect("/thanks")


class ThanksHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write("Thanks! That's a totally valid day!")


class TestHandler(webapp2.RequestHandler):
    def get(self):
        # q = self.request.get('q')
        # self.response.out.write(q)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write(self.request)

app = webapp2.WSGIApplication([('/', MainPage),
                               ('/testform', TestHandler),
                               ('/thanks', ThanksHandler)],
                              debug=True)