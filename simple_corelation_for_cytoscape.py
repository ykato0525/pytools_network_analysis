import pandas as pd
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import seaborn as sns
import sys

"""
入力ファイル
args[0]: expression.csv(細胞株名と発現量しかないデータを想定）
args[1]: metadata.csv
args[2]: threshold (相関係数の閾値 読み込むときはfloatにする)
args[2]: outputするファイル名（textで）
"""
# 引数の受け取り
args = sys.argv
expressionfile = args[1]
gene_list = args[2]
out_f = args[3]

print(gene_list)
# metadataの読み込み
list_of_genes = pd.read_csv(gene_list)
genes = list(list_of_genes["genes"])


# dataの読み込み
data = pd.read_csv(expressionfile, index_col=0, usecols=genes)

# dataを読み込んでいます
print("dataを読み込んでいます")
# プログレスバーの表示
# for i in range(10): 
#     print("□", end="")
#     sys.stdout.flush()
#     time.sleep(0.1)

print(data.shape)
# 相関行列の生成
print("相関行列を生成しています")
data_cor = data.corr()

# thresholdを決定する
threshold = float(args[3])
data_cor = data_cor[abs(data_cor) >= threshold]

# 自己相関も削除する
data_cor = data_cor[data_cor < 1.0]

# pandas -> networkxへの変換
print("networkxへ変換しています")
G = nx.from_pandas_adjacency(data_cor)

# Cytoscape用にファイルの出力
print("ファイルを出力しています")
nx.write_graphml(G, "../for_cytoscape/" + out_f + ".graphml")

if __name__ == "__main__":

    print("相関係数で作成したネットワーク図をcytoscape用に出力します")