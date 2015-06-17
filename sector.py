#! /usr/bin/python3
#coding=utf-8

import card
import re
import time
import threading

def getHrefList(html):
    reg = r'<a href="(/p/.*?)"'
    charset = r'charset="(.*?)"'

    hrefRe = re.compile(reg)
    charsetRe = re.compile(charset)

    charsetStr = re.findall(charsetRe,html.decode('UTF-8','ignore'))

    if charsetStr is not None:
        hrefList = re.findall(hrefRe,html.decode(str(charsetStr[0]),'ignore'))
    else:
        hrefList = re.findall(hrefRe,html.decode('UTF-8','ignore'))
    return hrefList


def main():
    html = card.getHtml('http://tieba.baidu.com/f/good?kw=%E5%A3%81%E7%BA%B8&ie=utf-8')
    Dir = '/home/Coderec/d/'
    hrefList = getHrefList(html)
    for x in hrefList:
        while len(threading.enumerate())>7:
            pass
        try:
            card.forSector('http://tieba.baidu.com'+x,Dir)
        except Exception as e:
            continue


if __name__ == '__main__':
    main()
