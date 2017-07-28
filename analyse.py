#coding:utf-8
import lxml
from lxml import etree
import requests
import re

reg = re.compile('<script.*?/script>', re.DOTALL)
reg_use = re.compile('comment|hidden', re.IGNORECASE)

#------------------------------------------------------------------------------------------
#  FOR TEST
# data = requests.get('http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=010000%2C00&district=000000&funtype=0000&industrytype=32&issuedate=9&providesalary=99&keyword=%E5%89%8D%E7%AB%AF%E5%BC%80%E5%8F%91&keywordtype=2&curr_page=1&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9')
# content = reg.sub('', data.content)
# data1 = requests.get('http://search.51job.com/jobsearch/search_result.php?fromJs=1&jobarea=010000%2C00&district=000000&funtype=0000&industrytype=32&issuedate=9&providesalary=99&keyword=%E5%89%8D%E7%AB%AF%E5%BC%80%E5%8F%91&keywordtype=2&curr_page=2&lang=c&stype=1&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&lonlat=0%2C0&radius=-1&ord_field=0&list_type=0&fromType=14&dibiaoid=0&confirmdate=9')
# content1 = reg.sub('', data1.content)
# with open('job1.html','w') as fp:
# 	fp.write(content)
# with open('job2.html','w') as fp:
# 	fp.write(content1)
#------------------------------------------------------------------------------------------

with open('job1.html','r') as fp:
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
			temp_dict['name'] = str(temp_dict['name']) + "[@class='" + child.get('name') + "']"
		elif len(temp_dict['attribute']) > 0:
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

# def dict_to_tree(tree_dict):
# 	if not tree_dict.has_key('node'):
# 		return
# 	print tree_dict['path'],'->',tree_dict['name'],'->',tree_dict['text'],'->',tree_dict['attribute']
# 	for key in tree_dict['node'].keys():
# 		dict_to_tree(tree_dict['node'][key])

def dict_to_tree(tree_dict, tree_list):
	if not tree_dict.has_key('node'):
		return
	tree_tuple = (tree_dict['path'], tree_dict['text'], str(tree_dict['attribute']))
	if len(reg_use.findall(tree_dict['path'])) == 0:
		# flag = True
		# for item in tree_dict['attribute']:
		# 	if len(reg_use.findall(tree_dict['attribute'][item])) != 0:
		# 		flag = False
		# 		break
		# if flag:
		# 	tree_list.append(tree_tuple)
		tree_list.append(tree_tuple)
	for key in tree_dict['node'].keys():
		dict_to_tree(tree_dict['node'][key], tree_list)

def cross_tree(tree_dict1, tree_dict2):
	pass


def judge_tree(tree_dict1, tree_dict2):
	if tree_dict1 == tree_dict2:
		return True
	else:
		return False


def cut_tree(tree_dict1, tree_dict2, tree):
	pass

# def dict_to_tree(tree_dict, name):
# 	if not tree_dict.has_key('node'):
# 		return
# 	path_str = name + '/' + str(tree_dict['name'])
# 	print path_str, tree_dict['text'], tree_dict['attribute']
# 	for key in tree_dict['node'].keys():
# 		dict_to_tree(tree_dict['node'][key],path_str)


if __name__ == '__main__':
	list1 = []
	list2 = []
	thisdict = wrapper_tree(html)
	thatdict = wrapper_tree(html1)
	dict_to_tree(thisdict, list1)
	dict_to_tree(thatdict, list2)

	# total_list = []
	# total_list.extend(list1)
	# total_list.extend(list2)
	# cross_list = list(set(total_list))
	# print len(cross_list)
	# print list1


	# list1_set = set(list1)
	# list2_set = set(list2)
	# print list1_set
	# cross_set = list1_set & list2_set
	# own_set = list1_set - cross_set
	# gen = [str(item[0])+"ECHIZEN"+str(item[1]) + "ECHIZEN"+str(item[2]) for item in list1_set]
	gen = [str(item) for item in list1]
	print list1
	# print set(gen)

	sift_list = list(gen)
	for xp in sift_list:
		xp = eval(xp)
		single = xp[1]
		print single

	# sift_list = list(set(gen))
	# for xp in sift_list:
	# 	mygroup = xp.split('ECHIZEN')
	# 	attri = eval(mygroup[1])
	# 	for key in attri.keys():
	# 		single = mygroup[0] + "/@" + key
	# 		print html.xpath(single)[0],
	# 	print '\r\n'