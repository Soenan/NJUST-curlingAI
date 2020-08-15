# -*- coding: utf-8 -*-
import socket
import time
import random
import math

# python 与客户端连接
host = '127.0.0.1'
port = 7788
obj = socket.socket()
obj.connect((host, port))
# 初始化
shotnum = str("0")
firstsecond = str("0")  # 先后手
state = []
ju = int(0)
keep_lose = 0
now_x, now_y = 0, 0
before_x, before_y = 0, 0


# pyinstaller -F CurlingAI.py

# 与大本营中心距离
def get_dist(x, y):
    if (x == 0 and y == 0):
        return 1000
    else:
        return (x - 2.375) ** 2 + (y - 4.88) ** 2


# 大本营内是否有球
def is_in_house(x, y):
    House_R = 1.830
    Stone_R = 0.145
    if get_dist(x, y) < (House_R + Stone_R) ** 2:
        return 1
    else:
        return 0


def list_to_str(list):
    tmp = str(list)[1:-1].replace(',', '')
    res = "BESTSHOT " + tmp
    return res


def tracel(y):
    if y > 4.68:
        return (((-0.0034 * y + 0.0765) * y - 0.6377) * y + 4.0576)
    else:
        return 100


def tracer(y):
    if y > 4.68:
        return (((0.0032 * y - 0.0708) * y + 0.5918) * y + 0.7665)
    else:
        return 100


def have_ball(x, y, sorted_res):
    l = x - 0.4
    r = x + 0.4
    # u = y - 0.2
    # d = y + 0.2
    block = 0
    for i in range(min(15, int(shotnum))):
        if sorted_res[i][0] == 1000:
            break
        # print(sorted_res[i])
        if (l <= sorted_res[i][2] and sorted_res[i][2] <= r and sorted_res[i][3] > y):
            block += 1
    if block == 0:
        return 0
    else:
        return 1


def xuanjin(sorted_res):
    print("xuanjin")
    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 右
        if float(sorted_res[i][3]) != 0:
            temp = tracel(float(sorted_res[i][3]))
            temp = int(temp * 100)
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 34, 34):
                ind = j + ttemp - temp - 145 + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    l = 0
    for i in range(237 - 145, 476):
        if (res[i] == 0):
            l = i
            break
    x_l = l - 237 + 145
    for i in range(237 + 145, 0, -1):
        if (res[i] == 0):
            if (x_l > 237 - 145 - i):
                x_l = 237 - 145 - i
                l = i
            break
    if (l > 330):
        x_l = 10000
    print(l)
    print(x_l)
    h_xl = l - 237
    h_xl = float(h_xl) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 左
        if float(sorted_res[i][3]) != 0:
            temp = tracer(float(sorted_res[i][3]))
            temp = int(temp * 100)
            # print(temp)
            ttemp = int(sorted_res[i][2] * 100)
            # print(ttemp)
            for j in range(- 34, 34):
                ind = j + ttemp - temp + 145 + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                # print(ind)
                res[ind] = 1
        else:
            break
    r = 477
    for i in range(237 + 145, 476):
        if (res[i] == 0):
            r = i
            break
    x_r = r - 237 - 145
    for i in range(237 + 145, 0, -1):
        if (res[i] == 0):
            if (x_r > 237 + 145 - i):
                x_r = 237 + 145 - i
                r = i
            break

    if (r == 477 or r < 145):
        x_r = 10000
    print(r)
    print(x_r)
    h_xr = r - 237
    h_xr = float(h_xr) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 直
        if float(sorted_res[i][3]) != 0:
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 34, 34):
                ind = j + ttemp
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    z = 237
    for i in range(237, 476):
        if (res[i] == 0):
            z = i
            break
    x_z = z - 237
    for i in range(237, 0, -1):
        if (res[i] == 0):
            if (x_z > 237 - i):
                x_z = 237 - i
                z = i
            break
    print(z)
    print(x_z)
    h_xz = z - 237
    h_xz = float(h_xz) / 100
    x = min(x_z, x_r)
    x = min(x, x_l)

    if (x_z == x):
        v = 2.99
        h_x = h_xz
        h_ang = 0
    if (x_r == x):
        v = 3.06
        h_x = h_xr
        h_ang = -10
    if (x_l == x):
        v = 3.06
        h_x = h_xl
        h_ang = 10
    if (x_r == x_l):
        if leftorright(sorted_res, x, 5, x + 1.5):
            v = 3.06
            h_x = h_xl
            h_ang = 10
        else:
            v = 3.06
            h_x = h_xr
            h_ang = -10
    bestshot = [v, h_x, h_ang]
    bestshot = list_to_str(bestshot)
    return bestshot


def qianguaqiu(sorted_res):
    print("xuanjin")
    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 右
        if float(sorted_res[i][3]) != 0:
            temp = tracel(float(sorted_res[i][3]))
            temp = int(temp * 100)
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 60, 60):
                ind = j + ttemp - temp - 145 + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    l = 0
    for i in range(237 - 145, 476):
        if (res[i] == 0):
            l = i
            break
    x_l = l - 237 + 145
    for i in range(237 + 145, 0, -1):
        if (res[i] == 0):
            if (x_l > 237 - 145 - i):
                x_l = 237 - 145 - i
                l = i
            break
    if (l > 330):
        x_l = 10000
    print(l)
    print(x_l)
    h_xl = l - 237
    h_xl = float(h_xl) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 左
        if float(sorted_res[i][3]) != 0:
            temp = tracer(float(sorted_res[i][3]))
            temp = int(temp * 100)
            # print(temp)
            ttemp = int(sorted_res[i][2] * 100)
            # print(ttemp)
            for j in range(- 60, 60):
                ind = j + ttemp - temp + 145 + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                # print(ind)
                res[ind] = 1
        else:
            break
    r = 477
    for i in range(237 + 145, 476):
        if (res[i] == 0):
            r = i
            break
    x_r = r - 237 - 145
    for i in range(237 + 145, 0, -1):
        if (res[i] == 0):
            if (x_r > 237 + 145 - i):
                x_r = 237 + 145 - i
                r = i
            break

    if (r == 477 or r < 145):
        x_r = 10000
    print(r)
    print(x_r)
    h_xr = r - 237
    h_xr = float(h_xr) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 直
        if float(sorted_res[i][3]) != 0:
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 60, 60):
                ind = j + ttemp
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    z = 237
    for i in range(237, 476):
        if (res[i] == 0):
            z = i
            break
    x_z = z - 237
    for i in range(237, 0, -1):
        if (res[i] == 0):
            if (x_z > 237 - i):
                x_z = 237 - i
                z = i
            break
    print(z)
    print(x_z)
    h_xz = z - 237
    h_xz = float(h_xz) / 100
    x = min(x_z, x_r)
    x = min(x, x_l)

    if (x_z == x):
        v = 2.99
        h_x = h_xz
        h_ang = 0
    if (x_r == x):
        v = 3.06
        h_x = h_xr
        h_ang = -10
    if (x_l == x):
        v = 3.06
        h_x = h_xl
        h_ang = 10

    bestshot = [v, h_x, h_ang]
    bestshot = list_to_str(bestshot)
    return bestshot


def bigleftxuanke(sorted_res):
    print("trybigleftxuanke")
    left = 0
    while left >= -0.05:
        ok=1
        offset = sorted_res[0][2] - 2.375 + left
        for i in range(1, min(15, int(shotnum))):
            if sorted_res[i][0] == 1000:
                break
            x = sorted_res[i][2]
            y = sorted_res[i][3]
            if y < sorted_res[0][3]:
                continue
            if (x - sorted_res[0][2]) ** 2 + (y - sorted_res[0][3]) ** 2 <= 0.295 ** 2:
                continue
            xpath = -0.0038 * y * y * y + 0.0833 * y * y - 0.6681 * y + 4.1115
            xpath += offset
            if abs(xpath - x) < 0.295 + 0.004:
                left -= 0.001
                ok=0
                break
        if ok==1:
            print('getleftxuanke:'+str(left))
            return left
    print('fail leftxuanke')
    return -1


def bigrightxuanke(sorted_res):
    print("trybigrightxuanke")
    right = 0
    while right <= 0.05:
        ok=1
        offset = sorted_res[0][2] - 2.375 + right
        for i in range(1, min(15, int(shotnum))):
            if sorted_res[i][0] == 1000:
                break
            x = sorted_res[i][2]
            y = sorted_res[i][3]
            if y < sorted_res[0][3]:
                continue
            if (x - sorted_res[0][2]) ** 2 + (y - sorted_res[0][3]) ** 2 <= 0.29 ** 2:
                continue
            xpath = -0.0006 * y * y + 0.0763 * y + 1.9955
            xpath += offset
            if abs(xpath - x) < 0.295 + 0.004:
                right += 0.001
                ok=0
                break
        if ok == 1:
            print('getrightxuanke:'+str(right))
            return right
    print('fail rightxuanke')
    return -1

def lianqiu(sorted_res):
    target = sorted_res[0]
    snakebefore =0
    snakeafter = 0
    for i in range(1,int(shotnum)):
        disX=sorted_res[i][2] - target[2]
        disY=sorted_res[i][3] - target[3]
        print("1 disX+disY"+str(disX)+' '+str(disY))
        if abs(disX) <= 0.2 and disY<0 and disY>=-0.35:
            target = sorted_res[i]
            snakeafter = 1
            for j in range(1,int(shotnum)):
                disX = sorted_res[j][2] - target[2]
                disY = sorted_res[j][3] - target[3]
                print("2 disX+disY"+str(disX)+' '+str(disY))
                if j!=i and abs(disX) <= 0.2 and disY<0 and disY>=-0.35:
                    snakeafter = 2
                    break
            break
    target = sorted_res[0]
    for i in range(1, int(shotnum)):
        disX = sorted_res[i][2] - target[2]
        disY = sorted_res[i][3] - target[3]
        print("before,disX+disY"+str(disX)+' '+str(disY))
        if abs(disX) <= 0.2 and disY > 0 and disY <=0.35:
            target = sorted_res[i]
            snakebefore = 1
            break
    print("snakebefore="+str(snakebefore))
    print("snakeafter=" + str(snakeafter))
    if snakebefore + snakeafter <=1:
        return 1
    else: return 0


def fight(sorted_res):
    print("fight")
    get = get_dist(sorted_res[0][2], sorted_res[0][3])
    print("getdis")
    print(get)
    for i in range(min(15, int(shotnum))):
        if (sorted_res[i][1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                sorted_res[i][1] % 4 == 2 and int(shotnum) % 2 == 1):
            if abs(sorted_res[i][2] - 2.375) ** 2 < get - 0.3:
                bl = 0
                for j in range(min(15, int(shotnum))):
                    if (i != j):
                        if abs(sorted_res[j][2] - sorted_res[i][2]) < 0.2:
                            bl += 1
                if (bl == 0):
                    return tuijin(sorted_res[i][3], sorted_res[i][2])

    for i in range(min(15, int(shotnum))):
        if abs(sorted_res[i][2] - 2.375) ** 2 < get - 0.3:
            bl = 0
            for j in range(min(15, int(shotnum))):
                if (i != j):
                    if abs(sorted_res[j][2] - sorted_res[i][2]) < 0.2:
                        bl += 1
            if (bl == 0):
                return tuijin(sorted_res[i][3], sorted_res[i][2])

    ball = sorted_res[0]
    for i in range(min(15, int(shotnum))):
        if sorted_res[i][0] == 1000:
            break
        disX = sorted_res[i][2] - sorted_res[0][2]
        if abs(disX) < 0.29 and sorted_res[i][3] > ball[3]:
            ball = sorted_res[i]
    # 撞ball这个球
    if abs(ball[3] - sorted_res[0][3]) < 0.12:
        v = 7
        h_x = ball[2] - 2.375 + 0.0232
        h_ang = 0
        bestshot = [v, h_x, h_ang]
        bestshot = list_to_str(bestshot)
        return bestshot
    else:
        k = (ball[3] - sorted_res[0][3]) / (ball[2] - sorted_res[0][2])
        print("k=" + str(k))
        cos = abs(sorted_res[0][2] - ball[2]) / (
            math.sqrt((sorted_res[0][3] - ball[3]) ** 2 + (sorted_res[0][2] - ball[2]) ** 2))
        disX = 0.29 * cos
        x = 0
        if k > 0:
            x = ball[2] + disX
            print(x)
        else:
            x = ball[2] - disX
            print(x)
        x = noblock(sorted_res, x, ball[3], k)
        if x < 0.15 or x > 4.6:
            v = 8
            h_x = ball[2] - 2.375 + 0.0232
            h_ang = 0
            bestshot = [v, h_x, h_ang]
            bestshot = list_to_str(bestshot)
            return bestshot
        if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
            v = 7
        else:
            v = 8
        h_x = x - 2.375 + 0.0232
        h_ang = 0
        bestshot = [v, h_x, h_ang]
        bestshot = list_to_str(bestshot)
        return bestshot


def lastxuanjin(sorted_res):
    print("lastxuanjin")
    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 右
        if float(sorted_res[i][3]) != 0:
            temp = tracel(float(sorted_res[i][3]))
            temp = int(temp * 100)
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 34, 34):
                ind = j + ttemp - temp - 145 + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    l = 0
    for i in range(237 - 145, 476):
        if (res[i] == 0):
            l = i
            break
    x_l = l - 237 + 145
    for i in range(237 + 145, 0, -1):
        if (res[i] == 0):
            if (x_l > 237 - 145 - i):
                x_l = 237 - 145 - i
                l = i
            break
    if (l > 330):
        x_l = 10000
    print(l)
    print(x_l)
    h_xl = l - 237
    h_xl = float(h_xl) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 左
        if float(sorted_res[i][3]) != 0:
            temp = tracer(float(sorted_res[i][3]))
            temp = int(temp * 100)
            # print(temp)
            ttemp = int(sorted_res[i][2] * 100)
            # print(ttemp)
            for j in range(- 34, 34):
                ind = j + ttemp - temp + 145 + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                # print(ind)
                res[ind] = 1
        else:
            break
    r = 477
    for i in range(237 + 145, 476):
        if (res[i] == 0):
            r = i
            break
    x_r = r - 237 - 145
    for i in range(237 + 145, 0, -1):
        if (res[i] == 0):
            if (x_r > 237 + 145 - i):
                x_r = 237 + 145 - i
                r = i
            break

    if (r == 477 or r < 145):
        x_r = 10000
    print(r)
    print(x_r)
    h_xr = r - 237
    h_xr = float(h_xr) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 直
        if float(sorted_res[i][3]) != 0:
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 34, 34):
                ind = j + ttemp
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    z = 237
    for i in range(237, 476):
        if (res[i] == 0):
            z = i
            break
    x_z = z - 237
    for i in range(237, 0, -1):
        if (res[i] == 0):
            if (x_z > 237 - i):
                x_z = 237 - i
                z = i
            break
    print(z)
    print(x_z)
    h_xz = z - 237
    h_xz = float(h_xz) / 100
    x = min(x_z, x_r)
    x = min(x, x_l)

    if (x_z == x):
        v = 2.99
        h_x = h_xz
        h_ang = 0
    if (x_r == x):
        v = 3.06
        h_x = h_xr
        h_ang = -10
    if (x_l == x):
        v = 3.06
        h_x = h_xl
        h_ang = 10
    if(x_r == x_l):
        if leftorright(sorted_res, x, 5, x + 1.5):
            v = 3.06
            h_x = h_xl
            h_ang = 10
        else:
            v = 3.06
            h_x = h_xr
            h_ang = -10
    print(int(get_dist(sorted_res[0][2], sorted_res[0][3]) * 100))
    if (sorted_res[0][1] % 4 == 0 and int(shotnum) % 2 == 0) or (sorted_res[0][1] % 4 == 2 and int(shotnum) % 2 == 1):
        bestshot = [v, h_x, h_ang]
        bestshot = list_to_str(bestshot)
        return bestshot
    else:
        if (x > int(get_dist(sorted_res[0][2], sorted_res[0][3]) * 100)):
            if (count_ball(sorted_res, 15) == 1):
                return fight(sorted_res)
        if (x > 60):
            return fight(sorted_res)
        bestshot = [v, h_x, h_ang]
        bestshot = list_to_str(bestshot)
        return bestshot


def noblock(sorted_res, x, miny, k):
    temp = x
    print("before noblock:" + str(temp))
    if k < 0:
        while (True):
            block = 0
            for i in range(min(15, int(shotnum))):
                if sorted_res[i][0] == 1000:
                    break
                if sorted_res[i][3] <= miny: continue
                if abs(sorted_res[i][2] - temp) < 0.29:
                    block = 1
            if block == 0:
                break
            else:
                temp += 0.001
    else:
        while (True):
            block = 0
            for i in range(min(15, int(shotnum))):
                if sorted_res[i][0] == 1000:
                    break
                if sorted_res[i][3] <= miny: continue
                if abs(sorted_res[i][2] - temp) < 0.29:
                    block = 1
            if block == 0:
                break
            else:
                temp -= 0.001
    print("after noblock:" + str(temp))
    return temp


def xuanke(sorted_res):
    print("xuanke")
    ismine = 0  # 离中心最近的球是否为自己的
    print("lianqiu:"+str(lianqiu(sorted_res)))
    num = count_num(sorted_res)
    count = count_ball(sorted_res, num)
    if count>=1:
        print("count>=2")
        for z in range(1,num):
            if ((abs(sorted_res[0][2] - sorted_res[z][2]) < 0.45 and abs(sorted_res[0][3] - sorted_res[z][3]) < 0.3) or (abs(sorted_res[0][2] - sorted_res[z][2]) < 0.3 and abs(sorted_res[0][3] - sorted_res[z][3]) < 0.45)) and boundary(1.2, sorted_res, count)==False and sorted_res[z][1]%4 == sorted_res[0][1]%4:
                block,middle = 0,float((sorted_res[0][2] + sorted_res[z][2])) / 2
                print("middle:"+str(middle))
                ball=sorted_res[0]
                for i in range(3,min(15, int(shotnum))):
                    if sorted_res[i][0] == 1000:
                        break
                    disX = sorted_res[i][2] - middle
                    if abs(disX) < 0.29 and sorted_res[i][3] > ball[3]:
                        block+=1
                        ball = sorted_res[i]
                if block==0:
                    v = 10
                    h_x = middle - 2.375 + 0.0232
                    h_ang = 0
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
                else:
                    k = (ball[3] - min(sorted_res[0][3],sorted_res[z][3])) / (ball[2] - middle)
                    print("k=" + str(k))
                    cos = abs(sorted_res[0][2] - ball[2]) / (math.sqrt((sorted_res[0][3] - ball[3]) ** 2 + (sorted_res[0][2] - ball[2])**2))
                    disX = 0.29 * cos
                    x = 0
                    if k > 0:
                        x = ball[2] + disX
                        print(x)
                    else:
                        x = ball[2] - disX
                        print(x)
                    x=noblock(sorted_res,x,ball[3],k)
                    if x>0.15 and x<4.6:
                        v = 7
                        if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                                ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
                            v = 7
                        else:
                            v = 8.5
                        h_x = x - 2.375 + 0.0232
                        h_ang = 0
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot
                break

    if (sorted_res[0][1] % 4 == 0 and int(shotnum) % 2 == 0) or (sorted_res[0][1] % 4 == 2 and int(shotnum) % 2 == 1):
        ismine = 1
    if ismine == 1:
        return xuanjin(sorted_res)

    if ismine == 0:  # 不是自己的
        # 判断敌方壶前、后方有无障碍
        before = 0  # 0表示无障碍遮挡 1表示有遮挡
        after = 0  # 0表示无障碍遮挡 1表示有遮挡
        # 球前遮挡数量 分左中右
        cntbeforeleft = 0
        cntbefore = 0
        cntbeforeright = 0
        # 球后遮挡数量 分左中右
        cntafterleft = 0
        cntafter = 0
        cntafterright = 0
        # 所有左右侧球
        left = 0
        right = 0
        # for i in range(1, len(sorted_res)):
        print("range:")
        print(min(15, int(shotnum)))
        for i in range(1, min(15, int(shotnum))):
            if sorted_res[i][0] == 1000:
                break
            if sorted_res[i][2] > 2.475:
                right += 1
            elif sorted_res[i][2] < 2.275:
                left += 1
            disX = sorted_res[i][2] - sorted_res[0][2]
            disY = sorted_res[i][3] - sorted_res[0][3]
            print("disX disY " + str(disX) + ' ' + str(disY))
            if disY > 0:  # 有球在目标球前方
                # 判断坐标之差小于直径 说明被遮挡
                if abs(disX) < 0.29:
                    before = 1
                    if disX > 0.05:
                        cntbeforeright += 1
                    elif disX < -0.05:
                        cntbeforeleft += 1
                    else:
                        cntbefore += 1
            else:  # 有球目标球在后方
                if abs(disY) < 0.29:  # 两者黏在一起,隔得太远就当不存在 不用管
                    if abs(disX) < 0.29:
                        after = 1
                        if disX > 0.05:
                            cntafterright += 1
                        elif disX < -0.05:
                            cntafterleft += 1
                        else:
                            cntafter += 1
        ball = sorted_res[0]

        if before == 0:  # 直线前方无障碍  撞击
            print("before=0")
            if int(shotnum) <= 5:  # 前5壶
                if sorted_res[0][3] > 4.05:  # 在上半区中间以下
                    v = 3.1
                    if sorted_res[0][3] < 5.76:  # 分段分速度贴近
                        v = 3.4
                    elif sorted_res[0][3] < 6.3:
                        v = 3.55
                    else:
                        v = 3.7
                    h_x = sorted_res[0][2] - 2.375 + 0.0232
                    h_ang = 0
                    if cntafter == 0:  # 后面没有直接挡住的 贴近
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot
                    else:  # 后面有挡住的 速度+0.5
                        v += 0.5
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot
                else:
                    # 判断中线有无壶
                    block = 0
                    for i in range(min(15, int(shotnum))):
                        if sorted_res[i][0] == 1000:
                            break
                        if sorted_res[i][3] < 6: continue
                        if sorted_res[i][2] > 2.23 and sorted_res[i][2] < 2.52:
                            block = 1
                    if block == 0:
                        bestshot = str("BESTSHOT 2.75 0 0")
                        return bestshot
                    else:
                        return xuanjin(sorted_res)
            else:  # 打定
                # 在上半区以上或者在左右边缘就xuanjin了
                if sorted_res[0][3] < 4.05 or sorted_res[0][2] < 0.875 or sorted_res[0][2] > 3.875 or sorted_res[0][
                    3] > 6.6:
                    block = 0
                    for i in range(min(15, int(shotnum))):
                        if sorted_res[i][0] == 1000:
                            break
                        if sorted_res[i][3] < 6.5: continue
                        if sorted_res[i][2] > 2.23 and sorted_res[i][2] < 2.52:
                            block = 1
                    if block == 0:
                        bestshot = str("BESTSHOT 2.75 0 0")
                        return bestshot
                    else:
                        print("edge xuanjin")
                        return xuanjin(sorted_res)
                v = 5
                if ball[3] > 8.7:
                    v = 5
                elif ball[3] > 7.5:
                    v = 5.25
                elif ball[3] > 6.8:
                    v = 5.5
                elif ball[3] > 5:
                    v = 6
                else:
                    v = 6.5
                h_x = sorted_res[0][2] - 2.375 + 0.0232
                h_ang = 0
                bestshot = [v, h_x, h_ang]
                bestshot = list_to_str(bestshot)
                return bestshot

        # 找最下面那颗无遮挡的球

        for i in range(min(15, int(shotnum))):
            if sorted_res[i][0] == 1000:
                break
            disX = sorted_res[i][2] - sorted_res[0][2]
            if abs(disX) < 0.29 and sorted_res[i][3] > ball[3]:
                ball = sorted_res[i]

        if before == 1 and after == 0:  # 前面有障碍后面无 旋进击打
            print("before=1 and after=0")
            if sorted_res[0][3] < 4.05 or sorted_res[0][2] < 0.875 or sorted_res[0][2] > 3.875 or sorted_res[0][
                3] > 6.4:
                block = 0
                for i in range(min(15, int(shotnum))):
                    if sorted_res[i][0] == 1000:
                        break
                    if sorted_res[i][3] < 6.5: continue
                    if sorted_res[i][2] > 2.23 and sorted_res[i][2] < 2.52:
                        block = 1
                if block == 0:
                    bestshot = str("BESTSHOT 2.75 0 0")
                    return bestshot
                else:
                    print("edge xuanjin")
                    return xuanjin(sorted_res)
            print("shotnum" + str(shotnum))
            l = bigleftxuanke(sorted_res)
            r = bigrightxuanke(sorted_res)
            print("l,r:" + str(l) +'   '+ str(r))
            h_xl = -1.42 + sorted_res[0][2] - 2.375
            h_xr = 1.42 + sorted_res[0][2] - 2.375
            if l != -1:
                h_xl += l
            if r != -1:
                h_xr += r
            if h_xl <= -2.225 and h_xr >= 2.225:  # 左右都出界,打定障碍球
                if shotnum == "15":
                    return lastxuanjin(sorted_res)
                if int(shotnum) < 5:
                    return qianguaqiu(sorted_res)
                print("left and right both are out of range")
                if abs(ball[2] - sorted_res[0][2]) > 0.12:  # 斜线撞
                    k = (ball[3] - sorted_res[0][3]) / (ball[2] - sorted_res[0][2])
                    print("k=" + str(k))
                    cos = abs(sorted_res[0][2] - ball[2]) / (
                        math.sqrt((sorted_res[0][3] - ball[3]) ** 2 + (sorted_res[0][2] - ball[2]) ** 2))
                    disX = 0.29 * cos
                    x = 0
                    if k > 0:
                        x = ball[2] + disX
                        print(x)
                    else:
                        x = ball[2] - disX
                        print(x)
                    if x < 0.15 or x > 4.6:
                        return xuanjin(sorted_res)
                    v = 7
                    h_x = x - 2.375 + 0.0232
                    h_ang = 0
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
                # 否则正碰
                v = 5
                if ball[3] > 8.7:
                    v = 5
                elif ball[3] > 7.5:
                    v = 5.25
                elif ball[3] > 6.8:
                    v = 5.5
                elif ball[3] > 5:
                    v = 6
                else:
                    v = 6.5
                h_x = ball[2] - 2.375 + 0.0232
                h_ang = 0
                bestshot = [v, h_x, h_ang]
                bestshot = list_to_str(bestshot)
                return bestshot
            if h_xl <= -2.225:  # 左侧出界右侧不出
                print("left out of range")
                ok = bigrightxuanke(sorted_res)  # 右侧旋磕
                if ok != -1 and lianqiu(sorted_res)==1:
                    h_x = 1.42 + sorted_res[0][2] - 2.375 + r
                    v = 3.4
                    h_ang = -10
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
                else:  # 不行
                    if shotnum == "15":
                        return lastxuanjin(sorted_res)
                    if int(shotnum) < 5:
                        return qianguaqiu(sorted_res)
                    if abs(ball[2] - sorted_res[0][2]) > 0.12:  # 斜线撞
                        k = (ball[3] - sorted_res[0][3]) / (ball[2] - sorted_res[0][2])
                        print("k=" + str(k))
                        cos = abs(sorted_res[0][2] - ball[2]) / (
                            math.sqrt((sorted_res[0][3] - ball[3]) ** 2 + (sorted_res[0][2] - ball[2]) ** 2))
                        disX = 0.29 * cos
                        x = 0
                        if k > 0:
                            x = ball[2] + disX
                            print(x)
                        else:
                            x = ball[2] - disX
                            print(x)
                        x = noblock(sorted_res, x, ball[3], k)
                        if x < 0.15 or x > 4.6:
                            return xuanjin(sorted_res)
                        v = 7
                        if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                                ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
                            v = 7
                        else:
                            v = 8.5
                        h_x = x - 2.375 + 0.0232
                        h_ang = 0
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot
                    v = 5
                    if ball[3] > 8.7:
                        v = 5
                    elif ball[3] > 7.5:
                        v = 5.25
                    elif ball[3] > 6.8:
                        v = 5.5
                    elif ball[3] > 5:
                        v = 6
                    else:
                        v = 6.5
                    h_x = ball[2] - 2.375 + 0.0232
                    h_ang = 0
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
            if h_xr >= 2.225:  # 右侧出界左侧不出
                print("right out of range")
                ok = bigleftxuanke(sorted_res)  # 左侧旋磕
                if ok != -1 and lianqiu(sorted_res)==1:
                    h_x = -1.42 + sorted_res[0][2] - 2.375 + l
                    v = 3.4
                    h_ang = 10
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
                else:  # 不行
                    if shotnum == "15":
                        return lastxuanjin(sorted_res)
                    if int(shotnum) < 5:
                        return qianguaqiu(sorted_res)
                    if abs(ball[2] - sorted_res[0][2]) > 0.12:
                        k = (ball[3] - sorted_res[0][3]) / (ball[2] - sorted_res[0][2])
                        print("k=" + str(k))
                        cos = abs(sorted_res[0][2] - ball[2]) / (
                            math.sqrt((sorted_res[0][3] - ball[3]) ** 2 + (sorted_res[0][2] - ball[2]) ** 2))
                        disX = 0.29 * cos
                        x = 0
                        if k > 0:
                            x = ball[2] + disX
                            print(x)
                        else:
                            x = ball[2] - disX
                            print(x)
                        x = noblock(sorted_res, x, ball[3], k)
                        if x < 0.15 or x > 4.6:
                            return xuanjin(sorted_res)
                        v = 7
                        if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                                ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
                            v = 7
                        else:
                            v = 8.5
                        h_x = x - 2.375 + 0.0232
                        h_ang = 0
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot
                    v = 5
                    if ball[3] > 8.7:
                        v = 5
                    elif ball[3] > 7.5:
                        v = 5.25
                    elif ball[3] > 6.8:
                        v = 5.5
                    elif ball[3] > 5:
                        v = 6
                    else:
                        v = 6.5
                    h_x = ball[2] - 2.375 + 0.0232
                    h_ang = 0
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot

            # 到这里左右都不出界 尝试先尝试右 不行就左
            print("l/r in range")
            ok = bigrightxuanke(sorted_res)
            if ok != -1 and lianqiu(sorted_res)==1:
                h_x = 1.42 + sorted_res[0][2] - 2.375 + r
                v = 3.4
                h_ang = -10
                bestshot = [v, h_x, h_ang]
                bestshot = list_to_str(bestshot)
                return bestshot
            else:
                ok = bigleftxuanke(sorted_res)
                if ok != -1 and lianqiu(sorted_res)==1:
                    h_x = -1.42 + sorted_res[0][2] - 2.375 + l
                    v = 3.4
                    h_ang = 10
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
                else:

                    if shotnum == "15":
                        return lastxuanjin(sorted_res)
                    if int(shotnum) < 5:
                        return qianguaqiu(sorted_res)
                    if abs(ball[2] - sorted_res[0][2]) > 0.12:
                        k = (ball[3] - sorted_res[0][3]) / (ball[2] - sorted_res[0][2])
                        print("k=" + str(k))
                        cos = abs(sorted_res[0][2] - ball[2]) / (
                            math.sqrt((sorted_res[0][3] - ball[3]) ** 2 + (sorted_res[0][2] - ball[2]) ** 2))
                        disX = 0.29 * cos
                        x = 0
                        if k > 0:
                            x = ball[2] + disX
                            print(x)
                        else:
                            x = ball[2] - disX
                            print(x)
                        x = noblock(sorted_res, x, ball[3], k)
                        if x < 0.15 or x > 4.6:
                            return xuanjin(sorted_res)
                        v = 7
                        if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                                ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
                            v = 7
                        else:
                            v = 8.5
                        h_x = x - 2.375 + 0.0232
                        h_ang = 0
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot
                    v = 5
                    if ball[3] > 8.7:
                        v = 5
                    elif ball[3] > 7.5:
                        v = 5.25
                    elif ball[3] > 6.8:
                        v = 5.5
                    elif ball[3] > 5:
                        v = 6
                    else:
                        v = 6.5
                    h_x = ball[2] - 2.375 + 0.0232
                    h_ang = 0
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot

        if before == 1 and after == 1:  # 前面后面都有障碍 旋进击打【大力】
            print("before=1 and after=1")
            if sorted_res[0][3] < 4.05 or sorted_res[0][2] < 0.875 or sorted_res[0][2] > 3.875 or sorted_res[0][
                3] > 6.4:
                block = 0
                for i in range(min(15, int(shotnum))):
                    if sorted_res[i][0] == 1000:
                        break
                    if sorted_res[i][3] < 6.5: continue
                    if sorted_res[i][2] > 2.23 and sorted_res[i][2] < 2.52:
                        block = 1
                if block == 0:
                    bestshot = str("BESTSHOT 2.75 0 0")
                    return bestshot
                else:
                    print("edge xuanjin")
                    return xuanjin(sorted_res)
            l = bigleftxuanke(sorted_res)
            r = bigrightxuanke(sorted_res)
            h_xl = -1.42 + sorted_res[0][2] - 2.375
            h_xr = 1.42 + sorted_res[0][2] - 2.375
            if l != -1:
                h_xl += l
            if r != -1:
                h_xr += r
            if h_xl <= -2.225 and h_xr >= 2.225:  # 左右都出界,打定障碍球
                if shotnum == "15":
                    return lastxuanjin(sorted_res)
                if int(shotnum) < 5:
                    return qianguaqiu(sorted_res)
                print("left and right both are out of range")
                v = 5
                if ball[3] > 8.7:
                    v = 5
                elif ball[3] > 7.5:
                    v = 5.25
                elif ball[3] > 6.8:
                    v = 5.5
                elif ball[3] > 5:
                    v = 6
                else:
                    v = 6.5
                if abs(ball[2] - sorted_res[0][2]) > 0.12:
                    k = (ball[3] - sorted_res[0][3]) / (ball[2] - sorted_res[0][2])
                    print("k=" + str(k))
                    cos = abs(sorted_res[0][2] - ball[2]) / (
                        math.sqrt((sorted_res[0][3] - ball[3]) ** 2 + (sorted_res[0][2] - ball[2]) ** 2))
                    disX = 0.29 * cos
                    x = 0
                    if k > 0:
                        x = ball[2] + disX
                        print(x)
                    else:
                        x = ball[2] - disX
                        print(x)
                    x = noblock(sorted_res, x, ball[3], k)
                    if x < 0.15 or x > 4.6:
                        return xuanjin(sorted_res)
                    v = 7
                    if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                            ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
                        v = 7
                    else:
                        v = 8.5
                    h_x = x - 2.375 + 0.0232
                    h_ang = 0
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
                h_x = ball[2] - 2.375 + 0.0232
                h_ang = 0
                bestshot = [v, h_x, h_ang]
                bestshot = list_to_str(bestshot)
                return bestshot
            if h_xl <= -2.225:  # 左侧出界右侧不出
                print("left out of range")
                ok = bigrightxuanke(sorted_res)  # 右侧旋磕
                if ok != -1 and lianqiu(sorted_res)==1:
                    h_x = 1.42 + sorted_res[0][2] - 2.375 + r
                    v = 3.4
                    h_ang = -10
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
                else:  # 不行
                    if shotnum == "15":
                        return lastxuanjin(sorted_res)
                    if int(shotnum) < 5:
                        return qianguaqiu(sorted_res)
                    v = 5
                    if ball[3] > 8.7:
                        v = 5
                    elif ball[3] > 7.5:
                        v = 5.25
                    elif ball[3] > 6.8:
                        v = 5.5
                    elif ball[3] > 5:
                        v = 6
                    else:
                        v = 6.5
                    if abs(ball[2] - sorted_res[0][2]) > 0.12:
                        k = (ball[3] - sorted_res[0][3]) / (ball[2] - sorted_res[0][2])
                        print("k=" + str(k))
                        cos = abs(sorted_res[0][2] - ball[2]) / (
                            math.sqrt((sorted_res[0][3] - ball[3]) ** 2 + (sorted_res[0][2] - ball[2]) ** 2))
                        disX = 0.29 * cos
                        x = 0
                        if k > 0:
                            x = ball[2] + disX
                            print(x)
                        else:
                            x = ball[2] - disX
                            print(x)
                        x = noblock(sorted_res, x, ball[3], k)
                        if x < 0.15 or x > 4.6:
                            return xuanjin(sorted_res)
                        v = 7
                        if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                                ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
                            v = 7
                        else:
                            v = 8.5
                        h_x = x - 2.375 + 0.0232
                        h_ang = 0
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot
                    h_x = ball[2] - 2.375 + 0.0232
                    h_ang = 0
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
            if h_xr >= 2.225:  # 右侧出界左侧不出
                print("right out of range")
                ok = bigleftxuanke(sorted_res)  # 左侧旋磕
                if ok != -1 and lianqiu(sorted_res)==1:
                    h_x = -1.42 + sorted_res[0][2] - 2.375 + l
                    v = 3.4
                    h_ang = 10
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
                else:  # 不行
                    if shotnum == "15":
                        return lastxuanjin(sorted_res)
                    if int(shotnum) < 5:
                        return qianguaqiu(sorted_res)
                    v = 5
                    if ball[3] > 8.7:
                        v = 5
                    elif ball[3] > 7.5:
                        v = 5.25
                    elif ball[3] > 6.8:
                        v = 5.5
                    elif ball[3] > 5:
                        v = 6
                    else:
                        v = 6.5
                    if abs(ball[2] - sorted_res[0][2]) > 0.12:
                        k = (ball[3] - sorted_res[0][3]) / (ball[2] - sorted_res[0][2])
                        print("k=" + str(k))
                        cos = abs(sorted_res[0][2] - ball[2]) / (
                            math.sqrt((sorted_res[0][3] - ball[3]) ** 2 + (sorted_res[0][2] - ball[2]) ** 2))
                        disX = 0.29 * cos
                        x = 0
                        if k > 0:
                            x = ball[2] + disX
                            print(x)
                        else:
                            x = ball[2] - disX
                            print(x)
                        x = noblock(sorted_res, x, ball[3], k)
                        if x < 0.15 or x > 4.6:
                            return xuanjin(sorted_res)
                        v = 7
                        if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                                ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
                            v = 7
                        else:
                            v = 8.5
                        h_x = x - 2.375 + 0.0232
                        h_ang = 0
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot
                    h_x = ball[2] - 2.375 + 0.0232
                    h_ang = 0
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
            # 都不出界
            print("l/r in range")
            ok = bigrightxuanke(sorted_res)
            if ok != -1 and lianqiu(sorted_res)==1:
                h_x = 1.42 + sorted_res[0][2] - 2.375 + r
                v = 3.4
                h_ang = -10
                bestshot = [v, h_x, h_ang]
                bestshot = list_to_str(bestshot)
                return bestshot
            else:
                ok = bigleftxuanke(sorted_res)
                if ok != -1 and lianqiu(sorted_res)==1:
                    h_x = -1.42 + sorted_res[0][2] - 2.375 + l
                    v = 3.4
                    h_ang = 10
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
                else:
                    if shotnum == "15":
                        return lastxuanjin(sorted_res)
                    if int(shotnum) < 5:
                        return qianguaqiu(sorted_res)
                    v = 5
                    if ball[3] > 8.7:
                        v = 5
                    elif ball[3] > 7.5:
                        v = 5.25
                    elif ball[3] > 6.8:
                        v = 5.5
                    elif ball[3] > 5:
                        v = 6
                    else:
                        v = 6.5
                    if abs(ball[2] - sorted_res[0][2]) > 0.12:
                        k = (ball[3] - sorted_res[0][3]) / (ball[2] - sorted_res[0][2])
                        print("k=" + str(k))
                        cos = abs(sorted_res[0][2] - ball[2]) / (
                            math.sqrt((sorted_res[0][3] - ball[3]) ** 2 + (sorted_res[0][2] - ball[2]) ** 2))
                        disX = 0.29 * cos
                        x = 0
                        if k > 0:
                            x = ball[2] + disX
                            print(x)
                        else:
                            x = ball[2] - disX
                            print(x)
                        x = noblock(sorted_res, x, ball[3], k)
                        if x < 0.15 or x > 4.6:
                            return xuanjin(sorted_res)
                        v = 7
                        if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                                ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
                            v = 7
                        else:
                            v = 8.5
                        h_x = x - 2.375 + 0.0232
                        h_ang = 0
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot
                    h_x = ball[2] - 2.375 + 0.0232
                    h_ang = 0
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot


def less_ball(sorted_res, R):
    left_up, left_down, right_up, right_down = 0, 0, 0, 0
    for i in range(0, min(15, int(shotnum))):
        if sorted_res[i][0] == 1000:
            break
        if sorted_res[i][2] > 2.375 and sorted_res[i][2] < 2.375 + R:
            if sorted_res[i][3] > 4.88 and sorted_res[i][3] < 4.88 + R:
                right_down += 1
            elif sorted_res[i][3] < 4.88 and sorted_res[i][3] > 4.88 - R:
                right_up += 1
        elif sorted_res[i][2] < 2.375 and sorted_res[i][2] > 2.375 - R:
            if sorted_res[i][3] > 4.88 and sorted_res[i][3] < 4.88 + R:
                left_down += 1
            elif sorted_res[i][3] < 4.88 and sorted_res[i][3] > 4.88 - R:
                left_up += 1
    count_ball = []
    count_ball.append([left_up, True, True])
    count_ball.append([left_down, True, False])
    count_ball.append([right_down, False, False])
    count_ball.append([right_up, False, True])
    count_ball = sorted(count_ball)
    return count_ball[0][1], count_ball[0][2]


def y_488(sorted_res):
    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 右
        if float(sorted_res[i][3]) != 0:
            temp = tracel(float(sorted_res[i][3]))
            temp = int(temp * 100)
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 34, 34):
                ind = j + ttemp - temp - 145 + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    l = 0
    for i in range(237 - 145, 476):
        if (res[i] == 0):
            l = i
            break
    x_l = l - 237 + 145
    for i in range(237 + 145, 0, -1):
        if (res[i] == 0):
            if (x_l > 237 - 145 - i):
                x_l = 237 - 145 - i
                l = i
            break
    if (l > 330):
        x_l = 10000
    print(l)
    print(x_l)
    h_xl = l - 237
    h_xl = float(h_xl) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 左
        if float(sorted_res[i][3]) != 0:
            temp = tracer(float(sorted_res[i][3]))
            temp = int(temp * 100)
            # print(temp)
            ttemp = int(sorted_res[i][2] * 100)
            # print(ttemp)
            for j in range(- 34, 34):
                ind = j + ttemp - temp + 145 + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                # print(ind)
                res[ind] = 1
        else:
            break
    r = 477
    for i in range(237 + 145, 476):
        if (res[i] == 0):
            r = i
            break
    x_r = r - 237 - 145
    for i in range(237 + 145, 0, -1):
        if (res[i] == 0):
            if (x_r > 237 + 145 - i):
                x_r = 237 + 145 - i
                r = i
            break

    if (r == 477 or r < 145):
        x_r = 10000
    print(r)
    print(x_r)
    h_xr = r - 237
    h_xr = float(h_xr) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 直
        if float(sorted_res[i][3]) != 0:
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 34, 34):
                ind = j + ttemp
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    z = 0
    for i in range(237, 476):
        if (res[i] == 0):
            z = i
            break
    x_z = z - 237
    for i in range(237, 0, -1):
        if (res[i] == 0):
            if (x_z > 237 - i):
                x_z = 237 - i
                z = i
            break
    print(z)
    print(x_z)
    h_xz = z - 237
    h_xz = float(h_xz) / 100
    x = min(x_z, x_r)
    x = min(x, x_l)

    if (x_z == x):
        v = 2.99
        h_x = h_xz
        h_ang = 0
    if (x_r == x):
        v = 3.06
        h_x = h_xr
        h_ang = -10
    if (x_l == x):
        v = 3.06
        h_x = h_xl
        h_ang = 10
    if (z == 0):
        v = -1
    if (z == 0 or x > 110):
        v = -1
    return v, h_x, h_ang


def y_616(sorted_res):
    n = 477
    off = 136
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 右
        if float(sorted_res[i][3]) != 0:
            temp = tracel_616(float(sorted_res[i][3]))
            temp = int(temp * 100)
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 36, 36):
                ind = j + ttemp - temp - off + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    l = 0
    for i in range(237 - off, 476):
        if (res[i] == 0):
            l = i
            break
    x_l = l - 237 + off
    for i in range(237 + off, 0, -1):
        if (res[i] == 0):
            if (x_l > 237 - off - i):
                x_l = 237 - off - i
                l = i
            break
    if (l > 475 - off):
        x_l = 10000
    print(l)
    print(x_l)
    h_xl = l - 237
    h_xl = float(h_xl) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 左
        if float(sorted_res[i][3]) != 0:
            temp = tracer_616(float(sorted_res[i][3]))
            temp = int(temp * 100)
            # print(temp)
            ttemp = int(sorted_res[i][2] * 100)
            # print(ttemp)
            for j in range(- 34, 34):
                ind = j + ttemp - temp + off + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                # print(ind)
                res[ind] = 1
        else:
            break
    r = 477
    for i in range(237 + off, 476):
        if (res[i] == 0):
            r = i
            break
    x_r = r - 237 - off
    for i in range(237 + off, 0, -1):
        if (res[i] == 0):
            if (x_r > 237 + off - i):
                x_r = 237 + off - i
                r = i
            break

    if (r == 477 or r < off):
        x_r = 10000
    print(r)
    print(x_r)
    h_xr = r - 237
    h_xr = float(h_xr) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 直
        if float(sorted_res[i][3]) != 0:
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 34, 34):
                ind = j + ttemp
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    z = 0
    for i in range(237, 476):
        if (res[i] == 0):
            z = i
            break
    x_z = z - 237
    for i in range(237, 0, -1):
        if (res[i] == 0):
            if (x_z > 237 - i):
                x_z = 237 - i
                z = i
            break
    print(z)
    print(x_z)
    h_xz = z - 237
    h_xz = float(h_xz) / 100
    x = min(x_z, x_r)
    x = min(x, x_l)

    if (x_z == x):
        v = 2.85
        h_x = h_xz
        h_ang = 0
    if (x_r == x):
        v = 2.92
        h_x = h_xr
        h_ang = -10
    if (x_l == x):
        v = 2.92
        h_x = h_xl
        h_ang = 10
    if (z == 0 or x > 120):
        v = -1
    return v, h_x, h_ang


def tracel_616(y):
    if y > 5.9:
        return (((-0.003 * y + 0.0789) * y - 0.7652) * y + 4.7728)
    else:
        return 100


def tracer_616(y):
    if y > 5.9:
        return (((0.0028 * y - 0.0754) * y + 0.7373) * y + 0.0048)
    else:
        return 100


def y_554(sorted_res):
    n = 477
    off = 140
    v_z = 2.92
    v_lr = 2.99
    edge = 120
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 右
        if float(sorted_res[i][3]) != 0:
            temp = tracel_554(float(sorted_res[i][3]))
            temp = int(temp * 100)
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 34, 34):
                ind = j + ttemp - temp - off + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    l = 0
    for i in range(237 - off, 476):
        if (res[i] == 0):
            l = i
            break
    x_l = l - 237 + off
    for i in range(237 + off, 0, -1):
        if (res[i] == 0):
            if (x_l > 237 - off - i):
                x_l = 237 - off - i
                l = i
            break
    if (l > 475 - off):
        x_l = 10000
    print(l)
    print(x_l)
    h_xl = l - 237
    h_xl = float(h_xl) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 左
        if float(sorted_res[i][3]) != 0:
            temp = tracer_554(float(sorted_res[i][3]))
            temp = int(temp * 100)
            # print(temp)
            ttemp = int(sorted_res[i][2] * 100)
            # print(ttemp)
            for j in range(- 34, 34):
                ind = j + ttemp - temp + off + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                # print(ind)
                res[ind] = 1
        else:
            break
    r = 477
    for i in range(237 + off, 476):
        if (res[i] == 0):
            r = i
            break
    x_r = r - 237 - off
    for i in range(237 + off, 0, -1):
        if (res[i] == 0):
            if (x_r > 237 + off - i):
                x_r = 237 + off - i
                r = i
            break

    if (r == 477 or r < off):
        x_r = 10000
    print(r)
    print(x_r)
    h_xr = r - 237
    h_xr = float(h_xr) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 直
        if float(sorted_res[i][3]) != 0:
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 34, 34):
                ind = j + ttemp
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    z = 0
    for i in range(237, 476):
        if (res[i] == 0):
            z = i
            break
    x_z = z - 237
    for i in range(237, 0, -1):
        if (res[i] == 0):
            if (x_z > 237 - i):
                x_z = 237 - i
                z = i
            break
    print(z)
    print(x_z)
    h_xz = z - 237
    h_xz = float(h_xz) / 100
    x = min(x_z, x_r)
    x = min(x, x_l)

    if (x_z == x):
        v = v_z
        h_x = h_xz
        h_ang = 0
    if (x_r == x):
        v = v_lr
        h_x = h_xr
        h_ang = -10
    if (x_l == x):
        v = v_lr
        h_x = h_xl
        h_ang = 10
    if (z == 0 or x > edge):
        v = -1
    return v, h_x, h_ang


def tracel_554(y):
    if y > 5.3:
        return (((-0.0032 * y + 0.0787) * y - 0.7065) * y + 4.4116)
    else:
        return 100


def tracer_554(y):
    if y > 5.3:
        return (((0.0018 * y - 0.0455) * y + 0.4529) * y + 0.9263)
    else:
        return 100


def y_423(sorted_res):
    n = 477
    off = 148
    v_z = 3.06
    v_lr = 3.13
    edge = 90
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 右
        if float(sorted_res[i][3]) != 0:
            temp = tracel_423(float(sorted_res[i][3]))
            temp = int(temp * 100)
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 34, 34):
                ind = j + ttemp - temp - off + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    l = 0
    for i in range(237 - off, 476):
        if (res[i] == 0):
            l = i
            break
    x_l = l - 237 + off
    for i in range(237 + off, 0, -1):
        if (res[i] == 0):
            if (x_l > 237 - off - i):
                x_l = 237 - off - i
                l = i
            break
    if (l > 475 - off):
        x_l = 10000
    print(l)
    print(x_l)
    h_xl = l - 237
    h_xl = float(h_xl) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 左
        if float(sorted_res[i][3]) != 0:
            temp = tracer_423(float(sorted_res[i][3]))
            temp = int(temp * 100)
            # print(temp)
            ttemp = int(sorted_res[i][2] * 100)
            # print(ttemp)
            for j in range(- 34, 34):
                ind = j + ttemp - temp + off + 237
                ind = max(ind, 0)
                ind = min(ind, 476)
                # print(ind)
                res[ind] = 1
        else:
            break
    r = 477
    for i in range(237 + off, 476):
        if (res[i] == 0):
            r = i
            break
    x_r = r - 237 - off
    for i in range(237 + off, 0, -1):
        if (res[i] == 0):
            if (x_r > 237 + off - i):
                x_r = 237 + off - i
                r = i
            break

    if (r == 477 or r < off):
        x_r = 10000
    print(r)
    print(x_r)
    h_xr = r - 237
    h_xr = float(h_xr) / 100

    n = 477
    res = [0 for i in range(n)]
    for i in range(min(15, int(shotnum) + 1)):  # 直
        if float(sorted_res[i][3]) != 0:
            ttemp = int(sorted_res[i][2] * 100)
            for j in range(- 34, 34):
                ind = j + ttemp
                ind = max(ind, 0)
                ind = min(ind, 476)
                res[ind] = 1
        else:
            break
    z = 0
    for i in range(237, 476):
        if (res[i] == 0):
            z = i
            break
    x_z = z - 237
    for i in range(237, 0, -1):
        if (res[i] == 0):
            if (x_z > 237 - i):
                x_z = 237 - i
                z = i
            break
    print(z)
    print(x_z)
    h_xz = z - 237
    h_xz = float(h_xz) / 100
    x = min(x_z, x_r)
    x = min(x, x_l)

    if (x_z == x):
        v = v_z
        h_x = h_xz
        h_ang = 0
    if (x_r == x):
        v = v_lr
        h_x = h_xr
        h_ang = -10
    if (x_l == x):
        v = v_lr
        h_x = h_xl
        h_ang = 10
    if (z == 0 or x > edge):
        v = -1
    return v, h_x, h_ang


def tracel_423(y):
    if y > 4:
        return (((-0.0027 * y + 0.0579) * y - 0.4739) * y + 3.5633)
    else:
        return 100


def tracer_423(y):
    if y > 4:
        return (((0.0025 * y - 0.0528) * y + 0.435) * y + 1.2332)
    else:
        return 100


def guaqiu(sorted_res):
    print("guaqiu")
    v = 2.4  # 速度
    h_x = 0  # 平移
    h_ang = 0  # 旋转
    # bestshot = [v, h_x, h_ang]
    # bestshot = list_to_str(bestshot)
    left, up = less_ball(sorted_res, 0.7)
    v, h_x, h_ang = y_488(sorted_res)
    # v, h_x, h_ang = y_554(sorted_res)
    # print(up)
    # print(bool(up) == 1)
    if (v == -1):
        if bool(up) == 1:
            v, h_x, h_ang = y_423(sorted_res)
            # if (v == -1):
            #     v, h_x, h_ang = y_616(sorted_res)#未完待续
        else:
            v, h_x, h_ang = y_554(sorted_res)
            if (v == -1):
                v, h_x, h_ang = y_616(sorted_res)
    if (v == -1):
        return xuanke(sorted_res)

    bestshot = [v, h_x, h_ang]
    bestshot = list_to_str(bestshot)
    return bestshot


def fangshou(sorted_res):
    print("fangshou")
    x = sorted_res[0][2]
    y = sorted_res[0][3]
    # print(x)
    # print(y)
    if (get_dist(x, y) > 0.7):  # 边缘球
        if int(shotnum) < 5:
            if have_ball(2.375, 6.5, sorted_res) == 0:
                v = 2.75  # 速度
                h_x = 0  # 平移
                h_ang = 0  # 旋转
                bestshot = [v, h_x, h_ang]
                bestshot = list_to_str(bestshot)
                return bestshot
            else:
                return xuanjin(sorted_res)
        else:
            if have_ball(2.375, 6, sorted_res) == 0:
                v = 2.85  # 速度
                h_x = 0  # 平移
                h_ang = 0  # 旋转
                bestshot = [v, h_x, h_ang]
                bestshot = list_to_str(bestshot)
                return bestshot
            else:
                return xuanjin(sorted_res)

    # if have_ball(x, y + 1.8, sorted_res) == 0:
    ran = random.randint(1, 2)
    if have_ball(x, y + 0.4, sorted_res) == 0:
        v = float(3.613 - 0.12234 * (y + 2.25))  # 速度
        h_x = x - 2.375  # 平移
        if (ran == 1):
            h_x = h_x - 0.17
        else:
            h_x = h_x + 0.13
        h_ang = 0  # 旋转
        bestshot = [v, h_x, h_ang]
        bestshot = list_to_str(bestshot)
        return bestshot
    # 两侧
    offx = 0.65
    offy = 1.1  # 1.49
    if have_ball(x - offx, y + offy - 0.2, sorted_res) == 0:
        if (x - offx >= 1.175 and x - offx <= 3.575):
            v = float(3.613 - 0.12234 * (y + offy))  # 速度
            h_x = x - 2.375 - offx  # 平移
            h_ang = 0  # 旋转
            bestshot = [v, h_x, h_ang]
            bestshot = list_to_str(bestshot)
            return bestshot
    if have_ball(x + offx, y + offy - 0.2, sorted_res) == 0:
        if (x + offx >= 1.175 and x + offx <= 3.575):
            v = float(3.613 - 0.12234 * (y + offy))  # 速度
            h_x = x - 2.375 + offx  # 平移
            h_ang = 0  # 旋转
            bestshot = [v, h_x, h_ang]
            bestshot = list_to_str(bestshot)
            return bestshot

    # return xuanjin(sorted_res)
    return guaqiu(sorted_res)


def last_xuanke(sorted_res):
    print("last_xuanke")
    ismine = 0  # 离中心最近的球是否为自己的
    print(ismine)
    if (sorted_res[0][1] % 4 == 0 and int(shotnum) % 2 == 0) or (sorted_res[0][1] % 4 == 2 and int(shotnum) % 2 == 1):
        ismine = 1
    if ismine == 1:
        return xuanjin(sorted_res)

    if ismine == 0:
        before = 0  # 0表示无障碍遮挡 1表示有遮挡
        for i in range(1, min(15, int(shotnum))):
            disX = sorted_res[i][2] - sorted_res[0][2]
            disY = sorted_res[i][3] - sorted_res[0][3]
            print("disX disY " + str(disX) + ' ' + str(disY))
            if disY > 0:  # 有球在目标球前方
                # 判断坐标之差小于直径 说明被遮挡
                if abs(disX) < 0.29:
                    before = 1
        ball = sorted_res[0]
        if before == 0:  # 无球遮挡
            v = 5
            if ball[3] > 8.7:
                v = 5
            elif ball[3] > 7.5:
                v = 5.25
            elif ball[3] > 6.8:
                v = 5.5
            elif ball[3] > 5:
                v = 6
            else:
                v = 6.5
            h_x = sorted_res[0][2] - 2.375 + 0.0232
            h_ang = 0
            bestshot = [v, h_x, h_ang]
            bestshot = list_to_str(bestshot)
            return bestshot
        else:  # 有球遮挡
            for i in range(min(15, int(shotnum))):
                disX = sorted_res[i][2] - sorted_res[0][2]
                if abs(disX) < 0.29 and sorted_res[i][3] > ball[3]:
                    ball = sorted_res[i]

            k = (ball[3] - sorted_res[0][3]) / (ball[2] - sorted_res[0][2])
            print("k=" + str(k))
            cos = abs(sorted_res[0][2] - ball[2]) / (
                math.sqrt((sorted_res[0][3] - ball[3]) ** 2 + (sorted_res[0][2] - ball[2])))
            offset = 0.29 * cos
            x = 0
            if k > 0:
                x = ball[2] + offset
                print('shot' + str(x))
            else:
                x = ball[2] - offset
                print('shot' + str(x))
            l = bigleftxuanke(sorted_res)
            r = bigrightxuanke(sorted_res)
            h_xl = -1.42 + sorted_res[0][2] - 2.375
            h_xr = 1.42 + sorted_res[0][2] - 2.375
            if l != -1:
                h_xl += l
            if r != -1:
                h_xr += r
            if h_xl <= -2.225 and h_xr >= 2.225:  # 左右都出界,打定障碍球
                print("left and right both are out of range")
                if x > 0.15 and x < 4.6:  # 斜线打击 不出界
                    print("k not out of range")
                    # 如果球是自己的
                    if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
                        print("ismine")
                        v = 8
                        h_x = x - 2.375 + 0.0232
                        h_ang = 0
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot
                    else:  # 球不是自己的
                        print("notmine")
                        v = 10
                        h_x = x - 2.375 + 0.01
                        h_ang = 0
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot

                else:
                    v = 5
                    if ball[3] > 8.7:
                        v = 5
                    elif ball[3] > 7.5:
                        v = 5.25
                    elif ball[3] > 6.8:
                        v = 5.5
                    elif ball[3] > 5:
                        v = 6
                    else:
                        v = 6.5
                    h_x = ball[2] - 2.375 + 0.0232
                    h_ang = 0
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
            if h_xl <= -2.225:  # 左侧出界右侧不出
                print("left out of range")
                ok = bigrightxuanke(sorted_res)  # 右侧旋磕
                if ok != -1 and lianqiu(sorted_res)==1:
                    h_x = 1.42 + sorted_res[0][2] - 2.375 + r
                    v = 3.4
                    h_ang = -10
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
                else:  # 不行 传击
                    if x > 0.15 and x < 4.6:  # 斜线传击 不出界
                        # 如果球是自己的
                        if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                                ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
                            print("ismine")
                            v = 8
                            h_x = x - 2.375 + 0.0232
                            h_ang = 0
                            bestshot = [v, h_x, h_ang]
                            bestshot = list_to_str(bestshot)
                            return bestshot
                        else:  # 球不是自己的
                            print("notmine")
                            v = 10
                            h_x = x - 2.375 + 0.01
                            h_ang = 0
                            bestshot = [v, h_x, h_ang]
                            bestshot = list_to_str(bestshot)
                            return bestshot

                    else:
                        v = 5
                        if ball[3] > 8.7:
                            v = 5
                        elif ball[3] > 7.5:
                            v = 5.25
                        elif ball[3] > 6.8:
                            v = 5.5
                        elif ball[3] > 5:
                            v = 6
                        else:
                            v = 6.5
                        h_x = ball[2] - 2.375 + 0.0232
                        h_ang = 0
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot
            if h_xr >= 2.225:  # 右侧出界左侧不出
                print("right out of range")
                ok = bigleftxuanke(sorted_res)  # 左侧旋磕
                if ok != -1 and lianqiu(sorted_res)==1:
                    h_x = -1.42 + sorted_res[0][2] - 2.375 + l
                    v = 3.4
                    h_ang = 10
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
                else:  # 不行 传击
                    if x > 0.15 and x < 4.6:  # 斜线打击 不出界
                        # 如果球是自己的
                        if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                                ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
                            print("ismine")
                            v = 8
                            h_x = x - 2.375 + 0.0232
                            h_ang = 0
                            bestshot = [v, h_x, h_ang]
                            bestshot = list_to_str(bestshot)
                            return bestshot
                        else:  # 球不是自己的
                            print("notmine")
                            v = 10
                            h_x = x - 2.375 + 0.01
                            h_ang = 0
                            bestshot = [v, h_x, h_ang]
                            bestshot = list_to_str(bestshot)
                            return bestshot

                    else:
                        v = 5
                        if ball[3] > 8.7:
                            v = 5
                        elif ball[3] > 7.5:
                            v = 5.25
                        elif ball[3] > 6.8:
                            v = 5.5
                        elif ball[3] > 5:
                            v = 6
                        else:
                            v = 6.5
                        h_x = ball[2] - 2.375 + 0.0232
                        h_ang = 0
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot

            # 到这里左右都不出界 尝试先尝试右 不行就左
            print("l/r in range")
            ok = bigrightxuanke(sorted_res)
            if ok != -1 and lianqiu(sorted_res)==1:
                h_x = 1.42 + sorted_res[0][2] - 2.375 + r
                v = 3.4
                h_ang = -10
                bestshot = [v, h_x, h_ang]
                bestshot = list_to_str(bestshot)
                return bestshot
            else:
                ok = bigleftxuanke(sorted_res)
                if ok != -1 and lianqiu(sorted_res)==1:
                    h_x = -1.42 + sorted_res[0][2] - 2.375 + l
                    v = 3.4
                    h_ang = 10
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
                    return bestshot
                else:
                    if x > 0.15 and x < 4.6:  # 斜线打击 不出界
                        # 如果球是自己的
                        print("ismine")
                        if (ball[1] % 4 == 0 and int(shotnum) % 2 == 0) or (
                                ball[1] % 4 == 2 and int(shotnum) % 2 == 1):
                            v = 8
                            h_x = x - 2.375 + 0.0232
                            h_ang = 0
                            bestshot = [v, h_x, h_ang]
                            bestshot = list_to_str(bestshot)
                            return bestshot
                        else:  # 球不是自己的
                            print("notmine")
                            v = 10
                            h_x = x - 2.375 + 0.01
                            h_ang = 0
                            bestshot = [v, h_x, h_ang]
                            bestshot = list_to_str(bestshot)
                            return bestshot

                    else:
                        v = 5
                        if ball[3] > 8.7:
                            v = 5
                        elif ball[3] > 7.5:
                            v = 5.25
                        elif ball[3] > 6.8:
                            v = 5.5
                        elif ball[3] > 5:
                            v = 6
                        else:
                            v = 6.5
                        h_x = ball[2] - 2.375 + 0.0232
                        h_ang = 0
                        bestshot = [v, h_x, h_ang]
                        bestshot = list_to_str(bestshot)
                        return bestshot


# pyinstaller -F CurlingAI.py
def count_num(sorted_res):
    num = 0
    while num < 15:
        if is_in_house(sorted_res[num][2], sorted_res[num][3]) == 0:
            break
        num += 1
    return num


def count_ball(sorted_res, num):
    result = 0
    for i in range(0, num):
        if (sorted_res[i][1] % 4) / 2 == int(shotnum) % 2:
            break
        result += 1
    return result


def count_their_ball(sorted_res, R, num):
    for i in range(0, num):
        if get_dist(sorted_res[i][2], sorted_res[i][3]) < R and (sorted_res[i][1] % 4) / 2 != int(shotnum) % 2:
            return False
    return True


def find_ball(sorted_res, num):
    result, number = 0, 1
    for i in range(0, num):
        if ((sorted_res[i][1] % 4) / 2) != (int(shotnum) % 2):
            result = i
            if i != num and (((sorted_res[i + 1][1] % 4) / 2) != (int(shotnum) % 2)):
                number = 2
            break
    return result, number


def boundary(R, sorted_res, count):
    empty = True
    for i in range(0, count):
        if ((sorted_res[i][2] - 2.375) * (sorted_res[i][2] - 2.375) + (sorted_res[i][3] - 4.88) * (
                sorted_res[i][3] - 4.88)) < R * R:
            empty = False
            break
    return empty


def tuijin(min_y, x):
    print("tuijin")
    print(min_y)
    if min_y > 9.3:
        v = 4.4
    elif min_y > 8.3:
        v = 4.3
    elif min_y > 8:
        v = 4.2
    elif min_y > 7.6:
        v = 4.14
    elif min_y > 7.45:  # ok
        v = 4.07
    elif min_y > 7.38:  # ok
        v = 4.02
    elif min_y > 7.3:  # ok
        v = 3.98
    elif min_y > 7.15:  # ok
        v = 3.94
    elif min_y > 7:  # ok
        v = 3.90
    elif min_y > 6.9:
        v = 3.85
    elif min_y > 6.8:  # ok
        v = 3.82
    elif min_y > 6.7:  # ok
        v = 3.78
    elif min_y > 6.6:  # ok
        v = 3.74
    elif min_y > 6.5:  # ok
        v = 3.69
    elif min_y > 6.4:  # ok
        v = 3.65
    elif min_y > 6.3:  # ok
        v = 3.61
    elif min_y > 6.2:  # ok
        v = 3.58
    elif min_y > 6.1:  # ok
        v = 3.55
    elif min_y > 6:  # ok
        v = 3.53
    elif min_y > 5.9:
        v = 3.51
    elif min_y > 5.85:
        v = 3.48
    elif min_y > 5.75:  # ok
        v = 3.46
    elif min_y > 5.6:  # ok
        v = 3.42
    elif min_y > 5.5:  # ok
        v = 3.38
    elif min_y > 5.4:  # ok
        v = 3.32
    elif min_y > 5.3:
        v = 3.31
    elif min_y > 5.2:
        v = 3.25
    elif min_y > 5.1:
        v = 3.2
    else:  # ok
        v = 3.18
    h_x = x - 2.375 + 0.0232
    h_ang = 0
    bestshot = [v, h_x, h_ang]
    bestshot = list_to_str(bestshot)
    return bestshot


def last_shot(sorted_res):
    print("last_shot")
    num = count_num(sorted_res)
    count = count_ball(sorted_res, num)
    print(num)
    i, number = find_ball(sorted_res, num)
    block = 0
    edge = 4.6
    m, j = 0, 0
    mine = True  # 中心球是我们的
    min_y = 100
    while m < 15:
        if sorted_res[m][0] == 1000:
            break
        if abs(sorted_res[m][2] - 2.375) < 1.2 and count_their_ball(sorted_res, abs(sorted_res[m][2] - 2.375) + 0.29,
                                                                    num) and sorted_res[m][3] > 5:
            block, j, mine = 0, 0, True
            while j < 15:  # 之前的所有壶遍历
                if sorted_res[j][0] == 1000:
                    break
                if (sorted_res[j][2] <= sorted_res[m][2] + 0.3 and sorted_res[j][2] >= sorted_res[m][2] - 0.3
                        and sorted_res[j][3] >= edge):  # 防守中线有壶
                    print('there is one')
                    if ((sorted_res[j][1] % 4) / 2) != (int(shotnum) % 2):
                        mine = False
                    block += 1
                    result = j
                    min_y = min(min_y, sorted_res[j][3])
                j += 1
        m += 1
        if block == 1 and mine == True:
            print('ready to push')
            break
    print('block = ' + str(block) + 'mine = ' + str(mine))
    if block == 1 and mine == True:
        bestshot = tuijin(min_y, sorted_res[result][2])
    else:
        if count == 0:
            if i == 0:
                bestshot = lastxuanjin(sorted_res)
            else:
                print('count==0,and change')
                print('number' + str(number))
                if number == 2:
                    bestshot = lastxuanjin(sorted_res)
                else:
                    point_num = 0
                    for k in range(i, num):
                        if ((sorted_res[k][1] % 4) / 2) == (int(shotnum) % 2):
                            point_num += 1
                    print('point_num' + str(point_num))
                    if point_num > 1:
                        sorted_res[0], sorted_res[i] = sorted_res[i], sorted_res[0]
                        bestshot = xuanke(sorted_res)
                    else:
                        bestshot = lastxuanjin(sorted_res)
        elif count == 1:
            print('count==1')

            bestshot = xuanke(sorted_res)
        elif count >= 2:
            if boundary(0.45, sorted_res, count):
                bestshot = lastxuanjin(sorted_res)
            else:
                bestshot = xuanke(sorted_res)
            if ((abs(sorted_res[0][2] - sorted_res[1][2]) < 0.45 and abs(sorted_res[0][3] - sorted_res[1][3]) < 0.3) or (abs(sorted_res[0][2] - sorted_res[1][2]) < 0.3 and abs(sorted_res[0][3] - sorted_res[1][3]) < 0.45)) and boundary(0.45, sorted_res, count)==False:
                k, fblock, fedge, middle = 0, 0, max(sorted_res[0][3], sorted_res[1][3]), float(
                    (sorted_res[0][2] + sorted_res[1][2])) / 2
                while k < 15:  # 之前的所有壶遍历
                    if sorted_res[k][0] == 1000:
                        break
                    if (sorted_res[k][2] <= middle + 0.3 and sorted_res[k][2] >= middle - 0.3
                            and float(sorted_res[k][3]) > fedge):  # 防守中线有壶
                        if ((sorted_res[k][1] % 4) / 2) != (int(shotnum) % 2):
                            mine = False
                        fblock += 1
                        result = i
                        min_y = min(min_y, sorted_res[i][3])
                    k += 1
                if block == 0:
                    v = 10
                    h_x = middle - 2.375 + 0.0232
                    h_ang = 0
                    bestshot = [v, h_x, h_ang]
                    bestshot = list_to_str(bestshot)
    return bestshot


def xian_last_shot(sorted_res):
    print("xian_last_shot")
    block = 0
    edge = 4.6
    i = 0
    mine = True  # 中心球是我们的
    min_y = 100
    num = count_num(sorted_res)
    count = count_ball(sorted_res, num)
    while i < 14:  # 之前的所有壶遍历
        if sorted_res[i][0] == 1000:
            break
        if (sorted_res[i][2] <= 2.675 and sorted_res[i][2] >= 2.075
                and float(sorted_res[i][3]) >= edge):  # 防守中线有壶
            if ((sorted_res[i][1] % 4) / 2) != (int(shotnum) % 2):
                mine = False
            block += 1
            result = i
            min_y = min(min_y, sorted_res[i][3])
        i += 1
    if block == 0:  # 中心无遮挡
        if count >= 1:
            p = 1
            p_block = 0
            while p < 14:  # 之前的所有壶遍历
                if sorted_res[p][0] == 1000:
                    break
                if (sorted_res[p][2] <= sorted_res[0][2] + 0.3 and sorted_res[p][2] >= sorted_res[0][2] - 0.3
                        and float(sorted_res[p][3]) > sorted_res[0][3]):  # 防守中线有壶
                    p_block += 1
                p += 1
            if p_block == 0:
                bestshot = tuijin(sorted_res[0][3],sorted_res[0][2])
            else:
                bestshot = last_xuanke(sorted_res)
        else:
            v = 2.92  # 速度
            h_x = 0  # 平移
            h_ang = 0  # 旋转
            bestshot = [v, h_x, h_ang]
            bestshot = list_to_str(bestshot)
            print('block == 0 , go to middle')
    elif block == 1 and mine == True:
        if min_y > 6:  # 这里写推进，注意！！！两个球不能在一条线上
            v = 0
            h_x = 0
            if min_y > 8.1:
                v = 4.22
                h_x = sorted_res[result][2] - 2.375 - 0.015
            elif min_y > 7.6:
                v = 4.05
                h_x = sorted_res[result][2] - 2.375 - 0.018
            elif min_y > 7.3:
                v = 3.92
                h_x = sorted_res[result][2] - 2.375 - 0.03
            elif min_y > 7:
                v = 3.85
                h_x = sorted_res[result][2] - 2.375 - 0.032
            elif min_y > 6.7:
                v = 3.82
                h_x = sorted_res[result][2] - 2.375 - 0.03
            else:
                v = 3.52
                h_x = sorted_res[result][2] - 2.375 - 0.042
            h_ang = 0
            bestshot = [v, h_x, h_ang]
            bestshot = list_to_str(bestshot)
            print('push')
        elif min_y > 5.3:
            bestshot = xuanjin(sorted_res)
            print('xuanjin')
        else:
            v = 2.92  # 速度
            h_x = 0  # 平移
            h_ang = 0  # 旋转
            bestshot = [v, h_x, h_ang]
            bestshot = list_to_str(bestshot)
    else:  # 改
        if boundary(0.45, sorted_res, count):
            bestshot = lastxuanjin(sorted_res)
        else:
            if count >= 1:
                q = 1
                q_block = 0
                while q < 14:  # 之前的所有壶遍历
                    if sorted_res[q][0] == 1000:
                        break
                    if (sorted_res[q][2] <= sorted_res[0][2] + 0.3 and sorted_res[q][2] >= sorted_res[0][2] - 0.3
                            and float(sorted_res[q][3]) > sorted_res[0][3]):  # 防守中线有壶
                        q_block += 1
                    q += 1
                if q_block == 0:
                    bestshot = tuijin(sorted_res[0][3],sorted_res[0][2])
                else:
                    okright = bigrightxuanke(sorted_res)
                    okleft = bigleftxuanke(sorted_res)
                    if okright != -1 or okleft != -1:
                        bestshot = last_xuanke(sorted_res)
                    else:
                        bestshot = lastxuanjin(sorted_res)
            else:
                bestshot = lastxuanjin(sorted_res)
    return bestshot


def leftorright(sorted_res, x, y, edge):
    l = 0
    r = 0
    for i in range(int(shotnum)):
        if(sorted_res[i][3] > y):
            if abs(sorted_res[i][2] - x) <= edge:
                if abs(sorted_res[i][2] - x) >= 0.15:
                    if(sorted_res[i][2] < x):
                        l += 1
                    else:
                        r += 1
    if(l >= r):
        return 1
    return 0

# pyinstaller -F CurlingAI.py
# 策略
def strategy(state_list):
    # 初始化
    print("strategy ver:8/14 20:51")
    global keep_lose, now_x, now_y, before_x, before_y
    sorted_res = []
    i = 0
    # 园内冰壶数量
    in_house = 0
    # 遍历 距离排序
    while i < 30:
        sorted_res.append([
            get_dist(float(state_list[0][i]), float(state_list[0][i + 1])),  # 到中心点的距离，场外为1000
            i,  # i % 4 == 0 为先手， i % 4 == 2 为后手    的壶
            float(state_list[0][i]),  # x坐标
            float(state_list[0][i + 1]),  # y坐标
            is_in_house(float(state_list[0][i]), float(state_list[0][i + 1]))  # 是否在大本营中
        ])
        if is_in_house(float(state_list[0][i]), float(state_list[0][i + 1])):
            in_house += 1
        i += 2

    sorted_res = sorted(sorted_res)
    print('keep_lose' + str(keep_lose))
    print('now ' + str(sorted_res[0][1]) + ' ' + str(shotnum))
    if ((sorted_res[0][1] % 4) / 2) != (int(shotnum) % 2):
        now_x, now_y = sorted_res[0][2], sorted_res[0][3]
        if (abs(now_x - before_x) < 0.01) and (abs(now_y - before_y) < 0.01) and (
                is_in_house(sorted_res[0][2], sorted_res[0][3]) == 1):
            keep_lose += 1
        else:
            keep_lose = 0
        before_x, before_y = now_x, now_y
    else:
        keep_lose = 0
    if keep_lose >= 3:
        ball = sorted_res[0]
        for i in range(min(15, int(shotnum))):
            if sorted_res[i][0] == 1000:
                break
            disX = sorted_res[i][2] - sorted_res[0][2]
            if abs(disX) < 0.29 and sorted_res[i][3] > ball[3]:
                ball = sorted_res[i]
        # 撞ball这个球
        v = 10
        h_x = ball[2] - 2.375 + 0.0232
        h_ang = 0
        bestshot = [v, h_x, h_ang]
        bestshot = list_to_str(bestshot)
        return bestshot

    for i in range(min(15, int(shotnum))):  # 打印所有数据
        if sorted_res[i][0] == 1000:
            break
        print(sorted_res[i])

    if in_house > 0:  # 有壶
        if int(shotnum) % 2 == 0:  # 先手
            if shotnum == "14":  # 最后一搏hhh
                return xian_last_shot(sorted_res)
            if sorted_res[0][1] % 4 == 0:  # 先手得分
                return fangshou(sorted_res)
            else:
                return xuanke(sorted_res)
        else:  # 后手
            if shotnum == "15":  # 最后一搏hhh
                return last_shot(sorted_res)
            if sorted_res[0][1] % 4 == 0:  # 先手得分
                return xuanke(sorted_res)
            else:
                return fangshou(sorted_res)
    else:  # 无壶
        if int(shotnum) % 2 == 0:  # 先手
            if shotnum == "14":  # 最后一搏hhh
                return xian_last_shot(sorted_res)
        else:  # 后手
            if shotnum == "15":  # 最后一搏hhh
                return last_shot(sorted_res)
        if int(shotnum) < 5:  # 前五壶
            i = 0
            block = 0
            edge = 6.8
            while i < 2 * int(shotnum):  # 之前的所有壶遍历
                if (float(state_list[0][i]) <= 2.6 and float(state_list[0][i]) >= 2.15
                        and float(state_list[0][i + 1]) >= edge):  # 防守中线有壶
                    block += 1
                i += 2
            if (block == 0):  # 中线无壶
                print("zhongxianwuhu")
                v = 2.75  # 速度
                h_x = 0  # 平移
                h_ang = 0  # 旋转
                bestshot = [v, h_x, h_ang]
                bestshot = list_to_str(bestshot)
                return bestshot
            else:
                return xuanjin(sorted_res)
        else:
            i = 0
            block = 0
            edge = 5.2
            while i < 2 * int(shotnum):  # 之前的所有壶遍历
                if (float(state_list[0][i]) <= 2.6 and float(state_list[0][i]) >= 2.15
                        and float(state_list[0][i + 1]) >= edge):  # 防守中线有壶
                    block += 1
                i += 2
            if (block == 0):  # 中线无壶
                print("zhongxianwuhu")
                v = 2.85  # 速度
                h_x = 0  # 平移
                h_ang = 0  # 旋转
                bestshot = [v, h_x, h_ang]
                bestshot = list_to_str(bestshot)
                return bestshot
            else:
                return xuanjin(sorted_res)

    # 一定要返回这几个值 否则程序卡住
    # 这几个应该用不到 出现就是bug了
    # print("WA")
    # v = 2.4  # 速度
    # h_x = 0  # 平移
    # h_ang = 0  # 旋转
    # bestshot = [v, h_x, h_ang]
    # bestshot = list_to_str(bestshot)
    # return bestshot


while True:
    ret = str(obj.recv(1024), encoding="utf-8")
    print("recv:" + ret)
    messageList = ret.split(" ")
    if messageList[0] == "NAME":  # 首局先后手 没用
        order = messageList[1]
        if order == str("Player1"):
            print("玩家1，首局先手")
        else:
            print("玩家2，首局后手")
    if messageList[0] == "ISREADY":
        time.sleep(0.5)
        obj.send(bytes("READYOK", encoding="utf-8"))
        print("send READYOK")
        obj.send(bytes("NAME 摩擦力规划局", encoding="utf-8"))
        # 名称
        print("send NAME")
    if messageList[0] == "POSITION":
        if state:
            state = []
        state.append(ret.split(" ")[1:31])
        # print("PO")
        print(state)
    if messageList[0] == "SETSTATE":
        # 第几投
        shotnum = ret.split(" ")[1]
        # 局数
        if ju != int(ret.split(" ")[2]):
            keep_lose = 0
        ju = int(ret.split(" ")[2])
        print(ju)
        # state.append(shotnum)
        if shotnum == "16":  # 重置
            if state:
                state = []
            state.append(ret.split(" ")[6:36])
            shotnum = "0"
        if shotnum == "0":  # 判断先后手
            firstsecond = ret.split(" ")[4]
        # print(firstsecond)
        print(state)
    if messageList[0] == "GO":
        shot = strategy(state)
        obj.send(bytes(shot, encoding="utf-8"))
    if messageList[0] == "MOTIONINFO":
        # 位置信息
        x_coordinate = float(messageList[1])
        y_coordinate = float(messageList[2])
        x_velocity = float(messageList[3])
        y_velocity = float(messageList[4])
        angular_velocity = float(messageList[5])
        # obj.send(bytes("SWEEP 4.0", encoding="utf-8"))

# 11.29
# pyinstaller -F CurlingAI.py
