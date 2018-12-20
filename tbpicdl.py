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
import os

#构建淘主图下载
class tb:
	def __init__(self,ids,size):
		self.ids=ids
		self.size=size

	def picdl(self):
		n=0
		idnum=len(set(self.ids))
		failid=[]
		if not os.path.exists(os.getcwd()+'/pic'):
			os.makedirs(os.getcwd()+'/pic')
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
					urllib.request.urlretrieve(picurl, "pic/%s.jpg" % str(i.replace('\n','')))
					n+=1
			except:
				failid.append(i.replace('\n',''))# None
		tkinter.messagebox.showinfo("提示","√任务完成")
		var.set('成功下载【'+str(n)+'】张主图,【'+str(idnum-n)+'】张失败!')
		fids.set(','.join(failid))
#关于
def aboutme():
	tkinter.messagebox.showinfo("关于","淘宝主图下载小助手V1.0\nBy 搭塔@datadt")
#帮助
def tips():
	tip.set('1.批量下载模式需提前将商品ID按行贴到同目录下ids.txt文件中;\n2.按需下载模式需在文本框输入单个或按英文逗号区分的多个ID;\n3.网页提取下载是根据网页源码加载分析的特殊方法,稳定性较差.')
#按需下载
def sigdl():
	sid=sigid.get().split(',')#获取文本框字符串值按逗号转列表
	tb(sid,setsize()).picdl()
#批量下载
def dobdl():
	sids=open("ids.txt","r",encoding='UTF-8').readlines()[1:]
	tb(sids,setsize()).picdl()
#按网页提取
def getitemids():
	global tburl
	try:
		tburl=askstring("Tips", "   请输入要下载图片所在的页面URL:\n当点击OK键后请耐心等待直至弹窗提醒！")
		headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.77 Safari/537.36'}
		html=requests.get(tburl,headers=headers).text
		pattern=re.compile('i/asynSearch.htm(.*?)" />')
		st=pattern.findall(html)
		asyurl=tburl.split('/')[0]+'//'+tburl.split('/')[2]+'/i/asynSearch.htm?callback=jsonp125&'+st[0].replace('amp;','').replace('?','')
		newhtml=requests.get(asyurl,headers=headers).text
		newpattern=re.compile(r'htm\?id=(.*?)&rn=')
		newids=newpattern.findall(newhtml)
		hid=[i for i in set(newids)]
		tb(hid,setsize()).picdl()
	except:
		tkinter.messagebox.showinfo("提示","请检查,URL有误或为空!")
		None
#显示失败ID
def vfailids():
	global fids
	l4=tk.Entry(myapp,textvariable=fids,font=('Microsoft YaHei UI',8),width=60).place(x=66,y=210)
#返回图片大小
def setsize():
	try:
		return int(lb1.get(lb1.curselection()))
	except:
		return int(800)
#设置图片大小
on_ck=False
def picsize():
	global on_ck
	if on_ck==False:
		on_ck=True
		lb1.place(x=10,y=100)
	else:
		on_ck=False
		lb1.place_forget()#当再次点击时，隐藏控件
#菜单
def menus(myapp):
    menu=tk.Menu(myapp)
    submenu1 = tk.Menu(menu, tearoff=1)#分窗,0为原窗,1为可拖动的新开窗
    submenu1.add_checkbutton(label='设置图片大小',command=picsize)#添加命令
    submenu1.add_command(label='网页提取下载',command=getitemids)#添加命令
    submenu1.add_command(label='查看失败的ID',command=vfailids)#添加命令
    menu.add_cascade(label='高级功能',menu=submenu1)#添加子选项
    submenu2 = tk.Menu(menu, tearoff=0)
    submenu2.add_command(label='提示',command=tips)
    submenu2.add_separator()#添加分隔线
    submenu2.add_command(label='关于',command=aboutme)
    menu.add_cascade(label='帮助',menu=submenu2)
    menu.add_cascade(label='退出',command=myapp.quit)
    myapp.config(menu=menu)

#主程序
myapp=tk.Tk()
myapp.title('淘宝主图下载')
myapp.resizable(0,0) #框体大小可调性，分别表示x,y方向的可变性
myapp.geometry('500x300')#主框体大小
menus(myapp)#启用菜单布局
frm=tk.Frame(myapp,width=500,height=165)#构建一个框架,放置主功能模块
frm.pack()
l1=tk.Label(frm,text='Hello,TB',font=('Arial',16),width=10,height=3,fg='blue').place(x=185,y=10)
b1=tk.Button(frm,text='批量下载',width=15,height=2,font=('Microsoft YaHei UI',12),fg='blue',bg='Coral',command=dobdl).place(x=50,y=100)
sigid=tk.StringVar()
b2=tk.Button(frm,text='按需下载',width=15,height=1,font=('Microsoft YaHei UI',12),fg='blue',bg='Coral',command=sigdl).place(x=290,y=100)
t=tk.Entry(frm,textvariable=sigid,width=22).place(x=290,y=140)
var = tk.StringVar()
l2=tk.Label(myapp,textvariable=var,font=('Microsoft YaHei UI',9),width=50,height=2,fg='blue').place(x=66,y=180)#下载完成状态标签
fids=tk.StringVar()
tip=tk.StringVar()
l3=tk.Label(myapp,textvariable=tip,justify=tk.LEFT,font=('Microsoft YaHei UI',8),width=50,height=3).place(x=66,y=230)#【帮助】-【提示】标签
lvar=tk.StringVar()
lvar.set((800,400,200))
lb1=tk.Listbox(myapp,listvariable=lvar,width=5,height=3)
lb1.select_set(0)#默认选中第一个
myapp.mainloop()
