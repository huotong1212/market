from random import choices, choice
import re
seeds = '1234567890'
codes = []
for num in range(4):
    codes.append(str(choices(seeds)))
print(codes)
# result = "".join(codes)
# print(result)

# seeds = "1234567890"
# random_str = []
# for i in range(4):
#     random_str.append(choice(seeds))
#
# print("".join(random_str))

ma = re.match('^1[3578]\d{9}$|^147\d{8}$|^176\d{8}$','17761864185')
print(bool(ma))