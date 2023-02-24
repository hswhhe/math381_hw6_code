from random import randint
import numpy as np
import matplotlib.pyplot as plt


def simulate_game(stock_A, stock_B, stock_num_A, stock_num_B, rolls, prof_A, prof_B, stock_num):
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

            if r2 == 0 and r1 in stock_num_A and stock_A[r1][1] >= 100:
                stock_A[r1][3] += (stock_A[r1][2] * amount / 100)
            if r2 == 0 and r1 == stock_num_B and stock_B[1] >= 100:
                stock_B[3] += (stock_B[2] * amount / 100)
            if r2 == 1 and r1 in stock_num_A:
                stock_A[r1][1] += amount
                if stock_A[r1][1] >= 200:
                    stock_A[r1][1] = 100
                    stock_A[r1][2] *= 2
            if r2 == 1 and r1 == stock_num_B:
                stock_B[1] += amount
                if stock_B[1] >= 200:
                    stock_B[1] = 100
                    stock_B[2] *= 2
            if r2 == 2 and r1 in stock_num_A:
                stock_A[r1][1] -= amount
                if stock_A[r1][1] <= 0:
                    stock_A[r1][1] = 100
                    stock_A[r1][2] = 0
                    return 0
            if r2 == 2 and r1 == stock_num_B:
                stock_B[1] -= amount
                if stock_B[1] <= 0:
                    stock_B[1] = 100
                    stock_B[2] = 0
                    return 1

    prof_A = 0
    prof_B = 0
    for i in range(stock_num):
        prof_A += stock_A[i][3] + (stock_A[i][1] * stock_A[i][2] / 100)
    
    for i in range(stock_num):
        prof_B += stock_B[i][3] + (stock_B[i][1] * stock_B[i][2] / 100)

    # prof_B = stock_B[3] + (stock_B[1] * stock_B[2] / 100)
    if prof_A == prof_B:
        return simulate_game(stock_A, stock_B, stock_num_A, stock_num_B, rolls, prof_A, prof_B, stock_num)
    elif prof_A > prof_B:
        return 1
    else:
        return 0

def play_game(turns, ply_threshold):
    cash = 5000
    rolls = 2 * turns
    simulation = 20000
    win = 0
    total_game = 0
    prob_list = []
    stock_num = 5  # Number of Stocks player A buys
    
    for _ in range(simulation):
        prob = 0
        # simulate the initial price for player
        stock_val = []
        stock_A = [[],[],[]]  # [[start value, curr value, # of shares, divs]]
        stock_B = []
        stock_num_A = []  # Indices of 
        start_values = []  # Initial Values of all stockes
        stock_num_B = []
        
        # choose the three stocks with highest start price for player A 
        # and one stock for player B that is higher than its threshold
        for _ in range(6):
            start_val = 5 * randint(1, 39)
            start_values.append(start_val)
            stock_val.append([start_val, start_val, cash * 100 / (stock_num * start_val), 0])
        sorted_price = sorted(stock_val, key=lambda x: x[0], reverse=True) # Initial Prices of stockes, in descending order.
        stock_A = sorted_price[0:stock_num]  # 3 stocks with highest values.
        stock_B = sorted_price[(6 - stock_num):6]
        stock_num_A = [i for i in range(stock_num)]
        stock_num_B = [i for i in range(6 - stock_num, 6)]

        # buy_B = 0  # boolean that decides if B buys a stock
        # for i in stock_val:
        #     if i[0] >= ply_threshold and buy_B == 0:
        #         stock_B = i
        #         stock_num_B = sorted_price.index(i)
        #         stock_B[2] *= stock_num
        #         buy_B = 1

        # find the profit and winning probability
        prof_A = 0
        prof_B = 0
        #if buy_B == 1:
        win += simulate_game(stock_A, stock_B, stock_num_A, stock_num_B, rolls, prof_A, prof_B, stock_num)
        total_game -= -1
        prob = win / total_game
        prob_list.append(prob)
  
    return prob_list
            


if __name__ == '__main__':
    all_values = []
    for i in range(10):
        prob_list = play_game(7, 120)
        all_values.append(prob_list)
            # print the plot
        plt.plot(range(len(prob_list)), all_values[i], label=f'trail {i+1}')
    plt.xlabel('Player A wining probability')
    plt.ylabel('Number of games')
    plt.ylim([0, 1])
    plt.title("Both Player Choose Diversed Strategy")
    plt.legend()
    plt.show()