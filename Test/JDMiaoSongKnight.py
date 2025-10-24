from dashscope import Generation

from Ai import Ai, prompts
from EzBookKeeping import EzBookKeeping


class JDMiaoSongKnight(Generation):
    def ai(self,orc_str:str, ez:EzBookKeeping, account_str:str):
        ai = Ai()
        messages = prompts()
        messages.append({"role": "system", "content": "交易类型: 2收入 3支出 4转账"})
        messages.append({"role": "system", "content": '返回json数组示例 {"data":[{},{}]}'})
        messages.append({"role": "system", "content": "如果交易类型是2收入 商品分类id从这里取值:" + self.income_category(ez)})
        messages.append({"role": "user", "content": orc_str})
        messages.append({"role": "user", "content": "这是ocr结果 可能包含多条付款记录 找出所有 付款账户:sourceAccount 订单编号:sn 实际付款金额:sourceAmount 订单金额:orderAmount 商户:shop 支付时间:time 商品说明:good_item 商品分类id:categoryId 交易类型:type"})
        print("=" * 20 + "请求内容" + "=" * 20)
        print(messages)
        return ai.exec(messages)

    # 过滤收入分类
    def income_category(self,ez:EzBookKeeping):
        expend_category_str = ''
        for category in ez.income_category:
           if category['name'] == '兼职收入' or category['name'] == '奖金':
            expend_category_str = expend_category_str + category.get('name') + category.get('id') + " "
        return expend_category_str

    def add_transactions(self,app,ai_message,ez,image):
        for data in ai_message.get('data'):
            #支出如果是3元 判断保险支出 其他都是罚款支出
            if data.get('type') == 3:
                if float(data.get('sourceAmount')) == 3 :
                    data['categoryId'] = 3776599975526400066
                else:
                    data['categoryId'] = 3776599975526400068
            ez.add_transactions(app, data, image)