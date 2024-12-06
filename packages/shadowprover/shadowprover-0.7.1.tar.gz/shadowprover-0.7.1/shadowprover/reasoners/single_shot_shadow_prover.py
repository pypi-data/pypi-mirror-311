import sys
# append the path of the
# parent directory
sys.path.append("..")
sys.path.append("../py_laser")
sys.path.append("../py_laser/syntax")


from edn_format import loads_all, Keyword
from syntax.reader import r, read_symbol_or_symbols
from syntax.expression import *
from reasoners.fol_prover import *
from syntax.reader import *

from reasoners.shadow_prover import *
from reasoners.planner import *

from unifiers.first_order_unify import *
import edn_format
from syntax.common import Symbol
from edn_format import Keyword, loads_all
from syntax.expression import *
from typing import List
from dataclasses import dataclass
from syntax.expression import Expression
import edn_format
from syntax.common import Symbol
from edn_format import Keyword, loads_all
from syntax.expression import *
from typing import List
from dataclasses import dataclass
from syntax.expression import Expression
from inference_systems.reader import read_inference_system

 
 
def translate(formula: Expression, enclosing_context=lambda x: r(f"(context top all all {x})"), is_object=False):
    if formula.is_modal():
        kernel = formula.get_kernel()
        cfun = lambda y: enclosing_context(r(f"(context {formula.get_modal_type()} {str(formula.agent) or 'all'} {formula.get_time()} {y})"))
        return  translate(kernel, cfun) 
    elif formula.is_predicate():
        end_context = str(enclosing_context("end"))
        if is_equals(formula):
            x = formula.args[0]
            y = formula.args[1]
            return r(f"(= {str(translate(x, enclosing_context, is_object=True))} {str(translate(y, enclosing_context, is_object=True),)})")
        else:
            if formula.args is None or len(formula.args) == 0:
                if is_object:
                    return Expression(Symbol("object"), [r(str(formula.head)),r(end_context)]) 
                else:
                    return Expression(Symbol("prop"), [r(str(formula.head)),r(end_context)]) 
            
            else:
                return Expression(formula.head, list(map(lambda x: translate(x, enclosing_context, is_object=True), formula.args)) + [r(end_context)]) 
    
    elif is_quantifier(formula):
        operator = formula.head
        args = formula.args
        vars = str(args[0])
        rest_args = " ".join(list(map(str, map(translate, formula.args[1:]))))
        
        return r(f"({operator} {vars} {rest_args})") 

    else:
        operator = formula.head
                
        args = " ".join(list(map(str, map(lambda x: translate(x, enclosing_context), formula.args))))
        
        return r(f"({operator} {args})") 
    


def tprove(givens, goal, find_answer=False, max_answers=5):
    inference_schemata = [

    ]
    inputs_t = list(map( translate, givens)) + inference_schemata
    goal_t = translate(goal)
    return fol_prove(inputs_t, goal_t, find_answer=find_answer, max_answers=max_answers)    

def tprove_string(givens, goal, find_answer=False, max_answers=5):
    return tprove(list(map(r, givens), r(goal),find_answer, max_answers ))

def get_cached_shadow_prover(find_answer=True, max_answers=5):
    @cache
    def cached_t_prover(inputs, output):
        return tprove(inputs, output, find_answer=find_answer, max_answers=max_answers)
    
    def _prover_(inputs, output):
        return cached_t_prover(frozenset(inputs), output)
    
    return _prover_