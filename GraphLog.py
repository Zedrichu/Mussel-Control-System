import matplotlib.pyplot as plt


file = open("data4I0.2.txt")
dataset = file.readlines()
timeData = []
tempData = []

for line in dataset:
    t,c = map(float, line.split(','))
    tempData.append(c)
    timeData.append(t)

ref = 18
plt.figure()
plt.scatter(timeData, tempData, color = 'k', alpha=0.5)
plt.plot([0,timeData[-1]], [ref, ref], '--', color = 'r')
plt.savefig('PIDplot.png')
