# -*- coding:utf-8 -*-
import re
import requests
from urllib import error
from bs4 import BeautifulSoup
import os
#导入所需模块，获取URL信息，抓取内容
num = 0
numPicture = 0
file = ''
List = []
#初始化列表，变量
def Find(url):
    global List
    print('正在智能检测图片总数，请稍等.....')
    t = 0
    i = 1
    s = 0
    while t < 100: #限制最大的图片可下载数量
        Url = url + str(t) + '&gsm=8c'
        try:
            Result = requests.get(Url, timeout=7)
        except BaseException:
            t = t+60
            continue
        else:
            result = Result.text
            pic_url = re.findall('"objURL":"(.*?)",', result, re.S)  # 先利用正则表达式找到图片url
            # pic_url是一个列表，正则表达式，找到图片地址，网页查看源代码。
            # 使用re.S参数以后，正则表达式会将这个字符串作为一个整体，在整体中进行匹配。
            # 从"objURL"开始，到(.*?)结束。  .*?代表尽可能少匹配，找了一个再找另一个
            s += len(pic_url)
            if len(pic_url) == 0:
                break
            else:
                List.append(pic_url)
                t = t + 60
    return s

def recommend(url): #定义提醒函数
    Re = []
    try:
        html = requests.get(url)
    except error.HTTPError as e:
        return
    else:
        html.encoding = 'utf-8'
        bsObj = BeautifulSoup(html.text, 'html.parser')
        div = bsObj.find('div', id='topRS')
        if div is not None:
            listA = div.findAll('a')
            for i in listA:
                if i is not None:
                    Re.append(i.get_text())
        return Re

def dowmloadPicture(html, keyword):
    global num
    pic_url = re.findall('"objURL":"(.*?)",', html, re.S)  # 利用正则表达式找到图片url
    print('找到关键词:' + keyword + '的图片，即将开始下载图片...')
    for each in pic_url:
        print('正在下载第' + str(num + 1) + '张图片，图片地址:' + str(each))
        try:
            if each is not None:
                pic = requests.get(each, timeout=10)
            else:
                continue
        except BaseException:
            print('错误，当前图片无法下载') #网络等原因导致无法下载的图片给出提示
            continue
        else:
            if num < 9:
                string = file + r'\\' + '0'+ str(num+1) + '.jpg'
            elif num >= 9:
                string = file + r'\\' + str(num + 1) + '.jpg'
            fp = open(string, 'wb')
            fp.write(pic.content)
            fp.close() #关闭文件操作
            num += 1
        if num >= numPicture:
            return

if __name__ == '__main__':  # 主函数入口
    word = input("请输入搜索关键词(可以是人名，地名等): ")
    url = 'http://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word='+word+'&ct=201326592&v=flip'
    # 查询网址，观察word，格式，flip代表关闭ajex即时刷新
    tot = Find(url)
    Recommend = recommend(url)  # 记录相关推荐
    print('经过检测%s类图片共有%d张' % (word, tot))
    numPicture = int(input('请输入想要下载的图片数量：  '))
    file = input('请建立一个存储图片的文件夹，输入文件夹名称即可： ')
    y = os.path.exists(file)
    if y == 1:
        print('该文件已存在，请重新输入')
        file = input('请建立一个存储图片的文件夹，输入文件夹名称即可： ')
        os.mkdir(file)
    else:
        os.mkdir(file) #调用OS库，新建文件夹
    t = 0
    while t < numPicture:
        try:
            url = url + '&pn='+str(t) + '&gsm=8c'
            result = requests.get(url, timeout=10)
        except error.HTTPError as e:
            print('网络错误，请调整网络后重试')
        else:
            dowmloadPicture(result.text, word)
        finally:
            t = t+20
    print('当前搜索结束，感谢使用') #结束提示
    for re in Recommend:
        print(re, end='  ')