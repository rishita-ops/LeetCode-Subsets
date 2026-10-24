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

            
