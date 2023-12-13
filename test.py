
# # d = {}
# # n = 1
# # for x in range(1, 10):
# #     n +=1
# #     d["string{0}".format(x)] = f"Hello{x}"
# #     print(n)
# # for b in d:
# #     print(d[b])

# # Create a sample DataFrame

# dff = {
#         "A": ["A0", "A1", "A2", "A3"],
#         "B": ["B0", "B1", "B2", "B3"],
#         "C": ["C0", "C1", "C2", "C3"],
#         "D": ["D0", "D1", "D2", "D3"],
#     }
# data1 = {
#         "A": ["A4", "A5", "A6", "A7"],
#         "B": ["B4", "B5", "B6", "B7"],
#         "C": ["C4", "C5", "C6", "C7"],
#         "D": ["D4", "D5", "D6", "D7"],
#     }
# data2 = {
#         "A": ["A8", "A9", "A10", "A11"],
#         "B": ["B8", "B9", "B10", "B11"],
#         "C": ["C8", "C9", "C10", "C11"],
#         "D": ["D8", "D9", "D10", "D11"],
#     }
# df1 = pd.DataFrame(data1)
# df2 = pd.DataFrame(data2)
# df = pd.DataFrame(dff)
# dataset = {
#     "a" : df1,
#     "b" : df2,
#     "c" : df
# }
# arr = []
# for i in dataset.values():
#     arr.append(i)
    
# # Print the updated DataFrame
# d4 = pd.concat(arr,ignore_index= True)
# print(d4)
# from datetime import datetime
# def date_info():
#     first_date = '2023/11/30'
#     # date_start = str(input())
#     # date_end = str(input())
#     d0 = datetime.strptime(first_date, "%Y/%m/%d")
#     d1 = datetime.strptime('2023/11/30', "%Y/%m/%d")
#     d2 = datetime.strptime('2023/12/02', "%Y/%m/%d")
#     b = d2
#     a = d1
#     print("b-a: ",b-a)
#     datediff = abs(d2-d1).days
#     print(datediff)
#     if str(datediff) == '0:00:00':
#         datediff = 0
#         print(datediff)
#     print(int('2023/11/30'))
#     # # if int(date_start[:4]) >= 2023:dddd
#     # datediff = abs((d2-(d1-d0)).day) +1 
    
#     #     return datediff
# date_info()
a = 2
b = 10
c = a-b
arr =[]
for i in range(a,b+1):
    arr.append(i)
print(arr)

for x in range(0,8+1):
    print(arr[x])
# print(len(arr))
# print(arr.pop(0))
# print(arr)
#wnat output 1,2,3,4,5s