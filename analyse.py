#coding:utf-8
import lxml
from lxml import etree

with open('k2.html','r') as fp:
	data = fp.read()

html = etree.HTML(data)
label_list = {}

def parser(html):
	tempdict = {}
	count = 0
	for child in html:
		temp_dict = {}
		temp_dict['name'] = child.tag
		temp_dict['node'] = parser(child)
		tempdict[count] = temp_dict
		count += 1
	return tempdict

def dict_to_tree(tree_dict):
	if not tree_dict.has_key('node'):
		return
	childnode = tree_dict['name']
	print childnode
	for key in tree_dict['node'].keys():
		dict_to_tree(tree_dict['node'][key])

if __name__ == '__main__':
	thisdict = parser(html)
	dictk = {}
	dictk['node'] = thisdict
	dictk['name'] = 'html'
	print dictk
	dict_to_tree(dictk)


