#!/usr/bin/env python
import os
import jinja2
import webapp2
from models import Sporocilo

template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=True)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if params is None:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))


class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("hello.html")

class RezultatHandler(BaseHandler):
    def post(self):
        rezultat = self.request.get("input-sporocilo")

        sporocilo = Sporocilo(besedilo=rezultat)

        sporocilo.put() # sporocilo shranimo (definiran v modelu ndb)

        return self.write(rezultat)

class ListHandler(BaseHandler):
    def get(self):
        seznam = Sporocilo.query().fetch() # v query bi lahko podali dodatne zahteve (od kdaj napre) fetch pa dobi sporocila ven
        params = {"seznam": seznam}
        return self.render_template("seznam.html", params=params)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, sporocilo_id):
        sporocilo = Sporocilo.get_by_id(int(sporocilo_id))

        params = {"sporocilo": sporocilo}
        return self.render_template("posamezno_sporocilo.html", params=params)


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/rezultat', RezultatHandler),
    webapp2.Route('/seznam', ListHandler),
    webapp2.Route('/sporocilo/<sporocilo_id:\d+>', PosameznoSporociloHandler), # v ime sporocilo_id shari kar bos prebral v \d+ (digit enkrat ali veckrat)
], debug=True)

# na localhost:8000 je admin streznik
# z ID-jem v admin strezniku lahko dobimo tocno doloceno sporocilo
# jinja_env na zacetku autoescape damo v True (ce vpisemo kaksne html tage v input)