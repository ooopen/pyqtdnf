import time

from service.StzbModel import StzbModel
from tools.DmTools import DmTools


class Stzb():

    def __init__(self):
        self.DmModel = StzbModel()
        self.DmModel.initWindow("雷电模拟器")
        self.DmModel.back()
        self.DmModel.conscription(0)


st = Stzb()
