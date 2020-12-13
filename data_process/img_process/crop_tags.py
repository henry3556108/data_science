import cv2
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def get_regional_solution(arr1):
    ls = []
    for index in range(len(arr1) - 1):
        # print(int(arr1[index + 1]) - int(arr1[index]), arr1[index + 1], arr1[index])
        ls.append(int(arr1[index + 1]) - int(arr1[index]))
    arr2 = np.array(ls)
    pos = []
    for index in range(len(arr2) - 1):
        if arr2[index] < 0 and arr2[index + 1] >= 0:
            pos.append(index)
    # print(pos)
    return pos

def crop(img):
    array = img
    h, w  = img.shape
    x, y = 0, 0
    arr = array.sum(axis = 1)
    pos = get_regional_solution(array.sum(axis = 1))
    df = [[i+1, arr[i+1]] for i in pos]
    df = pd.DataFrame(df, columns=["pos", "value"])
    df = df.sort_values(["value"])
    local_minimize = list(df.head(2)["pos"].values)
    local_minimize.sort()
    n_img = img[local_minimize[0]:local_minimize[1], 0:w]


    h, w  = n_img.shape
    arr2 = n_img
    arr = arr2.sum(axis = 0)
    pos = get_regional_solution(array.sum(axis = 0))
    df = [[i+1, arr[i+1]] for i in pos]
    df = pd.DataFrame(df, columns=["pos", "value"])
    df = df.sort_values(["value"])
    local_minimize = list(df.head(2)["pos"].values)
    local_minimize.sort()
    n_img = n_img[0:h, local_minimize[0]:local_minimize[1]]

    array = n_img
    h, w  = n_img.shape
    x, y = 0, 0
    arr = array.sum(axis = 1)
    pos = get_regional_solution(array.sum(axis = 1))
    df = [[i+1, arr[i+1]] for i in pos]
    df = pd.DataFrame(df, columns=["pos", "value"])
    df = df.sort_values(["value"])
    local_minimize = list(df.head(2)["pos"].values)
    local_minimize.sort()
    n_img = n_img[local_minimize[0]:local_minimize[1], 0:w]
    return n_img
    # cv2.imwrite()
    # cv2.imshow("test", n_img)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

def main():
    for i in range(1, 5):
        file_name = str(i)
        while(len(file_name) < 3):
            file_name = "0" + file_name
        img = cv2.imread('tags/{}.png'.format(file_name), cv2.IMREAD_GRAYSCALE)
        try:
            img = crop(img)
            cv2.imwrite(f"{file_name}.png", img)
        except:
            print(file_name)
if __name__ == "__main__":
    main()