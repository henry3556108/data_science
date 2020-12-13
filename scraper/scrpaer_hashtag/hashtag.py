# import requests
import pandas as pd
df = pd.read_csv("test_v2.csv")
df.to_excel("test_v3.xlsx", index=0)
# from bs4 import BeautifulSoup
# if __name__ == "__main__":
#     df = pd.DataFrame()
#     for i in range(500, 1000):
#         url = "https://top-hashtags.com/instagram/{}/"
#         print(i)
#         if i == 0 : 
#             url = f"https://top-hashtags.com/instagram/"
#         else:
#             # print(i*100+1)
#             url = url.format(i*100+1)
#         # print(url)
#         html = requests.get(url)
#         soup = BeautifulSoup(html.text)

#         ul = soup.find("ul", class_ = "i-group")
#         # print(ul.text)
#         lis = ul.findAll("li")
#         # print(lis.text)
#         for li in lis:
#             # print(li.text)
#             # break
#             num = li.find("div", class_ = "i-num").text
#             tag = li.find("div", class_ = "i-tag").text
#             total = li.find("div", class_ = "i-total").text
#             df = df.append([[num, tag, total]])
#             # print(df)
#         print(i)
#     df.to_csv("test_v2.csv", index=0)
        