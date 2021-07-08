# -*- coding: utf-8 -*-
import requests
import time
from public.headers import Headers
from public.mysqlpooldao import MysqlDao

mysql_dao = MysqlDao()

url = {
    u'上海': ('http://app.wishtv.com.cn/privilege/privilegeList?'
            'currentPage={page_num}&size=10&type=1&areaId=a9314e321e9144f985a30d0082ca6e8d'
            '&currentLocation=121.471542426216%2C31.209276258681&shangquanLabelNamesStr=&caixiLabelNamesStr='),
    u'北京':('http://app.wishtv.com.cn/privilege/privilegeList?'
           'currentPage={page_num}&size=10&type=1&areaId=285dbe4269014c5493f67a6a340961e7'
           '&currentLocation=121.471841634115%2C31.208905436198&shangquanLabelNamesStr=&caixiLabelNamesStr=')
}

for (city_name, url) in url.items():
    page_num = 1
    while 1:
        target_url = url.format(page_num=page_num)
        headers = Headers.get_headers()
        req = requests.get(target_url, headers=headers)
        html_json = req.json()
        if len(html_json) == 0:
            break
        print(target_url)
        print(html_json)
        for shop in html_json:
            shop_name = shop['restaurantName']
            shop_tel = shop['restaurantTel']
            shop_addr = shop['restaurantAddress']
            sku_name = shop['name']
            sku_price = shop['costStr']
            expiry_date = shop['validity']
            shop_hours = shop['useTime']
            shop_consumption = shop['restaurantPcc']
            shop_id = shop['id']
            sku_id = shop['articleId']
            values = (
                city_name, shop_name, shop_tel, shop_addr, sku_name, sku_price, expiry_date, shop_hours,
                shop_consumption,
                shop_id, sku_id)
            sql = ('INSERT ignore INTO `wish_copy` '
                   '(`city_name`, `shop_name`, `shop_tel`, `shop_addr`, `sku_name`, `sku_price`, '
                   '`expiry_date`, `shop_hours`, `consumption`,`shop_id`,`sku_id`)'
                   ' VALUES ("%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s", "%s")') % (values)
            print(sql)
            mysql_dao.execute(sql)
        page_num += 1
    print('game over')
