# --------------------------------------
# Instance Implementation 
# --------------------------------------
def make_instance(cls):
    """Return a new object instance, which is a dispatch dictionary."""
    attributes = {}
    def get_value(name):
        if name in attributes:
            return attributes[name]
        else:
            value = cls['get'](name)
        return bind_method(value, instance)
    def set_value(name, value):
        attributes[name] = value
    instance = {'get': get_value, 'set': set_value}
    return instance

# --------------------------------------
# Bound method values 
# --------------------------------------
def bind_method(value, instance):
    """Return a bound method if value is callable, or value otherwise."""
    if callable(value):
        def method(*args):
            return value(instance, *args)
        return method
    else:
        return value

# --------------------------------------
# Class implementation 
# --------------------------------------
def make_class(attributes, base_class=None):
    """Return a new class, which is a dispatch dictionary."""
    def get_value(name):
        if name in attributes:
            return attributes[name]
        elif base_class is not None:
            return base_class['get'](name)
    def set_value(name, value):
        attributes[name] = value
    def new(*args):
        return init_instance(cls, *args)
    cls = {'get': get_value, 'set': set_value, 'new': new}
    return cls

# --------------------------------------
# Initialization 
# --------------------------------------
def init_instance(cls, *args):
    """Return a new object with type cls, initialized with args."""
    instance = make_instance(cls)
    init = cls['get']('__init__')
    if init:
        init(instance, *args)
    return instance

# --------------------------------------
# Using Implemented Objects 
# --------------------------------------
def make_account_class():
    """Return the Account class, which has deposit and withdraw methods."""
    def __init__(self, account_holder):
        self['set']('holder', account_holder)
        self['set']('balance', 0)
    def deposit(self, amount):
        """Increase the account balance by amount and return the new balance."""
        new_balance = self['get']('balance') + amount
        self['set']('balance', new_balance)
        return self['get']('balance')
    def withdraw(self, amount):
        """Decrease the account balance by amount and return the new balance."""
        balance = self['get']('balance')
        if amount > balance:
            return 'Insufficient funds'
        self['set']('balance', balance - amount)
        return self['get']('balance')
    return make_class({'__init__': __init__, 'deposit': deposit,
                       'withdraw': withdraw, 'interest': 0.02})

# --------------------------------------

Account = make_account_class()
jim_acct = Account['new']('Jim')
print(jim_acct['get']('interest'))
#0.02
print(jim_acct['get']('deposit')(20))
#20
print(jim_acct['get']('withdraw')(5))
#15
jim_acct['set']('interest', 0.04)
print(Account['get']('interest'))

# --------------------------------------
# Inheritance: creating a subclass 
# --------------------------------------
def make_checking_account_class():
    """Return the CheckingAccount class, which imposes a $1 withdrawal fee."""
    def withdraw(self, amount):
        return Account['get']('withdraw')(self, amount + 1)
    return make_class({'withdraw': withdraw, 'interest': 0.01}, Account)
# --------------------------------------
'''
>>> Account = make_account_class()
>>> CheckingAccount = make_checking_account_class()
>>> jack_acct = CheckingAccount['new']('Jack')
>>> jack_acct['get']('interest')
0.01
>>> jack_acct['get']('deposit')(20)
20
>>> jack_acct['get']('withdraw')(5)
14
'''


# --------------------------------------
# Class implementation 
# --------------------------------------
'''
def make_class(attrs, base=None):
    """Return a new class (a dispatch dictionary) with given class attributes"""
    #print(attrs)
    # Getter: class attribute (looks in this class, then base)
    def get(name):
        if name in attrs: return attrs[name]
        elif base:        return base['get'](name)

    # Setter: class attribute (always sets in this class)
    def set(name, value): attrs[name] = value

    # Return a new initialized objec'aaa': 5.5t instance (a dispatch dictionary)
    def new(*args):
        # instance attributes (hides encapsulating function's attrs)
        attrs = {}

        # Getter: instance attribute (looks in object, then class (binds self if callable))
        def get(name):
            if name in attrs:       return attrs[name]
            else:
                value = cls['get'](name)
                if callable(value): return lambda *args: value(obj, *args)
                else:               return value

        # Setter: instance attribute (always sets in object)
        def set(name, value):       attrs[name] = value

        # instance dictionary
        obj = { 'get': get, 'set': set }

        # calls constructor if present
        init = get('__init__')
        if init: init(*args)

        return obj

    # class dictionary
    cls = { 'get': get, 'set': set, 'new': new }
    return cls
'''
