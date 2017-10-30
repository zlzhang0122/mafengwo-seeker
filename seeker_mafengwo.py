#!/usr/bin/python
# -*- encoding:utf-8 -*-

import urllib,time,requests,json
from lxml import etree
import pandas as pd

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def getPage(url):
    page = urllib.urlopen(url)
    html = page.read()
    return html

def getList():
    sightlist = []
    address = raw_input("请输入目的景点:")
    url = 'http://www.mafengwo.cn/search/s.php?q=' + str(address) + '&p={}' + '&t=poi&kt=1'
    i = 1
    while i <= 50:
        html = getPage(url.format(i))
        selector = etree.HTML(html)
        print '正在爬取第' + str(i) + '页的信息...'
        i += 1
        informations = selector.xpath('//div[@class="att-list"]/ul/li')
        #获取结果信息
        for inf in informations:
            sight_names = inf.xpath('./div/div[@class="ct-text "]/h3/a/text()')[0]
            sight_name = sight_names
            if sight_names.strip() != '':
                sight_name_list = sight_names.split("-")
                if len(sight_name_list) > 1:
                    sight_name = sight_name_list[1]
                    if sight_name.strip() != '':
                        sight_name = sight_name.replace(' ', '')
                        sight_name = sight_name.strip().encode(encoding='utf-8')
            sight_areas = inf.xpath('./div/div[@class="ct-text "]/ul/li[1]/a/text()')[0]
            sight_area = sight_areas
            if sight_area.strip() != '':
                sight_area_list = sight_area.split('-')
                if len(sight_area_list) > 1:
                    sight_area_name = sight_area_list[0]
                    sight_area_name_city = sight_area_list[1]
                    if sight_area_name.strip() != '' and sight_area_name == "中国" and sight_area_name_city.strip() != '':
                        sight_area = sight_area_name_city.encode(encoding='utf-8')
                    else:
                        sight_area = sight_area_name.encode(encoding='utf-8')
            sight_comments = inf.xpath('./div/div[@class="ct-text "]/ul/li[2]/a/text()')[0]
            sight_comment = sight_comments
            if sight_comments.strip() != '':
                sight_comment_list = sight_comments.split('(')
                if len(sight_comment_list) > 1:
                    sight_comment_more = sight_comment_list[1]
                    if sight_comment_more.strip() != '':
                        sight_comment = sight_comment_more[:-1]
                        if sight_comment.strip() != '':
                            sight_comment = sight_comment.encode(encoding='utf-8')
            sight_notes = inf.xpath('./div/div[@class="ct-text "]/ul/li[3]/a/text()')[0]
            sight_note = sight_notes
            if sight_notes.strip() != '':
                sight_note_list = sight_notes.split('(')
                if len(sight_note_list) > 1:
                    sight_note_more = sight_note_list[1]
                    if sight_note_more.strip() != '':
                        sight_note = sight_note_more[:-1]
                        if sight_note.strip() != '':
                            sight_note = sight_note.encode(encoding='utf-8')
            sightlist.append([sight_name, sight_area, sight_comment, sight_note])
            time.sleep(3)
    return sightlist,address

def listToExcel(list, name):
    df = pd.DataFrame(list, columns=['景点名称', '所在区域', '评论数', '游记数'])
    df.to_excel(name + '景点信息.xlsx', sheet_name='Sheet1')

def getBaiduGeo(sightlist):
    #百度密钥
    ak = '您的百度密钥'

    list = sightlist
    bjsonlist = []
    ejsonlist1 = []
    ejsonlist2 = []
    num=1
    for l in list:
        try:
            address = l[0]
            url = 'http://api.map.baidu.com/geocoder/v2/?address=' + address + '&output=json&ak=' + ak
            json_data = requests.get(url=url).json()
            json_geo = json_data['result']['location']
        except KeyError, e:
            print e.message
            continue
        try:
            json_geo['count'] = int(l[2]) * 0.03 + int(l[3]) * 0.07
            bjsonlist.append(json_geo)
            ejson1 = {l[0] : [json_geo['lng'], json_geo['lat']]}
            ejsonlist1 = dict(ejsonlist1, **ejson1)
            ejson2 = {'name': l[0], 'value': int(l[2]) * 0.03 + int(l[3]) * 0.07}
            ejsonlist2.append(ejson2)
            print '正在生成第' + str(num) + '个景点的经纬度'
            num += 1
        except Exception,e:
            print e.message
            continue
    bjsonlist = json.dumps(bjsonlist)
    ejsonlist1 = json.dumps(ejsonlist1, ensure_ascii=False)
    ejsonlist2 = json.dumps(ejsonlist2, ensure_ascii=False)
    with open('./points.json', "w") as f:
        f.write(bjsonlist)
    with open('./geoCoordMap.json', "w") as f:
        f.write(ejsonlist1)
    with open('./data.json', "w") as f:
        f.write(ejsonlist2)

def main():
    sightlist, address = getList()
    listToExcel(sightlist, address)
    getBaiduGeo(sightlist)

if __name__ == '__main__':
    main()