import requests
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup
class Parser():
   def __init__(self):
      self.urls= []
      self.parsed = []
      self.failed = 0
      self.found = []
      self.stop = False

   def load(self,page):
      return requests.get(page, timeout=20).text

   def clean(self):
      self.found = []
      self.parsed = []
      self.failed = 0
      self.urls = []

   def parse(self,page):
      if page not in self.parsed:
         self.parsed.append(page)
         soup = BeautifulSoup(self.load(page))
         urls = [link.get("href") for link in soup.findAll('a')]
         for url in urls:
            url = urljoin(page,url)
            self.urls.append(url)
         self.found.append({"URL":page,"TITLE":soup.title.string, "HOST":urlparse(page).netloc})

   def show(self):
      print(self.urls)
      print("Failed: %s" % self.failed)

   def deeper(self, count):
      for i in range(count):
         for url in self.urls:
            try:
               self.parse(url)
            except:
               self.failed += 1
            if self.failed > count * 100 or self.stop == True:
               break
         if self.failed > count * 100 or self.stop == True:
            break

   def run(self,search):
      self.stop = False
      if "http://" in search or "https://" in search:
         self.parse(search)
      else:
         self.parse("https://duckduckgo.com/html/?q=" +  search)
      self.deeper(1)

