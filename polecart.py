import gym 
import time
import pygame
import random
import os
import time
import Main
from Main import AMOUNT_INPUTS,AMOUNT_OUTPUTS,MAX_HIDDEN
from Genome import Genome
from Evaluation import Evaluation
from Pool import Individual,Species,Pool
import Visualize

def eval_genomes(evaluations, visualize=False):
    environment = gym.make('Acrobot-v1')
    #environment._max_episode_steps = 10000

    for i in range(0, len(evaluations)):
        inputs = environment.reset()
        #environment.render()
        for dummy in range(200):
            #print(dummy)
            outputs = evaluations[i].eval(inputs)
            do = 0

            if not (outputs[0] == None) and outputs[0] > 0.5:
                do = 1

            if not (outputs[0] == None) and outputs[0] < -0.5:
                do = -1

            observation, reward_gain, completed, _ = environment.step(do)
            if visualize:
                environment.render()
                time.sleep(0.033)

            evaluations[i].increase_fitness(reward_gain)
        
            inputs = observation

            if completed:
                #continue
                #print(evaluations[i].individual.fitness)
                break 
        
        evaluations[i].increase_fitness(210)
    environment.close()
            


pool = Pool(AMOUNT_INPUTS, MAX_HIDDEN, AMOUNT_OUTPUTS)
pool.initialize(100)


evaluation_list = []

for species in pool.species_list:
    for individual in species.population:
        evaluation_list.append(Evaluation(individual))
        #individual.genome.print_genes()
        

for i in range(0, 1000):

    #print("Hiero")
    indiv_amount = 0
    for species in pool.species_list:
        for individual in species.population:
            evaluation_list.append(Evaluation(individual))
            indiv_amount += 1 

    #print("amount individuals: " + str(indiv_amount))
    #print("Hiero2")
    eval_genomes(evaluation_list) 
    #print("Hiero3")
    #print("Generation: " + str(i))
    #print("Total fitness: " + str(pool.total_average_fitness()))

    # for species in pool.species_list:
    #     for individual in species.population:
    #         print(individual.fitness)

    evaluation_list = []

    pool.new_generation()
    #print("amount species: " + str(len(pool.species_list)))
    try:
        if i % 1 == 0:
            pool.get_best_individual().genome.print_genes()
            evaluation_list = [Evaluation(pool.get_best_individual())]
            eval_genomes(evaluation_list, True)
            print("lol")
            evaluation_list = []
            pool.get_best_individual().genome.print_genes()
        #Visualize.visualize(pool.get_best_individual().genome)
        #pass
    except Exception as e:
        print(e)

    print(i, pool.total_average_fitness())


# Amount inputs: 6 amount outputs: 1