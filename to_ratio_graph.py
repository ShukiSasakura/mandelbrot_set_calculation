#!/usr/bin/env python3

from matplotlib import pyplot as plt
from matplotlib import ticker
import numpy as np
import pandas as pd
import datetime
import sys
import io

# 日本語フォントの設定
from matplotlib import rcParams
rcParams['font.family'] = 'sans-serif'
rcParams['font.sans-serif'] = ['Hiragino Maru Gothic Pro', 'Yu Gothic', 'Meirio', 'Takao', 'IPAexGothic', 'IPAPGothic', 'VL PGothic', 'Noto Sans CJK JP']

# 測定結果の tsv を貼り付ける
wasm_tsv = """
n	time
1	86.098254358
2	44.459961389
3	49.044414905
4	35.024008336
5	31.85907721
6	25.58213768
7	22.976530636
8	20.066620286
9	17.873032034
10	16.176885348
11	14.799783985
12	13.619973728
13	12.55477119
14	11.698362865
15	10.982570394
16	10.297050439
17	9.827527351
18	9.17530129
19	8.826022522
20	8.386677929
21	8.149320364
22	7.864137911
23	7.383447395
24	7.378326429
25	6.887127284
26	6.813841202
27	6.856769802
28	6.416254571
29	6.200870283
30	6.394930166
31	6.223941207
32	6.045345366
33	5.903388403
34	5.670356677
35	5.682507384
36	5.661199255
37	5.46720693
38	5.368328138
39	5.240133942
40	5.261385821
"""

native_tsv = """
n	time
1	60.551087486
2	31.876678993
3	36.237582513
4	25.526657808
5	23.008541245
6	18.533562577
7	16.662968736
8	14.446146081
9	12.955121574
10	11.78423157
11	10.690468345
12	9.87015279
13	9.046649937
14	8.505914005
15	7.943911312
16	7.440088829
17	7.081187356
18	6.661231085
19	6.378304329
20	5.992203963
21	5.780110237
22	5.571375815
23	5.313813204
24	5.091237298
25	4.934876135
26	4.776632319
27	4.517219085
28	4.439967686
29	4.254802745
30	4.131006533
31	4.036731839
32	3.916328807
33	3.934376436
34	3.80856619
35	3.691732193
36	3.616290643
37	3.615260527
38	3.475781145
39	3.406637798
40	3.348074294
"""

thread_num_label = []

for i in range(40):
    if (i + 1) % 5 == 0:
        label = i + 1
        thread_num_label.append(label)
    else:
        thread_num_label.append('')

# 貼り付けた tsv をファイルとして認識させる
wasm_tsv = io.StringIO(wasm_tsv)
native_tsv = io.StringIO(native_tsv)

# tsv をデータフレームとして読み込む
wasm_df = pd.read_table(wasm_tsv)
native_df = pd.read_table(native_tsv)

# tsv から特定のカラムを取り出す場合の例
# https://numpy.org/doc/stable/reference/generated/numpy.loadtxt.html
# https://it-ojisan.tokyo/numpy-tsv/
# [[10 21 32 43]
#  [14 25 36 47]
#  [18 29 30 41]]
# 1行目と3行目を読み込む
# [[21 43]
#  [25 47]
#  [29 41]]
# wasm_array = np.loadtxt(wasm_tsv, delimiter = "\t", dtype = float, usecols = (1, 3))
# native_array = np.loadtxt(native_tsv, delimiter = "\t", dtype = float, usecols = (1, 3))


# 各軸の値をセットする
##  縦軸を基準値の比率とする場合
### 表示する比率の基準となる値を取り出す
wasm_n1 = wasm_df[wasm_df['n'] == 1]['time'][0]
native_n1 = native_df[native_df['n'] == 1]['time'][0]

### 基準値を各データで割り，基準値に比べて小さい場合に大きな値としている
x = wasm_df['n']
y1 = wasm_n1/wasm_df['time']
y2 = native_n1/native_df['time']

## 縦軸を時間とする場合
#x = wasm_df['n']
y3 = wasm_df['time']
y4 = native_df['time']

# y1 軸と y2 軸を重ねるために 2つの ax を作成して重ねる
fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()

# ax1 のほうに X軸とラベルを書く
## 時間の場合
## ax1.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
## ax1.xaxis.set_major_locator(md.HourLocator(byhour=range(0, 24, 3), tz=None))
## date = datetime.strptime(target_date, '%Y%m%d')
## label = date.strftime('時刻 (%Y年%m月%d日 {}曜日)').format('月火水木金土日'[date.weekday()])

## ラベルと数値を単純に並べる場合
label = "スレッド数"
ax1.set_xlabel(label)

# 折れ線グラフのプロット
# ax1 のほうに比率をプロット Y軸 (左) にラベルを書く
ax1.plot(x, y1, c='g', label='Wasm', marker='^', lw=1)
ax1.plot(x, y2, c='r', label='Native', marker='o', lw=1)
ax1.set_ylabel("スレッド数1における時間に対する効率")

#罫線
ax1.grid()
ax1.set_axisbelow(True)

# ax2 のほうに時間をプロット Y軸 (右) にラベルを書く
#width = 0.4
#ax2.bar(x, y3, width, color='b', label='wasm')
#ax2.bar(x + width, y4, width, color='r', label='native')
#ax2.set_ylabel("時間 (s)")

# 棒グラフのプロット
# ax1.bar(x, y1, c='b', label='sample')

# 目盛り位置，上限値設定
ax1.set_xticks(x, thread_num_label)

# ax1 と ax2 の凡例をつなげて，ax1 側に書く
hdr1, leg1 = ax1.get_legend_handles_labels()
#hdr2, leg2 = ax2.get_legend_handles_labels()
#ax1.legend(hdr1 + hdr2, leg1 + leg2, loc='upper left')
ax1.legend(hdr1, leg1, loc='upper left')

#xtick = np.arange(len(x))
#ax1.set_xticks(xtick + (width / 2), x)
#ax1.set_ylim(0, max(y4) * 1.1)
#plt.ticklabel_format(style='plain',axis='y')
#plt.tick_params(labelsize=6)

# グラフの pdf 出力
date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filename = "plot"
## ファイル名を日付にする場合
## filename = f'{date}'
plt.savefig(filename + '.pdf')

sys.exit()
