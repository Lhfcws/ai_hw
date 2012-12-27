#! /usr/bin/env python
#coding=utf-8

import urllib 
import re
import bs4
import HTMLParser
import html5lib
import datetime

def has_nickname(tag):
    return tag.has_key('nick-name')

def has_uid(tag):
    return tag.has_key('nick-name') and tag.has_key('href')

def extractRawData(text, f):
    re_h=re.compile('</?\w+[^>]*>')
    
   #'''从script中提取内容'''
    soup=bs4.BeautifulSoup(text)
    t=soup.select("script")
    for text in t:
        if str(text).find('"pid":"pl_weibo_feedlist"')>0:
            s=str(text)
            break

    start=s.find("html")
    start+=7
    html_parser = HTMLParser.HTMLParser()
    s = html_parser.unescape(s[start:-12])
    end=s.find("<!--")
    s=s[:end]
    s=re.sub(r"\\\/","/",s)
    s=s.decode("unicode_escape")

   #'''页面解析'''
    soup1=bs4.BeautifulSoup(s,"html5lib")

    contents=soup1.find_all("dl",{"class":"feed_list"})
 
    for i in contents:
        soup2=bs4.BeautifulSoup(str(i),from_encoding="utf-8")
        
       #'''提取mid'''
        mid=soup2.dl["mid"]
     #   print 'mid:%s' % mid
        
       #'''提取weibo内容'''
       #'''
        tweet=soup2.findAll('em')
        if soup2.dl.has_key("isforward"):
            
            isforward=1
            if len(tweet) == 3:
                retweetContent=re_h.sub('',str(tweet[2]))
   #             print 'retweetContent:%s' % retweetContent   #转发内容
   
                reAuthor=soup2.findAll(has_nickname)[-1].string
                reAuthor=re.sub(r'@','',reAuthor)
    #            print 'reAuthor:%s' % reAuthor  #转发weibo作者
        else:
            retweetContent=None
            reAuthor=None
       #'''
       #'''
        tweetContent=re_h.sub('',str(tweet[0]))
        p = re.compile("http[0-9|:|/| |.|a-z|A-Z]*")
#        p1 = re.compile("(/?\w+[^)]*)")
        tweetContent = re.sub(p, "", tweetContent)
#       tweetContent = re.sub(p1, "", tweetContent)
        print  tweetContent   #weibo内容
         
        author=soup2.findAll(has_nickname)[0].string
        #print 'author:%s' % author  #weibo作者
       #'''
        suid=soup2.findAll(has_uid)[0]['suda-data']
        uid=suid[-10:]
        
        #print '' % uid
        f.write(uid+"\n")
    
       #'''提取url'''
       #'''
        url_tag=soup2.find("a", mt="url")
        if url_tag!=None:
            url=url_tag.string 
        #    print 'url:%s' % url
        else:
            url=None
       #'''
        
       #'''提取weibo发布时间'''
        date=soup2.find_all('a','date')[-1]['date']
       # print 'date:%s' % date
        
       #'''获取地理信息'''
        geo_tag=soup2.findAll("p",{"class":"map_data"})

        if len(geo_tag)!=0:
            soup3=bs4.BeautifulSoup(str(geo_tag))
            geo=soup3.a['action-data'].split('&')[0]
            temp=str(geo).split('=')[-1]
            longitude=temp.split(',')[0]
            latitude=temp.split(',')[1]
           # print 'longitude:%s' % longitude
           # print 'latitude:%s' % latitude       
        else:
            geo_tag=None
            longitude=None
            latitude=None 
            
       #'''提取话题'''
        topic_tag=soup2.findAll("a",{"class":"a_topic"})
        if len(topic_tag)!=0:
            topic=re_h.sub('',str(topic_tag))
            #print 'topic:%s' % topic
        else:
            topic=None
        #print "\n"
    
def main():
    src="http://s.weibo.com/weibo/%25E6%25A2%2581%25E5%258D%259A&scope=ori&timescope=custom:2012-10-30:2012-10-30&Refer=g&page="
    for page in xrange(1, 51):
        f = open("uidlist","a")
        page = '%d' % page
        #url="http://s.weibo.com/weibo/%s&page=%s" % (keyword.encode('utf-8'), str(page))
        url = src + str(page)
        #print url
          
        mf = urllib.urlopen(url)
        c = mf.read()
        c = str(c)
           
        content = extractRawData(c, f)
        f.close()

if __name__ == '__main__':
    main()



