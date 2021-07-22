
count = 0
newPrice = 49

arr= {1: [48, 947212], 2: [49, 7374733], 3: [50, 5585327], 4: [51, 8226490]}

for k, v in arr.items():
     if (v[0] <= newPrice):
         count = count + v[1]

print(count)
