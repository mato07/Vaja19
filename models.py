from google.appengine.ext import ndb #tu se skriva nas objekt


class Sporocilo(ndb.Model): # ndb.Model se zna pogovarjati z bazo
    besedilo = ndb.StringProperty() # dobro za kratke tekste
    nastanek = ndb.DateTimeProperty(auto_now_add=True) # vpise trenutni datum