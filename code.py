"""
2913. Subarrays Distinct Element Sum of Sqaures :
You are given a 0-indexed integer array nums
The distinct count of a subarray of nums is defined as:
    - Let nums[i..j] be a subarray of nums consisting of all the indices from i to j such that 0 <= i <= j < nums.length
    - Then the number of distinct values in nums[i..j] is called the distinct count of nums[i..j]
    - Return the sum of the squares of distinct counts of all subarrays of nums
A subarray is a contiguous non-empty sequence of elements within an array
Example:
Input: nums = [1,2,1]
Output: 15
Explanation: Six possible subarrays are:
[1]: 1 distinct value
[2]: 1 distinct value
[1]: 1 distinct value
[1,2]: 2 distinct values
[2,1]: 2 distinct values
[1,2,1]: 2 distinct values
The sum of the squares of the distinct counts in all subarrays is equal to 12 + 12 + 12 + 22 + 22 + 22 = 15.
"""
class Solution:
    def subsets(self, nums: list[int]) -> list[list[int]]:
        result = []
        
        def backtrack(index, current_path):
            # Append a copy of the current subset to the result
            result.append(list(current_path))
            
            for i in range(index, len(nums)):
                # Include the element
                current_path.append(nums[i])
                # Move to the next element
                backtrack(i + 1, current_path)
                # Exclude the element (backtrack)
                current_path.pop()
                
        backtrack(0, [])
        return result

            