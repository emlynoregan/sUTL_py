from jsonpath import jsonpath

def builtins():
    def pathF(parentscope, scope, l, src, tt, b):
            fullpath = scope.get("path", "")

            prefix = fullpath[:1]
            path = fullpath[1:]
            childscope = None

            if prefix == '@':
                childscope = parentscope
            elif prefix == '^':
                childscope = scope # is this even a thing?
            elif prefix == '*':
                childscope = l
            elif prefix == '$':
                childscope = src
            elif prefix == '~':
                childscope = tt

            if childscope:
                if path and not path[0] == ".":
                    path = "$.%s" % path
                else:
                    path = "$%s" % path

                if path == "$":
                    retval = [childscope]
                else:
                    retval = jsonpath(childscope, path, use_eval=False)
                return retval
#                retval = [lmatch.value for lmatch in parse(path).find(childscope)]
#                 return retval if retval else []
            else:
                return []
    
    def ifF(parentscope, scope, l, src, tt, b):
        retval = None
        condvalue = False;

        if "cond" in scope:
            condvalue = _evaluate(parentscope, scope["cond"], l, src, tt, b)

        if condvalue:
            if "true" in scope:
                retval = _evaluate(parentscope, scope["true"], l, src, tt, b)
        else:
            if "false" in scope:
                retval = _evaluate(parentscope, scope["false"], l, src, tt, b)

        return retval
    
    def keysF(parentscope, scope, l, src, tt, b):
        obj = scope.get("map")
        if isObject(obj):
            return obj.keys()
        else:
            return None

    def valuesF(parentscope, scope, l, src, tt, b):
        obj = scope.get("map")
        if isObject(obj):
            return obj.values()
        else:
            return None

    def typeF(parentscope, scope, l, src, tt, b):
        item = scope.get("value")
        if isObject(item):
            return u"map"
        elif isArray(item):
            return u"list"
        elif isString(item):
            return u"string"
        elif isNumber(item):
            return u"number"
        elif isBool(item):
            return u"boolean"
        elif item is None:
            return u"null"
        else:
            return u"unknown"
        
    def makemapF(parentscope, scope, l, src, tt, b):
        retval = {}
        item = scope.get("value")
        if isArray(item):
            retval = { entry[0]: entry[1] for entry in item if isArray(entry) and len(entry) >= 2 and isString(entry[0]) } 
            return retval
        
    def getBinOpF(iF, jF, aDoOpF):
        def OpF(parentscope, scope, l, src, tt, b):
            try:
                i = iF(scope)
                j = jF(scope)
                retval = aDoOpF(i, j)
            except Exception, ex:
                print ex
                retval = None
            return retval
        return OpF

    def getUnOpF(iF, aDoOpF):
        def OpF(parentscope, scope, l, src, tt, b):
            try:
                i = iF(scope)
                retval = aDoOpF(i)
            except Exception, ex:
                print ex
                retval = None
            return retval
        return OpF

    retval = {
        "path": pathF,
        "+": getBinOpF(lambda scope: scope.get("a", 0), lambda scope: scope.get("b", 0), lambda i, j: i + j),
        "-": getBinOpF(lambda scope: scope.get("a", 0), lambda scope: scope.get("b", 0), lambda i, j: i - j),
        "*": getBinOpF(lambda scope: scope.get("a", 1), lambda scope: scope.get("b", 1), lambda i, j: i * j),
        "/": getBinOpF(lambda scope: scope.get("a", 1), lambda scope: scope.get("b", 1), lambda i, j: i / j),
        "=": getBinOpF(lambda scope: scope.get("a", 0), lambda scope: scope.get("b", 0), lambda i, j: type(i) == type(j) and i == j),
        "!=": getBinOpF(lambda scope: scope.get("a", 0), lambda scope: scope.get("b", 0), lambda i, j: type(i) != type(j) or i != j),
        ">=": getBinOpF(lambda scope: scope.get("a", 0), lambda scope: scope.get("b", 0), lambda i, j: i >= j),
        "<=": getBinOpF(lambda scope: scope.get("a", 0), lambda scope: scope.get("b", 0), lambda i, j: i <= j),
        ">": getBinOpF(lambda scope: scope.get("a", 0), lambda scope: scope.get("b", 0), lambda i, j: i > j),
        "<": getBinOpF(lambda scope: scope.get("a", 0), lambda scope: scope.get("b", 0), lambda i, j: i < j),
        "&&": getBinOpF(lambda scope: scope.get("a", True), lambda scope: scope.get("b", True), lambda i, j: i and j),
        "||": getBinOpF(lambda scope: scope.get("a", False), lambda scope: scope.get("b", False), lambda i, j: i or j),
        "!": getUnOpF(lambda scope: scope.get("a", False), lambda i: not i),
        "if": ifF,
        "keys": keysF,
        "values": valuesF,
        "type": typeF,
        "makemap": makemapF
    }
    
    retval.update(
        {"has%s" % key: lambda(parentscope, scope, l, src, tt, b): True for key in retval.keys()}
    )
    
    return retval

def evaluate(src, tt, l):
    return _evaluate(src, tt, l, src, tt, builtins())

def _evaluate(s, t, l, src, tt, b):
    if isEval(t):
        retval = _evaluateEval(s, t, l, src, tt, b)
    elif isBuiltinEval(t):
        retval = _evaluateBuiltin(s, t, l, src, tt, b)
    elif isQuoteEval(t):
        retval = _quoteEvaluate(s, t.get("'"), l, src, tt, b)
    elif isColonEval(t):
        retval = t.get(":")
    elif isDictTransform(t):
        retval = _evaluateDict(s, t, l, src, tt, b)
    elif isListTransform(t):
        if len(t) > 0 and t[0] == "&&":
            retval = _flatten(_evaluateList(s, t[1:], l, src, tt, b))
        else:
            retval = _evaluateList(s, t, l, src, tt, b)
    elif isPathTransform(t):
        retval = _evaluatePath(s, t[2:], l, src, tt, b)
    elif isPathHeadTransform(t):
        retval = _evaluatePathHead(s, t[1:], l, src, tt, b)
    else:
        retval = t # simple transform
    return retval

def _quoteEvaluate(s, t, l, src, tt, b):
    if isDoubleQuoteEval(t):
        retval = _evaluate(s, t.get("''"), l, src, tt, b)
    elif isDictTransform(t):
        retval = _quoteEvaluateDict(s, t, l, src, tt, b)
    elif isListTransform(t):
        retval = _quoteEvaluateList(s, t, l, src, tt, b)
    else:
        retval = t # simple transform
    return retval

def _evaluateBuiltin(s, t, l, src, tt, b):
    retval = None

    builtinf = b.get(t.get("&"))

    if builtinf:
        s2 = _evaluateDict(s, t, l, src, tt, b)

        l2 = _evaluateDict(s, t["*"], l, src, tt, b) if "*" in t else l

#         try:
        retval = builtinf(s, s2, l2, src, tt, b)
#         except Exception, ex:
#             retval = None # if the builtin fails, we just return None

    return retval

def _evaluateEval(s, t, l, src, tt, b):
    t2 = _evaluate(s, t.get("!"), l, src, tt, b)

    s2 = _evaluateDict(s, t, l, src, tt, b)

    l2 = _evaluateDict(s, t["*"], l, src, tt, b) if "*" in t else l

    return _evaluate(s2, t2, l2, src, tt, b)

def _evaluateDict(s, t, l, src, tt, b):
    retval = {
        key: _evaluate(s, t[key], l, src, tt, b) 
            for key in t.keys()
            if (key != "!") and (key != "&")
    } 
    return retval

def _quoteEvaluateDict(s, t, l, src, tt, b):
    retval = {
        key: _quoteEvaluate(s, t[key], l, src, tt, b) 
            for key in t.keys()
    } 
    return retval

def _evaluateList(s, t, l, src, tt, b):
    return [_evaluate(s, item, l, src, tt, b) for item in t]

def _quoteEvaluateList(s, t, l, src, tt, b):
    return [_quoteEvaluate(s, item, l, src, tt, b) for item in t]

def _evaluatePathHead(s, t, l, src, tt, b):
    resultlist = _evaluatePath(s, t, l, src, tt, b)

    return resultlist[0] if resultlist else None

def _evaluatePath(s, t, l, src, tt, b):
    path_t = {
        "&": "path",
        "path": t
    }

    return _evaluate(s, path_t, l, src, tt, b)

def _flatten(lst):
    lst2 = [item if isArray(item) else [item] for item in lst]
    return [item for sublist in lst2 for item in sublist]

def isBuiltinEval(obj):
    return isObject(obj) and "&" in obj

def isEval(obj): 
    return isObject(obj) and "!" in obj

def isQuoteEval(obj):
    return isObject(obj) and "'" in obj

def isDoubleQuoteEval(obj):
    return isObject(obj) and "''" in obj

def isColonEval(obj):
    return isObject(obj) and ":" in obj

def isDictTransform(obj):
    return isObject(obj)

def isListTransform(obj):
    return isArray(obj)

def isObject(obj):
    return isinstance(obj, dict)

def isArray(obj):
    return isinstance(obj, list)

def isString(obj):
    return isinstance(obj, basestring)

def isNumber(obj):
    return isinstance(obj, (int, float))

def isBool(obj):
    return isinstance(obj, bool)

def isPathHeadTransform(obj):
    return isString(obj) and obj[:1] == "#"

def isPathTransform(obj):
    return isString(obj) and obj[:2] == "##"

def compilelib(decls, dists, test):
    return _compilelib(decls, dists, {}, test, builtins())

def _compilelib(decls, dists, l, test, b):
    resultlib = {}
    resultlib.update(l) # start as a copy of the existing library

    # need to add recursive requirements into resultlib

    selfreqs = {
        decl.get("name", ""): decl.get("transform-t") 
            for decl in decls 
            for reqname in decl.get("requires", []) 
                if not reqname in l and isPrefix(reqname, decl.get("name", ""))
    }
                             
    resultlib.update(selfreqs)

    # construct list of names of all required decls not already in the library
    needreqs = [
        reqname 
            for decl in decls 
            for reqname in decl.get("requires", []) 
                if not reqname in l and not isPrefix(reqname, decl.get("name", ""))
    ]
    
    all_candidate_decls = { reqname: [] for reqname in needreqs }

    for reqname in needreqs:
        candidate_decls = [distdecl 
            for dist in dists 
            for distdecl in dist 
                if isPrefix(reqname, distdecl.get("name", ""))  
        ]
        
        all_candidate_decls[reqname].extend(candidate_decls)

    #here all_candidate_decls is a dict of candidate_decls by name in decl requires

    fails = []

    for reqname in all_candidate_decls:
        candidate_decls = all_candidate_decls[reqname]

        if candidate_decls:
            fails2total = []
            for candidate_decl in candidate_decls:
                clresult = _compilelib([candidate_decl], dists, resultlib, test, b)

                if "fail" in clresult:
                    fails2total.extend(clresult["fail"])
                elif "lib" in clresult:
                    fails2total = [] # not a fail

                    for libkey in clresult["lib"]:
                        resultlib[libkey] = clresult["lib"][libkey]

                    resultlib[reqname] = candidate_decl.get("transform-t")

            if fails2total:
                fails.extend(fails2total)

    # here resultlib contains everything we could find for reqnames

    if test:
        for decl in decls:
            declreq = {
                reqname: None for reqname in decl
            }
            
            # decllib is resultlib filtered by names in decl.requires
            decllib = { libkey: resultlib[libkey] for libkey in resultlib.keys() if libkey in declreq }
            
            # evaluate the test. If truthy, the test fails
            fail = evaluate(decl.get("transform-t"), decl.get("test-t"), decllib)
            if fail:
                fails.append(fail)

    if fails:
        return {"fail": fails}
    else:
        return {"lib": resultlib}


def isPrefix(str1, str2):
    return str2.startswith(str1)




