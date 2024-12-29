from tabulate import tabulate
import pandas as pd

Weights1 = [3,2,1,4,5]
Values1 = [25,20,15,40.50]
Cap1 = 6
n1 = len(Weights1)

Weights2 = [1,3,4,5]
Values2 = [1,4,5,7]
Cap2 = 7
n2 = len(Weights2)

Weights3 = [3,3,3,3]
Values3 = [4,1,12,11]
Cap3 = 7
n3 = len(Weights3)

Weights4 = [24, 36, 48, 60, 72, 84, 96, 108, 120]
Values4 = [24000, 36000, 48000, 60000, 72000, 84000, 96000, 108000, 120000]
Cap4 = 280
n4 = len(Weights4)

Weights5 = [1,2,3,4,5]
Values5 = [6,10,12,18,20]
Cap5 = 9
n5 = len(Weights5)

class code():

    def MFKnapsack(i, j, F, W, V):
    
        if F[i][j] < 0:
            if j < W[i-1]:
                value = code.MFKnapsack(i - 1, j, F, W, V)
            else:
                value = max(code.MFKnapsack(i - 1, j, F, W, V), V[i-1] + code.MFKnapsack(i - 1, j - W[i-1], F, W, V))
            
            F[i][j] = value

        return F[i][j]
    
    def initiTable(Wl, Capacity):

        table = [[-1 for _ in range(Capacity + 1)] for _ in range(Wl + 1)]

        for i in range(Wl + 1):
            table[i][0] = 0
        for j in range(Capacity + 1):
            table[0][j] = 0

        return table
    
    def Calc(table):
        print(table)

        df = pd.DataFrame(table, columns=range(len(table[0])), index=range(len(table)))

        return tabulate(df, headers = 'keys', tablefmt = 'psql')

class run():

    First = code.initiTable(4, 5)
    print(code.MFKnapsack(4, 5, First, Weights1, Values1))
    print(code.Calc(First),'\n')
    
    Test = code.initiTable(3, 4)
    print(code.MFKnapsack(3, 4, Test, Weights1, Values1))
    print(code.Calc(Test),'\n')

    Firstsort = code.initiTable(3, Cap1)
    print(code.MFKnapsack(3, Cap1, Firstsort, Weights1, Values1))
    print(code.Calc(Firstsort),'\n')

    Second = code.initiTable(n2, Cap2)    
    print(code.MFKnapsack(n2, Cap2, Second, Weights2, Values2))
    print(code.Calc(Second),'\n')

    Third = code.initiTable(n3, Cap3)
    print(code.MFKnapsack(n3, Cap3, Third, Weights3, Values3))
    print(code.Calc(Third),'\n')
    
    Fourth = code.initiTable(n4, Cap4)
    print(code.MFKnapsack(n4, Cap4, Fourth, Weights4, Values4))
    print(code.Calc(Fourth),'\n')

    Fifth = code.initiTable(n5, Cap5)
    print(code.MFKnapsack(n5, Cap5, Fifth, Weights5, Values5))
    print(code.Calc(Fifth),'\n')
