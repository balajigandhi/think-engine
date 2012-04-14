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
#
import webapp2
#from nltk import book
#from bs4 import *
from index import *

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.out.write('Think Engine!')
        #self.response.out.write(text1)

class IndexHandler(webapp2.RequestHandler):
    def get(self):
        index, graph = crawl_web('http://www.udacity.com/cs101x/final/multi.html')
        self.response.out.write(index)
        #self.response.out.write(text1)

app = webapp2.WSGIApplication([('/', MainHandler),
                               ('/index', IndexHandler)],
                               debug=True)
