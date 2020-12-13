import pandas as pd

from matplotlib import pyplot as plt

import os

# print(files)

def plot(df, axs):
    fig, axs = plt.subplots(axs)
    # print(axs)
    cols = df.columns
    cols = cols.drop(["DATE"])
    print(cols)
    for index, col in enumerate(cols):
        print(index)
        # if col == "DATE":
        #     continue
        axs[index].plot(df[col])
        axs[index].set_title(col)
    fig.tight_layout()
    plt.show()
    # pass
# def scaler(df, scaler_type, file_name = None):
#     columns = df.columns
#     record = [file_name, "\n"]
#     # print(columns)
#     for c in columns:
#         if scaler_type == "z-score":
#             tmp = []
#             minimum = df[c].min()
#             maximum = df[c].max()
            
#             mean = df[c].mean()
#             std = df[c].std()
#             df[c] = df[c].apply(lambda x : (x - mean) / std)
#             tmp.append("column name:")
#             tmp.append(c)
#             tmp.append(", std:")
#             tmp.append(str(std))
#             tmp.append(", mean:")
#             tmp.append(str(mean))
#             tmp.append(", min:")
#             tmp.append(str(minimum))
#             tmp.append(", max:")
#             tmp.append(str(maximum))
#             s = " ".join(tmp)
#             record.append("\t")
#             record.append(s)
#             record.append("\n")
            
        
#     if file_name != None:
#         with open("record.txt", "a") as f:
#             for s in record:
#                 f.write(s)
#     return df
if __name__ == "__main__":
    src = "data_need/point/"
    files = os.listdir(src)
    for f in files:
        # if f.startswith("Monthly"):
        df = pd.read_csv(os.path.join(src, f))
        axs = len(df.columns) - 1
        plot(df, axs)
            # print()
            # pass
        # if f.startswith("Quarterly"):
            # pass
        # if f.startswith("Weeklyly"):
            # pass
    # folder = "data_need/diff"
    # files = os.listdir(folder)
    # dfs = []
    # for f in files:
    #     if f.endswith("_diff_only.csv"):
    #         df = pd.read_csv(os.path.join(folder,f), index_col=0)
    #         # df = scaler(df, "z-score", f)
    #         plot(df)