# -*- coding: utf-8 -*-
"""
@Author: HuangJianYi
@Date: 2024-11-18 18:57:33
@LastEditTime: 2024-11-28 13:56:52
@LastEditors: HuangJianYi
@Description: 
"""
import datetime
import math
from copy import deepcopy
from seven_cloudapp_frame.libs.customize.seven_helper import *
from hk_cdp.models.enum import *

class CdpHelper:
    
    @classmethod
    def get_business_db(self, business_code, cdp_db_config):
        """
        :description: 获取对应的数据库名
        :param business_code: 商家代码
        :param cdp_db_config: 数据库连接串
        :last_editors: HuangJianYi
        """
        cdp_db_config = SevenHelper.json_loads(cdp_db_config)
        rawdata_db_config = cdp_db_config
        rawdata_db_config['db'] = f"hk_{business_code}_rawdata"
        cdp_db_config = deepcopy(cdp_db_config)
        cdp_db_config["db"] = f"hk_{business_code}_cdp"
        return rawdata_db_config, cdp_db_config 
    
    @classmethod
    def get_valid_date(self, valid_type, expire_type, expire_value, expire_year, expire_month, expire_day):
        """
        :description: 计算积分/成长值过期时间
        :param valid_type: 有效类型(1-永久有效 2-指定时间)
        :param expire_type: 过期类型(1-指定天 2-指定时间)
        :param expire_value: 过期值
        :param expire_year: 过期年
        :param expire_month: 过期月
        :param expire_day: 过期日
        :last_editors: HuangJianYi
        """
        if valid_type == ValidType.forever.value:
            return '2900-01-01 00:00:00'
        else:
            if expire_type == ExpireType.appoint_day.value: # 指定天过期
                return (datetime.datetime.now() + datetime.timedelta(days=int(expire_value))).strftime("%Y-%m-%d 23:59:59")
            else:
                if expire_year and expire_month and expire_day:
                    current_year = datetime.datetime.now().year
                    expire_date = datetime.datetime(current_year + int(expire_year), int(expire_month), int(expire_day), 23, 59, 59)
                    return expire_date.strftime("%Y-%m-%d 23:59:59")
                else:
                    return '2900-01-01 00:00:00'

    @classmethod
    def reward_algorithm(self, value_type, reward_value):
        """
        :description: 奖励算法
        :param value_type: 算法类型(1-四舍五入 2-向上取整 3-向下取整)
        :param reward_value: 根据订单算法的值
        :last_editors: HuangJianYi
        """
        if value_type == RoundingType.half_up.value: # 四舍五入
            reward_value = round(reward_value)
        elif value_type == RoundingType.ceiling.value: # 向上取整
            reward_value = math.ceil(reward_value)
        elif value_type == RoundingType.floor.value: # 向下取整
            reward_value = math.floor(reward_value)
        return reward_value



   