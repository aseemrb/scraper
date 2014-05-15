import webapp2
import sys
import urllib2
import os
import jinja2
import re
import logging
import json
import urlparse

#importing beautifulsoup
sys.path.insert(0, 'libs')
from bs4 import BeautifulSoup

#setting up jinja2 to pick files from templates dir
template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
                               autoescape = True)


#Shorthand functions to make life easier
class BaseHandler(webapp2.RequestHandler):
    def write(self, *a, **kw):
        self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

class MainHandler(BaseHandler):
    def get(self):
        self.render("index.html")


class Scrape(BaseHandler):
    def get(self):
        url = self.request.get('url')
        content = urllib2.urlopen(url).read()
        soup = BeautifulSoup(content)
        parsed = list(urlparse.urlparse(url))
        # logging.info(parsed)
        
        self.response.headers['Content-Type'] = 'application/json'
        links = []
        anchs = []
        
        for element in soup.find_all('a', 'symb'):
            if element.has_attr('class'):
                parsed[2] = element['href']
                anchs.append(urlparse.urlunparse(parsed))
                
        for image in soup.find_all('img'):
            # print "Image: %(src)s" % image
            # filename = image["src"].split("/")[-1]
            parsed[2] = image["src"]
            if (image["src"].lower().startswith("http") or 
                image["src"].lower().find('.co')!=-1 or 
                image["src"].lower().find('.org')!=-1):
                links.append(image["src"])
            else:
                links.append(urlparse.urlunparse(parsed))
        
        urls = json.dumps([dict(url=l) for l in links])
        anchors = json.dumps([dict(hlink=an) for an in anchs])
        # logging.info(urls)
        obj = {
               "urls" : urls,
               "anchors": anchors
               }
        # logging.info(obj)
        # logging.info("{ \"urls\" : " +  urls + "," + " \"anchors\" : " +  anchors + " }")
        self.response.out.write("{ \"urls\" : " +  urls + ", \"anchors\" : " +  anchors + " }")


app = webapp2.WSGIApplication([
    ('/', MainHandler),
    ('/scrape/.*', Scrape)
], debug=True)
