import matplotlib.pyplot as plt
import ast

def value(typ):
    if typ == 1:
        return 5
    if typ in (9,10):
        return -3
    if typ== 5:
        return 3
    if typ == 2:
        return 2
    if typ ==4:
        return 3
    if typ ==3:
        return 2
    if typ == 7:
        return 2
    if typ == 8:
        return -5
    if typ == 11:
        return -10
    if typ == 13:
        return -1
    if typ == 0:
        return 10
    if typ == 6:
        return 0
    if typ == 12:
        return 0


list_Ifp=[]
list_Itp=[]
list_Cfp=[]
list_Ctp=[]
list_Cr=[]
list_Ir=[]

with open('datas.txt','r',encoding='utf-8') as file:
    for line in file:
        line = line.strip()
        parts = line.split('|')
        camp=bool(int(parts[0]))
        tuple_str = parts[1].strip('()')
        tuple_parts = tuple_str.split(',')
        move = (int(tuple_parts[0]), int(tuple_parts[1]))
        list_str = parts[2]
        beach = ast.literal_eval(list_str)
        from_typ=beach[move[0]]
        if camp:
            C_from_p = move[0]
            C_to_p = move[1]
            list_Cfp.append(C_from_p)
            list_Ctp.append(C_to_p)
        else:
            I_from_p=move[0]
            I_to_p=move[1]
            list_Ifp.append(I_from_p)
            list_Itp.append(I_to_p)
        king_p=beach.index(12)
        shuai_p=beach.index(6)

        Chn_pieces = 0
        Intl_pieces = 0
        Chn_pose = 0
        Intl_pose = 0
        p = 0
        for i in beach:
            if i != None:
                if i < 8:
                    Chn_pieces += 1
                    Chn_pose += p // 10

                else:
                    Intl_pieces += 1
                    Intl_pose += p // 10
            p += 1
        if camp:
            Chn_average = Chn_pose / Chn_pieces
            list_Cr.append(round(Chn_average, 1))
        else:
            Intl_average = Intl_pose / Intl_pieces
            list_Ir.append(round(Intl_average, 1))


x=[]
y=[]

for i in list_Cfp:
    i=i//10
    x.append(i)
for i in list_Ctp:
    i=i//10
    y.append(i)


plt.scatter(x, y,s=100,alpha=0.05)
plt.title('Chn ptx and pfx')
plt.xlabel('pt')
plt.ylabel('pf')
plt.show()