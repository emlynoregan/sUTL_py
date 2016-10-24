from copy import deepcopy
from string import split, strip

def _processPath(startfrom, parentscope, scope, l, src, tt, b):
    la = scope.get("a")
    lb = scope.get("b")
    lnotfirst = scope.get("notfirst")
    
    if lnotfirst:
        return _doPath(la, lb)
    else:
        laccum = _doPath([startfrom], la)
        return _doPath(laccum, lb)
    
def _doPath(a, b):
    retval = []
    
    if isArray(a):
        if not b is None and b != "":
            for litem in a:
                try:
                    if b == "**":
                        retval.append(litem)
                        lstack = [litem]
                        while lstack:
                            lstackItem = lstack.pop()
                            if isObject(lstackItem):
                                retval.extend(lstackItem.values())
                                lstack.extend(lstackItem.values())
                            elif isArray(lstackItem):
                                retval.extend(lstackItem)
                                lstack.extend(lstackItem)
                    elif b == "*":
                        if isObject(litem):
                            retval.extend(litem.values())
                        elif isArray(litem):
                            retval.extend(litem)
                    elif isObject(litem) and isString(b):
                        if b in litem:
                            retval.append(litem.get(b))
                    elif isArray(litem) and isNumber(b):
                        if b >= 0 and b < len(litem):
                            retval.append(litem[b])
                except:
                    pass # something bad happened, dump this one
        else:
            retval = a
    # else wtf? Just do nothing
    
    return retval

def builtins():
    
#     def pathF(parentscope, scope, l, src, tt, b):
#         '''
#         DEPRECATED
#         '''
#         fullpath = scope.get("path", "")
# 
#         prefix = fullpath[:1]
#         path = fullpath[1:]
#         childscope = None
# 
#         if prefix == '@':
#             childscope = parentscope
#         elif prefix == '^':
#             childscope = scope # is this even a thing?
#         elif prefix == '*':
#             childscope = l
#         elif prefix == '$':
#             childscope = src
#         elif prefix == '~':
#             childscope = tt
# 
#         if childscope:
#             if path and not path[0] == ".":
#                 path = "$.%s" % path
#             else:
#                 path = "$%s" % path
# 
#             if path == "$":
#                 retval = [childscope]
#             else:
#                 retval = jsonpath(childscope, path, use_eval=False)
#             return retval
#         else:
#             return []
    
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
    
    def zipF(parentscope, scope, l, src, tt, b):
        llist = scope.get("list")

        retval = deepcopy([list(item) for item in zip(*llist)])

        return retval

    def removeKeysF(parentscope, scope, l, src, tt, b):
        lmap = scope.get("map")
        lkeys = scope.get("keys")
        lkeys = lkeys if lkeys else []
        
        retval = None
        if lmap != None:
            retval = deepcopy(lmap)
            for lkey in lkeys:
                if lkey in retval:
                    del retval[lkey]

        return retval
    
    def sortF(parentscope, scope, l, src, tt, b):
        llist = scope.get("list")

        retval = sorted(llist) if llist else llist
 
        return retval
    
    def lenF(parentscope, scope, l, src, tt, b):
        obj = scope.get("list")
        if isArray(obj):
            return len(obj)
        else:
            return 0

    def keysF(parentscope, scope, l, src, tt, b):
        obj = scope.get("map")
        if isObject(obj):
            return [unicode(lkey) for lkey in obj.keys()]
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
        
    def andF(parentscope, scope, l, src, tt, b):
        a = scope.get("a")
        b = scope.get("b")
        
        if "a" in scope:
            if "b" in scope:
                return a and b
            else:
                return a
        else:
            return b

    def reduceF(parentscope, scope, l, src, tt, b):
        llist = scope.get("list")
        t = scope.get("t")
        accum = scope.get("accum")
        
        if isArray(llist):
            for ix, item in enumerate(llist):
                s2 = dict(parentscope)
                s2.update(scope)
                s2["item"] = item
                s2["accum"] = accum
                s2["ix"] = ix
                
                accum = _evaluate(s2, t, l, src, tt, b)
                
        return accum

    def rawPathingF(parentscope, scope, l, src, tt, b):
        a = scope.get("a")
        b = scope.get("b")
        notfirst = scope.get("notfirst")
        
        if notfirst:
            return _doPath(a, b)
        else:
            if a is None:
                return _doPath([b], None)
            else:
                return _doPath([a], b)
        
    def headF(parentscope, scope, l, src, tt, b):
        b = scope.get("b")

        if isArray(b):
            if len(b):
                return b[0]
            else:
                return None
            
    def tailF(parentscope, scope, l, src, tt, b):
        b = scope.get("b")

        if isArray(b):
            if len(b):
                return b[1:]
            else:
                return []

    def splitF(parentscope, scope, l, src, tt, b):
        lvalue = scope.get("value")
        lsep = scope.get("sep") 
        lmax = scope.get("max")

        if not lvalue:
            retval = None
        elif lmax and not isNumber(lmax):
            retval = None
        else:
            if not lsep:
                lsep = ","
            if lmax:
                retval = unicode(lvalue).split(unicode(lsep), lmax)
            else:
                retval = unicode(lvalue).split(unicode(lsep))

        return retval

    def trimF(parentscope, scope, l, src, tt, b):
        lvalue = scope.get("value")
        
        if not lvalue:
            retval = None
        else:
            retval = unicode(lvalue).strip()

        return retval

    def posF(parentscope, scope, l, src, tt, b):
        lvalue = scope.get("value")
        lsub = scope.get("sub")
        
        if not lvalue:
            retval = None
        elif not lsub:
            retval = None
        else:
            retval = unicode(lvalue).find(unicode(lsub))
        
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
        
    def Get(aDict, aKey, aDefault):
        retval = aDict.get(aKey)
        if retval is None:
            retval = aDefault
        return retval
    
    def DoEq(i, j):
#         print ("In Equals")
#         print (type(i))
#         print (i)
#         print (type(j))
#         print (j)
        retval = type(i) == type(j) and i == j
#         print retval
        return retval
    
    retval = {
#         "path": pathF,
        "+": getBinOpF(
            lambda scope: 
                Get(scope, "a", 0), 
            lambda scope: 
                Get(scope, "b", 0), 
            lambda i, j: i + j
        ),
        "-": getBinOpF(lambda scope: Get(scope, "a", 0), lambda scope: Get(scope, "b", 0), lambda i, j: i - j),
        "x": getBinOpF(lambda scope: Get(scope, "a", 1), lambda scope: Get(scope, "b", 1), lambda i, j: i * j),
        "/": getBinOpF(lambda scope: Get(scope, "a", 1), lambda scope: Get(scope, "b", 1), lambda i, j: i / j),
        "=": getBinOpF(lambda scope: Get(scope, "a", None), lambda scope: Get(scope, "b", None), lambda i, j: DoEq(i,j)),
        "!=": getBinOpF(lambda scope: Get(scope, "a", None), lambda scope: Get(scope, "b", None), lambda i, j: not (DoEq(i,j))),
        ">=": getBinOpF(lambda scope: Get(scope, "a", None), lambda scope: Get(scope, "b", None), lambda i, j: i >= j),
        "<=": getBinOpF(lambda scope: Get(scope, "a", None), lambda scope: Get(scope, "b", None), lambda i, j: i <= j),
        ">": getBinOpF(lambda scope: Get(scope, "a", None), lambda scope: Get(scope, "b", None), lambda i, j: i > j),
        "<": getBinOpF(lambda scope: Get(scope, "a", None), lambda scope: Get(scope, "b", None), lambda i, j: i < j),
        "&&": andF,
        "||": getBinOpF(lambda scope: Get(scope, "a", False), lambda scope: Get(scope, "b", False), lambda i, j: i or j),
        "!": getUnOpF(lambda scope: Get(scope, "b", False), lambda i: not i),
        "if": ifF,
        "zip": zipF,
        "removekeys": removeKeysF,
        "len": lenF,
        "keys": keysF,
        "values": valuesF,
        "type": typeF,
        "makemap": makemapF,
        "reduce": reduceF,
        "quicksort": sortF,
        "head": headF,
        "tail": tailF,
        "split": splitF,
        "trim": trimF,
        "pos": posF,
        "$": lambda parentscope, scope, l, src, tt, b: _processPath(src, parentscope, scope, l, src, tt, b),
        "@": lambda parentscope, scope, l, src, tt, b: _processPath(parentscope, parentscope, scope, l, src, tt, b),
        "^": lambda parentscope, scope, l, src, tt, b: _processPath(scope, parentscope, scope, l, src, tt, b),
        "*": lambda parentscope, scope, l, src, tt, b: _processPath(l, parentscope, scope, l, src, tt, b),
        "~": lambda parentscope, scope, l, src, tt, b: _processPath(tt, parentscope, scope, l, src, tt, b),
        "%": rawPathingF
    }
    
    retval.update(
        {u"has%s" % key: lambda parentscope, scope, l, src, tt, b: True for key in retval.keys()}
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
    elif isArrayBuiltinEval(t, b):
        retval = _evaluateArrayBuiltin(s, t, l, src, tt, b)
    elif isListTransform(t):
        if len(t) > 0 and t[0] == "&&":
            retval = _flatten(_evaluateList(s, t[1:], l, src, tt, b))
        else:
            retval = _evaluateList(s, t, l, src, tt, b)
    elif isStringBuiltinEval(t, b):
        retval = _evaluateStringBuiltin(s, t, l, src, tt, b)
#     elif isPathTransform(t):
#         retval = _evaluatePath(s, t[2:], l, src, tt, b)
#     elif isPathHeadTransform(t):
#         retval = _evaluatePathHead(s, t[1:], l, src, tt, b)
    else:
        if isinstance(t, str):
            retval = unicode(t)
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

def _getArrayBuiltinName(aOp):
    if len(aOp):
        return aOp[1:]
    else:
        return None

def _evaluateStringBuiltin(s, t, l, src, tt, b):
    arr = t.split(".")
    
    arr2 = []
    
    for item in arr:
        itemParsed = item
        try:
            itemParsed = int(item)
        except ValueError, _:
            pass # expected, just means it's a string
        arr2.append(itemParsed)

    return _evaluateArrayBuiltin(s, arr2, l, src, tt, b)
    
def _evaluateArrayBuiltin(s, t, l, src, tt, b):
    op = t[0]
    
    opChar = op[0]
    
    uset = {
      "&": _getArrayBuiltinName(op),
      "args": t[1:], 
#      "args": _evaluateList(s, t[1:], l, src, tt, b),
      "head": opChar == "^"
    }
    
    return _evaluateBuiltin(s, uset, l, src, tt, b)
    
def _evaluateBuiltin(s, t, l, src, tt, b):
    retval = None

    largs = t.get("args")
    if isArray(largs):
        if len(largs) == 0:
            uset = {
                "&": t.get("&")
            }
            
            retval = _evaluateBuiltin(s, uset, l, src, tt, b)
        elif len(largs) == 1:
            uset = {
                "&": t.get("&"),
                "b": _evaluate(s, largs[0], l, src, tt, b)
            }
            
            retval = _evaluateBuiltin(s, uset, l, src, tt, b)
        else:
            #2 or more items in the args list. Reduce over them
            llist = largs[1:]
            retval = _evaluate(s, largs[0], l, src, tt, b)
            for ix, item in enumerate(llist):
                uset = {
                    "&": t.get("&"),
                    "a": retval,
                    "b": _evaluate(s, item, l, src, tt, b),
                    "notfirst": ix > 0
                }
                
                retval = _evaluateBuiltin(s, uset, l, src, tt, b)
                
        if isArray(retval) and t.get("head"):
            if retval:
                retval = retval[0]
            else:
                retval = None
    else:
        builtinf = b.get(t.get("&"))
        if builtinf:
            llibname = "_override_%s" + t.get("&")
        else:
            llibname = t.get("&")
            
        if llibname in l:
            t2 = dict(t)
            t2["!"] = ["^*", t["&"]]
            del t2["&"]

            retval = _evaluateEval(s, t2, l, src, tt, b)
        elif builtinf:
            s2 = dict(s) if isObject(s) else {}
            s2.update(_evaluateDict(s, t, l, src, tt, b))
    
            l2 = _evaluateDict(s, t["*"], l, src, tt, b) if "*" in t else l
    
            retval = builtinf(s, s2, l2, src, tt, b)
                
    return retval

def _evaluateEval(s, t, l, src, tt, b):
    t2 = _evaluate(s, t.get("!"), l, src, tt, b)
    
    s2 = dict(s) if isObject(s) else {}
    s2.update(_evaluateDict(s, t, l, src, tt, b))

    l2 = _evaluateDict(s, t["*"], l, src, tt, b) if "*" in t else l

    return _evaluate(s2, t2, l2, src, tt, b)

def _evaluateDict(s, t, l, src, tt, b):
    retval = {
        unicode(key): _evaluate(s, t[key], l, src, tt, b) 
            for key in t.keys()
            if (key != "!") and (key != "&")
    } 
    return retval

def _quoteEvaluateDict(s, t, l, src, tt, b):
    retval = {
        unicode(key): _quoteEvaluate(s, t[key], l, src, tt, b) 
            for key in t.keys()
    } 
    return retval

def _evaluateList(s, t, l, src, tt, b):
    return [_evaluate(s, item, l, src, tt, b) for item in t]

def _quoteEvaluateList(s, t, l, src, tt, b):
    return [_quoteEvaluate(s, item, l, src, tt, b) for item in t]

# def _evaluatePathHead(s, t, l, src, tt, b):
#     resultlist = _evaluatePath(s, t, l, src, tt, b)
# 
#     return resultlist[0] if resultlist else None

# def _evaluatePath(s, t, l, src, tt, b):
#     path_t = {
#         "&": "path",
#         "path": t
#     }
# 
#     return _evaluate(s, path_t, l, src, tt, b)

def _flatten(lst):
    lst2 = [item if isArray(item) else [item] for item in lst]
    return [item for sublist in lst2 for item in sublist]

def isArrayBuiltinEval(arr, b):
    retval = arr and isArray(arr) 
    
    if retval:
        op = arr[0]
            
        retval = op and isString(op) and (op[0] in ["&", "^"]) and _getArrayBuiltinName(op) in b
        
    return retval

def isStringBuiltinEval(astr, b):
    retval = False
    
    if isString(astr):
        arr = astr.split(".")
        retval = isArrayBuiltinEval(arr, b)
    
    return retval

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
    return isinstance(obj, (int, float, long))

def isBool(obj):
    return isinstance(obj, bool)

# def isPathHeadTransform(obj):
#     return isString(obj) and obj[:1] == "#"
# 
# def isPathTransform(obj):
#     return isString(obj) and obj[:2] == "##"

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




