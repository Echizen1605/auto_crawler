#coding:utf-8
import lxml
from lxml import etree
import requests
import re

reg = re.compile('<script.*?/script>', re.DOTALL)
reg1 = re.compile('<style.*?</style>', re.DOTALL)
reg2 = re.compile('<!--.*?-->', re.DOTALL)
reg_use = re.compile('comment|hidden|javascript|js|css', re.IGNORECASE)

with open('job1.html','rb') as fp:
	content = fp.read()
with open('job2.html','rb') as fp:
	content1 = fp.read()

content = reg.sub('',reg1.sub('',reg2.sub('',content)))
content1 = reg.sub('',reg1.sub('',reg2.sub('',content1)))
html = etree.HTML(content)
html1 = etree.HTML(content1)

def parser(html, name):
	tempdict = {}
	count = 0
	path_str = name + '/'
	for child in html:
		temp_dict = {}
		temp_dict['name'] = str(child.tag)
		temp_dict['attribute'] = child.attrib
		if child.get('id') != None:
			temp_dict['name'] = str(temp_dict['name']) + "[@id='" + child.get('id') + "']"
		elif child.get('class') != None:
			temp_dict['name'] = str(temp_dict['name']) + "[@class='" + child.get('class') + "']"
		elif child.get('name') != None:
			temp_dict['name'] = str(temp_dict['name']) + "[@name='" + child.get('name') + "']"
		elif len(temp_dict['attribute']) > 0:
			if type(temp_dict['attribute']) == 'dict':
				temp_dict['name'] += "[@" + temp_dict['attribute'].keys()[0] + "='" + temp_dict['attribute'][temp_dict['attribute'].keys()[0]] + "'"
				for key in temp_dict['attribute'].keys()[1:]:
					temp_dict['name'] += " and @" + key + "='" + temp_dict['attribute'][key] + "'"
				temp_dict['name'] += "]"
		temp_dict['path'] = (path_str + str(temp_dict['name']))
		temp_dict['name'] = str(child.tag)
		if child.text != None:
			temp_dict['text'] = child.text.strip()
		else:
			temp_dict['text'] = None
		temp_dict['node'] = parser(child, temp_dict['path'])
		temp_dict['index'] = count + 1
		tempdict[count] = temp_dict
		count += 1
	return tempdict

def wrapper_tree(html):
	tree_dict = parser(html, '/html')
	dictk = {}
	dictk['node'] = tree_dict
	dictk['name'] = 'html'
	dictk['text'] = None
	dictk['attribute'] = {}
	dictk['path'] = '/html'
	dictk['index'] = 1
	return dictk

def dict_to_tree(tree_dict, tree_list):
	if not tree_dict.has_key('node'):
		return
	tree_tuple = (tree_dict['index'], tree_dict['path'], tree_dict['text'], str(tree_dict['attribute']))
	if len(reg_use.findall(str(tree_dict['attribute']))) == 0 or len(reg_use.findall(str(tree_dict['path']))) == 0:
		tree_list.append(tree_tuple)
	tree_list.append(tree_tuple)
	for key in tree_dict['node'].keys():
		dict_to_tree(tree_dict['node'][key], tree_list)


def get_ctokens(*dict_tree):
	ctoken_list = []
	for tree in dict_tree:
		ctoken_list.append(tree)
	print ctoken_list


class defined_tuple(object):
	def __init__(self, mytuple):
		self.mytuple = mytuple
	def __eq__(self, other):
		return self.mytuple[1] == other.mytuple[1] and self.mytuple[2] == other.mytuple[2]
	def __hash__(self):
		return hash(self.mytuple[1]) ^ hash(self.mytuple[2])


if __name__ == '__main__':
	list1 = []
	list2 = []
	thisdict = wrapper_tree(html)
	thatdict = wrapper_tree(html1)
	dict_to_tree(thisdict, list1)
	dict_to_tree(thatdict, list2)

	myset = set()
	for i in list1:
		myset.add(defined_tuple(i))

	hisset = set()
	for j in list2:
		hisset.add(defined_tuple(j))
	
	ownset = myset - hisset

	xpath_set = set()
	for item in ownset:
		xpath_set.add(item.mytuple[1])
	
	xpath_list = list(xpath_set)
	for item in xpath_list:
		print item
		print len(html.xpath(item))
		for k in html.xpath(item):
			if len(k.xpath('text()')) > 0:
				print k.xpath('text()')[0]