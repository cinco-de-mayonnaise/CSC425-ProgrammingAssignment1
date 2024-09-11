import sympy
import sys
import random
from typing import Dict, Iterable

from sympy.parsing.sympy_parser import parse_expr
"""
Goal: Create a system of predicates that take in values, and determine whether it is true or false

"""

def mistake():
    exit()

class Predicate():
    """A predicate is any mathematical expression that evaluates to either True or False. 
    
    Example:  <br>
    324 > 12+16 <br>
    cos(x)**2 > -500 <br>
    -1 == 1

    A predicate with variables would typically need to be evaluated, by providing values for all variables, before it can evaluate to True or False.

        x == 3; x=3   (True)
        x > 5;        (Unknown, can't decide because we don't know x)
        x > 5; x=2  (False)

    If a predicate's value is undeterminable, trying to evaluate it will return None. This should NOT be interpreted as it being exclusively False or True, 
    but should be thought of as "This predicate could be True" or "This predicate could be False"  
    """
    p: sympy.core.basic.Basic = None

    def __init__(self, predicate_string) -> None:
        try:
            parse_expr(predicate_string)
        except:
            raise SyntaxError("This predicate is not valid! Please check your input properly")
        
        self.p = parse_expr(predicate_string, evaluate=False)  # should be some expression

        #try:
        #    self.p.subs()        # attempt substitution and check whether its ok

    def __repr__(self) -> str:
        return self.p.__repr__()
    
    def eval(self, args: dict):
        """asdf"""
        retval = self.p.subs(args)
        #print(retval)
        if isinstance(retval, (sympy.logic.boolalg.BooleanTrue, sympy.logic.boolalg.BooleanFalse)):
            return bool(retval)
        else:    # it is still some type of mathematical expression, so args did not contain variables to evaluate the statement.
                    # may even be an invalid exprssion!!
            return None
        
    def get_freesymbols(self):
        return self.p.free_symbols


def solveCSP_BackTracking_ForwardChecking(variables: Iterable[str], domains: Dict[str, list[int]], constraints: Iterable[Predicate]):
    
    def init():
        nonlocal variables
        nonlocal domains
        nonlocal constraints 

        variables = set(variables)
        for v in variables:  # ensure all variables have a defined domain
            if v not in domains.keys():
                raise ValueError("A variable has been declared without a domain being defined for it")
        
        # ensure all constraints involve only the variables that have been defined
        all_freevars = set()
        for c in constraints:
            all_freevars = all_freevars.union(c.get_freesymbols())
        for v in all_freevars:
            if v.__repr__() not in variables:
                raise ValueError("One of the constraints involve an undefined variable {}. This constraint couldn't ever be satisfied.".format(v))
        
        # build a list of variables in the order of least participation in constraints
        count_vars = dict()
        for p in constraints:
            for sym in p.get_freesymbols():
                sym = sym.__repr__()
                count_vars[sym] = count_vars.get(sym, 0) + 1
        vars_order_LCV = [x[0] for x in sorted(count_vars.items(), key=lambda item: item[1])]
        print(vars_order_LCV)

        print("Good to go!")

        return vars_order_LCV
    
    vars_order_LCV = init()
    
    # build a list of variables in the order of smallest domain
    def select_unassigned_var(cur_assign: Dict[str, int]):
        nonlocal variables
        nonlocal constraints
        nonlocal vars_order_LCV

        to_pick = [v for v in variables if v not in cur_assign.keys()]
        # select a random var
        #return random.choice(to_pick)
        
        for v in vars_order_LCV:
            if v not in cur_assign.keys():
                return v
    
    def order_domain_values(var: str, cur_assign: Dict[str, int]):
        pass

    def is_valid_assignment(cur_assign: Dict[str, int]):
        nonlocal constraints

        for c in constraints:
            if c.eval(cur_assign) is not True:
                return False

        return True
    
    def is_consistent(val: int, var: str, cur_assign: Dict[str, int]):
        nonlocal constraints

        ### WARNING: this may modify cur_assign outside of this function, we may need a copy
        cur_assign[var] = val         

        for c in constraints:
            if c.eval(cur_assign) is False:
                return False

        return True
        
    def backtrack(a: Dict[str, int]):
        # read-only!!!! no change!!!!
        nonlocal variables
        nonlocal domains
        nonlocal constraints

        if (is_valid_assignment(a)):
            return a

        var = select_unassigned_var(a)
        #for val in order_domain_values(var, assignment, csp):
        for val in domains[var]:
            if is_consistent(val, var, a):
                a[var] = val
                result = backtrack(a)
                if result is not None:
                    return result
            a.pop(var)
        
        return None

    return backtrack(dict())

    

def main():
    FILENAME = "test2.txt"
    inputfile = None
    with open(FILENAME, "r") as f:
        inputfile = f.read().split('\n')

    # Input section 1: Variable name and count
    variable_list = [v for v in inputfile.pop(0).split()]

    # Input section 2: Domain for every variable
    domain_ALL = dict()
    for v in variable_list:
        try:
            domain_thisvar = [int(k) for k in inputfile.pop(0).split()]
            domain_ALL[v] = domain_thisvar
        except:
            print("There is a mistake in the input file. Please change the input file by referring to the correct input format and try again.")
            return
        
    # Input section 3: Enter predicates
    try:
        predicates_count = int(inputfile.pop(0))
    except:
        print("There is a mistake in the input file. Please change the input file by referring to the correct input format and try again.")
        return
    
    predicates_ALL = []
    for i in range(predicates_count):
        predicates_ALL.append(Predicate(inputfile.pop(0)))
    
    if (len(inputfile) > 0):
        print("Warning: There is leftover data in the input file. Ignoring...")

    print(variable_list)
    print(domain_ALL)
    print(predicates_ALL)

    #for p in predicates_ALL:
    #    print(p.get_freesymbols())

    #print(predicates_ALL[-1].eval({"a": 4, }))
    #print(predicates_ALL[-1].eval({"a": 1, "b": 5, "c":2}))
    #print(predicates_ALL[-1].eval({"a": 4, "b":-1}))
    # Parse predicates: 
    print(solveCSP_BackTracking_ForwardChecking(variable_list, domain_ALL, predicates_ALL))
    

main()