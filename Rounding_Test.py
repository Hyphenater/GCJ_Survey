import numpy as np

nums = [30, 40, 21, 8, 10]
percentages = [num / sum(nums) * 100 for num in nums]
print(percentages)

percentage_sum = sum(percentages)
print(percentage_sum)
