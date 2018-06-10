from sympy import *
from math import *
import copy


NR = [
    [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10],  # 0
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],  # 1
    [1, 1, 3, 5, 15, 17, 51, 85, 255, 257, 771],  # 2
    [2, 1, 1, 7, 11, 13, 61, 67, 79, 465, 721],  # 3
    [3, 1, 3, 7, 5, 7, 43, 49, 147, 439, 1013],  # 4
    [4, 1, 1, 5, 3, 15, 51, 125, 141, 177, 759],  # 5
    [5, 1, 3, 1, 1, 9, 59, 25, 89, 321, 835],  # 6
    [6, 1, 1, 3, 7, 31, 47, 109, 173, 181, 949],  # 7
    [7, 1, 3, 3, 9, 9, 57, 43, 43, 225, 113]  # 8
]


def parabolic_interpolation(lam, p):
    #  initializing coefficients
    a, b, c = symbols("a b c")
    #  solving equation system for a, b, and c
    coefficients = solve([a*lam[0]**2 + b*lam[0] + c - p[0],
                          a*lam[1]**2 + b*lam[1] + c - p[1],
                          a*lam[2]**2 + b*lam[2] + c - p[2]], dict=True)
    #  extrema is -b/2*a
    extrema = -1*coefficients[0][b]/(2*coefficients[0][a])
    return extrema


# getting the real part of the X
def D(X):
    return X - trunc(X)


# calculating LPtau-point Q
def lptau(I, N):

    # NR - direction numbers
    # I - point serial number
    # N - dimensions amount
    # initializing point Q
    Q = []
    A = I
    # see "m"
    M = 1 + trunc(log(A) / log(2))

    # calculating values for each of J dimensions of point Q
    for J in range(1, N+1):
        S = 0  # S = 0/

        for K in range(1, M+1):
            NS = 0  # NS = 0/

            for L in range(K, M+1):
                B = NR[J][L]
                NS = NS + trunc(2*D(A/2**L)) * trunc(2*D(B/2**(L+1-K)))

            S = S + D(0.5*NS) / 2**(K-1)

        Q.append(S)

    return Q


# pareto w/ knowingly non-optimal exclusion
def pareto(Q):

    # Q - array of LPtau-points
    new_Q = []  # new Q (after exclusions)
    count = 0
    while True:
        count += 1
        print("step: " + str(count))
        # flag - we've got more optimal array
        flag = False

        # checking all points of the array (until we got more optimal array)
        print(len(Q))
        print(len(new_Q))
        for j in range(0, len(Q)):

            # getting first (or, if array haven't changed - next one) point of the array
            point = Q[j]
            print(point)

            # point_flag - need to insert current point to more optimal array
            point_flag = True

            # matching first (current) point against rest ones
            print("j is " + str(j))
            print("before cycle new_Q len is " + str(len(new_Q)))
            for i in range(0, len(Q)):

                # print(Q[i])
                # # in case of adding part w/ custom first point - handling meeting current point
                # if (point[0] == Q[i][0]) and (point[1] == Q[i][1]):
                #     new_Q.append(Q[i])

                # if the next point is better than the current one by at least one parameter -
                # taking it to the new, more optimal array
                if (point[0] > Q[i][0]) or (point[1] > Q[i][1]):
                    new_Q.append(Q[i])

                # we don't need to add current point ('cause there's more optimal one) and do have more optimal array
                if (point[0] > Q[i][0]) and (point[1] > Q[i][1]):
                    flag = True
                    point_flag = False

            print("after cycle new_Q len is " + str(len(new_Q)))
            print(flag)

            if point_flag:
                new_Q.append(point)

            # if we've got more optimal array - break the current cycle and proceed to the new array
            if flag:
                # setting sub-optimal array for current one
                print("internal: Q is " + str(Q))
                print("internal: it's length is " + str(len(Q)))
                Q.clear()
                Q = copy.deepcopy(new_Q)
                print("internal: new_Q is " + str(new_Q))
                print("internal: it's length is " + str(len(new_Q)))
                new_Q.clear()
                break

            new_Q.clear()
            # else - checking the next point of the current array

        # we've got more optimal array, so now we proceed to optimising it (precisely, going to the beginning)
        if flag:
            continue
        # we haven't got more optimal array after checking all points left - means, it is the most optimal
        else:
            break

    return Q
