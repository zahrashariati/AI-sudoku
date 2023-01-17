import json
import random
import ssl
import time


# *** you can change everything except the name of the class, the act function and the problem_data ***

class Sudoku:
    def __init__(self, sudoku_arr:list):
        self.sudoku = sudoku_arr
        
        
    def fitness(self ,solution):
        index = 0
        
        temp_sudoku = self.sudoku.copy()
        for i in range(len(temp_sudoku)):
            if(temp_sudoku[i] == 0):
                temp_sudoku[i]=int(solution[index])
                index +=1
        fitness = 0
        fitness_1 = 0
        fitness_2 = 0
        fitness_3 = 0

        for i in range(9):
            row = temp_sudoku[i*9:i*9+9]
            for j in range(1,10):
                if(row.count(j) == 0):
                    fitness+=1
                    fitness_1+=1
                
        
        for j in range(3):
            for k in range(3):
                col = []
                index = j*27+k*3
                col += temp_sudoku[index :index+3]
                col += temp_sudoku[index+9 :index+12]
                col += temp_sudoku[index +18:index+21]
                for i in range(1,10):
                    if(col.count(i) == 0):
                        fitness+=1
                        fitness_2+=1    

        for i in range(9):
            col = temp_sudoku[i:i+ 9*9:9]
            for i in range(1,10):
                if(col.count(i) == 0):
                    fitness+=1
                    fitness_3+=1
            
        

        return (fitness , fitness_1 , fitness_2 , fitness_3)
                


class Genetic(object):
    
    def __init__(self, sudoku:Sudoku):
        self.sudoku = sudoku
        self.solve = False
        self.solution = ''
    def create_new_Solution(self, solution_alph , solution_beta):
        index = int(len(solution_alph)/2)
        first_child = solution_alph[:index] + solution_beta[index:]
        second_child = solution_beta[:index] + solution_alph[index:]
        # first_child = ''
        # second_child = ''
        # for i in range(len(solution_alph)):
        #     res = int(solution_alph[i])+int(solution_beta[i])
        #     if(res > 9):
        #         res -=9
        #     first_child += str(res)
        # for i in range(len(solution_alph)):
        #     res = int(solution_alph[i])-int(solution_beta[i])
        #     if(res < 1):
        #         res +=9
        #     second_child += str(res)   
       
        
        fitness_alpha = self.sudoku.fitness(first_child) 
        fitness_beta = self.sudoku.fitness(second_child)
        if(fitness_alpha[0] == 0 ):
            self.solve = True
            self.solution = first_child
        if( fitness_beta[0] == 0):
            self.solve = True
            self.solution = second_child
        if(fitness_alpha[0] > fitness_beta[0]):
            return (second_child , *fitness_beta)
        return (first_child , *fitness_alpha)
    def muta_sol(self,solution_str):
        other_sol = ''
        # if(len(solution_str) > 20):
        #     other_sol = self.muta_sol(solution_str[9::])
        #     solution_str = solution_str[:9]
        index = random.randint(0,len(solution_str)-1)
        s =[str(x) for x in range(1,10) ]
        s.remove(solution_str[index])
        solution_str =  solution_str[:index] + random.choice(s) + solution_str[index+1:] + other_sol
        return solution_str

        
        
        
    def mutation(self , solution):
        chance = random.randint(0,4)
        # if(chance == 1):
        #     return solution
        new_solution= self.muta_sol(solution[0])
        fitness_sol = self.sudoku.fitness(new_solution)
        if(fitness_sol[0] == 0):
            self.solve = True
            self.solution = new_solution
        return  (new_solution ,*fitness_sol)
    def Create_newGeneration(self , solutions:list  ):
        new_generation = [x for x in solutions[:2]]
        for i in range(2):
            for j in solutions[i+2::2]:
                new_generation.append(self.create_new_Solution(solutions[i][0] , j[0]))
        for i in range(len(new_generation)):
            new_generation[i] = self.mutation(new_generation[i])
        return new_generation
    def create_random_genum(self ,number):
        solution = ''
        for i in range(number):
            solution += str(random.randint(1,9))
        return (solution,*self.sudoku.fitness(solution))
    def create_generation_zero(self):
        number = self.sudoku.sudoku.count(0)
#5695386679154823497196418293546216789485243
        generation0 = []
        for i in range(number+17):
            generation0.append(self.create_random_genum(number))
        return generation0
    def Solve(self ):
        next_generation = self.create_generation_zero()
        while not self.solve:
            
            next_generation.sort(key = lambda x : x[1])
            print('-'*10)
            for i in next_generation:
                print(i)
            print('-'*10)
            next_generation = self.Create_newGeneration(next_generation)
    
        


        
    
        
        
class AI:
    # ^^^ DO NOT change the name of the class ***

    def __init__(self):
        pass
    
    # the solve function takes a json string as input
    # and outputs the solved version as json
    def solve(self, problem):#322138839521597968596537126312449
        # ^^^ DO NOT change the solve function above ***
        sample_json = """
       {
        "sudoku":[
            [1 , 0 , 4 , 8 , 6 , 5 , 2 , 3 , 7],
            [7 , 0 , 5 , 4 , 1 , 2 , 9 , 6 , 8],
            [8 , 0 , 2 , 3 , 9 , 7 , 1 , 4 , 5],
            [9 , 0 , 1 , 7 , 4 , 8 , 3 , 5 , 6],
            [6 , 0 , 8 , 5 , 3 , 1 , 4 , 2 , 9],
            [4 , 0 , 3 , 9 , 2 , 6 , 8 , 7 , 1],
            [3 , 0 , 9 , 6 , 5 , 4 , 7 , 1 , 2],
            [2 , 0 , 6 , 1 , 7 , 9 , 5 , 8 , 3],
            [5 , 0 , 7 , 2 , 8 , 3 , 6 , 9 , 4]
        ]
        }
        """
        problem_data = json.loads(sample_json)
        # ^^^ DO NOT change the problem_data above ***
        sudoku = [item for row in problem_data['sudoku'] for item in row ]
        
        
        problem_sudoku = Sudoku(sudoku)
        start_time = time.time()
        alg = Genetic(problem_sudoku)
        alg.Solve()
        print(alg.solution)
        print("--- %s seconds ---" % (time.time() - start_time))

        # TODO implement your code here

        # finished is the solved version
        return finished

a = AI()
print('aaaaaa')
a.solve("")