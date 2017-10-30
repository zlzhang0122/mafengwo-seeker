#!/usr/bin/python
# -*- encoding:utf-8 -*-

import xlrd

worksheet = xlrd.open_workbook(u'中国景点信息.xlsx')
sheet_names = worksheet.sheet_names()
inf_list = []
add_list = []
for sheet_name in sheet_names:
    sheet1 = worksheet.sheet_by_name(sheet_name)
    i= 0
    while i < 750:
        rows = sheet1.row_values(i)
        i+=1
        inf_list.append(rows)
    del inf_list[0]
    for li in inf_list:
        li[2] = li[2].split('.')[0]
        li[3] = li[3].split('.')[0]

    ##前二十个景点倒序
    j=0
    list=[]
    top_list = []
    name_list = []
    while j<21:
        rows = sheet1.row_values(j)
        j+=1
        list.append(rows)
    del list[0]
    k=1
    for li in list:
        top_list.append(str(int(li[3]) + int(li[4])))
        name_list.append(str(li[1].encode('utf-8')))
        k+=1
    top_list.reverse()
    name_list.reverse()
    print("First 20:")
    print (top_list)
    for item in name_list:
        print item,

    top_20_place_key = []
    top_20_place_value = []
    for_sort_dict = {}
    for item in inf_list:
        for_sort_dict.update({item[1].encode('utf-8'):str(int(item[3]) * 0.03 + int(item[4]) * 0.07)})
    for_sort_dict = sorted(for_sort_dict.iteritems(), key = lambda d:d[1], reverse=True)
    t=0
    for item in for_sort_dict:
        if t < 20:
            top_20_place_key.append(item[0])
            top_20_place_value.append(item[1])
            t+=1
    print("\nTop 20:")
    for item in top_20_place_key:
        print item,
    print("\nNum:")
    print(top_20_place_value)

    for li in inf_list:
        add_list.append(li[2])
    add_key = []
    add_value = []
    add = set(add_list)
    add_dict = {}
    for item in add:
        add_dict.update({item:add_list.count(item)})
    s_add_dict = sorted(add_dict.items(), key = lambda d:d[1])
    for value in s_add_dict:
        add_key.append(value[0])
        add_value.append(value[1])
    print("Address:")
    for item in add_key:
        print item,
    print("\nCount:")
    print(add_value)

    comment_list = []
    comment_key = []
    comment_value = []
    for itemAdd in add_key:
        comment = []
        i = 0
        while i < 749:
            if inf_list[i][2].encode("utf-8") == str(itemAdd.encode("utf-8")):
                comment.append(int(inf_list[i][3]) * 0.03 + int(inf_list[i][4]) * 0.07)
            i+=1
        maxcomment = max(comment)
        mincomment = min(comment)
        average = "{:.2f}".format(sum(comment)/len(comment))
        comment_list.append([mincomment, maxcomment, average])
    comment_dict = dict(zip(add_key, comment_list))
    s_comment_dict = sorted(comment_dict.items(), key = lambda d:d[1][1], reverse=True)
    for value in s_comment_dict:
        comment_key.append(value[0])
        comment_value.append(value[1])
    print("Comment:")
    for item in comment_key:
        print item,
    print("\ncomment:")
    print(comment_value)