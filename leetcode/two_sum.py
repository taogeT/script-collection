# -*- coding: utf-8 -*-
"""
From: https://leetcode.com/problems/two-sum/description/
"""


class Solution:
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        res = {}
        for index, num in enumerate(nums):
            if num not in res:
                res[target - num] = index
            else:
                return [res[num], index]
        return []
