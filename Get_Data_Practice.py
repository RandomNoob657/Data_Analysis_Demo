from unittest.mock import inplace

import pandas as pd

# 导入和预览数据
original_data = pd.read_csv("./Data Files/e_commerce.csv")

#评估数据整齐度, 干净度
print(original_data.sample(10))
print(original_data.info())

# 评估缺失值
print(f'''展示Description缺失的行:
{original_data[(original_data["Description"].isnull()) & (original_data["UnitPrice"]!=0)]}
''')
print(f'''展示CustomerID缺失的行:
{original_data[original_data["CustomerID"].isnull()]}
''')

# 评估重复数据
print(f'''展示各列有多少重复数据:
{original_data.isnull().sum()}
''')

# 评估不一致数据
print(f'''观察Country是否存在不一致数据:
{original_data["Country"].value_counts()}
''')

# 评估无效或错误数据
print(f'''观察是否存在无效数据:
{original_data.describe()}
''')
print(f'''查看Quantity负数的行具体情况:
{original_data[original_data["Quantity"]<0]}
''')
print(f'''进一步查看Quantity为负数, 是否都是InvoiceNo以C开头, 且UnitPrice不为0:
{original_data[(original_data["Quantity"]<0) & (original_data["InvoiceNo"].str[0] != "C") & (original_data["UnitPrice"] != 0)]}
''')
print(f'''查看UnitPrice是负数的行:
{original_data[["UnitPrice", "Description"]][(original_data["UnitPrice"] < 0)]}
''')

print(f'''数据评估后, 待处理事项有:
1. InvoiceDate转换为日期时间格式
2. CustomerID转换为字符串
3. Description缺失的行删除
4. Country清洗: USA替换为United States, UK/U.K.替换为United Kingdom
5. Quantity为负值的行删除
6. UnitPrice为负值的行删除
''')

# 负值一个DataFrame, 用于存储清洗后数据
cleaned_data = original_data.copy()
print(cleaned_data.info())
print(cleaned_data.sample(10))

# 将InvoiceData转换为日期时间
cleaned_data["InvoiceDate"] = pd.to_datetime(cleaned_data["InvoiceDate"])
print(cleaned_data.info())

# 将CustomerID转换为字符串
cleaned_data["CustomerID"] = cleaned_data["CustomerID"].astype("string")
cleaned_data["CustomerID"] = cleaned_data["CustomerID"].str.slice(0,-2)
print(cleaned_data["CustomerID"])

# 删除Description缺失的观察值
cleaned_data.dropna(subset = ["Description"], inplace=True)
print(f"是否还存在空值: {cleaned_data[cleaned_data["Description"].isnull()]}")
print(f"是否还存在空值: {cleaned_data["Description"].isnull().sum()}")
print(f"删除Description缺失后数据量变化: {original_data.shape[0]} → {cleaned_data.shape[0]}")

#清洗Country的不一致值
cleaned_data.replace({"Country":{"USA":"United States", "UK":"Unitied Kingdom", "U.K.":"United Kingdom"}},inplace = True)
print(cleaned_data["Country"].value_counts())
print(len(cleaned_data[cleaned_data["Country"] == "USA"]))
print(len(cleaned_data[cleaned_data["Country"] == "UK"]))
print(len(cleaned_data[cleaned_data["Country"] == "U.K"]))



# 删除Quantity为负值的观察值
cleaned_data["Quantity"] = cleaned_data["Quantity"].drop(cleaned_data[cleaned_data["Quantity"] < 0].index)
print(cleaned_data["Quantity"].describe())

# 删除UnitPrice为负值的观察值
cleaned_data = cleaned_data[cleaned_data["UnitPrice"] >= 0]
print(cleaned_data["UnitPrice"].describe())

# 保存清理后的数据
cleaned_data.to_json("./Data Files/e_commerce_cleaned.json", index=False)
cleaned_data_review = pd.read_json("./Data Files/e_commerce_cleaned.json")
print(cleaned_data_review.head(10))