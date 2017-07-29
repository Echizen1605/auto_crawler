#coding:utf-8
import lxml
from lxml import etree
import requests
import re

reg = re.compile('<script.*?/script>', re.DOTALL)
reg_use = re.compile('comment|hidden|javascript|js|css', re.IGNORECASE)

with open('job1.html','rb') as fp:
	content = fp.read()
with open('job2.html','r') as fp:
	content1 = fp.read()

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
		if child.text != None:
			temp_dict['text'] = child.text.strip()
		else:
			temp_dict['text'] = None
		temp_dict['node'] = parser(child, temp_dict['path'])
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
	return dictk

def dict_to_tree(tree_dict, tree_list):
	if not tree_dict.has_key('node'):
		return
	tree_tuple = (tree_dict['path'], tree_dict['text'], str(tree_dict['attribute']))
	if len(reg_use.findall(str(tree_dict['attribute']))) == 0 or len(reg_use.findall(str(tree_dict['path']))) == 0:
		tree_list.append(tree_tuple)
	for key in tree_dict['node'].keys():
		dict_to_tree(tree_dict['node'][key], tree_list)

if __name__ == '__main__':
	list1 = []
	list2 = []
	thisdict = wrapper_tree(html)
	thatdict = wrapper_tree(html1)
	dict_to_tree(thisdict, list1)
	dict_to_tree(thatdict, list2)

	# list1 = list(set([item[0] for item in list1]))
	# list2 = list(set([item[0] for item in list2]))
	# print set(list1) - set(list2)

	sift_list = list(set(list1)-set(list2))

	for item in sift_list:
		xp = item[0]
		try:
			attr = eval(item[2])
		except Exception as ex:
			continue
		for at in attr.keys():
			xpa = xp + "/@" + at
			for sin_item in html.xpath(xpa):
				print sin_item
				