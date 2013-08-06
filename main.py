import numpy as np
import scipy.optimize as op

chicken = 0
carrots = 1
thyme = 2
onions = 3
noodles = 4
garlic = 5
parsley = 6

ingredients = [chicken, carrots, thyme, onions, noodles, garlic, parsley]
ingredient_names = {chicken : 'chicken', carrots : 'carrots', thyme : 'thyme', onions: 'onions', noodles: 'noodles', garlic : 'garlic', parsley : 'parsley'}

elaine = 0
george = 1
jerry = 2
newman = 3

stores = [elaine, george, jerry, newman]
store_names = {elaine : "elaine's", george : "george's", jerry : "jerry's", newman : "newman's" }

store_inventory = {
          elaine : {chicken : 5, carrots : 1, thyme : 3, onions : 6, noodles:5, garlic : 2, parsley :3 },
          george : {chicken : 6, carrots : 8, thyme : 19, onions : 12, noodles:0, garlic : 1, parsley :6 },
          jerry  : {chicken : 2, carrots : 5, thyme : 16, onions : 10, noodles:3, garlic : 1, parsley :2},
          newman : {chicken : 3, carrots : 2, thyme : 6, onions : 4, noodles:9, garlic : 0, parsley :1 },}


ratios = {chicken : .4, carrots : .12, thyme : .08, onions : .15, noodles: .15, garlic : .05, parsley : .05}
max_per_store = {elaine: 12, george: 8, jerry: 15, newman:17}


def calc_total_pounds_of_food(x):
    return np.sum(x)

def objective_function(x):
    return -1 * calc_total_pounds_of_food(x)

def extract_store_specific_pounds(x, store):
    start_index = store * len(ingredients)
    end_index = start_index + len(ingredients)
    result =  x[start_index:end_index]
    return result

def extract_ingredient_specific_pounds(x, ingredient):
    result = x[ingredient::len(ingredients)]
    return result

def calc_food_ratio_constraint(ingredient):
    return ({'type' : 'ineq',
             'fun' : lambda x : np.sum(extract_ingredient_specific_pounds(x, ingredient)) - (calc_total_pounds_of_food(x) * ratios[ingredient]) },)

def calc_max_per_store_constraint(store):
    return ({'type' : 'ineq',
             'fun' : lambda x : max_per_store[store] - np.sum(extract_store_specific_pounds(x, store))},)

def calc_constraints():
    constraints = ()

    for ingredient in ingredients:
        constraints += calc_food_ratio_constraint(ingredient)

    for store in stores:
        constraints += calc_max_per_store_constraint(store)

    return constraints

def calc_bounds():
    bounds = []

    for s in stores:
        for i in ingredients:
            bounds.append((0, store_inventory[s][i]))

    return bounds

def calc_initial_guess():
    guess = []

    for s in stores:
        for i in ingredients:
            guess.append(store_inventory[s][i])

    return guess

def perform_optimization():
    guess = calc_initial_guess()
    bnds = calc_bounds()
    cnstrs = calc_constraints()
    result = op.minimize(objective_function, guess, method="SLSQP", bounds=bnds, constraints=cnstrs, options={'ftol' : 1e-12})
    return result

def print_summary(result):
    print 'Soup Nazi should pick up %f lbs of ingredients' % (result.fun * -1)
    index = 0
    for s in stores:
        print "%f lbs of food from %s. Able to carry %f pounds." % (np.sum(extract_store_specific_pounds(result.x, s)), store_names[s], max_per_store[s])
        for i in ingredients:
            print "\t%s: %f lbs (%f in stock)" % (ingredient_names[i], result.x[index], store_inventory[s][i])
            index = index + 1


    print
    print
    for i in ingredients:
        lbs = np.sum(extract_ingredient_specific_pounds(result.x, i))
        total_inventory = np.sum(map(lambda s : store_inventory[s][i], store_inventory.keys()))
        percent = (lbs / result.fun) * -100
        print '%f lbs of %s. %f available across all stores. %f%%' % (lbs, ingredient_names[i], total_inventory, percent)






result = perform_optimization()
print_summary(result)





