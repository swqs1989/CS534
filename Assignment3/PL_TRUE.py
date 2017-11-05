from utils import *

def pl_true(exp, model={}):
    """Return True if the propositional logic expression is true in the model,
    and False if it is false. If the model does not specify the value for
    every proposition, this may return None to indicate 'not obvious';
    this may happen even when the expression is tautological."""
    # print("exp: %r, model: %r" %(exp, model))
    # print("call function")
    if exp in (True, False):
        return exp
    op, args = exp.op, exp.args
    if is_prop_symbol(op):
        # print(model.get(exp))
        return model.get(exp)
    elif op == '~':
        p = pl_true(args[0], model)
        if p is None:
            return None
        else:
            return not p
    elif op == '|':
        result = False
        for arg in args:
            p = pl_true(arg, model)
            if p is True:
                return True
            if p is None:
                result = None
        return result
    elif op == '&':
        result = True
        for arg in args:
            p = pl_true(arg, model)
            if p is False:
                return False
            if p is None:
                result = None
        return result
    p, q = args
    if op == '==>':
        return pl_true(~p | q, model)
    elif op == '<==':
        return pl_true(p | ~q, model)
    pt = pl_true(p, model)
    if pt is None:
        return None
    qt = pl_true(q, model)
    if qt is None:
        return None
    if op == '<=>':
        return pt == qt
    elif op == '^':  # xor or 'not equivalent'
        return pt != qt
    else:
        raise ValueError("illegal operator in logic expression" + str(exp))

def is_symbol(s):
    """A string s is a symbol if it starts with an alphabetic char."""
    return isinstance(s, str) and s[:1].isalpha()

def is_prop_symbol(s):
    """A proposition logic symbol is an initial-uppercase string."""
    return is_symbol(s) and s[0].isupper()

def Symbol(name):
    """A Symbol is just an Expr with no args."""
    return Expr(name)


def symbols(names):
    """Return a tuple of Symbols; names is a comma/whitespace delimited str."""
    return tuple(Symbol(name) for name in names.replace(',', ' ').split())

(A, B, C, D) = symbols("A,B,C,D")
H = Symbol("H")
# print(is_symbol("-a"))
Number = (int, float, complex)
Expression = (Expr, Number)


# print(pl_true(ex1, {Expr("A"): True, Expr("B"): True}))
print(pl_true(expr("M"), {Expr("M"): True}))

question = "g"
# if question == "b":
print("b. ")
print("Partial model: A ==> B, when B is True, ")
ex1 = expr("A ==> B")
print(pl_true(ex1, {B: True}))

print("Partial model: A | B, when A is True, ")
ex2 = expr("A | B")
print(pl_true(ex2, {Expr("A"): True}))

print("Partial model: A & B, when B is False, ")
ex3 = expr("A & B")
print(pl_true(ex3, {Expr("B"): False}))

# elif question == "c":
print("c. ")
print("Partial model: A & B, when B is False, ")
ex4 = expr("A & B")
print(pl_true(ex4, {Expr("B"): False}))

print("-"*50)
print("Partial model: A | B, when B is False, ")
ex5 = expr("A | B")
print(pl_true(ex5, {Expr("B"): False}))

# elif question == "d":
print("d. ")
ex6 = expr("A | ~A")
print(pl_true(ex6))

# elif question == "e":
print("e. ")
ex7 = expr("A | B | C | D")
print(pl_true(ex7, {Expr("A"): False, Expr("B"): True}))
