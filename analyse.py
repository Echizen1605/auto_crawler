#coding:utf-8
import lxml
from lxml import etree
import requests
import re
import math
import jieba

reg = re.compile('<script.*?/script>', re.DOTALL)
reg1 = re.compile('<style.*?</style>', re.DOTALL)
reg2 = re.compile('<!--.*?-->', re.DOTALL)
reg_use = re.compile('comment|hidden|javascript|js|css', re.IGNORECASE)

# with open('job1.html','rb') as fp:
# 	content = fp.read()
# with open('job2.html','rb') as fp:
# 	content1 = fp.read()
content = requests.get('https://job.dajie.com/80c1a5e9-668c-4c87-be30-052ffdf021e3.html').content
content1 = requests.get('https://job.dajie.com/a8a0c51e-cbe4-4082-aa65-bcdc01389e2e.html').content

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
			temp_dict['tokens'] = jieba.lcut(temp_dict['text'], cut_all=False)
		else:
			temp_dict['text'] = None
			temp_dict['tokens'] = []
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
	dictk['tokens'] = []
	return dictk

def dict_to_tree(tree_dict, tree_list):
	if not tree_dict.has_key('node'):
		return
	tree_tuple = (tree_dict['index'], tree_dict['path'], tree_dict['text'], str(tree_dict['attribute']), str(tree_dict['tokens']))
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


class defined_cos(object):
	def __init__(self, mytuple):
		self.mytuple = mytuple
	def __eq__(self, other):
		return self.mytuple[1] == other.mytuple[1] and self.mytuple[3] == other.mytuple[3]
	def __hash__(self):
		return hash(self.mytuple[1]) ^ hash(self.mytuple[3])


def cos_calculate(tree_list1, tree_list2):
	myset = set()
	tree1_set = set(tree_list1)
	tree2_set = set(tree_list2)
	# print len(tree1_set)
	# print len(tree2_set)
	# print len(tree1_set & tree2_set)
	myset.union(tree1_set)
	myset.union(tree2_set)
	result = len(tree1_set & tree2_set)/math.sqrt((len(tree1_set)*len(tree2_set)))
	print result

def cmp_html(x, y):
	return len(x)-len(y)


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
				lcut_list = jieba.lcut(k.xpath('text()')[0], cut_all=False)
				print "-------------------------"
				print "FOLLOWING CUT_LIST:"
				print "-------------------------"
				if '职位' in lcut_list:
					for item in lcut_list:
						print item

	cos_calculate(list1, list2)
	# xpath_list.sort(cmp_html)
	# for i in xpath_list:
	# 	print i
