from sUTL import sUTL

def main():
    decl = {"transform-t": {"&": "@", "head": True}}
    z = {
        "transform-t": {"x": {"x": {"x": {"s": "^@"}}}, "y": {"x": {"x": {"s": "^@"}}}}
    }

    source = {
      "y": 3
    }
   
    s = sUTL

    def compilelib():
        libs = [[
          {
              "name": "six",
              "transform-t": {
                  "x": 6
              }
          }
        ]]
     
        libr = s.compilelib([decl], libs, False)
        lib = libr["lib"]
        
        return lib

    def run(lib, b):
        return s._evaluate(source, decl["transform-t"], lib, source, decl["transform-t"], b)

    lib = compilelib()
    
    import cProfile

    p = cProfile.Profile()
    
    b = s.builtins()
    
    p.enable()
    result = p.runcall(run, lib, b)
    p.disable()
    p.print_stats()
 
    print result

# def main():
#   s = Sutl()
# 
#   v = s.ExampleString()
#   print type(v)
#   print v  
# 
#   v = s.ExampleInt()
#   print type(v)
#   print v  
# 
#   v = s.ExampleFloat()
#   print type(v)
#   print v  
# 
#   v = s.ExampleBool()
#   print type(v)
#   print v  
# 
#   v = s.ExampleNull()
#   print type(v)
#   print v  
# 
#   v = s.ExampleArray()
#   print type(v)
#   print v  
# 
#   v = s.ExampleDict()
#   print type(v)
#   print type(v.x)
#   print v  
# 
#   def isObject(obj):
#     return isinstance(obj, dict)
# 
#   def isArray(obj):
#     return isinstance(obj, list)
# 
#   def convertToAnon(aObj):
#     if isObject(aObj):
#     convDict = {key: convertToAnon(aObj[key]) for key in aObj}
#     return _hx_AnonObject(convDict)
#     elif isArray(aObj):
#     return [convertToAnon(litem) for litem in aObj]
#     elif isinstance(aObj, str):
#     return unicode(aObj)
#     else:
#     return aObj
# 
#   def convertFromAnon(aObj):
#     if isinstance(aObj, _hx_AnonObject):
#     retval = dict(aObj.__dict__)
#         retval = {key: convertFromAnon(retval[key]) for key in retval}
#     return retval
#     elif isArray(aObj):
#     return [convertFromAnon(litem) for litem in aObj]
#     else:
#     return aObj
# 
#   libs = [[
#     {
#         "name": "six",
#         "transform-t": 6
#     }
#   ]]
# 
#   libsconv = convertToAnon(libs)
# 
#   source = {
#     "y": 3
#   }
#   
#   sourceconv = convertToAnon(source)
# 
#   decl = {
#     "transform-t": {
#       "x": [{"&": "six"}, "^@"]
#     },
#     "requires": ["six"]
#   }
# 
#   declconv = convertToAnon(decl)
# 
#   print declconv
# 
#   libr = s.compilelib([declconv], libsconv)
#   lib = libr.lib
#   print convertFromAnon(libsconv)
#   print convertFromAnon(lib)
# 
#   result = s.evaluate(sourceconv, getattr(declconv, "transform-t"), lib, 0)
# 
#   print result
#   print convertFromAnon(result)


main()