import os
import numpy as np
import xlrd

"""0工作区编号(必填)	1钻孔编号(必填)	2回次号(必填)	3测点序号(必填)	4深度自(m)	5深度至(m)	
6岩心长度(m)	7测点位置(cm)	8岩性	9γ+β计数率	10γ+β照射量率	11γ+β换算系数	12γ计数率	13γ照射量率	14γ换算系数
"""


def tgtLen_cal(tgt):
    tolen = .0
    nc = []
    if tgt == 1:
        target_index = np.where(cols_doublejs >= 12)
        kuangduans = cols_shendus[target_index[0][0]] + cols_cedianweizhi[target_index[0][0]]
        for i in range(1, len(target_index[0])):
            cookie_e = 0.1
            cookie_s = 0.1
            if target_index[0][i] - target_index[0][i-1] >= 5:
                if cols_cedianweizhi[target_index[0][i-1]] == cols_yanxinchang[target_index[0][i-1]]:
                    cookie_e = 0
                if kuangduans == cols_shendus[target_index[0][i-1]]:
                    cookie_s = 0
                print("矿段的位置为", "%.2f" % (kuangduans-cookie_s), "~", "%.2f" % (kuangduane+cookie_e))
                nc.append(cols_double[target_index[0][i]])
                nca = np.sort(np.array(nc))
                print(nca)
                # print(nca[0], "~", nca[-2], "最高为", nca[-1])
                nc = []
                tolen += kuangduane - kuangduans + cookie_s + cookie_e
                kuangduans = cols_shendus[target_index[0][i]] + cols_cedianweizhi[target_index[0][i]]
                kuangduane = cols_shendus[target_index[0][i]] + cols_cedianweizhi[target_index[0][i]]
            else:
                kuangduane = cols_shendus[target_index[0][i]] + cols_cedianweizhi[target_index[0][i]]
                nc.append(cols_double[target_index[0][i]])
        print("矿段的位置为", "%.2f" % (kuangduans - cookie_s), "~", "%.2f" % (kuangduane + cookie_e))
        nca = np.sort(np.array(nc))
        print(nca)
        # print(nca[0], "~", nca[-2], "最高为", nca[-1])
        tolen += kuangduane - kuangduans + cookie_s + cookie_e
        print("编录矿段总长度为", "%.2f" % tolen)

    return tolen


def len2_cal():
    sheet2 = wb.sheet_by_index(1)
    cols_doublejs_jc = np.array(sheet2.col_values(9)[3:], dtype=float)
    target_index = np.where(cols_doublejs_jc >= 12)
    length = len(target_index[0])
    return length


def nC_mean_cal(st):
    if st == 1:
        total = .0
        num = 0
        for i in range(0, len(cols_double)):
            if cols_doublejs[i] > 12:
                total += cols_double[i]
                num += 1
        return total/num
    else:
        sheet2 = wb.sheet_by_index(1)
        if sheet2 == 0:
            return
        cols_doublejs_jc = np.array(sheet2.col_values(9)[3:], dtype=float)
        cols_double_jc = np.array(sheet2.col_values(10)[3:], dtype=float)
        total = .0
        num_jc = 0
        for i in range(0, len(cols_double_jc)):
            if cols_doublejs_jc[i] > 12:
                total += cols_double_jc[i]
                num_jc += 1
        if num_jc <= 0:
            num_jc = 1
        return total/num_jc


def len_total_cal():
    len_total = cols_yanxinchang[0]
    for i in range(1, len(cols_huici)):
        if cols_huici[i] != cols_huici[i-1]:
            len_total += cols_yanxinchang[i]
    return len_total


def kknormrate_cal(rockk):
    line_num = 0
    index = []
    max = 0
    min = 5
    for line in cols_yanxing:
        if rockk in line:
            index.append(line_num)
        line_num += 1
    if len(index) < 1:
        print("该层段无", rockk, ";")
        return 0
    for i in index:
        if cols_doublejs[i] < 12:
            if cols_double[i] < min:
                min = cols_double[i]
            if cols_double[i] > max:
                max = cols_double[i]
    if max == min:
        return max
    output = str(min) + " ~ " + str(max)
    return output


def meanrate_cal():
    total = .0
    num = 0
    for i in range(0, len(cols_double)):
        if cols_doublejs[i] < 12:
            total += cols_double[i]
            num += 1
    return total/num

path = r'./table/ZKN18-7物探编录.xls'
wb = xlrd.open_workbook(filename=path)
sheet1 = wb.sheet_by_index(0)
cols_huici = np.array(sheet1.col_values(2)[3:], dtype=int)  # 获取列内容
cols_shendus = np.array(sheet1.col_values(4)[3:], dtype=float)
cols_shendue = np.array(sheet1.col_values(5)[3:], dtype=float)
cols_yanxinchang = np.array(sheet1.col_values(6)[3:], dtype=float)
cols_cedianweizhi = np.array(sheet1.col_values(7)[3:], dtype=float)
cols_yanxing = np.array(sheet1.col_values(8)[3:])
cols_doublejs = np.array(sheet1.col_values(9)[3:], dtype=float)
cols_double = np.array(sheet1.col_values(10)[3:], dtype=float)

print("岩心总长度为：", "%.2f" % len_total_cal())
print("岩心一般照射量率为：", "%.2f" % meanrate_cal())
if kknormrate_cal("泥岩") != 0:
    print("泥岩γ+β照射量率一般为", kknormrate_cal("泥岩"), "；")
if kknormrate_cal("细砂岩") != 0:
    print("细砂岩γ+β照射量率一般为", kknormrate_cal("细砂岩"), "；")
if kknormrate_cal("中砂岩") != 0:
    print("中砂岩γ+β照射量率一般为", kknormrate_cal("中砂岩"), "；")
if kknormrate_cal("粗砂岩") != 0:
    print("粗砂岩γ+β照射量率一般为", kknormrate_cal("粗砂岩"), "；")

length = tgtLen_cal(1)
length2 = len2_cal()
s1 = nC_mean_cal(1) * length
s2 = nC_mean_cal(2) * 0.2 * length2
err = 200 * (s1 - s2) / (s1 + s2)
if err > 5:
    err -= 3
print("检查矿段约为 %.2f" % (length2*0.2))
print("矿段编录面积为", "%.2f" % s1, ',',
      "检查编录矿段面积为", "%.2f" % s2, ',',
      "误差为", "%.2f" % err, '%')
