import requests
from PIL import Image
import re

session = requests.Session()


class NotMatchException(Exception):
    pass


def get_uuid():
    r = session.get(
        'https://login.wx.qq.com/jslogin?appid=wx782c26e4c19acffb&redirect_uri=https%3A%2F%2Fwx.qq.com%2Fcgi-bin%2Fmmwebwx-bin%2Fwebwxnewloginpage&fun=new&lang=zh_CN&_=1490617350290')
    uuid = re.findall('"(.*?)"', r.text)
    if len(uuid) != 1:
        raise NotMatchException("uuid not match")
    return uuid[0]


def verify_qrcode(uuuuuuid):
    url = f'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={uuuuuuid}&tip=1&r=-263699104&_=1490617350291'
    r = session.get(url)
    assert r.text == 'window.code=408;', 'error'


def qrcode(uuuuuuid):
    url = f'https://login.weixin.qq.com/qrcode/{uuuuuuid}'
    return session.get(url)


def redirect_url(uuuuuuid):
    url = f'https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid={uuuuuuid}&tip=0&r=-270845779&_=1490624454643https://login.wx.qq.com/cgi-bin/mmwebwx-bin/login?loginicon=true&uuid=geoVJU3asA==&tip=0&r=-270845779&_=1490624454643'
    r = session.get(url)
    redirect_url = re.findall('"(.*?)"', r.text)
    return redirect_url[0]


def new_login_page(redirect_url):
    url = f'{redirect_url}&fun=new&version=v2&lang=zh_CN'
    r = session.get(url)
    ticket = re.findall('<pass_ticket>(.*?)</pass_ticket>', r.text)
    return ticket[0]


def webweixin_it(ticket):
    ticket_url = ticket.replace('%2', '%252')
    payload = {'r': '-272121405', 'lang': 'zh_CN', 'pass_ticket': ticket}
    headers = {'Accept': 'application/json, text/plain, */*',
               'Accept-Encoding': 'gzip, deflate, br',
               'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6',
               'Cache-Control': 'no-cache',
               'Connection': 'keep-alive',
               'Content-Length': '148',
               'Content-Type': 'application/json;charset=UTF-8',
               'DNT': '1',
               'Host': 'wx.qq.com',
               'Origin': 'https://wx.qq.com',
               'Pragma': 'no-cache',
               'Referer': 'https://wx.qq.com/?&lang=zh_CN',
               'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
    url = f'https://wx.qq.com/cgi-bin/mmwebwx-bin/webwxinit?r=-272121405&lang=zh_CN&pass_ticket={ticket_url}'
    r = session.post(url, data=payload, headers=headers)
    print(r.text)
    return r.json()


if __name__ == '__main__':
    uuuuuuid = get_uuid()
    print(uuuuuuid)
    verify_qrcode(uuuuuuid)
    print('verified')
    r = qrcode(uuuuuuid)
    print('opening')
    with open('hzzz.jpg', 'wb') as f:
        f.write(r.content)

    image = Image.open('hzzz.jpg')
    image.show()

    input('扫完随便来输个什么')
    redirect = redirect_url(uuuuuuid)
    ticket = new_login_page(redirect)
    data = webweixin_it(ticket)
    print(data)
