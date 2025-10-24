from dashscope import Generation
from Ai import Ai, prompts

class Common(Generation):
    def ai(self,orc, expend_category_str, income_category_str, account_str):
        orc_str = ''
        for str in orc:
            orc_str = orc_str + str + ' '
        messages = prompts()
        messages.append({"role": "system", "content": "交易类型: 2收入 3支出 4转账"})
        messages.append({"role": "user", "content": "如果交易类型是3支出 商品分类id从这里取值:" + expend_category_str})
        messages.append({"role": "user", "content": "如果交易类型是2收入 商品分类id从这里取值:" + income_category_str})
        messages.append({"role": "user", "content": "付款账户 从这里取值:" + account_str})
        messages.append({"role": "user", "content": "工作日上午9点左右7元一下消费 分类设置为饮料分类"})
        messages.append({"role": "user", "content": "交易类型 一般情况下是 3支出"})
        messages.append({"role": "user", "content": orc_str})
        messages.append({"role": "user","content": "这是ocr结果 找出其中 付款账户:sourceAccount 订单编号:sn 实际付款金额:sourceAmount 订单金额:orderAmount 商户:shop 支付时间:time 商品说明:good_item 商品分类id:categoryId 交易类型:type 返回json对象"})
        ai = Ai()
        return ai.exec(messages)