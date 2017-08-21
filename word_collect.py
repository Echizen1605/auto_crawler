#coding:utf-8
import lxml
from lxml import etree
import jieba
import jieba.analyse
with open('job1.html', 'rb') as fp:
	content = fp.read()
with open('job2.html', 'rb') as fp:
	content1 = fp.read()

html = etree.HTML(content)
word_list = html.xpath("/html/body/div[@class='dw_wp']/div[@id='resultList']/div[@class='el']/p[@class='t1 ']/span/a/text()")
html1 = etree.HTML(content1)
word_list.extend(html1.xpath("/html/body/div[@class='dw_wp']/div[@id='resultList']/div[@class='el']/p[@class='t1 ']/span/a/text()"))
new_word_list = [item.strip() for item in word_list]

cut_word_list = []
for word in new_word_list:
	cut_word_list.extend(jieba.cut(word, cut_all=False))

txt_content = ''
for eve_word in cut_word_list:
	txt_content += eve_word + ','
print txt_content

tags = jieba.analyse.extract_tags(txt_content, 50)
print "------------"
print tags

for i in tags:
	print i
