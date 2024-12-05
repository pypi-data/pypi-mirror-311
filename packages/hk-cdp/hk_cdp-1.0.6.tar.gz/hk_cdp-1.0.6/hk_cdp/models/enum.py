# -*- coding: utf-8 -*-
"""
:Author: HuangJianYi
:Date: 2024-11-25 17:06:14
@LastEditTime: 2024-11-25 11:13:22
@LastEditors: HuangJianYi
:description: 枚举类
"""

from enum import Enum
from enum import unique

@unique
class OrderStatus(Enum):
    """
    :description: 订单状态
    """
    WAIT_BUYER_PAY = 1 #等待买家付款
    SELLER_CONSIGNED_PART = 2 #卖家部分发货
    WAIT_SELLER_SEND_GOODS = 3 #等待卖家发货,即:买家已付款
    WAIT_BUYER_CONFIRM_GOODS = 4 #等待买家确认收货,即:卖家已发货
    TRADE_BUYER_SIGNED = 5 #买家已签收,货到付款专用
    TRADE_FINISHED = 6 #交易成功
    TRADE_CLOSED = 7 #付款以后用户退款成功，交易自动关闭
    TRADE_CANCEL = 8 #付款以前，卖家或买家主动关闭交易


@unique
class RefuundStatus(Enum):
    """
    :description: 退款状态
    """
    NO_REFUND = 1 # 无退款
    WAIT_SELLER_AGREE = 2 # 买家已经申请退款，等待卖家同意
    WAIT_BUYER_RETURN_GOODS = 3 # 卖家已经同意退款，等待买家退货
    WAIT_SELLER_CONFIRM_GOODS = 4 # 买家已经退货，等待卖家确认收货
    SELLER_REFUSE_BUYER = 5 # 卖家拒绝退款
    CLOSED = 6 # 退款关闭
    SUCCESS = 7 # 退款成功
