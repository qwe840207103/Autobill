import os

import requests
from datetime import datetime

class EzBookKeeping:
    base_url = os.getenv("EZ_BOOKKEEPING_API_URL")

    def __init__(self):
        self.income_category = []
        self.expend_category = []
        self.accounts = []
        self.expend_category_str = ''
        self.income_category_str = ''
        self.account_str = ''
        self.token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyVG9rZW5JZCI6IjQxMjYzMTY2MjYzOTcxMjc3MzEiLCJqdGkiOiIzNzc2NTk5OTc1MTIzNzQ2ODE2IiwidXNlcm5hbWUiOiJhZG1pbiIsInR5cGUiOjEsImlhdCI6MTc1ODc5MDQ2NiwiZXhwIjoxNzYxMzgyNDY2fQ.K4Y5i6C4GiXDulKtiu3AwufS720p9FPs8CWdEIz3NqA'

    def category_list(self):
        response = self.get_request(self.base_url +'/api/v1/transaction/categories/list.json')
        result = response.json()['result']
        for item in result.get('2'):
            if item.get('subCategories') is not None:
                for subCategories in item['subCategories']:
                    self.init_category(self.expend_category,subCategories)
        for item in result.get('1'):
            if item.get('subCategories') is not None:
                for subCategories in item['subCategories']:
                    self.init_category(self.income_category, subCategories)

        for category in self.expend_category:
            self.expend_category_str = self.expend_category_str + category.get('name') + category.get('id')

        for category in self.income_category:
            self.income_category_str = self.income_category_str + category.get('name') + category.get('id')

    def account_list(self):
        response = self.get_request(self.base_url +'/api/v1/accounts/list.json')
        for item in response.json()['result']:
            self.init_account(item)
            if item.get('subAccounts') is not None:
                for subAccount in item['subAccounts']:
                    self.init_account(subAccount)
        for account in self.accounts:
            self.account_str = self.account_str + account.get('name') + ' '

    def add_transactions(self,app_name,json,image):
        print("=" * 20 + "交易写入" + "=" * 20)
        data = dict()
        data['sourceAccountId'] = self.get_account(json,app_name)
        data['type'] = int(json.get('type'))
        if  json.get('shop') != json.get('good_item'):
            data['comment'] = json.get('sn') + ' ' + json.get('shop') + ' ' + json.get('good_item')
        else:
            data['comment'] = json.get('sn','') + ' ' + json.get('good_item','')
        data['categoryId'] = str(json.get('categoryId'))
        data['time'] =  int(datetime.strptime(json.get('time'), "%Y-%m-%d %H:%M:%S").timestamp())
        data['utcOffset'] = 8 * 60
        data['sourceAmount'] =  abs(int (float(json.get('sourceAmount')) * 100))

        if image is not None:
            data['pictureIds'] = [image]
        response = self.post_request(self.base_url+'/api/v1/transactions/add.json',data)
        print(data)
        print(response)

    def upload_image(self, image_path):
        with open(image_path, 'rb') as f:
            files = {
                'picture': (image_path, f, 'image/jpeg')
            }
            response = self.post_request(self.base_url+'/api/v1/transaction/pictures/upload.json',files=files)
            print(response)
            if response.status_code == 200:
                return response.json()['result']
            else:
                return None

    def init_account(self,item):
        if item['type'] == 1:
            account = dict()
            account['name'] = item['name']
            account['id'] = item['id']
            self.accounts.append(account)


    def init_category(self,categories,item):
        category = dict()
        category['name'] = item['name']
        category['id'] = item['id']
        categories.append(category)

    def get_request(self,url):
        headers = {
            'Authorization': 'Bearer '+ self.token,
            'Content-Type': 'application/json'
        }
        response = requests.get(url,headers=headers)
        return response

    def post_request(self,url:str,data=None,files=None):
        headers = {
            'Authorization': 'Bearer '+ self.token
        }
        if files is None:
            headers['Content-Type'] = 'application/json'
        response = requests.post(url,headers=headers,json=data,files=files)
        return response

    def get_account(self,json,app_name:str):
        source_account_id = None
        source_account = json.get('sourceAccount').replace("（", '(').replace("）", ')').replace(">", '')
        for account in self.accounts:
            if source_account == account.get('name'):
                source_account_id = account.get('id')

        # 个别app付款截图没有 支付账户信息
        # todo 考虑将app名称传给ai 利用ai识别账户
        if source_account_id is None:
            if app_name == '中国工商银行':
                source_account_id = '3776614238844354560'
            if app_name == '京东秒送骑士':
                source_account_id = '3776610639661760512'
            if app_name == '美团众包':
                source_account_id = '3776610577384734721'
        return source_account_id