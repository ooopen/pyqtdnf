curritem = {"num": 1}
class a():
    def test(self):
        for i in range(10):
            print(curritem)
            item = curritem
            item['num'] = item['num'] + 1
a().test()
