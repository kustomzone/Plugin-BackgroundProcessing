import importlib

class Scope(object):
    def __init__(self, inherits=None):
        self.vars = {}
        self.inherits = inherits
        self.inheritsVariable = {}

    def import_(self, names, from_, level):
        for name, asname in names:
            if asname is None:
                asname = name

            if from_ is not None:
                line = "from %s import %s as import_module" % (from_, name)
            else:
                line = "import %s as import_module" % name

            exec compile(line, "<import>", "single")
            self[asname] = import_module
            del import_module


    def __getitem__(self, name):
        if name in self.inheritsVariable:
            scope = self.inheritsVariable[name]
            return scope[name]
        if name in self.vars:
            return self.vars[name]
        if self.inherits is not None:
            return self.inherits[name] # Recursive: type(inherits)==Scope

        raise NameError(name)

    def __setitem__(self, name, value):
        if name in self.inheritsVariable:
            scope = self.inheritsVariable[name]
            scope[name] = value
            return

        self.vars[name] = value


    def inherit(self):
        return Scope(self)
    def inheritVariable(self, scope, name):
        self.inheritsVariable[name] = scope




# Fill scope (usually scope0) with default variables
def populateScope(scope):
    # Exceptions
    import exceptions
    for name in vars(exceptions):
        scope[name] = getattr(exceptions, name)

    # Built-in constants
    scope["False"] = False
    scope["True"] = True
    scope["None"] = None
    scope["NotImplemented"] = NotImplemented
    scope["Ellipsis"] = Ellipsis