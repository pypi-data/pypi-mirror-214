from abc import ABC, abstractmethod
import importlib
import inspect
# import sys, os
from functools import partial, wraps

# --------------------------------------------------------------

def curry(func):
    if isinstance(func, partial):
        # Handle functools.partial objects
        num_required_args = func.func.__code__.co_argcount
        num_wrapped_args = len(func.args) + len(func.keywords)

        @wraps(func)
        def curried(*args, **kwargs):
            all_args = func.args + args
            all_kwargs = {**func.keywords, **kwargs}
            evaluated_args = [arg.evaluate({}) if isinstance(arg,Evaluable) else arg for arg in args]

            if len(all_args) + len(all_kwargs) >= num_required_args:
                return func(*evaluated_args, **all_kwargs)
            else:
                return curry(partial(func.func, *evaluated_args, **all_kwargs))

        return curried
    elif isinstance(func, LambdaFunctionValue):
        num_required_args = len(func.args)

        @wraps(func)
        def curried(*args, **kwargs):
            evaluated_args = [arg.evaluate({}) if isinstance(arg,Evaluable) else arg for arg in args]
            if len(args) + len(kwargs) >= num_required_args:
                # return func(*evaluated_args, **kwargs)
                return func.evaluate({},*evaluated_args)
            else:
                return curry(partial(func, *evaluated_args, **kwargs))
        return curried
    else:
        # Handle regular functions
        num_required_args = func.__code__.co_argcount

        @wraps(func)
        def curried(*args, **kwargs):
            evaluated_args = [arg.evaluate({}) if isinstance(arg,Evaluable) else arg for arg in args]
            if len(args) + len(kwargs) >= num_required_args:
                return func(*evaluated_args, **kwargs)
            else:
                return curry(partial(func, *evaluated_args, **kwargs))

        return curried

def curry_builtin(func):
    # Define a lambda that wraps the built-in function
    return lambda *args, **kwargs: func(*args, **kwargs)

def add_module_functions_to_dict(module_name,alias):
    # core.hello()
    try:
        module=importlib.import_module(module_name)
    except ModuleNotFoundError:
        print(f"The module {module_name} was not found.")
        return
    
    FUNCTION_DICT[alias] = {}

    for(name,func) in inspect.getmembers(module,inspect.getmodule):
        if callable(func):
            try:
                args = inspect.getfullargspec(func).args
            except:
                args = []
            FUNCTION_DICT[alias][name]=curry_builtin(func)
            # FUNCTION_DICT[alias][name]=FunctionDef(name,args,curry(func))


# Now you can add the functions of a module to the FUNCTION_DICT like this:
# add_module_functions_to_dict('aleph')


class Evaluable(ABC):
    """
    Abstract base class for all evaluable entities in the maryChain language.

    This class defines the interface for all classes that can be evaluated in the maryChain language. 
    It is an abstract base class (ABC), which means that it cannot be instantiated directly. 
    Instead, other classes should inherit from this class and implement the abstract methods defined here.

    Each evaluable entity in maryChain is represented by an instance of a class that inherits from Evaluable.
    This class has an abstract method `evaluate`, which should be implemented by all subclasses to define their evaluation semantics.

    The evaluate method of a class representing an evaluable entity in maryChain takes keyword arguments (`kwargs`) 
    which could be used to provide context necessary for evaluation, such as a dictionary of variable names and their values. 
    """

    @abstractmethod
    def evaluate(self, env):
        """
        Abstract method for evaluating an entity.

        This method is meant to be overridden by each concrete subclass of Evaluable. The overriding method 
        should implement the specific evaluation semantics of the entity it represents.

        Parameters:
        **kwargs: Arbitrary keyword arguments that could be used to provide context necessary for evaluation. 

        Returns:
        The result of evaluating the entity.
        """
        pass


class Expression(Evaluable):
    """
    Abstract base class for all expressions in the maryChain language.
    Inherits from the Evaluable abstract base class.
    """
    pass

class Program(Evaluable):
    def __init__(self, imports, expression):

        self.imports = imports
        self.expression = expression

    def evaluate(self,env):

        for import_stmt in self.imports:
            import_stmt.evaluate(env)

        if self.expression:
            return self.expression.evaluate(env)

class Import(Expression):
    def __init__(self, module_parts, alias):
        # self.module_name = '.'.join(module_parts)
        self.module_name = module_parts
        self.alias = alias

    def evaluate(self,env):
        add_module_functions_to_dict(self.module_name, self.alias)





# --------------------------------------------------------------
#  environment

ENVIRONMENT = {'👽':'Alessio Ricco'}

# --------------------------------------------------------------

class CurriedFunction(Expression):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    def evaluate(self,env):

        print(f"evaluate: CurriedFunction f:{self.func} a:{self.args} k:{env}")

        # Apply currying to the function being curried
        curried_func = curry(self.func.evaluate(env))

        # Apply the partially applied arguments to the curried function
        # evaluated_args = [arg.evaluate() for arg in self.args]
        evaluated_args = []
        args0 = self.args[0]
        for arg in args0:

            if isinstance(arg,list) and isinstance(arg[0],Evaluable):
                evaluated_args.append(arg)
                continue

            if isinstance(arg,Evaluable):
                evaluated_args.append(arg)
                continue
            
            evaluated_args.append(arg)

        return curried_func(*evaluated_args)

class FunctionCall(Expression):
    def __init__(self, func, args):
        self.func = func
        self.args = args

    '''function_call : function_call LPAREN args RPAREN
                     | function_call LPAREN RPAREN
                     | IDENTIFIER'''

    def evaluate(self,env):
            print(f"evaluate: FunctionCall f:{self.func} a:{self.args} k:{env}")
            func = None

            # Check if it's a curried function
            if isinstance(self.func, CurriedFunction):
                func = self.func

            # Check if it's an Identifier
            elif isinstance(self.func, Identifier):
                ident = self.func.evaluate()
                if isinstance(ident, CurriedFunction):
                    func = ident
                elif isinstance(ident, FunctionCall):
                    func = ident
                else:
                    raise ValueError(f"Identifier {self.func.name} is not a function or lambda")

            # Check if it's a regular FunctionCall
            elif isinstance(self.func, FunctionCall):
                func = self.func
            elif isinstance(self.func, LambdaFunction):
                func = self.func
                evaluated_args = [arg.evaluate(env) for arg in self.args]
                return func.evaluate(env).evaluate(env,*evaluated_args)
            
            if func:
                evaluated_args = [arg.evaluate(env) for arg in self.args]
                return func.evaluate(*evaluated_args)

            raise ValueError("Invalid function call")

class LetIn(Expression):
    """
    This class represents a "let-in" expression in the maryChain language. A let-in expression
    is used to bind a value to an identifier in a certain scope. The syntax is as follows:

        let <identifier> = <expression> in <body>

    After the expression is evaluated, the result is bound to the identifier, and this binding
    is valid within the body of the let-in expression.
    """

    def __init__(self, identifier, value_expression, body):
        """
        Initializes a new instance of the LetIn class.

        Args:
            identifier: The identifier to which the value will be bound.
            value_expression: The expression that will be evaluated to determine the value
                to bind to the identifier.
            body: The body of the let-in expression, where the identifier is bound to the value.
        """
        self.identifier = identifier
        self.value_expression = value_expression
        self.body = body

    def evaluate(self,env):
        """
        Evaluates the let-in expression.

        This is done by first evaluating the value expression, then creating a new scope where the 
        identifier is bound to the value. The body of the let-in expression is then evaluated in this new 
        scope. Finally, the old scope is restored.

        Returns:
            The result of evaluating the body of the let-in expression.
        """
        # Evaluate the value expression and create a new scope where the identifier is bound to the value.
        value = self.value_expression.evaluate(env)
        # new_env = ENVIRONMENT.copy()
        new_env = env.copy()
        new_env[self.identifier] = value

        # Evaluate the body in the new scope.
        # old_env = ENVIRONMENT
        # ENVIRONMENT = new_env
        try:
            return self.body.evaluate(new_env)
        finally:
            pass
            # ENVIRONMENT = old_env  # Restore the old environment

class Assignment(Expression):
    def __init__(self, identifier, value_expression):
        self.identifier = identifier
        self.value_expression = value_expression

    def evaluate(self,env):
        value = self.value_expression.evaluate(env)
        # new_env = env.copy()
        env[self.identifier] = value
        return value

class BinOp(Expression):
    """
    This class represents a binary operation in the maryChain language. A binary operation is 
    an operation that takes two operands and performs a specified operation on them.

    The supported operators are:
        '+'  - addition
        '-'  - subtraction
        '*'  - multiplication
        '/'  - division
        '&&' - logical AND
        '||' - logical OR
        '->' - logical implication
        '>'  - greater than
        '<'  - less than
        '>=' - greater than or equal to
        '<=' - less than or equal to
        '==' - equality (same as)
    """

    def __init__(self, left, op, right):
        """
        Initializes a new instance of the BinOp class.

        Args:
            left: The left operand of the binary operation.
            op: The operator of the binary operation.
            right: The right operand of the binary operation.
        """
        self.left = left
        self.op = op
        self.right = right

    def evaluate(self, env):
        """
        Evaluates the binary operation and returns the result.

        This is done by first evaluating the left and right operands, then applying the operator to the results.

        Returns:
            The result of the binary operation.

        Raises:
            ValueError: If the operator is not supported.
        """
        if self.op == '+':
            return evaluate(self.left,env) + evaluate(self.right,env)
        if self.op == '-':
            return evaluate(self.left,env) - evaluate(self.right,env)
        if self.op == '*':
            return evaluate(self.left,env) * evaluate(self.right,env)
        if self.op == '/':
            return evaluate(self.left,env) / evaluate(self.right,env)
        if self.op == '&&':
            return evaluate(self.left,env) and evaluate(self.right,env)
        if self.op == '||':
            return evaluate(self.left,env) or evaluate(self.right,env) 
        if self.op == '->':
            return not evaluate(self.left,env) or evaluate(self.right,env)
        if self.op == '>':
            return evaluate(self.left,env) > evaluate(self.right,env) 
        if self.op == '<':
            return evaluate(self.left,env) < evaluate(self.right,env)    
        if self.op == '>=':
            return evaluate(self.left,env) >= evaluate(self.right,env)   
        if self.op == '<=':
            return evaluate(self.left,env) <= evaluate(self.right,env) 
        if self.op == '==':
            return evaluate(self.left,env) == evaluate(self.right,env) 
        raise ValueError(f'Unknown operator: {self.operator}')


class Number(Expression):
    """
    This class represents a numeric literal in the maryChain language. 

    A numeric literal can be an integer or a floating-point number, and this class can handle both.
    """

    def __init__(self, value):
        """
        Initializes a new instance of the Number class.

        Args:
            value: The numeric value represented by the instance. Can be either an integer or a float.

        Note:
            If the value cannot be converted to an integer, it will be converted to a float.
        """
        self.value = value
        try:
            self.value = int(value)
        except ValueError:
            self.value = float(value)

    def evaluate(self,env):
        """
        Evaluates the number, which in practice means returning the numeric value.

        Returns:
            The numeric value of the Number instance.
        """
        return self.value


class String(Expression):
    """
    This class represents a string literal in the maryChain language. 

    The `String` class inherits from the `Expression` class and provides methods for the manipulation of string values.
    """

    def __init__(self, value):
        """
        Initializes a new instance of the String class.

        Args:
            value: The string value represented by the instance.
        """
        self.value = value

    def evaluate(self,env):
        """
        Evaluates the string, which in practice means returning the string value.

        Returns:
            The string value of the String instance.
        """
        return self.value


class Boolean(Expression):
    """
    This class represents a boolean literal in the maryChain language. 

    The `Boolean` class inherits from the `Expression` class and provides methods for the manipulation of boolean values.
    """

    def __init__(self, value):
        """
        Initializes a new instance of the Boolean class.

        Args:
            value: The boolean value represented by the instance.
        """
        self.value = bool(value)

    def evaluate(self,env):
        """
        Evaluates the boolean, which in practice means returning the boolean value.

        Returns:
            The boolean value of the Boolean instance.
        """
        return self.value


class Identifier(Expression):
    """
    This class represents an Identifier in the maryChain language. 

    The `Identifier` class inherits from the `Expression` class and provides a way to interact with variables
    and function calls.
    """

    def __init__(self, name):
        """
        Initializes a new instance of the Identifier class.

        Args:
            name: The name of the variable or function this identifier refers to.
        """
        self.name = name

    def evaluate(self, env):
        """
        Evaluates the Identifier. If the identifier name is in the environment, its value is returned. 
        If the name corresponds to a function in the function dictionary, the name is returned. 
        If the name is an instance of a function call, it is evaluated.

        Returns:
            The value of the Identifier if it exists in the environment, its name if it exists in the function dictionary,
            or the result of its evaluation if it is a FunctionCall.
        """

        name = self.name

        if self.name in env:
            return env[self.name]
        elif self.name in ENVIRONMENT:
            return ENVIRONMENT[self.name]
        elif self.name in FUNCTION_DICT:
            return FUNCTION_DICT[self.name]
        
        if "." in name:  # Check if func is a qualified function name
            module_name, func_name = name.split(".")
            if (module_name not in FUNCTION_DICT) or (func_name not in FUNCTION_DICT[module_name]):
                raise ValueError(f"Function {self.func} is not defined")
            return FUNCTION_DICT[module_name][func_name]

        # if isinstance(self.name, FunctionCall):
        #     return self.name.evaluate()
        return name

class UnaryOperation(Expression):
    """
    This class represents a unary operation in the maryChain language. 

    The `UnaryOperation` class inherits from the `Expression` class and encapsulates an operator and 
    an operand for operations such as unary minus and logical not.
    """

    def __init__(self, operator, operand):
        """
        Initializes a new instance of the UnaryOperation class.

        Args:
            operator: The operator of the unary operation. It could be '-' for unary minus or 'not' for logical not.
            operand: The operand on which the unary operation is to be performed.
        """
        self.operator = operator
        self.operand = operand

    def evaluate(self,env):
        """
        Evaluates the UnaryOperation. If the operator is '-', the negation of the operand is returned.
        If the operator is 'not', the logical not of the operand is returned.

        Returns:
            The result of the unary operation on the operand.

        Raises:
            ValueError: If the operator is not recognized.
        """
        if self.operator == '-':
            return -evaluate(self.operand)
        if self.operator == 'not':
            return not evaluate(self.operand)
        raise ValueError(f'Unknown operator: {self.operator}')

class While(Expression):
    """
    This class represents a while loop in the maryChain language. 

    The `While` class inherits from the `Expression` class and encapsulates a condition and a body.
    The body of the while loop is executed as long as the condition evaluates to True.
    """

    def __init__(self, condition, body):
        """
        Initializes a new instance of the While class.

        Args:
            condition: The condition of the while loop. It should be an expression that evaluates to a boolean.
            body: The body of the while loop. It's a sequence of expressions that will be executed 
                  as long as the condition is True.
        """
        self.condition = condition
        self.body = body

    def evaluate(self,env):
        """
        Evaluates the While loop. The condition is checked before each iteration. 
        If the condition is True, the body is executed, otherwise the loop is exited.

        Returns:
            The result of the last expression evaluated in the body of the loop.

        Raises:
            None
        """
        # result = self.condition.evaluate(env)
        # while result != False:
        #     result = self.body.evaluate(env)
        #     if self.condition.evaluate(env) == False:
        #         break
        b_result = None
        c_result = self.condition.evaluate(env)
        while c_result:
            b_result = self.body.evaluate(env)
            c_result = self.condition.evaluate(env)
            # if self.condition.evaluate(env) == False:
            #     break
        return b_result

class IfThenElse(Expression):
    """
    This class represents a conditional "if-then-else" statement in the maryChain language.

    The `IfThenElse` class inherits from the `Expression` class and encapsulates a condition,
    an expression to evaluate if the condition is true, and another expression to evaluate if
    the condition is false.
    """

    def __init__(self, condition, true_expr, false_expr):
        """
        Initializes a new instance of the IfThenElse class.

        Args:
            condition: The condition of the if-then-else statement. It should be an expression that evaluates to a boolean.
            true_expr: The expression that will be evaluated if the condition is true.
            false_expr: The expression that will be evaluated if the condition is false.
        """
        self.condition = condition
        self.true_expr = true_expr
        self.false_expr = false_expr

    def evaluate(self,env):
        """
        Evaluates the IfThenElse statement. 

        The condition is evaluated first. If the condition is True, the true_expr is evaluated and its 
        result is returned. If the condition is False, the false_expr is evaluated and its result is returned.

        Returns:
            The result of the evaluated true_expr if the condition is true, or the result of the evaluated
            false_expr if the condition is false.

        Raises:
            None
        """
        if evaluate(self.condition):
            return evaluate(self.true_expr)
        else:
            return evaluate(self.false_expr)

class IfThen(Expression):
    """
    The IfThen class represents a conditional expression in a programming language. 
    It contains a condition and an expression that gets evaluated if the condition is true.
    """

    def __init__(self, condition, true_expr):
        """
        Initialize IfThen with a condition and an expression to be evaluated if the condition is true.

        :param condition: The condition of the 'if' statement.
        :param true_expr: The expression to be evaluated if the condition is true.
        """
        self.condition = condition
        self.true_expr = true_expr

    def evaluate(self,env):
        """
        Evaluate the IfThen expression. If the condition is true, evaluate and return the true expression. 
        If the condition is false, return the last evaluated result in the environment. 
        If there is no last result in the environment, return None.

        :return: Result of evaluating the true expression if the condition is true, 
                 or the last result in the environment if the condition is false.
        """
        # Evaluate the condition
        if self.condition.evaluate(env):
            # If the condition is true, evaluate and return the true expression
            return self.true_expr.evaluate(env)
        # elif '%lastresult%' in ENVIRONMENT:
        #     # If the condition is false, return the last evaluated result in the environment
        #     return ENVIRONMENT['%lastresult%']
        else:
            # If there is no last result in the environment, return None
            return None  

class Lazy(Expression):
    """
    The Lazy class represents a lazy evaluation of an expression in a programming language. 
    It contains a function and its evaluated state and value.
    """

    def __init__(self, func):
        """
        Initialize Lazy with a function to be lazily evaluated.

        :param func: The function to be evaluated.
        """
        self.func = func
        self.is_evaluated = False  # Indicates if the function has been evaluated
        self.value = None  # Holds the result of the evaluation

    def evaluate(self,env):
        """
        Evaluate the Lazy expression if it hasn't been evaluated before. 
        The result is cached for future uses.

        :return: Result of evaluating the function.
        """
        # If the function hasn't been evaluated before
        if not self.is_evaluated:
            # If the function is callable
            if callable(self.func):
                # Evaluate and cache the result
                self.value = evaluate(self.func())
            else:
                # If the function is not callable, evaluate and cache the result
                self.value = evaluate(self.func)
            # Mark as evaluated
            self.is_evaluated = True

        # Return the cached value
        return self.value

    def __repr__(self):
        """
        Return a string representation of the Lazy object.
        """
        # If the function has been evaluated
        if self.is_evaluated:
            return f"<Evaluated lazy object with value: {self.value}>"
        else:
            # If the function hasn't been evaluated
            return "<Unevaluated lazy object>"

class Pipe(Expression):
    """
    The Pipe class represents a pipeline operation in a programming language.
    A pipeline operation is one where the result of one operation (left) is used as the input to another operation (right).
    """

    def __init__(self, left, right):
        """
        Initialize Pipe with two expressions: left and right.

        :param left: The left expression to be evaluated first.
        :param right: The right expression that takes the result of the left expression as an argument.
        """
        self.left = left
        self.right = right

    def evaluate(self,env):
        """
        Evaluate the Pipe expression. 
        The left expression is evaluated first and its result is fed as an argument to the right expression.

        :return: Result of evaluating the right expression with the result of the left expression.
        """
        # Evaluate the left expression and store its result in a special variable '%lastresult%'
        # ENVIRONMENT['%lastresult%'] = self.left.evaluate()

        # Insert the result of the left expression as the first argument of the right expression
        func = None
        if isinstance(self.right,FunctionCall):
            func = self.right
            func.args.insert(0, self.left)
            return func.evaluate(env)
            # return l.evaluate(*func.args)
        
        if isinstance(self.right,Identifier):  
            name = self.right.name  
            if isinstance(name,str) and name in ENVIRONMENT:
                if isinstance(ENVIRONMENT[name],FunctionCall):
                    func = ENVIRONMENT[name]
                    func.args.insert(0, self.left)
                    l = func.evaluate(env)
                    return l.evaluate(*func.args)

            elif isinstance(name,str) and name in FUNCTION_DICT:
                func = FUNCTION_DICT[name]
                if isinstance(func,LambdaFunction):        
                    l = func.evaluate(env)
                    return l.evaluate(self.left)
                elif callable(func):
                    return func(self.left.evaluate(env))
                
        if isinstance(self.right,CurriedFunction):
            # function = self.right.func
            # args = self.right.args
            self.right.args[0].insert(0, self.left)
            return self.right.evaluate(env)
                        
        # Evaluate the right expression and return the result
        return self.right.evaluate(env)

class LambdaFunctionValue(Expression):
    """
    The LambdaFunctionValue class represents a lambda function in a programming language.
    A lambda function is a small anonymous function that can take any number of arguments but can have only one expression.
    """

    def __init__(self, args, body):
        """
        Initialize LambdaFunctionValue with arguments and body of the lambda function.

        :param args: The arguments that the lambda function accepts.
        :param body: The expression that forms the body of the lambda function.
        """
        self.args = args
        self.body = body

    def evaluate(self, env, *args):
        """
        Define the behavior of the LambdaFunctionValue instance when it's 'called' like a function.
        If the number of arguments provided during the call doesn't match the lambda function's arguments,
        a TypeError is raised.

        :param args: The arguments provided during the function call.
        :return: Result of evaluating the lambda function's body with the provided arguments.
        """

        print(f"evaluate: LambdaFunctionValue f:{self.body} a:{self.args} k:{args}")

        # Check if the number of arguments provided during the call matches the number of arguments the function accepts
        # if len(args) != len(self.args):
        #     raise TypeError("wrong number of arguments")
        if len(args) > len(self.args):
            raise TypeError("wrong number of arguments")
        
        # Create a local environment where the arguments are bound to their values
        local_env = ENVIRONMENT.copy()
        local_env.update(zip([arg.evaluate(env) for arg in self.args], args))

        body = self.body
        local_args = []
        if callable(body):
            for arg in args:
                value = arg
                if isinstance(value,Evaluable):
                    value = arg.evaluate(local_env)
                local_args.append(value)
            return body(*local_args)

        # Evaluate the function's body in the local environment and return the result
        return body.evaluate(local_env)
    
    # def evaluate(self):
    #     pass


class LambdaFunction(Expression):
    """
    The LambdaFunction class represents a lambda function definition in a programming language. 
    This class is used to create a lambda function object (LambdaFunctionValue) when evaluated.
    """

    def __init__(self, args, body):
        """
        Initialize LambdaFunction with arguments and body of the lambda function.

        :param args: The arguments that the lambda function accepts.
        :param body: The expression that forms the body of the lambda function.
        """
        self.args = args
        self.body = body

    def evaluate(self,env):
        """
        Evaluate the lambda function to a LambdaFunctionValue object which can be called like a function.

        :return: A LambdaFunctionValue object that represents the lambda function.
        """
        print(f"evaluate: LambdaFunction f:{self.body} a:{self.args} ")
        return LambdaFunctionValue(self.args, self.body)

def out_func(x):
    if isinstance(x, Lazy):
        x = x.evaluate()
    print(x)
    return x

def add_func(x, y):
    if isinstance(x, Lazy):
        x = x.evaluate()
    if isinstance(y, Lazy):
        y = y.evaluate()
    return x + y

# def eval_func(x):
#     return x.func()

FUNCTION_DICT = {
    # This dictionary maps function names to FunctionDef instances that implement the function.

    # The 'out' function prints its argument and returns None. 
    # It's implemented with the 'print_func' function and curried to allow partial application.
    'out': (out_func),

    # The 'add' function adds its two arguments. 
    # It's implemented with the 'add_func' function and curried to allow partial application.
    'add': (add_func),

    # The 'eval' function evaluates its argument as a maryChain expression. 
    # It's implemented with the 'eval_func' function and curried to allow partial application.
    # 'eval': (eval_func),
}

def inject_parsing(parse):
    FUNCTION_DICT['exec'] = (lambda x: evaluate(parse(x)))
    return 

def evaluate(node, env=ENVIRONMENT):
    """
    The evaluate function is used to evaluate different types of nodes in an abstract syntax tree (AST).
    It returns the evaluated result of the node.

    :param node: A node in the AST. The node could be a string, integer, float, or an instance of Expression class.
    :return: The evaluated result of the node.
    """
    if node is None:
        return None
    
    if isinstance(node, str):
        # If the node is a string, return the string itself
        return node
    
    if isinstance(node, int):
        # If the node is an integer, return the integer itself
        return node
    
    if isinstance(node, float):
        # If the node is a float, return the float itself
        return node
    
    if isinstance(node, Evaluable):
        # If the node is an instance of Expression class, evaluate the expression and return the result
        return node.evaluate(env)
    
    # If the node is none of the above types, raise a ValueError
    raise ValueError(f'Unknown node type: {node}')
