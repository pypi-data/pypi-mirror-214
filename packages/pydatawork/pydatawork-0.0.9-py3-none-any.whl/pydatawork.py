
# -*- coding: utf-8 -*-
import urllib.request
import json
import requests
import os



def break_words(stuff):
    """This function will break up words for us."""
    words = stuff.split(' ')
    return words

def sort_words(words):
    """Sorts the words.""" # 文档字符串，是注释的一种
    return sorted(words)

def print_first_word(words):
    """Prints the first word after popping it off."""
    word = words.pop(0)
    print(word)

def print_last_word(words):
    """Print the last word after popping it off."""
    word = words.pop(-1)
    print(word)

def sort_sentence(sentence):
    """Takes in a full sentence and returns the sorted words"""
    words = break_words(sentence)
    return sort_words(words)  # 没懂这个函数

def print_first_and_last(sentence):
    """Prints the first and last words of the sentence."""
    words = break_words(sentence)
    print_first_word(words)
    print_last_word(words)

def print_first_and_last_sorted(sentence):
    """Sorts the words then prints the first and last one."""
    words = sort_sentence(sentence)
    print_first_word(words)
    print_last_word(words)
    

def get_weibo(path,id,weibo_name):
    """
    path:输入存放路径；
    id:微博id；
    weibi_name:存放文件夹的名字。
    """
    path = path
    id = id # 在微博上获取

    proxy_addr = "122.241.72.191:808"
    weibo_name = weibo_name # 可以自定义名字


    def use_proxy(url, proxy_addr):
        req = urllib.request.Request(url)
        req.add_header("User-Agent",
                    "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.221 Safari/537.36 SE 2.X MetaSr 1.0")
        proxy = urllib.request.ProxyHandler({'http': proxy_addr})
        opener = urllib.request.build_opener(proxy, urllib.request.HTTPHandler)
        urllib.request.install_opener(opener)
        data = urllib.request.urlopen(req).read().decode('utf-8', 'ignore')
        return data


    def get_containerid(url):
        data = use_proxy(url, proxy_addr)
        content = json.loads(data).get('data')
        for data in content.get('tabsInfo').get('tabs'):
            if (data.get('tab_type') == 'weibo'):
                containerid = data.get('containerid')
        return containerid


    def get_userInfo(id):
        url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
        data = use_proxy(url, proxy_addr)
        content = json.loads(data).get('data')
        profile_image_url = content.get('userInfo').get('profile_image_url')
        description = content.get('userInfo').get('description')
        profile_url = content.get('userInfo').get('profile_url')
        verified = content.get('userInfo').get('verified')
        guanzhu = content.get('userInfo').get('follow_count')
        name = content.get('userInfo').get('screen_name')
        fensi = content.get('userInfo').get('followers_count')
        gender = content.get('userInfo').get('gender')
        urank = content.get('userInfo').get('urank')
        print("微博昵称：" + name + "\n" + "微博主页地址：" + profile_url + "\n" + "微博头像地址：" + profile_image_url + "\n" + "是否认证：" + str(verified) + "\n" + "微博说明：" + description + "\n" + "关注人数：" + str(guanzhu) + "\n" + "粉丝数：" + str(fensi) + "\n" + "性别：" + gender + "\n" + "微博等级：" + str(urank) + "\n")


    def get_weibo(id, file):
        global pic_num
        pic_num = 0
        i = 1
        while True:
            url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id
            weibo_url = 'https://m.weibo.cn/api/container/getIndex?type=uid&value=' + id + '&containerid=' + get_containerid(url) + '&page=' + str(i)
            try:
                data = use_proxy(weibo_url, proxy_addr)
                content = json.loads(data).get('data')
                cards = content.get('cards')
                if (len(cards) > 0):
                    for j in range(len(cards)):
                        print("-----正在爬取第" + str(i) + "页，第" + str(j) + "条微博------")
                        card_type = cards[j].get('card_type')
                        if (card_type == 9):
                            mblog = cards[j].get('mblog')
                            attitudes_count = mblog.get('attitudes_count')
                            comments_count = mblog.get('comments_count')
                            created_at = mblog.get('created_at')
                            reposts_count = mblog.get('reposts_count')
                            scheme = cards[j].get('scheme')
                            text = mblog.get('text')
                            if mblog.get('pics') != None:
                                # print(mblog.get('original_pic'))
                                # print(mblog.get('pics'))
                                pic_archive = mblog.get('pics')
                                for _ in range(len(pic_archive)):
                                    pic_num += 1
                                    print(pic_archive[_]['large']['url'])
                                    imgurl = pic_archive[_]['large']['url']
                                    img = requests.get(imgurl)
                                    # f = open(path + weibo_name + '\\' + str(pic_num) + str(imgurl[-4:]),'ab')  # 存储图片，多媒体文件需要参数b（二进制文件）# 原始代码
                                    f = open(os.path.join(path, weibo_name, str(pic_num) + str(imgurl[-4:])), 'ab') # 存储图片，多媒体文件需要参数b（二进制文件）
                                    f.write(img.content)  # 多媒体存储content
                                    f.close()

                            with open(file, 'a', encoding='utf-8') as fh:
                                fh.write("----第" + str(i) + "页，第" + str(j) + "条微博----" + "\n")
                                fh.write("微博地址：" + str(scheme) + "\n" + "发布时间：" + str(
                                    created_at) + "\n" + "微博内容：" + text + "\n" + "点赞数：" + str(
                                    attitudes_count) + "\n" + "评论数：" + str(comments_count) + "\n" + "转发数：" + str(
                                    reposts_count) + "\n")
                    i += 1
                else:
                    break
            except Exception as e:
                print(e)
                i += 1  # 添加这一行
                pass

    # # 在指定路径下，先建立一个名为weibo的文件夹
    # if os.path.isdir(os.path.join(path,"weibo")):
    #     pass
    # else:
    #     os.mkdir(os.path.join(path,"weibo"))

    if os.path.isdir(os.path.join(path,weibo_name)):
        pass
    else:
        os.mkdir(os.path.join(path,weibo_name))
    file = os.path.join(path, weibo_name, weibo_name + ".txt")

    get_userInfo(id)
    get_weibo(id, file)
    print("微博数据获取完毕")

