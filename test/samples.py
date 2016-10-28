mylist = [x*x for x in range(3)]
for i in mylist:
    print(i)

print(mylist)

# mylist2 = (x*x for x in range(3))
for i in (x*x for x in range(3)):
    print(i)

# print(mylist2)