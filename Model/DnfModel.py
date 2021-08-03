# coding:utf-8
from tools.Db import Db


class DnfModel():
    db = None

    def __init__(self):
        self.db = Db()

    def getConfig(self):
        query = (
            "SELECT a.id as uid,a.idimg,b.*, c.c_price,c.c_price_min,c.sleep_num from dnf_ids a left join dnf_object b on a.gzone_id = b.gzone_id left join dnf_gzone c on c. id = a.gzone_id where a.status = 1")
        ret = self.db.execute(query)
        return ret

    # `ids_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '角色id',
    # `msg` text NOT NULL,
    # `create_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
    def addSyslog(self, *args):
        query = "INSERT into dnf_syslog  values (null,%s,%s,now())"
        self.db.execute(query, args)

    # `ids_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '角色id',
    # `type` tinyint(4) NOT NULL DEFAULT '0' COMMENT '操作类型：1，登录，2登出',
    # `jb` int(10) NOT NULL DEFAULT '0' COMMENT '剩余金币数量',
    # `create_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP,
    def addIdslog(self, *args):
        query = "INSERT into dnf_ids_log  values (null,%s,%s,%s,now())"
        self.db.execute(query, args)

    # `ids_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '角色id',
    # `object_id` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '购买物品id',
    # `is_succ` tinyint(3) unsigned NOT NULL DEFAULT '0' COMMENT '是否成功0否1是',
    # `buy_snum` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '购买成功数量',
    # `buy_scost` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '购买总花费',
    # `act_price` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '实际单价',
    # `seting_price` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '配置单价',
    # `create_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '创建时间',
    def addBuylog(self, *args):
        query = "INSERT into dnf_buylog values (null,%s,%s,%s,%s,%s,%s,%s,now())"
        self.db.execute(query, args)

    # `object_id` int(10) NOT NULL DEFAULT '0' COMMENT '物品id',
    # `gzone_id` int(10) NOT NULL DEFAULT '0' COMMENT '游戏区服id',
    # `price1` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '销售价1',
    # `count1` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '数量1',
    # `sellh1` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '数量1最早拍卖剩余时间',
    # `price2` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '销售价2',
    # `count2` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '数量2',
    # `sellh2` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '数量2最早拍卖剩余时间',
    # `price3` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '销售价3',
    # `count3` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '数量3',
    # `sellh3` int(10) NOT NULL DEFAULT '0' COMMENT '数量3最早拍卖剩余时间',
    # `price4` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '销售价4',
    # `count4` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '数量4',
    # `sellh4` int(10) unsigned NOT NULL DEFAULT '0' COMMENT '数量4最早拍卖剩余时间',
    # `create_time` datetime NOT NULL ON UPDATE CURRENT_TIMESTAMP COMMENT '统计时间',
    def addPricetrend(self, *args):
        query = "INSERT into dnf_pricetrend values (null,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,now())"
        self.db.execute(query, args)

    def getPricetread(self, *args):
        query = "SELECT * from dnf_pricetrend where gzone_id=%s and price1>0  order by id desc limit 1"
        ret = self.db.execute(query, args)
        return ret

# args = (1, 1,1,1,3,4,5,4,5,6)
#
#
# r = DnfModel().getConfig()
#
# print(r)
