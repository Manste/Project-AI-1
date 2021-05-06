
pos = [True, False]

count = 0
countTrue1 = 0
countTrue2 = 0
countTrue3 = 0
for A in pos:
    for B in pos:
        for C in pos:
            for D in pos:
                count += 1
                if ((not A) or C) and ((not B) or C):
                    countTrue1 += 1
                if((not C) or (not A)) and not(B or C):
                    countTrue2 += 1
                    print(A,B,C,D)
                T1 = ((not A) or B)
                T2 = not((not B) or (not C))
                T3 = not(D or A)
                if T1 and T2 and T3:
                    countTrue3 += 1
                    print(A,B,C,D)

print("Number: "+str(countTrue1))
print("Number: "+str(countTrue2))
print("Number: "+str(countTrue3))
