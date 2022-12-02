from GA import *
import numpy as np
import json
import os


if os.path.exists("session.txt"):
    with open("session.txt", "r") as file:
        for i in range(4):
            file.readline()
        pop_size = int(file.readline())
        num_select = int(file.readline())
        num_play = int(file.readline())
        rate = float(file.readline())
        id = file.readline()[:-1]
    ga = GA(pop_size, num_select, rate, num_play, id=id)
    ga.run(1000, session=True)
else:
    ga = GA(3200, 50, 0.1, 10)
    params = {"pop_size": ga.pop_size, "num_select": ga.num_select, "rate": ga.rate}
    open(f"snakes_{ga.pop_size}_{ga.id}/params.txt", "w").write(json.dumps(params))
    ga.run(1000, plot=True)

os.remove("session.txt")


#Game().run_demo("snakes_3200_8fc2446df1d94476833ac9f8783d0175")


"""
while True:
    snakes = [NeuronalNetwork() for _ in range(ga.num_select)]
    for i in range(len(snakes)):
        data = np.load(f"snakes_{ga.pop_size}_{ga.id}/gen_199/snake_{i}.npy", allow_pickle=True)
        snakes[i].weights = data[0]
        snakes[i].biases = data[1]
    for i in range(len(snakes)):
        run = Game().run_AI_dis(snakes[i])
        print(f"SCORE for snake {i} : {run[1]}")



for pop_size in range(100, 1100, 500):
    for num_select in range(pop_size//100, pop_size//10, 5):
        for rate in range(0, 100, 5):
                ga = GA(pop_size, num_select, rate/100, 20)
                params = {"pop_size": pop_size, "num_select": num_select, "rate": rate/10}
                open(f"snakes_{ga.pop_size}_{ga.id}/params.txt", "w").write(json.dumps(params))
                ga.run(200, plot=True)
"""

