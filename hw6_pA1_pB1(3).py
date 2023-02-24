from random import randint
import numpy as np
import matplotlib.pyplot as plt
import sys
#sys.setrecursionlimit(10**6)
def simulate_game(stock_A, stock_B, stock_num_A, stock_num_B, rolls, prof_A, prof_B):
    # simulate the dice roll for each roll
    for _ in range(rolls):
            r1 = randint(0, 5)  # 0: stock1, 1: stock2, ... , 5: stock6
            r2 = randint(0, 2)  # 0 is div, 1: up, 2: down
            r3 = randint(0, 2)  # 0: 5, 1: 10, 2: 20

            if r3 == 0:
                amount = 5
            elif r3 == 1:
                amount = 10
            else:
                amount = 20
            if r2 == 0 and r1 == stock_num_A and stock_A[1] >= 100:
                stock_A[3] += (stock_A[2] * amount / 100)
            if r2 == 0 and r1 == stock_num_B and stock_B[1] >= 100:
                stock_B[3] += (stock_B[2] * amount / 100)
            if r2 == 1 and r1 == stock_num_A:
                stock_A[1] += amount
                if stock_A[1] >= 200:
                    stock_A[1] = 100
                    stock_A[2] *= 2
            if r2 == 1 and r1 == stock_num_B:
                stock_B[1] += amount
                if stock_B[1] >= 200:
                    stock_B[1] = 100
                    stock_B[2] *= 2
            if r2 == 2 and r1 == stock_num_A:
                stock_A[1] -= amount
                if stock_A[1] <= 0:
                    stock_A[1] = 100
                    stock_A[2] = 0
                    return 0
            if r2 == 2 and r1 == stock_num_B:
                stock_B[1] -= amount
                if stock_B[1] <= 0:
                    stock_B[1] = 100
                    stock_B[2] = 0
                    return 1

    if stock_num_A != 8:
        prof_A = stock_A[3] + (stock_A[1] * stock_A[2] / 100)
    if stock_num_B != 8:
        prof_B = stock_B[3] + (stock_B[1] * stock_B[2] / 100)
    if prof_A == prof_B:
        return simulate_game(stock_A, stock_B, stock_num_A, stock_num_B, rolls, prof_A, prof_B)
    elif prof_A > prof_B:
        return 1
    else:
        return 0

def play_game(turns, ply_A, ply_B):
    cash = 5000
    rolls = 2 * turns
    simulation = 10000
    win = 0
    total_game = 0
    prob_list = []
    
    for _ in range(simulation):
        prob = 0
        # simulate the initial price for player
        stock_val = []
        stock_A = [] # [start value, curr value, # of shares, divs]
        stock_B = []
        stock_num_A = 8
        stock_num_B = 8
        for _ in range(6):
            start_val = 5 * randint(1, 39)
            stock_val.append(start_val)

        # choose the highest first satisfied stock as the invest stock
        # how to store accordingly with the stock? or should we just choose the first stock higher than threshold?
        # stock_val = sorted(stock_val)
        buy_A = 0 # boolean that decides if A buys a stock
        buy_B = 0
        for item in stock_val:
            if item >= ply_A and buy_A == 0:
                stock_A = [item, item, cash * 100 / item, 0]
                stock_num_A = stock_val.index(item)
                buy_A = 1
                continue
            if item >= ply_B and buy_B == 0 :
                stock_B = [item, item, cash * 100 / item, 0]
                stock_num_B = stock_val.index(item)
                buy_B = 1

        # find the profit and winning probability
        prof_A = 0
        prof_B = 0
        if buy_A == 1 or buy_B == 1:
            win += simulate_game(stock_A, stock_B, stock_num_A, stock_num_B, rolls, prof_A, prof_B)
            total_game -= -1
            prob = win / total_game
            prob_list.append(prob)
  
    return prob_list
            


if __name__ == '__main__':
    all_ci = []
    for a_value in range (0, 100, 20):
        all_ci.append([])
        for b_value in range(100, 200, 20):
            all_values = []
            for i in range(10):
                prob_list = play_game(7, a_value, b_value)
                all_values.append(prob_list)
                    # print the plot
                #plt.plot(range(len(prob_list)), all_values[i], label=f'trail {i+1}')
            # plt.xlabel('Player A wining probability')
            # plt.ylabel('Number of games')
            # plt.ylim([0.0, 1])
            # plt.title("Player both play threshold strategy")
            # plt.legend(loc='upper center', bbox_to_anchor=(0.5, 0.95),
            #     ncol=3, fancybox=True, shadow=True)
            # plt.show()
            all_values_mean = sorted([sum(all_values[i])/ len(prob_list) for i in range(10)])

            all_ci[int(a_value/20)].append([all_values_mean[0], all_values_mean[9]]) 
            # print(f"Confidence Interval with 99.8 percent level:({all_values_mean[0]}, {all_values_mean[9]})")
            # giant_list = [element for innerList in all_values for element in innerList]
            # fig, ax = plt.subplots(figsize =(10, 7))
            # ax.hist(giant_list, bins = 1000)
            # ax.set_xlim([0.4, 0.6])
            # ax.set_title('Histogram of Player A Winning Probability')
            # ax.set_xlabel('Probability')
            # plt.show()
    print(all_ci)