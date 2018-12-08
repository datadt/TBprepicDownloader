# !/usr/bin/env python
# -*- coding: utf-8 -*-
'''
@Author:      datadt
@Tool:        Sublime Text3
@DateTime:    2018-12-06 19:22:14
'''
# subject:tk learning
import requests
from bs4 import BeautifulSoup
import urllib.request
import re
import tkinter as tk
import tkinter.messagebox
from tkinter.simpledialog import askstring

class tb:
	def __init__(self,ids,size):
		self.ids=ids
		self.size=size

	def picdl(self):
		n=0
		idnum=len(set(self.ids))
		failid=[]
		for i in set(self.ids):
			url='https://item.taobao.com/item.htm?id='+str(i.replace('\n',''))
			soup=BeautifulSoup(requests.get(url).text,'lxml')
			try:
				try:
					try:
						s=soup.find_all('ul',attrs={'id':'J_UlThumb'})[0]#解决颜色等分类描述没有图片的情况，按照第一张预览图取主图 way1
					except:
						s=soup.find_all('img',attrs={'id':'J_ImgBooth'})[0]#取第一张图 way2
				except:
					try:
						s=soup.find_all('dl',attrs={'class':'tb-prop tm-sale-prop tm-clear tm-img-prop '})[0]#列表内元素，链接多商品的情况下取第一个商品图片链接 way3
					except:
						s=soup#直接从网页源获取 way4
				finally:
					pattern=re.compile('//(.*?)_\d+x\d+q90.jpg')
					result=pattern.findall(str(s))[0]
					picurl='https://'+result+'_'+str(self.size)+'x'+str(self.size)+'q90.jpg'
					urllib.request.urlretrieve(picurl, "%s.jpg" % str(i.replace('\n','')))
					n+=1
			except:
				failid.append(i.replace('\n',''))# None
		tkinter.messagebox.showinfo("提示","任务完成")
		var.set('成功下载【'+str(n)+'】张主图,【'+str(idnum-n)+'】张失败!')
		fids.set(','.join(failid))

def sigdl():
	sid=sigid.get().split(',')#获取文本框字符串值按逗号转列表
	tb(sid,800).picdl()

def aboutme():
	tkinter.messagebox.showinfo("关于","淘宝主图下载小助手V1.0\nBy 搭塔@datadt")

def tips():
	tip.set('1.批量下载模式需提前将商品ID按行贴到同目录下ids.txt文件中;\n2.按需下载模式需在文本框输入单个ID也可按英文,分开的多个ID.')

def getitemids():
	global tburl
	try:
		tburl=askstring("Tips", "   请输入要下载图片所在的页面URL\n当点击OK键后请耐心等待直至弹窗提醒！")
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
		html=requests.get(tburl,headers=headers).text
		pattern=re.compile('i/asynSearch.htm(.*?)" />')
		st=pattern.findall(html)
		asyurl=tburl.split('/')[0]+'//'+tburl.split('/')[2]+'/i/asynSearch.htm?callback=jsonp125&'+st[0].replace('amp;','').replace('?','')
		newhtml=requests.get(asyurl,headers=headers).text
		newpattern=re.compile(r'htm\?id=(.*?)&rn=')
		newids=newpattern.findall(newhtml)
		hid=[i for i in set(newids)]
		tb(hid,800).picdl()
	except:
		tkinter.messagebox.showinfo("提示","URL有误或为空")
		None

def vfailids():
	global fids
	l4=tk.Entry(window,textvariable=fids,font=('Microsoft YaHei UI',8),width=60)#功能正在加紧开发中
	l4.place(x=66,y=210)

def menus(window):
    menu=tk.Menu(window)
    submenu1 = tk.Menu(menu, tearoff=0)
    submenu1.add_checkbutton(label='网页提取下载',command=getitemids)#添加命令
    submenu1.add_checkbutton(label='查看失败的ID',command=vfailids)#添加命令
    menu.add_cascade(label='高级功能',menu=submenu1)#添加子选项
    submenu2 = tk.Menu(menu, tearoff=0)
    submenu2.add_command(label='提示',command=tips)
    submenu2.add_separator()#添加分隔线
    submenu2.add_command(label='关于',command=aboutme)
    menu.add_cascade(label='帮助',menu=submenu2)
    menu.add_cascade(label='退出',command=window.quit)
    window.config(menu=menu)

window=tk.Tk()
window.title('淘宝主图下载')
window.geometry('500x300')
menus(window)
l1=tk.Label(window,text='Hello,TB\n',font=('Arial',16),width=15,height=5,fg='blue')        
l1.pack()
sids=open("ids.txt","r",encoding='UTF-8').readlines()[1:]
b1=tk.Button(window,text='批量下载',width=15,height=2,font=('Microsoft YaHei UI',12),fg='blue',bg='Coral',command=tb(sids,800).picdl)
b1.place(x=50,y=100)
sigid=tk.StringVar()
t=tk.Entry(window,textvariable=sigid,width=22)
t.place(x=290,y=140)
b2=tk.Button(window,text='按需下载',width=15,height=1,font=('Microsoft YaHei UI',12),fg='blue',bg='Coral',command=sigdl)
b2.place(x=290,y=100)
var = tk.StringVar()
l2=tk.Label(window,textvariable=var,font=('Microsoft YaHei UI',9),width=50,height=2,fg='blue')
l2.place(x=66,y=180)
fids=tk.StringVar()
tip=tk.StringVar()
l3=tk.Label(window,textvariable=tip,font=('Microsoft YaHei UI',8),width=50,height=3)#提示标签
l3.place(x=66,y=230)
window.mainloop()