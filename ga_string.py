import random
import os
from copy import deepcopy as copy

class population:
    def __init__(self):
        self.debug=0
        self.max_fitness=0
        self.total_population=0
        self.target=[]
        self.fitness_val=[]
        self.individuals=[]
        self.individuals_after_Selection=[]

    def set_target(self,target):
        for i in range(len(target)):
            self.target.append(target[i])
        self.max_fitness=26*len(target)
            
    def get_target(self):
        return self.target

    def get_max_fitness(self):
        return self.max_fitness

    def get_best_individuals(self):
        return self.individuals[0].get_data()

    def generate(self,val):
        self.total_population=val
        for i in range(val):
            self.individuals.append(0)
            self.individuals[i]=individual(i,len(self.target))

    def ranking(self):
        temp_data=[]
        for i in range(self.total_population):
            temp_data.append((self.fitness_val[i],self.individuals[i].get_index()))
        temp_data.sort(reverse=True)
        for i in range(self.total_population):
            self.fitness_val[i]=temp_data[i][0]
            self.individuals_after_Selection.append(self.individuals[temp_data[i][1]])
        self.new_population()

    def fitness(self,anu=1):
        for i in range(self.total_population):
            self.fitness_val.append(0)
            sum_data=0
            data=self.individuals[i].get_data()
            for j in range(len(data)):
                sum_data+=abs(data[j]-char_to_int(self.target[j]))
            self.fitness_val[i]=self.max_fitness-sum_data
            if(anu!=0):
                if(anu!=2):
                    print(f'=> {i+1}.\tfitness ==> \t{self.fitness_val[i]}\tdata ==>\t{int_to_char(self.individuals[i].get_data())}')
                elif(anu==2 and i==0):
                    print(f'=> {i+1}.\tfitness ==> \t{self.fitness_val[i]}\tdata ==>\t{int_to_char(self.individuals[i].get_data())}')

    def sorting(self):
        for i in range(len(self.individuals)):
            self.fitness_val.append(0)
            sum_data=0
            data=self.individuals[i].get_data()
            for j in range(len(data)):
                sum_data+=abs(data[j]-char_to_int(self.target[j]))
            self.fitness_val[i]=self.max_fitness-sum_data

        temp_data=[]
        for i in range(self.total_population):
            temp_data.append((self.fitness_val[i],self.individuals[i].get_index()))
        temp_data.sort(reverse=True)
        for i in range(self.total_population):
            self.fitness_val[i]=temp_data[i][0]
            self.individuals_after_Selection.append(self.individuals[temp_data[i][1]])
        self.new_population()
            

    def selection(self):
        sum_fitness=0
        for i in range(len(self.fitness_val)):
            sum_fitness+=self.fitness_val[i]
        if(self.debug):
            print("selection roullete")
        while len(self.individuals_after_Selection)!=self.total_population:
            for j in range(self.total_population): 
                if((random.uniform(0,1)) < (self.fitness_val[j]/sum_fitness)):
                    if(self.debug):
                        print(f"indeks ke {j}\tfitness ==>\t{self.fitness_val[j]}\trate {(self.fitness_val[j]/sum_fitness)*100:.2f}%\tdata ==>\t{int_to_char(self.individuals[j].get_data())}")
                    self.individuals_after_Selection.append(0)
                    self.individuals_after_Selection[len(self.individuals_after_Selection)-1]=individual(1,1)
                    self.individuals_after_Selection[len(self.individuals_after_Selection)-1].generate(len(self.individuals_after_Selection)-1,(self.individuals[j].get_data()))
                    break
        self.fitness(0)

    def crossover(self):
        individual_len=len(self.individuals[0].get_data())-1
        temp_data=[]
        is_odd=len(self.fitness_val)%2
        half_population=int(len(self.individuals)/2)
        if(self.debug):
            print("crossover")
        for i in range(half_population):
            a=self.individuals[i].get_data()
            b=self.individuals[i+half_population].get_data()
            if(random.uniform(1,0) < 0.6):
                random1=random.randint(0,individual_len)
                random2=random.randint(random1,individual_len)
                for j in range(individual_len):
                    if j>=random1 and j<=random2:
                        a[j],b[j]=b[j],a[j]
            temp_data.append(a)
            temp_data.append(b)
        for i in range(len(self.individuals)):
            self.individuals_after_Selection.append(0)
            self.individuals_after_Selection[i]=individual(1,1)
            self.individuals_after_Selection[i].generate(i,(temp_data[i]))
        self.new_population()
        self.fitness(0)

    def mutation(self):
        if(self.debug):
            print("mutation")
        temp_data=[]
        for i in range(len(self.individuals)):
            a=self.individuals[i].get_data()
            if(random.uniform(0,1) < 0.2):
                acak=random.randint(0,len(self.individuals[0].get_data()))-1
                a[acak]+=random.randint(-2,2)
                if(a[acak]>26):
                    a[acak]=26
                elif(a[acak]<1):
                    a[acak]=1
            temp_data.append(a)
        for i in range(len(self.individuals)):
            self.individuals_after_Selection.append(0)
            self.individuals_after_Selection[i]=individual(1,1)
            self.individuals_after_Selection[i].generate(i,(temp_data[i]))
        self.new_population()
        self.fitness(0)

    def new_population(self):
        # self.individuals = copy(self.individuals_after_Selection)
        for i in range(self.total_population):
            self.individuals[i]=copy(individual(i,len(self.individuals[i].get_data())))
            # print(self.individuals_after_Selection[i].get_data())
            self.individuals[i].generate(i,self.individuals_after_Selection[i].get_data())
        self.individuals_after_Selection=[]

    def evolve(self):
        # self.fitness(self.debug)
        self.sorting()
        self.best_chromosome=copy(self.individuals[0])
        # print(f"PEMILIHAN {int_to_char(self.best_chromosome.get_data())}")
        self.selection()
        self.crossover()
        self.mutation()
        self.sorting()
        self.individuals[len(self.individuals)-1].generate(len(self.individuals)-1,self.best_chromosome.get_data())
        # print(f"PRIVILLEGE FOR {int_to_char(self.best_chromosome.get_data())}")
        self.sorting()
        self.fitness(self.debug+2)



class individual:
    def __init__(self,index_data,val):
        self.debug=0
        self.index_data=index_data
        self.data=[]
        for i in range(val):
            self.data.append(random.randint(1,26))
        if self.debug:
            print(f"{int_to_char(self.data)}")

    def generate(self,index_data, data):
        self.index_data=index_data
        self.data=data

    def get_index(self):
        return self.index_data
    
    def get_data(self):
        return self.data

def char_to_int(char):
    if len(char)==1:
        return ord(char)-96
    data=[]
    for i in range(len(char)):
        data.append(ord(char[i])-96)
    return data

def int_to_char(int):
    if len(int)==1:
        return chr(int+96)
    data=[]
    for i in range(len(int)):
        data.append(chr(int[i]+96))
    return data

def enter():
    print("")

def main():
    # os.system("clear")
    total_population=50
    total_evolution=500
    while True:
        nama=population()
        target=input("masukkan kata (tanpa spasi): ").lower().replace(" ", "")
        if target=="keluar":
            break
        nama.set_target(target)
        # nama.set_target("andika")
        print(f"target \t\t= {nama.get_target()}")
        print(f"max fitness \t= {nama.get_max_fitness()}")
        input("tekan enter untuk lanjut")
        nama.generate(total_population)

        for i in range(total_evolution):
            print(f"POPULASI {i+1}  \t", end='')
            nama.evolve()
            if nama.get_best_individuals() == char_to_int(nama.get_target()):
                break
        print("info: tulis 'keluar' untuk berhenti")

if __name__ == "__main__":
    main()