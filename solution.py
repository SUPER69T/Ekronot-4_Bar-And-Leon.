from functools import reduce
from unittest import case

# ------------------------------------------------
# Q1 - OOP (Python)
# ------------------------------------------------
class Date:
    def __init__(self, year, month, day):
        self.day = day
        self.month = month
        self.year = year

    def get_day(self):
        return self.day
    def get_month(self):
        return self.month
    def get_year(self):
        return self.year

    def __str__(self):
        match self.month:
            case 1: m = "january"
            case 2: m = "february"
            case 3: m = "march"
            case 4: m = "april"
            case 5: m = "may"
            case 6: m = "june"
            case 7: m = "july"
            case 8: m = "august"
            case 9: m = "september"
            case 10: m = "october"
            case 11: m = "november"
            case 12: m = "december"
        return f"{self.get_day()}th of {m}, {self.get_year()}"
    def __repr__(self):
        return str(self.get_year()) + " " + str(self.get_month()) + " " + str(self.get_day())

# ------------------------------------------------
class Time:
    def __init__(self, minutes, hours):
        self.hours = hours
        self.minutes = minutes

    def get_hours(self):
        return self.hours

    def get_minutes(self):
        return self.minutes

    def __eq__(self, other):
        return self.minutes == other.minutes and self.hours == other.hours

    def __hash__(self):
        return hash((self.get_minutes(), self.get_hours()))

    def __str__(self):
        return f"{self.get_minutes():02}:{self.get_hours():02}"

    def __repr__(self):
        return f"{self.get_minutes():02}:{self.get_hours():02}"


# ------------------------------------------------
class CalendarEntry():
    def __init__(self, day, month, year):
        self.date = Date(day, month, year)
        self.tasks = {}

    #getters:
    def get_date(self):
        return self.date
    def get_day(self):
        return self.date.get_day()
    def get_month(self):
        return self.date.get_month()
    def get_year(self):
        return self.date.get_year()
    def get_tasks(self):
        return self.tasks

    #setters:
    #def set_task_list(self,task_list):
    #    self.tasks = task_list

    def addTask(self, task_name, start_time, end_time):
        start_time_taken = False
        end_time_taken = False
        for n1,n2 in self.tasks.keys():
            if start_time == n1: start_time_taken = True
            if end_time == n2: end_time_taken = True

        if start_time_taken and end_time_taken:
            print(f"Task {task_name} was already taken")
        else:
            # self.tasks = {(start_time, end_time) : task_name}
            self.tasks[(start_time, end_time)] = task_name
            # self.tasks

    def __str__(self):
        output_list = ""

        for i, ((k1, k2), v) in enumerate(self.tasks.items()):
            output_list += f"{i + 1}. {k1.__str__()} - {k2.__str__()} - {v}.\n"

        return f"Todo list for {self.get_date().__str__()}:\n{output_list}"

    def __repr__(self):
        return f"{self.get_day()}, {self.get_month()}, {self.get_year()}, {self.get_tasks()}"

# ------------------------------------------------
'''
>>> today = Date(2025, 9, 24)
>>> today
Date(2025,9,24)
>>> today.year
2025
>>> print(today)
24th of Sep, 2025
>>> todo = CalendarEntry(2025, 9, 24)
>>> t = Time(10,0)
>>> str(t)
'10:00'
>>> todo.addTask('PPL lecture', t, Time(13,0))
>>> todo.addTask('PPL homework#4', Time(14,0), Time(16,0))
>>> todo.tasks
{('14:00', '16:00'): 'PPL homework#4', ('10:00', '13:00'): 'PPL lecture'} #we weren't given accurate instructions on whether overlap is legal... 
>>> print(todo)
Todo list for 24th of Sep, 2025 :
1. 10:00 - 13:00 - PPL lecture
2. 14:00 - 16:00 - PPL homework#4
'''

# ------------------------------------------------
# Q2 - Shmython(Object System)
# ------------------------------------------------
def make_class(attrs, base=None):
    """Return a new class (a dispatch dictionary) with given class attributes"""
    def get(name):
        if name in attrs:
            return attrs[name]
        elif base is not None: #added is not None.
            return base['get'](name)
    def set(name, value):
        attrs[name] = value
    def new(*args):
        attrs = {} #object attributes.

        def get(name):
            if name in attrs:
                return attrs[name]
            else:
                value = cls['get'](name)
                if callable(value):
                    return lambda *args: value(obj, *args) #the new method's attributes.
                else:
                    return value

        # Setter: instance attribute (always sets in object)
        def set(name, value):
            attrs[name] = value

        # instance dictionary
        obj = {'get': get, 'set': set}

        # calls constructor if present
        init = get('__init__')
        if init: init(*args)

        return obj

    # class dictionary
    cls = {'get': get, 'set': set, 'new': new}
    return cls

# ------------------------------------------------
def make_date_class():
    def __init__(self,year,month,day):
        self['set']('year',year)
        self['set']('month', month)
        self['set']('day', day)

    def __str__(self):

        match self['get']('month'):
            case 1:
                m = "january"
            case 2:
                m = "february"
            case 3:
                m = "march"
            case 4:
                m = "april"
            case 5:
                m = "may"
            case 6:
                m = "june"
            case 7:
                m = "july"
            case 8:
                m = "august"
            case 9:
                m = "september"
            case 10:
                m = "october"
            case 11:
                m = "november"
            case 12:
                m = "december"

        return f"{self['get']('day')}th of {m}, {self['get']('year')}."

    return make_class({'__init__':__init__, '__str__':__str__})

Date1 = make_date_class()

# ------------------------------------------------
def make_calentry_class():
    def __init__(self, year , month, day):
        self['set']('date', Date1['new'](year, month, day))
        self['set']('tasks', {})

    def addTask(self, name, t1, t2):
        self['get']('tasks')[(t1['get']('__str__')(), t2['get']('__str__')())] = name

    return make_class({'__init__': __init__, 'addTask': addTask})

CalendarEntry1 = make_calentry_class()


# ------------------------------------------------

def make_time_class():
    def __init__(self, minutes, hours):
        self['set']('minutes',minutes)
        self['set']('hours', hours)

    def __str__(self):
        return f"{self['get']('minutes'):02} : {self['get']('hours'):02}"

    return make_class({'__init__':__init__, '__str__':__str__})
Time1 = make_time_class()
# ------------------------------------------------
'''
>>> today = Date1['new'](2025, 9, 24)
>>> today['get']('__str__')()
'24th of Sep, 2025'
>>> today['get']('year')
2025
>>> todo = CalendarEntry1['new'](2025, 9, 24)
>>> t = Time1['new'](10,0)
>>> t['get']('__str__')()
'10:00'
>>> todo['get']('addTask')('PPL lecture', t, Time1['new'](13,0))
>>> todo['get']('addTask')('PPL homework#4', Time1['new'](14,0), Time1['new'](16,0))
>>> todo['get']('tasks')
{('10:00', '13:00'): 'PPL lecture', ('14:00', '16:00'): 'PPL homework#4'}
'''


# ------------------------------------------------
# Q3 - Shmython (Object System)
# ------------------------------------------------
def make_class1(attrs, base=None):
    """Return a new class (a dispatch dictionary) with given class attributes"""

    def get(name):
        if name in attrs:
            return attrs[name]
        elif base:
            return base['get'](name)

    def set(name, value):
        attrs[name] = value

    def new(*args):
        attrs = {}

        def get(name):
            if name in attrs:
                return attrs[name]
            else:
                value = cls['get'](name)
                if callable(value):
                    return lambda *args: value(obj, *args)
                else:
                    return value

        # Setter: instance attribute (always sets in object)
        def set(name, value):
            attrs[name] = value

        # instance dictionary
        obj = {'get': get, 'set': set}

        # calls constructor if present
        init = get('__init__')
        if init: init(*args)

        return obj

    # class dictionary
    cls = {'get': get, 'set': set, 'new': new}#, 'copy' : copy
    return cls


# ------------------------------------------------
def make_account_class():
    def init(self, owner):
        self['set']('owner', owner)
        self['set']('balance', 0)

    #def init(self, owner, other):

    def copy(other):
        if isinstance(other):
            #creating a new object of class - 'make_account_class' - type, and copying all obj - attributes.
            temp_acc = Account['new'](other['get']('owner'))
            temp_acc['set']('balance', other['get']('balance'))
            return temp_acc
        else:
            print("not an instance of Account class")

    def isinstanceof(obj):
        if not isinstance(obj, dict) or 'get' not in obj:# checking whether 'obj' has the 'get' instance - attribute,
            #or an attributes-dictionary in and by itself as a quick - entrance-check.
            #ngl: GPT recommended checking this way, even though my original idea was integrating the built-in python isinstanceof - method,
            #but these classes don't have that same isinstanceof attribute, and all objects do contain some other 'checkable' data we can -
            #work with like the get/set instance attributes, or the class's attributes: 'copy' / 'balance'.
            return False

        try:
            obj['get']('owner')   #}checking for instance attributes.
            obj['get']('balance') #}

        except KeyError: #google says this is used for keys-in-a-dictionary Error raising:
            return False

        return 'copy' in Account and callable(Account['get']('copy')) #the class has a 'copy' key within it's -
        #methods-dictionary, and: 'copy' is actually callable, meaning it's a well-defined - 'method' within our class.

    return make_class1({'__init__': init, 'interest': 0.03, 'copy': copy, 'isinstanceof' : isinstanceof})


Account = make_account_class()
# ------------------------------------------------
'''
>>> acc1 = Account['new']('Bob')
>>> acc1['set']('bank','Leumi')
>>> acc1['get']('owner')
'Bob'
>>> acc1['get']('balance')
0
>>> acc2 = Account['copy']( acc1 ) #this type of copy method - 
#initiation requires - copy to be a
>>> acc2['get']('owner')
'Bob'
>>> acc2['set']('owner','Jim')
>>> acc1['get']('owner')
'Bob'
>>> acc2['get']('owner')
'Jim'
>>> acc2['set']('balance',100)
>>> acc1['get']('balance')
0
>>> acc2['get']('balance')
100
>>> acc2['set']('bank','Discount')
>>> acc1['get']('bank')
'Leumi'
>>> acc2['get']('bank')
'Discount'
'''


# ------------------------------------------------
# Q4 - Generic Functions
# ------------------------------------------------
class Hours(object):
    pass


# ------------------------------------------------
class Days(object):
    pass


# ------------------------------------------------
class Weeks(object):
    pass


# ------------------------------------------------
##############################
# Tag-based type dispatching #
##############################

def type_tag(x):
    """Return the tag associated with the type of x."""
    return type_tag.tags[type(x)]


type_tag.tags = {}


def apply(operator_name, x, y):
    """Apply an operation ('add' or 'sub') to x and y."""
    tags = (type_tag(x), type_tag(y))
    key = (operator_name, tags)
    return apply.implementations[key](x, y)


apply.implementations = {}

# ------------------------------------------------
'''
>>> h1, d1, w1 = Hours( 14 ), Days( 1 ), w1 = Weeks( 2 )
>>> h1.value
14
>>> h1
Hours(14)
>>> d1
Days(1)
>>> str( d1 )
'1 day'
>>> w1
Weeks(2)
>>> str( w1 )
'2 weeks'
>>> apply('add',Hours(1),Days(2))
Hours(49)
>>> apply('add',Days(2),Hours(48))
Days(4)
>>> apply('add',Weeks(2),Days(5))
Days(19)
>>> apply('add',Weeks(2),Hours(5))
Hours(341)
>>> apply('sub',Hours(1),Days(2))
Hours(47)
>>> apply('sub',Days(2),Hours(72))
Days(1)
>>> apply('sub',Weeks(2),Days(5))
Days(9)'''
# ------------------------------------------------
############
# Coercion #
############


coercions = {}


def coerce_apply(operator_name, x, y):
    """Apply an operation ('add' or 'sub') to x and y."""
    tx, ty = type_tag(x), type_tag(y)
    if tx != ty:
        if (tx, ty) in coercions:
            tx, x = ty, coercions[(tx, ty)](x)
        elif (ty, tx) in coercions:
            ty, y = tx, coercions[(ty, tx)](y)
        else:
            return 'No coercion possible.'
    assert tx == ty
    key = (operator_name, tx)
    return coerce_apply.implementations[key](x, y)


coerce_apply.implementations = {}

# ------------------------------------------------
'''
>>> coerce_apply('add',Hours(1),Days(2))
Hours(49)
>>> coerce_apply('add',Days(2),Hours(48))
Hours(96)
>>> coerce_apply('add',Weeks(2),Days(5))
Days(19)
>>> coerce_apply('add',Weeks(2),Hours(5))
Hours(341)
>>> coerce_apply('sub',Hours(1),Days(2))
Hours(47)
>>> coerce_apply('sub',Days(2),Hours(72))
Hours(24)
>>> coerce_apply('sub',Weeks(2),Days(5))
Days(9)
'''


# ------------------------------------------------
# Q5 - Exceptions
# ------------------------------------------------
def fill_list(*argv):
    pass


# ------------------------------------------------
'''
>>> fill_list()
ValueError : Incorrect number of arguments
'Fatal function error'
>>> fill_list(1,2,3,4,5,6)
ValueError : Incorrect number of arguments
'Fatal function error'
>>> fill_list(-3.5,'Python')
TypeError : The first parameter must be positive and integer number
TypeError : The second parameter must be tuple or list
TypeError : Parameters error
'Fatal function error'
>>> fill_list(4,'Python')
TypeError : The second parameter must be tuple or list
TypeError : Parameters error
'Fatal function error'
>>> fill_list(4,((1,2,3),[2,3],(7,8),18))
< Sequence element: (1, 2, 3) >, ValueError : Sequence element must be pair
< Index: 7 >, IndexError : list index out of range
< Sequence element: 18 >, TypeError : Sequence element must be tuple or list
AssertionError : The list is not complete
[None, None, None, None]
>>> fill_list(4,((3,5),(-1,10),(1,15),(2,20),(0,25)))
< Index: -1 >, IndexError : The place is busy
[25, 15, 20, 5]
'''


# ------------------------------------------------
# Q6 - Recursive Data Structures
# ------------------------------------------------
class Tree():
    def __init__(self, value, nodes=None):
        self.value = value
        self.nodes = nodes

    def __repr__(self):
        if self.nodes:
            return 'Tree({0},{1})'.format(self.value, repr(self.nodes))
        return 'Tree({0})'.format(self.value)


def BuildTree(tree):
    pass


# ------------------------------------------------
def is_AVL_tree(tree):
    pass


# ------------------------------------------------
'''
>>> t1 = BuildTree((((1,2), 3), (4, (5, 6))))
>>> t1
Tree(3,[Tree(2,[Tree(1,[Tree(1), Tree(2)]), Tree(3)]), Tree(2,[Tree(4), Tree(1,[Tree(5), Tree(6)])])])
>>> is_AVL_tree( t1 )
True
>>> t2 = BuildTree(((2, 3), (4, (5, 6, (8, 2)))))
>>> t2
Tree(4,[Tree(1,[Tree(2), Tree(3)]), Tree(3,[Tree(4), Tree(2,[Tree(5), Tree(6), Tree(1,[Tree(8), Tree(2)])])])])
>>> is_AVL_tree(t2)
False
>>> t3 = BuildTree((((19,1,6), (1,(2,3))), (((1,2),6), (5, 6, (8, 2)))))
>>> t3
Tree(4,[Tree(3,[Tree(1,[Tree(19), Tree(1), Tree(6)]), Tree(2,[Tree(1), Tree(1,[Tree(2), Tree(3)])])]), Tree(3,[Tree(2,[Tree(1,[Tree(1), Tree(2)]), Tree(6)]), Tree(2,[Tree(5), Tree(6), Tree(1,[Tree(8), Tree(2)])])])])
>>> is_AVL_tree( t3 )
True
>>> '''

# ------------------------------------------------
# Q7 - Interpreter
# ------------------------------------------------
from functools import reduce
from operator import mul, add


def read_eval_print_loop():
    """Run a read-eval-print loop for calculator."""
    while True:
        try:
            expression_tree = calc_parse(input('calc> '))
            print(calc_eval(expression_tree))
        except (SyntaxError, TypeError, ZeroDivisionError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):  # <Control>-D, etc. <ctrl-C>
            print('Calculation completed.')
            return


# Eval & Apply

class Exp(object):
    """A call expression in Calculator. """

    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

    def __repr__(self):
        return 'Exp({0}, {1})'.format(repr(self.operator), repr(self.operands))

    def __str__(self):
        operand_strs = ', '.join(map(str, self.operands))
        return '{0}({1})'.format(self.operator, operand_strs)


def calc_eval(exp):
    """Evaluate a Calculator expression."""
    if type(exp) in (int, float):
        return exp
    if type(exp) == Exp:
        arguments = list(map(calc_eval, exp.operands))
        return calc_apply(exp.operator, arguments)


def calc_apply(operator, args):
    """Apply the named operator to a list of args."""
    if operator in ('add', '+'):
        return sum(args)
    if operator in ('sub', '-'):
        if len(args) == 0:
            raise TypeError(operator + 'requires at least 1 argument')
        if len(args) == 1:
            return -args[0]
        return sum(args[:1] + [-arg for arg in args[1:]])
    if operator in ('mul', '*'):
        return reduce(mul, args, 1)
    if operator in ('div', '/'):
        if len(args) != 2:
            raise TypeError(operator + ' requires exactly 2 arguments')
        numer, denom = args
        return numer / denom


# Parsing

def calc_parse(line):
    """Parse a line of calculator input and return an expression tree."""
    tokens = tokenize(line)
    expression_tree = analyze(tokens)
    if len(tokens) > 0:
        raise SyntaxError('Extra token(s): ' + ' '.join(tokens))
    return expression_tree


def tokenize(line):
    """Convert a string into a list of tokens."""
    spaced = line.replace('(', ' ( ').replace(')', ' ) ').replace(',', ' , ')
    return spaced.strip().split()


known_operators = ['add', 'sub', 'mul', 'div', '+', '-', '*', '/']


def analyze(tokens):
    """Create a tree of nested lists from a sequence of tokens."""
    assert_non_empty(tokens)
    token = analyze_token(tokens.pop(0))
    if type(token) in (int, float):
        return token
    if token in known_operators:
        if len(tokens) == 0 or tokens.pop(0) != '(':
            raise SyntaxError('expected ( after ' + token)
        return Exp(token, analyze_operands(tokens))
    else:
        raise SyntaxError('unexpected ' + token)


def analyze_operands(tokens):
    """Analyze a sequence of comma-separated operands."""
    assert_non_empty(tokens)
    operands = []
    while tokens[0] != ')':
        if operands and tokens.pop(0) != ',':
            raise SyntaxError('expected ,')
        operands.append(analyze(tokens))
        assert_non_empty(tokens)
    tokens.pop(0)  # Remove )
    return operands


def assert_non_empty(tokens):
    """Raise an exception if tokens is empty."""
    if len(tokens) == 0:
        raise SyntaxError('unexpected end of line')


def analyze_token(token):
    """Return the value of token if it can be analyzed as a number, or token."""
    try:
        return int(token)
    except (TypeError, ValueError):
        try:
            return float(token)
        except (TypeError, ValueError):
            return token


def run():
    read_eval_print_loop()


# ---------------------- a -----------------------
'''
calc> round(div(2,3),2)
0.67
calc> round(div(4,3))
TypeError: round requires exactly 2 arguments
calc> round(div(4,3),3.5)
TypeError: round A second parameter must be integer
'''
# ---------------------- b -----------------------
'''
calc> sumeven(12345,567)
TypeError: sumeven requires exactly 1 argument
calc> sumodd(12.345)
ValueError: sumodd require positive and integer argument
calc> sumeven(-12345)
ValueError: sumeven require positive and integer argument
calc> sumeven(12345)
6
calc> mul(sumeven(12345),sumodd(3456))
48
'''


# ------------------------------------------------
# driver
# ------------------------------------------------
def driver():
    """
    print('<<< Q1 >>>')
    today = Date(2025, 9, 24)
    print(repr(today))
    print(today.year)
    print(today)
    todo = CalendarEntry(2025, 9, 24)
    t = Time(10, 0)
    print(str(t))
    todo.addTask('PPL lecture', t, Time(13, 0))
    todo.addTask('PPL homework#4', Time(14, 0), Time(16, 0))
    print(todo.tasks)
    print()
    print(todo)
    """
    """
    print('<<< Q2 >>>')
    today = Date1['new'](2025, 9, 24)
    print(today['get']('__str__')())
    print(today['get']('year'))
    
    todo = CalendarEntry1['new'](2025, 9, 24)
    t = Time1['new'](10, 0)
    print(t['get']('__str__')())
    todo['get']('addTask')('PPL lecture', t, Time1['new'](13, 0))
    todo['get']('addTask')('PPL homework#4', Time1['new'](14, 0), Time1['new'](16, 0))
    print(todo['get']('tasks'))
    """
    #"""
    print('<<< Q3 >>>')
    acc1 = Account['new']('Bob')
    acc1['set']('bank', 'Leumi')
    print(acc1['get']('owner'), end=', ')
    print(acc1['get']('balance'), end=', ')
    acc2 = Account['copy'](acc1)
    print(acc2['get']('owner'), end=', ')
    acc2['set']('owner', 'Jim')
    print(acc1['get']('owner'), end=', ')
    print(acc2['get']('owner'), end=', ')
    acc2['set']('balance', 100)
    print(acc1['get']('balance'), end=', ')
    print(acc2['get']('balance'), end=', ')
    acc2['set']('bank', 'Discount')
    print(acc1['get']('bank'), end=', ')
    print(acc2['get']('bank'))
    #"""
    """
    print('<<< Q4 >>>')
    h1, d1, w1 = Hours(14), Days(1), Weeks(2)
    print(h1.value, end=', ')
    print(repr(h1))
    print(repr(d1), end=', ')
    print(str(d1))
    print(repr(w1), end=', ')
    print(str(w1))
    print(repr(apply('add', Hours(1), Days(2))), end=', ')
    print(repr(apply('add', Days(2), Hours(48))), end=', ')
    print(repr(apply('add', Weeks(2), Days(5))), end=', ')
    print(repr(apply('add', Weeks(2), Hours(5))), end=', ')
    print(repr(apply('sub', Hours(1), Days(2))), end=', ')
    print(repr(apply('sub', Days(2), Hours(72))), end=', ')
    print(repr(apply('sub', Weeks(2), Days(5))))
    print(repr(coerce_apply('add', Hours(1), Days(2))), end=', ')
    print(repr(coerce_apply('add', Days(2), Hours(48))), end=', ')
    print(repr(coerce_apply('add', Weeks(2), Days(5))), end=', ')
    print(repr(coerce_apply('add', Weeks(2), Hours(5))), end=', ')
    print(repr(coerce_apply('sub', Hours(1), Days(2))), end=', ')
    print(repr(coerce_apply('sub', Days(2), Hours(72))), end=', ')
    print(repr(coerce_apply('sub', Weeks(2), Days(5))))
    """
    """
    print('<<< Q5 >>>')
    print(fill_list())
    print(fill_list(1, 2, 3, 4, 5, 6))
    print(fill_list(-3.5, 'Python'))
    print(fill_list(4, 'Python'))
    print(fill_list(4, ((1, 2, 3), [2, 3], (7, 8), 18)))
    print(fill_list(4, ((3, 5), (-1, 10), (1, 15), (2, 20), (0, 25))))
    """
    """
    print('<<< Q6 >>>')
    t1 = BuildTree((((1, 2), 3), (4, (5, 6))))
    print(repr(t1))
    print(is_AVL_tree(t1))
    t2 = BuildTree(((2, 3), (4, (5, 6, (8, 2)))))
    print(repr(t2))
    print(is_AVL_tree(t2))
    t3 = BuildTree((((19, 1, 6), (1, (2, 3))), (((1, 2), 6), (5, 6, (8, 2)))))
    print(repr(t3))
    print(is_AVL_tree(t3))
    """
# ------------------------------------------------
'''
<<< Q1 >>>
Date(2025,9,24)
2025
24th of Sep, 2025
10:00
{('14:00', '16:00'): 'PPL homework#4', ('10:00', '13:00'): 'PPL lecture'}
Todo list for 24th of Sep, 2025 :
1. 10:00 - 13:00 - PPL lecture
2. 14:00 - 16:00 - PPL homework#4

<<< Q2 >>>
24th of Sep, 2025
2025
10:00
{('10:00', '13:00'): 'PPL lecture', ('14:00', '16:00'): 'PPL homework#4'}
<<< Q3 >>>
Bob, 0, Bob, Bob, Jim, 0, 100, Leumi, Discount
<<< Q4 >>>
14, Hours(14)
Days(1), 1 day
Weeks(2), 2 weeks
Hours(49), Days(4), Days(19), Hours(341), Hours(47), Days(1), Days(9)
Hours(49), Hours(96), Days(19), Hours(341), Hours(47), Hours(24), Days(9)
<<< Q5 >>>
ValueError : Incorrect number of arguments
Fatal function error
ValueError : Incorrect number of arguments
Fatal function error
TypeError : The first parameter must be positive and integer number
TypeError : The second parameter must be tuple or list
TypeError : Parameters error
Fatal function error
TypeError : The second parameter must be tuple or list
TypeError : Parameters error
Fatal function error
< Sequence element: (1, 2, 3) >, ValueError : Sequence element must be pair
< Index: 7 >, IndexError : list index out of range
< Sequence element: 18 >, TypeError : Sequence element must be tuple or list
AssertionError : The list is not complete
[None, None, None, None]
< Index: -1 >, IndexError : The place is busy
[25, 15, 20, 5]
<<< Q6 >>>
Tree(3,[Tree(2,[Tree(1,[Tree(1), Tree(2)]), Tree(3)]), Tree(2,[Tree(4), Tree(1,[Tree(5), Tree(6)])])])
True
Tree(4,[Tree(1,[Tree(2), Tree(3)]), Tree(3,[Tree(4), Tree(2,[Tree(5), Tree(6), Tree(1,[Tree(8), Tree(2)])])])])
False
Tree(4,[Tree(3,[Tree(1,[Tree(19), Tree(1), Tree(6)]), Tree(2,[Tree(1), Tree(1,[Tree(2), Tree(3)])])]), Tree(3,[Tree(2,[Tree(1,[Tree(1), Tree(2)]), Tree(6)]), Tree(2,[Tree(5), Tree(6), Tree(1,[Tree(8), Tree(2)])])])])
True
'''
driver()
