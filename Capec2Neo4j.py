#!/usr/bin/env python

#
# Last modification: 2017-06-10
# Homepage: 
#
# The MIT License (MIT)
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# ITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

# Regular expressions
import re
# Xml : dictionary mapping
import xmltodict

import CypherWriter
import Xml2Cypher



#
# Fixes xmlToDict inconsistent behavior with dictionaries
def normalizeDict(object):
  if not isinstance(object, list):
    return [ object ]
  
  return object

def filterComment(params):
  return re.match('(\w+)(<!--.*-->)?', params['text']).group(1)

def splitString(params):
  return params['text'].split(params['separator'])

def structuredTextTraverse(node, level):
  arr = []
  
  indent = "  " * level
  arr.append('%s<div level="%d">' % (indent, level))
  
  level += 1
  indent = "  " * level
  
  if 'Text_Title' in node:
    for t in normalizeDict(node['Text_Title']):
      arr.append('%s<h1>%s</h1>' % (indent, t))
  
  if 'Text' in node:
    for t in normalizeDict(node['Text']):
      arr.append('%s<p class="text">%s</p>' % (indent, t))
      
  if 'Code_Example_Language' in node:
    for t in normalizeDict(node['Code_Example_Language']):
      arr.append('%s<p class="code_example_language">%s</p>' % (indent, t))
  
  if 'Code' in node:
    for t in normalizeDict(node['Code']):
      arr.append('%s<p class="code">%s</p>' % (indent, t))
  
  if 'Comment' in node:
    for t in normalizeDict(node['Comment']):
      arr.append('%s<p class="comment">%s</p>' % (indent, t))
  
  if 'Block' in node:
    for block in normalizeDict(node['Block']):
      arr += structuredTextTraverse(block, level)
  
  indent = "  " * (level - 1)
  arr.append('%s</div>' % (indent))
  
  return arr

def structuredText(params):
  return '\n'.join(structuredTextTraverse(params['node'], 0))

def parseRsTarget(params):
  return 'Category' if params['text'] == 'Category' else 'AttackPattern'

def parseRsNature(params):
  return 'CHILD_OF' if params['text'] == 'ChildOf' else 'HAS_MEMBER'

def main():
  x2c = Xml2Cypher.parse('capec_v2.10.schema')
  
  nodeWriter = CypherWriter.CypherWriter('capec_v2.10-nodes.cql')
  rsWriter = CypherWriter.CypherWriter('capec_v2.10-relationships.cql')
  
  # CAPEC XML definitions
  capecXMLFile = 'capec_v2.10.xml'
  capecXMLEncoding = 'utf8'
  capecXMLNamespaces = { 'http://capec.mitre.org/capec-2': None }

  # Load XML file into a dictionary object
  with open(capecXMLFile, encoding=capecXMLEncoding) as fd:
    root = xmltodict.parse(
      fd.read(),
      namespaces =          capecXMLNamespaces,
      process_namespaces =  True
    )
    
    x2c.apply(root, nodeWriter, rsWriter, { 'filterComment': filterComment, 'splitString': splitString, 'structuredText': structuredText, 'parseRsTarget': parseRsTarget, 'parseRsNature': parseRsNature })
  
  nodeWriter.close()
  rsWriter.close()

main()