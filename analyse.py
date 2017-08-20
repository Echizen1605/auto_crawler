#coding:utf-8
import lxml
from lxml import etree
import requests
import re
import math
import jieba
import copy

reg = re.compile('<script.*?/script>', re.DOTALL)
reg1 = re.compile('<style.*?</style>', re.DOTALL)
reg2 = re.compile('<!--.*?-->', re.DOTALL)
reg_use = re.compile('comment|hidden|javascript|js|css', re.IGNORECASE)

with open('job1.html','rb') as fp:
	content = fp.read()
with open('job2.html','rb') as fp:
	content1 = fp.read()
# content = requests.get('https://job.dajie.com/80c1a5e9-668c-4c87-be30-052ffdf021e3.html').content
# content1 = requests.get('https://job.dajie.com/a8a0c51e-cbe4-4082-aa65-bcdc01389e2e.html').content

# content = requests.get('http://my.yingjiesheng.com/job_805115.html').content
# content1 = requests.get('http://my.yingjiesheng.com/job_805112.html').content
# with open('detail1.html', 'rb') as fp:
# 	content = fp.read()
# with open('detail2.html', 'rb') as fp:
# 	content1 = fp.read()


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
		temp_dict['index'] = html.index(child)
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
	# tree_list.append(tree_tuple)
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


class defined_pathlist(object):
	def __init__(self, mylist):
		self.mylist = mylist
	def __eq__(self, other):
		if len(self.mylist) == len(other.mylist):
			for i in range(len(self.mylist)):
				if self.mylist[i] != other.mylist[i]:
					return False
			return True
		else:
			return False
	def __hash__(self):
		return hash(tuple(self.mylist))


def cos_calculate(tree_list1, tree_list2):
	myset = set()
	tree1_set = set(tree_list1)
	tree2_set = set(tree_list2)
	myset.union(tree1_set)
	myset.union(tree2_set)
	result = len(tree1_set & tree2_set)/math.sqrt((len(tree1_set)*len(tree2_set)))
	print result

def cmp_html(x, y):
	return len(x.split('/'))-len(y.split('/'))

def calculate_prefix(list1):
	list_union = []
	compare_list_one = []
	compare_list_two = []
	path_list = ['/']
	for i in range(len(list1)):
		templist = list1[i].split('/')
		templist.remove('')
		list_union.append(defined_pathlist(templist))
		compare_list_one.append(copy.deepcopy(list1[i]))
		compare_list_two.append(copy.deepcopy(templist))
	print '************************************'
	temp_addition_list = []
	count = 0
	while True:
		list_union = list(set(list_union))
		if len(list_union) == 0:
			break
		remove_var = [k for k in list_union if k.mylist==[]]
		if len(remove_var) != 0:
			list_union.remove(remove_var[0])
		first_list = [i.mylist.pop(0) for i in list_union]
		first_str_list = list(set(first_list))
		temp_path_list = copy.deepcopy(path_list)
		temp_s_path_list = copy.deepcopy(path_list)
		for s_path in path_list:
			for k in first_str_list:
				for j in range(len(compare_list_one)):
					if compare_list_one[j].startswith(s_path):
						if len(compare_list_two[j]) - 1 >= count:
							if compare_list_two[j][count] == k:
								if first_list.count(k) > 1:
									temp_s_path_list[temp_s_path_list.index(s_path)] += k + '/'
									temp_s_path_list.append(s_path)
								else:
									temp_addition_list.append(temp_s_path_list[temp_s_path_list.index(s_path)][:-1])
		path_list = list(set(temp_s_path_list))
		for path in temp_path_list:
			path_list.remove(path)
		count += 1
	return list(set(temp_addition_list))

def parser_enhance(html, name):
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
			temp_dict['name'] = str(temp_dict['name']) + "[@class='" + child.get('class') + "' and position()=" + str(html.index(child)+1) + "]"
		elif child.get('name') != None:
			temp_dict['name'] = str(temp_dict['name']) + "[@name='" + child.get('name') + "' and position()=" + str(html.index(child)+1) + "']"
		elif len(temp_dict['attribute']) > 0:
			if type(temp_dict['attribute']) == 'dict':
				temp_dict['name'] += "[@" + temp_dict['attribute'].keys()[0] + "='" + temp_dict['attribute'][temp_dict['attribute'].keys()[0]] + "'"
				for key in temp_dict['attribute'].keys()[1:]:
					temp_dict['name'] += " and @" + key + "='" + temp_dict['attribute'][key] + "'"
				temp_dict['name'] += " and position()=" + str(html.index(child)+1) + "]"
		else:
			temp_dict['name'] += "[position()=" + str(html.index(child)+1) + "]"
		temp_dict['path'] = (path_str + str(temp_dict['name']))
		temp_dict['name'] = str(child.tag)
		if child.text != None:
			temp_dict['text'] = child.text.strip()
			temp_dict['tokens'] = jieba.lcut(temp_dict['text'], cut_all=False)
		else:
			temp_dict['text'] = None
			temp_dict['tokens'] = []
		temp_dict['node'] = parser_enhance(child, temp_dict['path'])
		tempdict[count] = temp_dict
		count += 1
	return tempdict


def bianli(tree_dict, sublist):
	global job_info
	sublist.append(tree_dict['path'])
	print tree_dict['text']
	print tree_dict['attribute']
	if tree_dict['text'] != None:
		if len(re.findall(u'下一页', tree_dict['text'])) > 0:
			job_info['page'] = tree_dict['attribute']['href']
			job_info['xpath'].append(tree_dict['path'])
			job_info['text'].append(tree_dict['text'])
	for key in tree_dict['node'].keys():
		bianli(tree_dict['node'][key],sublist)

def detect_xpath(given_xpath_list, html):
	import os.path
	for single_xpath in given_xpath_list:
		this_node = html.xpath(single_xpath)
		for eve_node in this_node:
			this_dict = parser_enhance(eve_node, single_xpath)
			my_dict = {}
			my_dict['node'] = this_dict
			my_dict['path'] = single_xpath
			my_dict['text'] = '开始'
			my_dict['attribute'] = None
			sublist = []
			bianli(my_dict, sublist)
			for item in list(set(sublist)):
				print item
			print '***********************************'

		that_node = html1.xpath(single_xpath)
		for eve_node in that_node:
			this_dict = parser_enhance(eve_node, single_xpath)
			my_dict = {}
			my_dict['node'] = this_dict
			my_dict['path'] = single_xpath
			my_dict['text'] = '开始'
			my_dict['attribute'] = None
			sublist = []
			bianli(my_dict, sublist)
			for item in list(set(sublist)):
				print item
			print '***********************************'

def classify(xpath_list, html, cross_list):
	xpath_info = {}
	count = 0
	for single_xpath in xpath_list:
		templist = []
		tempdict = {}
		for every_xpath in cross_list:
			if every_xpath.startswith(single_xpath):
				now_html = html.xpath(every_xpath + '/text()')
				templist = [text_content.strip() for text_content in now_html]
				tempdict[every_xpath] = templist
		xpath_info[count] = tempdict
		cross_list.remove(every_xpath)
		count += 1
	print xpath_info.keys()
	print xpath_info

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
	
	ownset = (myset - hisset) ^ (hisset - myset)

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
	xpath_list.sort(cmp_html)
	for i in xpath_list:
		print i

	print calculate_prefix(xpath_list)
	job_info = {}
	job_info['xpath'] = []
	job_info['text'] = []
	detect_xpath(calculate_prefix(xpath_list), html)
	print job_info

	new_list = calculate_prefix(xpath_list)
	new_list.sort(cmp_html, reverse=True)
	print new_list

	classify(new_list, html, xpath_list)
	

