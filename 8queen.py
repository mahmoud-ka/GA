# -*- coding: utf-8 -*-
"""
Created on Fri May 20 19:47:49 2022

@author: python
"""

import numpy as np
import statistics as st
import random

def init_pop(popsize):
    population=np.zeros((popsize,8))
    for i in range(popsize):
        population[i]=np.random.randint(8,size=8)
    return population

#print(init_pop(10))

def fitness(chromosome):
    fitness=0
    for i in set(list(chromosome)):
        
        if np.count_nonzero(chromosome==i)>1:
            
            fitness+=1
    cross=0
    #print(chromosome)
    for i in range(8):
        for j in [x for x in range(8) if x !=i]:
            if (chromosome[i]-chromosome[j])/(i-j)==1 or (chromosome[i]-chromosome[j])/(i-j)==-1:
                cross+=1
            
    return fitness+(cross/2)


def parent_selection(popsize):
    murate=0.5
    crossrate=0.1
    mupop_size=int(np.ceil(murate*popsize))
    crosspop_size=int(2*np.ceil((crossrate*popsize)/2))
    childpop_size=mupop_size+crosspop_size
    matingpoolindex=np.random.randint(0,popsize,int(childpop_size))
    return matingpoolindex,mupop_size,crosspop_size

def twopoints_crossover(parent1,parent2):
    chromlen=len(parent1)
    crosspoints=sorted(random.sample(range(1,chromlen-1),2))
    #print(crosspoints)
    child=np.concatenate((parent1[0:crosspoints[0]],parent2[crosspoints[0]:crosspoints[1]],parent1[crosspoints[1]:]))
    return child

def crossover(population,crosspop_siz,matingpoolindex):
    chrom_size=len(population[0])
    children_cross=np.zeros((crosspop_siz,chrom_size))
    i=0
    while i<crosspop_siz:
        x=matingpoolindex[i]
        y=matingpoolindex[i+1]
        parent1=population[x]
        parent2=population[y]
        child1=twopoints_crossover(parent1,parent2)
        child2=twopoints_crossover(parent2,parent1)
        children_cross[i]=child1
        children_cross[i+1]=child2
        i+=2
    return children_cross


        
def creep(parent):
    chromlen=len(parent)
    r=np.random.rand(chromlen)

    child=np.zeros(chromlen)
    for i in range(chromlen):
        if r[i]<0.3:
            child[i]=int((parent[i]+1)%8)
        elif (r[i]>=0.3 and r[i]<0.6):
            child[i]=int((parent[i]-1)%8)
        elif (r[i]>=0.6 and r[i]<0.8):
            child[i]=int((parent[i]+2)%8)
        else:
            child[i]=int((parent[i]-2)%8)
            child[i]=int((parent[i]-2)%8)
            print(r[i])
            print(parent[i])
            print(child[i])
    return child
        


def mutate(population,mupop_size,matingpoolindex):
    chrom_size=len(population[0])
    children_mut=np.zeros((mupop_size,chrom_size))
    crosspop_size=len(matingpoolindex)-mupop_size-1
    i=crosspop_size
    j=0
    while i<len(matingpoolindex)-1:
        x=matingpoolindex[i]
        parent_single=population[x]
        muchild=creep(parent_single)
        children_mut[j]=muchild
        i+=1
        j+=1
    return children_mut


def survivor_selection(totalpop,mainpopsize):
    totalpopsize=len(totalpop)
    fitness_=np.zeros(totalpopsize)
    for i in range(totalpopsize):
        fitness_[i]=fitness(totalpop[i])
    total_bestindexes=np.argsort(fitness_)
    final_bestindexes=total_bestindexes[0:mainpopsize]
    newpop=totalpop[final_bestindexes]
    newpopfitness=fitness_[final_bestindexes]
    return newpop,newpopfitness


popsize=10
mainpopsize=popsize
generation=500
population=init_pop(popsize)
best_fitness_array=np.zeros(generation)
best_average_array=np.zeros(generation)

for item in range(generation):
    print('generation',item)
    matingpoolindex,mupop_size,crosspop_size=parent_selection(popsize)
    offspring_cross=crossover(population, crosspop_size, matingpoolindex)
    offspring_mu=mutate(population, mupop_size, matingpoolindex)
    totalpop=np.concatenate((population,offspring_cross,offspring_mu),0)
    new_pop, newpopfitness=survivor_selection(totalpop,mainpopsize)
    bestindex=np.argsort(newpopfitness)
    final_bestindex=bestindex[0]
    best_fitness_array[item]=newpopfitness[final_bestindex]
    best_average_array[item]=st.mean(newpopfitness)
    population=new_pop
    
    
    


  
bestindex=np.argsort(newpopfitness)
final_bestindex=bestindex[0]
bestsolution=new_pop[final_bestindex]
bestsolution_fitness=newpopfitness[final_bestindex]



print('........................................')
print('best solution and fitness\n',[bestsolution,bestsolution_fitness])












    




