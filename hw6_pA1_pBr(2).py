from random import randint
import numpy as np
import matplotlib.pyplot as plt


def simulate_game(turns, ply_A):
    cash = 5000
    rolls = 2 * turns
    simulation = 20000
    win = 0
    total_game = 0
    prob_list = []
    
    for i in range(simulation):
        prob = 0
        total_game += 1
        # simulate the initial price for player
        stock_val = []
        stock_A = [] # [start value, curr value, # of shares, divs]
        stock_B = []
        stock_num_A = 8
        stock_num_B = randint(0, 5)
        for _ in range(6):
            start_val = 5 * randint(1, 39)
            stock_val.append(start_val)
        stock_B_price = stock_val[stock_num_B]
        stock_B = [stock_B_price, stock_B_price, cash * 100 / stock_B_price, 0]
        # choose the highest first satisfied stock as the invest stock
        # how to store accordingly with the stock? or should we just choose the first stock higher than threshold?
        # stock_val = sorted(stock_val)
        buy_A = 0 # boolean that decides if A buys a stock
        for item in stock_val:
            if item >= ply_A and buy_A == 0:
                stock_A = [item, item, cash * 100 / item, 0]
                stock_num_A = stock_val.index(item)
                buy_A = 1

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
            if r2 == 2 and r1 == stock_num_B:
                stock_B[1] -= amount
                if stock_B[1] <= 0:
                    stock_B[1] = 100
                    stock_B[2] = 0
            
        # find the profit and winning probability
        prof_A = 5000
        prof_B = 5000
        if stock_num_A != 8:
            prof_A = stock_A[3] + (stock_A[1] * stock_A[2] / 100) - cash
        prof_B = stock_B[3] + (stock_B[1] * stock_B[2] / 100) - cash
        if prof_A > prof_B:
            win += 1
        prob = win / total_game
        prob_list.append(prob)

    return prob_list
            


if __name__ == '__main__':
    all_values = []
    for i in range(10):
        all_values.append(simulate_game(7, 120))
            # print the plot
        plt.plot(range(20000), all_values[i], label=f'trail {i+1}')
    plt.xlabel('Player A wining probability')
    plt.ylabel('Number of games')
    plt.ylim([0, 1])
    plt.title("Player both play threshold strategy")
    plt.legend()
    plt.show()
