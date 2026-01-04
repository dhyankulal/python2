import pandas as pd

df1= pd.read_excel("games1.xlsx")

p1=df1.iloc[0,1]
p2=df1.iloc[0,2]
avg=(p1+p2)/2
#print(avg)

names=df1.iloc[:,0]
#print(names)
games1=df1.iloc[:,1]
#print(games1)

names = df1.iloc[:,0]
games1 = df1.iloc[:,1]
games2 = df1.iloc[:,2]
'''
for i in range(0,len(names),1):
    print(names[i],"-",games1[i],"points in chess,",games2[i],"points in carrom")
'''
maxGames1 = max(games1)
maxGames2 = max(games2)
#print(maxGames1,"is the highest score in chess")
#print(maxGames2,"is the highest score in carrom")
pos1=df1.index.get_loc(maxGames1)
pos2=df1.index.get_loc(maxGames2)
champ_chess = names[pos1]
champ_carrom = names[pos2]
print(champ_chess,"is the champion of chess with points",maxGames1)
print(champ_carrom,"is the champion of carrom with points",maxGames2)