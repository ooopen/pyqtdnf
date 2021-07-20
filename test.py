curritem = {'name': '无色小晶块', 'min': 10, 'buyPrice': 50, 'sellPrice': 52, 'nextRole': None, 'id': 1}

for i in range(10):
    print(curritem)
    item = curritem.items()
    item2 = {}
    for k,v in item:
        item2[k] = v
    item2['sellPrice'] = item2['sellPrice'] + 1

print(item2)