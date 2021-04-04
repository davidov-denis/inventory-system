# def count_del_5(n):
#     k = int(n ** .5)
#     if k ** 2 != n:
#         return False
#     count = 0
#     for x in range(2, k):
#         if n % x == 0:
#             count += 1
#         if count > 1:
#             return False
#     return count == 1
#
#
# for n in range(35000000, 45000000 + 1):
#     if count_del_5(n):
#         print(n)

# a = 38950081
# for i in range(2, a):
#     if a % i == 0:
#         print(i)