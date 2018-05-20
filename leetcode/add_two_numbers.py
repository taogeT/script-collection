# -*- coding: utf-8 -*-
"""
From: https://leetcode.com/problems/add-two-numbers/description/
"""


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


class Solution:

    def addTwoNumbers(self, l1, l2):
        """
        :type l1: ListNode
        :type l2: ListNode
        :rtype: ListNode
        """
        y = r = ListNode(0)
        x = 0
        while l1 is not None or l2 is not None or x != 0:
            if l1:
                p = l1.val
                l1 = l1.next
            else:
                p = 0
            if l2:
                q = l2.val
                l2 = l2.next
            else:
                q = 0
            r.next = ListNode((p + q + x) % 10)
            x = (p + q + x) // 10
            r = r.next
        return y.next
