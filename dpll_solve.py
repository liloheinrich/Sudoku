import copy
    
def check_done(clauses):
    """ Figures out if the problem is solved, not solvable, or unfinished. 

    inputs
        clauses: 2D array of clauses

    returns
        True if all clauses are satisfied
        False if there's a clause that cannot be satisfied
        None if there are still undetermined clauses left
    """
    if(len(clauses) == 0):
            return True
            
    for c in clauses:
        if(len(c) == 0):
            return False

    return None
                
def assign(assm, p):
    """ Assigns the literal 'p' to a value in the dictionary 'assm'. If the input is 
    negated, assigns p to false. If the input is not negated, assigns p to true. 

    inputs
        assm: dictionary of literal assignments
        p: a literal represented by an integer value
    """
    if p >= 0:
        assm[abs(p)] = 1
    else:
        assm[abs(p)] = 0
    
def simplify(clauses, p):
    """ Updates clauses to reflect the impact of the assignment of literal 'p'.
    If clauses are now satisfied by p, they can be removed. If clauses are not 
    satisfied by p, then p is no longer relevant and is removed from the clause.

    inputs
        clauses: 2D array of clauses
        p: a literal represented by an integer value

    returns
        copy_clauses: 2D array of clauses, updated to remove references to literal 'p'
    """
    copy_clauses = copy.deepcopy(clauses) 
    i = 0
    while i < len(copy_clauses):
    
        # get rid of clauses that are now satisfied by true
        if p in copy_clauses[i]:
            del copy_clauses[i]
            
        # get rid of references to this bc it's unhelpful as false
        else:
            if -p in copy_clauses[i]:
                copy_clauses[i].remove(-p)
            i += 1

    return copy_clauses

def solve_sat(clauses, assm):
    """ Recursively solves the rest of the satisfiability problem. Base case: 
    we have determined satisfiability using check_done(). Otherwise, pick
    a literal that hasn't been assigned yet, try assigning it to false then
    recurse. If that doesn't work, try assigning it to true then recurse.

    inputs
        clauses: 2D array of clauses
        assm: dictionary of literal assignments

    returns
        sat: boolean that is true if satisfiable, false otherwise
        assm: dictionary of literals to satisfying assignments
    """ 
    result = check_done(clauses)
    if result != None:
        return result, assm

    copy_assm = copy.deepcopy(assm)
    val_list = list(copy_assm.values())
    key_list = list(copy_assm.keys())
    idx = val_list.index(None)
    p = key_list[idx]

    # try false first
    assign(copy_assm, -p)
    copy_clauses = simplify(clauses, -p)
    result = solve_sat(copy_clauses, copy_assm)
    if(result[0]): return result
    
    # if that didn't work, try true
    assign(copy_assm, p)
    copy_clauses = simplify(clauses, p)
    return solve_sat(copy_clauses, copy_assm)

def get_vars(clauses):
    """ Picks out all of the literals from the clauses to create
    the assignments dictionary. 

    inputs
        clauses: 2D array of clauses

    returns 
        assm: dictionary meant to hold the assignments of the literals
    """
    assm = dict()
    for c in clauses:
        for p in c:
            assm[abs(p)] = None
    return assm

def assign_pure_literals(clauses, assm):
    """ Assigns pure literals - literals that show up in a lenth-1 clause 
    and therefore have an obvious and necessary assignment value. 

    inputs
        clauses: 2D array of clauses
        assm: dictionary of literal assignments

    returns 
        clauses: 2D array of clauses updated to remove references to pure literals
        assm: dictionary of updated literal assignments 
    """
    i = 0
    while i < len(clauses):
        if(len(clauses[i]) == 1):
            assign(assm, clauses[i][0])
            clauses = simplify(clauses, clauses[i][0])
            i = 0
        else:
            i += 1
    return clauses, assm

def dpll(clauses):
    """ Solves the satisfiability problem. First checks whether satisfiability 
    has been determined using check_done(). Otherwise, it sets up the variable 
    assignment dictionary, assigns pure literals, and runs the solver.

    inputs
        clauses: 2D array of clauses

    returns
        sat: boolean that is true if satisfiable, false otherwise
        assm: dictionary of literals to satisfying assignments
    """ 

    # see if the problem is already solved
    result = check_done(clauses)
    if result != None: return result

    assm = get_vars(clauses)

    # assign the variables that can only go one way
    clauses, assm = assign_pure_literals(clauses, assm)
    
    # solve the rest of the unit clauses recursively
    return solve_sat(clauses, assm)


# DO NOT USE 0 AS A LITERAL AS IT CANNOT HOLD A SIGN VALUE
# Small test cases provided below

# TRUE               
# clauses  = [[1, -5, 4, 2], [-1, 5, 3, 4, 2], [-3, -4, 2], [3], [5]]

# FALSE
# clauses  = [[3, 1, 2], [3, 1, -2], [3, -1, 2], [-3, 1, 2], 
#     [3, -1, -2], [-3, 1, -2], [-3, -1, 2], [-3, -1, -2]]
                
# TRUE
# clauses  = [[3, 1, -2], [-3, -1, 2], [-3, 1, -2]]

# print(dpll(clauses))