
class a():

    curritem = {"num":1}

    def test(self):
        for i in range(10):
            item = self.curritem
            item['num'] =  self.curritem['num']+1
            print(item)

a().test()