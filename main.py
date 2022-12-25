from parserURL import Parser
from urllib.parse import urlencode
from flask import Flask, render_template, request, Response
from threading import Thread
import time

app = Flask(__name__)
app.config['CSRF_ENABLED'] = True
app.config['SECRET_KEY'] = "d99w89a0d0c"

class crawl():
   def __init__(self):
      self.pr = Parser()
      self.log = ""
      self.t = Thread()

   def search(self, words):
      self.t = Thread(target=self.pr.run,args=(words,))
      self.t.start()
      print("searching...")

   def is_running(self):
      if self.t.is_alive():
         return "true"
      else:
         return "false"

   def listurl(self):
      urls = ""
      for i in self.pr.found:
         urls += "%s <br>" % i["URL"]
      return urls

c = crawl()

@app.route("/")
def _index():
   return render_template("index.html")

@app.route("/run")
def _run():
   kw = request.args.get("kw")
   if c.is_running() == "false":
      if kw:
         c.found = {}
         c.pr.clean()
         c.search(kw)
         return "Starting crawling '%s'" % kw
      return "Empty keywords!"
   return "Already running."

@app.route("/isrunning")
def _isrunning():
   return c.is_running()

@app.route("/list.txt")
def _check():
   if request.args.get("astype") == "plain":
      return Response(c.listurl().replace("<br>","\n"), mimetype='application/x-please-download-me')
   return c.listurl()

@app.route("/count")
def _count():
   return str(len(c.pr.found))

@app.route("/stop")
def _stop():
   c.pr.stop = True
   return "Shutting down..."

app.run(port = 8080, debug=True)
