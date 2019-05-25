a = [16, 2,16, 4, 2, 128, 64, 7, 1, 64, 32, 5, 8]
dictionary = {}
for index, item in enumerate(a):
  number = item
  a[index] = 0
  for index1, item1 in enumerate(a):
    if number * item1 == 256:
      dictionary[number] = [number,index+1,item1,index1+1]
for value in dictionary.values():
  print(value)





