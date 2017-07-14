#coding:utf-8
import lxml
from lxml import etree

with open('k.html','r') as fp:
	data = fp.read()

html = etree.HTML(data)
label_list = {}

def parser(html):
	tempdict = {}
	temp_dict = {}
	count = 0
	for child in html:
		temp_dict['name'] = child.tag
		temp_dict['node'] = parser(child)
		tempdict[count] = temp_dict
		count += 1
	return tempdict

if __name__ == '__main__':
	print parser(html)
