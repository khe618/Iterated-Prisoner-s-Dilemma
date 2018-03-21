from random import random
class Individual:
    def __init__(self):
        self.prbs = [random(), random(), random(), random(), random()]
        #[p(d,d), p(d,c), p(c,d), p(c,c), p(i,i)]
        #p(i,i) is the probability of cooperation at the initial states, p(c,d) is the probability
        #of cooperation when the AI cooperates and the opponent defects
        self.score = 0
    def reset(self):
        self.score = 0
    def update_score(self, score):
        self.score += score
    def next_move(self, index):
        if self.prbs[index] > random():
            return 1
        return 0
        #1 = cooperate, 0 = defect
    def mutate(self):
        for i in range(5):
            if random() < 0.05: #mutation rate
                self.prbs[i] = random()
def simulate_game(individual_1, individual_2):
    move_1 = individual_1.next_move(4)
    move_2 = individual_2.next_move(4)
    last_move_1 = move_1
    last_move_2 = move_2
    score_1 = payoff_matrix[(move_1 << 1) | move_2]
    score_2 = payoff_matrix[(move_2 << 1) | move_1]
    for i in range(99):
        move_1 = individual_1.next_move((last_move_1 << 1) | move_2)
        move_2 = individual_2.next_move((last_move_2 << 1) | move_1)
        score_1 += payoff_matrix[(move_1 << 1) | move_2]
        score_2 += payoff_matrix[(move_2 << 1) | move_1]
        last_move_1 = move_1
        last_move_2 = move_2
    individual_1.update_score(score_1)
    individual_2.update_score(score_2)
def fitness_function():        
    for i in range(len(population) - 1):
        for j in range(i + 1, len(population)):
            simulate_game(population[i], population[j])
    population.sort(key = lambda x: x.score, reverse = True)
def cumulative_score():
    temp = [0]
    for individual in population:
        temp.append(individual.score + temp[-1])
    return temp[1:]
def create_children(n):
    children_arr = []
    cum_prbs = cumulative_score()
    cum_prbs = [x / cum_prbs[-1] for x in cum_prbs]
    while len(children_arr) < n:
        rand = random()
        for k, prb in enumerate(cum_prbs):
            if rand <= prb:
                parent_1 = population[k]
                break
        rand = random()
        for k, prb in enumerate(cum_prbs):
            if rand <= prb:
                parent_2 = population[k]
                break
        temp_1 = parent_1.prbs[:]
        temp_2 = parent_2.prbs[:]
        random_index = int(random() * 5)
        (temp_1[random_index], temp_2[random_index]) = (temp_2[random_index], temp_1[random_index])
        child_1 = Individual()
        child_2 = Individual()
        child_1.prbs = temp_1
        child_2.prbs = temp_2
        children_arr.append(child_1)
        children_arr.append(child_2)
    return children_arr
def replace(n):
    #n must be even to maintain constant population size
    children = create_children(n)
    population[len(population) - n:] = children
    for individual in population:
        individual.reset()
def mutate_population():
    for individual in population:
        individual.mutate()
#payoff matrix:
#       C       D
#C    [1,1]   [-1,2]
#D    [2,-1]  [0,0]
payoff_matrix = [0, 2, -1, 1]        
population = [Individual() for i in range(100)]
for i in range(200): #generations
    fitness_function()
    print(population[0].score)
    print(population[0].prbs)
    replace(20)
    mutate_population()
