# -*- coding: utf-8 -*- #
"""
Created on 2018年11月30日
@author: Leo
"""


# 交易时间(自定义参数需要传入交易时间, 通过kwargs传入)
# (今天, 最近一周, 最近一个月, 最近三个月, 自定义时间)
TRADE_TIME = \
    ["today", "sevenDay", "oneMonth", "threeMonths", "customDate"]

# 交易状态
# (所有状态, 进行中, 等待付款, 等待发货, 等待确认发货,
#  退款, 成功, 失败, 退款待处理, 等待买家签收,
#  等待签收确认, 等待系统打款给卖家, 维权)
TRADE_STATUS = \
    ["all", "inProcess", "waitPay", "waitSendGoods", "waitConfirmGoods",
     "refund", "success", "fail", "refundInProcess", "codWaitBuyerPay",
     "codWaitReceiptConfirm", "codWaitSysPaySeller", "mr"]

# 关键词
# (流水号, 交易信息, 对方名称)
KEYWORD_LIST = ["bizNo", "generalInfo", "oppositeName"]

# 时间类型
# (创建时间, 付款时间, 收款时间)
TIME_TYPE = ["createDate", "payDate", "receiveDate"]

# 资金流向
# (全部, 收入, 支出)
MONEY_FLOW = ["all", "in", "out"]

# 交易方式
# (担保交易, 即时到账, 货到付款)
TRADE_WAT = ["S", "FP", "COD"]

# 交易分类
# (全部, 购物, 线下, 理财, 转账,
#  还款, 缴费, 充值, 提现, 还贷款,
#  手机充值)
TRADE_TYPE = ["ALL", "SHOPPING", "OFFLINENETSHOPPING", "FINANCE", "TRANSFER",
              "CCR", "PUC_CHARGE", "DEPOSIT", "WITHDRAW", "PERLOAN",
              "MOBILE_RECHARGE"]
