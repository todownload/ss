
x = input()

sList = x.split()
numList = []
for a in sList:
    if a:
        numList.append(int(a))

for a in sorted(numList):
    print(a,end=" ")



