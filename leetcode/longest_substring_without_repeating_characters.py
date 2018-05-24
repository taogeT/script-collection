# -*- coding: utf-8 -*-
"""
From: https://leetcode-cn.com/problems/longest-substring-without-repeating-characters/description/
"""


class Solution:

    def lengthOfLongestSubstring(self, s):
        """
        :type s: str
        :rtype: int
        """
        max_string = ''
        max_len = 0
        for s_index, s_value in enumerate(s):
            if s_value not in max_string:
                max_string += s_value
            else:
                max_len = max_len if len(max_string) < max_len else len(max_string)
                max_string = max_string[max_string.find(s_value) + 1:] + s_value
        return max_len if len(max_string) < max_len else len(max_string)
