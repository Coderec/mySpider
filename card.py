#! /usr/bin/python3
#coding=utf-8

import re
import urllib.request
import time
import threading
import os
import random
import socket
from queue import Queue

def getHtml(url):
    req = urllib.request.Request(url, headers = {
        'Connection': 'Keep-Alive',
        'Accept': 'text/html, application/xhtml+xml, */*',
        'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN;q=0.5,zh-Hans;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/34.0.1847.137 Safari/537.36 LBBROWSER'
    })
    page=urllib.request.urlopen(req,timeout=10)
    return page.read()

def getImageList(html):
    global title
    title = "无标题"

    '''charset匹配编码 reg1和reg2匹配图片 titlteReg匹配标题'''
    charset = r'charset="(.*?)"'
    # reg1 = r'src="(.*?\.(jpg|jpeg|png|gif))"'
    # reg2 = r"src='(.*?\.(jpg|jpeg|png|gif))'"
    reg3 = r"(src=.*?\.(jpg|jpeg|png|gif))"
    titleReg = r'<title>(.*?)</title>'

    '''编译正则'''
    # imgRe1 = re.compile(reg1)
    # imgRe2 = re.compile(reg2)
    imgRe3 = re.compile(reg3)
    titleRe = re.compile(titleReg)
    charsetRe = re.compile(charset)

    '''匹配编码时默认用utf8'''
    charsetStr = re.findall(charsetRe,html.decode('UTF-8','ignore'))

    '''若没有找到编码就使用utf8'''
    if charsetStr is not None:
        # imgList1 = re.findall(imgRe1,html.decode(str(charsetStr[0]),'ignore'))
        # imgList2 = re.findall(imgRe2,html.decode(str(charsetStr[0]),'ignore'))
        imgList3 = re.findall(imgRe3,html.decode(str(charsetStr[0]),'ignore'))
        titleList = re.findall(titleRe,html.decode(str(charsetStr[0]),'ignore'))
    else:
        imgList1 = re.findall(imgRe1,html.decode('UTF-8','ignore'))
        imgList2 = re.findall(imgRe2,html.decode('UTF-8','ignore'))
        imgList3 = re.findall(imgRe3,html.decode('UTF-8','ignore'))
        titleList = re.findall(titleRe,html.decode('UTF-8','ignore'))

    if titleList is not None:
        title = titleList[0]
    return imgList3

class Spider(threading.Thread):
    """self.name就是tilte """
    def __init__(self, name):
        super(Spider, self).__init__()
        self.name = name
        print(self.name+' started')
        print('''
        '''+str(len(threading.enumerate()))+'''个线程运行中...
        ''')

    def run(self):
        i=1
        global queue
        global Dir

        '''网址字典，用来随机选取网址赋给头部的referer'''
        refDic = {1:'http://baike.baidu.com/link?url=4Hhv-nFsuG8I1spmQ1goo8AgY12PbMnZ-drj-NB16K-_ZcCuCAiNiMOcGlrQPWSYk1dZ-x2Wcwd1QLqn7_Qds_',
        2:'https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&tn=baidu&wd=referer&rsv_pq=a41f0dc700003af7&rsv_t=baefAbldUzfiGw18W0zd2Av4g2ogS0t7%2FmypScWbCkCdkqzVYrhGV%2FuBTn4&rsv_enter=1&rsv_sug3=9&rsv_sug1=5&bs=reference',
        3:'http://image.baidu.com/i?tn=baiduimage&ps=1&ct=201326592&lm=-1&cl=2&nc=1&word=%E4%BA%A4%E9%80%9A&ie=utf-8',
        4:'https://www.baidu.com/',
        5:'http://www.googleforchina.com/index_desktop.html'}

        while True :
            headers = [('Host','img0.imgtn.bdimg.com'),
                        ('Connection', 'keep-alive'),
                        ('Cache-Control', 'max-age=0'),
                        ('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'),
                        ('User-Agent', 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/36.0.1985.125 Safari/537.36'),
                        ('Accept-Encoding','gzip,deflate,sdch'),
                        ('Accept-Language', 'zh-CN,zh;q=0.8'),
                        ('If-None-Match', '90101f995236651aa74454922de2ad74'),
                        ('referer',refDic[random.randrange(1,6,1)]),
                        ('If-Modified-Since', 'Thu, 01 Jan 1970 00:00:00 GMT')]
            opener = urllib.request.build_opener()
            opener.addheaders = headers
            try:
                imgUrl=queue.get(timeout=3)
            except Exception as e:
                print("下载结束: "+self.name+'\n')
                break
            try:
                tmpurl = imgUrl[0].replace('src=','').replace('\\','').replace('\&quot;','').replace('"','').replace("'",'')
                f = open(Dir+'%s%s.%s' %(self.name,i,imgUrl[1]),"wb")
                pic = opener.open(tmpurl)
                f.write(pic.read())
                pic.close()
                f.close()
                print(tmpurl+'\n完成'+str(i)+'张\n')
            except Exception as e:
                print("解析失败: "+self.name+'\n')
            finally :
                i+=1

def main():
    html = getHtml('http://tieba.baidu.com/p/3825522906?da_from=ZGFfbGluZT1EVCZkYV9wYWdlPTImZGFfbG9jYXRlPXAwMDA1JmRhX2xvY19wYXJhbT0xJmRhX3Rhc2s9dGJkYSZkYV9vYmpfaWQ9MTQ2MDAmZGFfb2JqX2dvb2RfaWQ9MjYwOTgmZGFfdGltZT0xNDM0NDY0MjI3JmRhX3JlZl9maWQ9NjA4&da_sign=a73a0f032613ae50e16f626de80f3fff&tieba_from=tieba_da')
    imgList = getImageList(html)
    global queue
    global Dir
    Dir = '/home/Coderec/d/'
    # +title+'/'
    if not os.path.exists(Dir):
        os.mkdir(Dir)
    queue = Queue()
    for x in imgList:
        queue.put(x)
    threading.stack_size(32768*16)
    socket.setdefaulttimeout(10)
    s = Spider('s1')
    s.start()


def forSector(url,D):
    print("downloading "+url)
    html = getHtml(url)
    imgList = getImageList(html)
    global Dir
    Dir = D +title+'/'
    if not os.path.exists(Dir):
        os.mkdir(Dir)
    global queue
    queue = Queue()
    for x in imgList:
        queue.put(x)
    threading.stack_size(32768*16)
    socket.setdefaulttimeout(10)
    s = Spider(title)
    s.start()

if __name__ == '__main__':
    main()
