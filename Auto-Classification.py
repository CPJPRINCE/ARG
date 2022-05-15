import os
from pathlib import Path
import pandas as pd
import time

tflag = None
oflag = None
throt = 0

OutputFile = "Output.xlsx"
TreeRoot = os.getcwd()

def listdirs(cwd):
    R = 1
    listdir = os.listdir(cwd)
    listdir = sorted([f for f in listdir if not f.startswith('.') and f != os.path.basename(__file__) and f != os.path.basename(OutputFile)])
    l = cwd.count(os.sep)
    l = l-L
    for file in listdir:
        d = os.path.join(cwd,file)
        listD.append(str(d))
        P = Path(d).parent
        listP.append(str(P))
        listL.append(l)
        if os.path.isdir(d):
            A = "Dir"
            listR.append(R)
            listA.append(A)
            listdirs(d)
        else:
            lr = l+1
            A = "Arc"
            listR.append(R)
            listA.append(A)
        R = R+1

# Loops through the Reference, because this works backwards.

def RefLoop(R, P, S, NR):
    time.sleep(throt)
    N = row['Name']
    print("S: " + str(S))
    L = row['Level']
    idx = df.index[df['Name'] == P]
    #print(idx)
    if idx.size == 0:
        print("No Match - Top Level reached")
        if L == 0:
            NR = str(1) + "/" + str(R)
        else:
            NR = str(1) + "/" + NR
        NewRef.append(NR)
        PrintRef.append(NR)
        print("NewRef: " + NR)
    else:
        print("Match - Top Level not reached")
        PR = df.loc[idx].Ref.item()
        #PN = df.loc[idx].Name.item()
        PP = df.loc[idx].Parent.item()
        #PL = df.loc[idx].Level.item()
        if S == 1:
            NR = str(PR) + "/" + str(R)
            print("N:" + str(N))
            print("R: " + str(R))
        else:
            NR = str(PR) + "/" + str(NR)
            print("PP: " + str(PP))
        print("NR: " + NR)
        P = PP
        S = S+1
        RefLoop(R, P, S, NR)   

cwd = TreeRoot

L = cwd.count(os.sep)
R = 1
listD = []
listR = []
listP = []
listA = []
listL = []

listdirs(cwd)

# print(len(listL))
# print(len(listR))
# print(len(listD))
# print(len(listP))
# print(len(listA))

# Creating the Dataframe in Pandas

df = pd.DataFrame({'Level':listL,'Ref':listR,'Name':listD,'Parent':listP,'Att':listA})
#print(df) 
df = df.merge(df[['Name','Parent','Ref']],how='left',left_on='Parent',right_on='Name')
df = df.drop(['Name_y','Parent_y'], axis=1)
df = df.rename(columns={'Ref_x':'Ref','Ref_y':'PRef','Name_x':'Name','Parent_x':'Parent'})
df['PRef'] = df['PRef'].fillna(0).astype(int)
df = df.astype({'PRef': int})
    
NewRef = []

# Looping over the Dataframe Rows

for index,row in df.iterrows():
    PrintRef = []
    print("Row: " + str(index))
    R = row['Ref']
    P = row['Parent']
    S = 1
    NR = 1
    RefLoop(R, P, S, NR)
    print()
    print(PrintRef)
    print()

#print(NewRef)
df['NRef'] = NewRef

df.to_excel(OutputFile)