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

# コマンドライン引数でログファイルを受け取る
if len(sys.argv) == 3:
    wasm_csv = sys.argv[1]
    native_csv = sys.argv[2]
else:
    print("Usage: python to_ratio_graph.py <wasm_logfile> <native_logfile>")

# csv をデータフレームとして読み込む
wasm_df = pd.read_csv(wasm_csv, names=['thread_num', 'time'])
native_df = pd.read_csv(native_tsv, names=['thread_num', 'time'])

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

# x軸ラベル準備
thread_num_label = []
for i in range(len(wasm_df['thread_num'])):
    if (i + 1) % 5 == 0:
        label = i + 1
        thread_num_label.append(label)
    else:
        thread_num_label.append('')

# 各軸の値をセット
## x軸の値をセット
x = wasm_df['thread_num']

##  y軸の値を基準値の比率とする場合
### 表示する比率の基準となる値を取り出す
wasm_n1 = wasm_df[wasm_df['thread_num'] == 1]['time'][0]
native_n1 = native_df[native_df['thread_num'] == 1]['time'][0]

### 基準値を各データで割り，基準値に比べてより小さい値が大きくなるようにする
y1 = wasm_n1/wasm_df['time']
y2 = native_n1/native_df['time']

## y軸の値を時間とする場合
y3 = wasm_df['time']
y4 = native_df['time']

## y軸の値を時間あたりの計算量(pixel/s)にする場合
y5 = 300000000/wasm_df['time']
y6 = 300000000/native_df['time']

# y1 軸と y2 軸を重ねるために 2つの ax を作成して重ねる
fig, ax1 = plt.subplots()
# ax2 = ax1.twinx()

# ax1 のほうに X軸とラベルを書く
## 時間を取得して表示する場合
## ax1.xaxis.set_major_formatter(md.DateFormatter('%H:%M'))
## ax1.xaxis.set_major_locator(md.HourLocator(byhour=range(0, 24, 3), tz=None))
## date = datetime.strptime(target_date, '%Y%m%d')
## label = date.strftime('時刻 (%Y年%m月%d日 {}曜日)').format('月火水木金土日'[date.weekday()])

## ラベルと数値を単純に並べる場合
label = "スレッド数"
ax1.set_xlabel(label)

# 折れ線グラフのプロット
# ax1 のほうに比率をプロット Y軸 (左) にラベルを書く
ax1.plot(x, y6, c='r', label='Native', ls='-', lw=1)
ax1.plot(x, y5, c='g', label='Wasm', ls='--', lw=1)
ax1.set_ylabel("時間あたりの計算ピクセル数 (pixel/s)")

# 棒グラフのプロット
# ax1 のほうに時間をプロット Y軸 (左) にラベルを書く
#width = 0.4
#ax1.bar(x - 0.2, y3, width, color='g', label='Wasm')
#ax1.bar(x + 0.2, y4, width, color='r', label='Native')
#ax1.set_ylabel("実行時間 (s)")

#罫線
ax1.grid()
ax1.set_axisbelow(True)

# 目盛り位置，上限値設定
ax1.set_xticks(x, thread_num_label)
ax1.set_ylim(0, y6.max() * 1.1)
#ax1.set_ylim(0, y3.max() * 1.1)

# ax1 と ax2 の凡例をつなげて，ax1 側に書く
#hdr2, leg2 = ax2.get_legend_handles_labels()
#ax1.legend(hdr1 + hdr2, leg1 + leg2, loc='upper left')
hdr1, leg1 = ax1.get_legend_handles_labels()
ax1.legend(hdr1, leg1, loc='upper left')

# グラフの pdf 出力
date = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
filename = "plot"
## ファイル名を日付にする場合
## filename = f'{date}'
plt.savefig(filename + '.pdf')

sys.exit()
