# -*- coding: utf-8 -*-
"""
源自: https://en.wikipedia.org/wiki/Subset_sum_problem
是子集和问题的一种实现方式
"""

import time


if __name__ == '__main__':
    x_list = [1150, 495, 995, 995, 995, 995, 100, 750, 3305, 75, 510, 3265, 2145, 1935, 140, 140, 15, 1330, 2800, 1250, 350, 850, 110]
    target = 8270
    error = 0.009

    start_time = time.time()

    S = [(0, [])]
    for x in x_list:
        T = [(x + y, y_list + [x]) for y, y_list in S]
        U = T + S
        U.sort(key=lambda a: a[0])
        y, y_list = U[0]
        S = [(y, y_list)]
        for z, z_list in U:
            if y + error * target / len(x_list) < z <= target:
                y = z
                S.append((z, z_list))
        else:
            while abs(S[-1][0] - target) < error:
                print(S.pop())
    print(time.time() - start_time)
