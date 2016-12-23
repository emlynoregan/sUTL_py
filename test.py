from sUTL import sUTL
import json

def main():
    s = sUTL

    libs = [[
      {
          "name": "six",
          "transform-t": {
              "x": 6
          }
      }
    ]]
 
    source = {
      "y": 3
    }
   
    decl = {
      "transform-t": {
        "x": [{"&": "six"}, "^@"]
      },
      "requires": ["six"]
    }
 
    libr = s.compilelib([decl], libs, False)
    lib = libr["lib"]
 
    result = s.evaluate(source, decl["transform-t"], lib)

    def slow():
        with open("sUTL_core.dist.json") as f:
            lcoredist = json.load(f)

        lsource = {
          "roleinfos": [
            {
                "admin": {
                    "modules": [
                        "Client", 
                        "People", 
                        "Timeline", 
                        "Video", 
                        "Schedule", 
                        "Inbox", 
                        "Outbox", 
                        "Config", 
                        "Metrics", 
                        "ViewSkills", 
                        "PathAuthor", 
                        "PathPerform", 
                        "PathResults", 
                        "ViewTasks", 
                        "Groups"
                    ], 
                    "capabilities": [
                        "Config;r", 
                        "Device2;r", 
                        "Device2;w", 
                        "Event;r", 
                        "Group2;r", 
                        "Group2;w", 
                        "Person2;r", 
                        "Person2;w", 
                        "VideoInfo2;r", 
                        "VideoInfo2;w", 
                        "NotificationTemplate;r", 
                        "NotificationTemplate;w", 
                        "Notification;w", 
                        "ReceivedNotification;w", 
                        "Config;w", 
                        "Metric;r", 
                        "Path;r", 
                        "Path;w", 
                        "PathDef;r", 
                        "PathDef;w", 
                        "Task;r", 
                        "Metric;w", 
                        "Action;w", 
                        "Action;r", 
                        "App;r", 
                        "App;w"
                    ]
                }, 
                "client": {
                    "modules": [
                        "unmanaged"
                    ], 
                    "capabilities": [], 
                    "roles": [
                        "admin", 
                        "adminviewer", 
                        "trainee"
                    ]
                }, 
                "adminviewer": {
                    "modules": [
                        "Client", 
                        "People", 
                        "Timeline", 
                        "Video", 
                        "Schedule", 
                        "Inbox", 
                        "Outbox", 
                        "Config", 
                        "Metrics", 
                        "ViewSkills", 
                        "PathAuthor", 
                        "PathPerform", 
                        "PathResults", 
                        "ViewTasks", 
                        "Groups"
                    ], 
                    "capabilities": [
                        "Config;r", 
                        "Device2;r", 
                        "Event;r", 
                        "Group2;r", 
                        "Person2;r", 
                        "VideoInfo2;r", 
                        "NotificationTemplate;r", 
                        "Config;w", 
                        "Metric;r", 
                        "Path;r", 
                        "PathDef;r", 
                        "Task;r", 
                        "Action;r", 
                        "App;r"
                    ]
                }, 
                "trainee": {
                    "modules": [
                        "Video", 
                        "Inbox", 
                        "HasSkills", 
                        "HasTasks", 
                        "studentview"
                    ], 
                    "capabilities": [
                        "Config;r", 
                        "VideoInfo2;r"
                    ]
                }
            },
            {
                "admin": {
                    "modules": [
                        "Client", 
                        "People", 
                        "Timeline", 
                        "Video", 
                        "Schedule", 
                        "Inbox", 
                        "Outbox", 
                        "Config", 
                        "Metrics", 
                        "ViewSkills", 
                        "PathAuthor", 
                        "PathPerform", 
                        "PathResults", 
                        "ViewTasks", 
                        "Groups"
                    ], 
                    "capabilities": [
                        "Config;r", 
                        "Device2;r", 
                        "Device2;w", 
                        "Event;r", 
                        "Group2;r", 
                        "Group2;w", 
                        "Person2;r", 
                        "Person2;w", 
                        "VideoInfo2;r", 
                        "VideoInfo2;w", 
                        "NotificationTemplate;r", 
                        "NotificationTemplate;w", 
                        "Notification;w", 
                        "ReceivedNotification;w", 
                        "Config;w", 
                        "Metric;r", 
                        "Path;r", 
                        "Path;w", 
                        "PathDef;r", 
                        "PathDef;w", 
                        "Task;r", 
                        "Metric;w", 
                        "Action;w", 
                        "Action;r", 
                        "App;r", 
                        "App;w"
                    ]
                }, 
                "client": {
                    "modules": [
                        "unmanaged"
                    ], 
                    "capabilities": [], 
                    "roles": [
                        "admin", 
                        "adminviewer", 
                        "trainee"
                    ]
                }, 
                "adminviewer": {
                    "modules": [
                        "Client", 
                        "People", 
                        "Timeline", 
                        "Video", 
                        "Schedule", 
                        "Inbox", 
                        "Outbox", 
                        "Config", 
                        "Metrics", 
                        "ViewSkills", 
                        "PathAuthor", 
                        "PathPerform", 
                        "PathResults", 
                        "ViewTasks", 
                        "Groups"
                    ], 
                    "capabilities": [
                        "Config;r", 
                        "Device2;r", 
                        "Event;r", 
                        "Group2;r", 
                        "Person2;r", 
                        "VideoInfo2;r", 
                        "NotificationTemplate;r", 
                        "Config;w", 
                        "Metric;r", 
                        "Path;r", 
                        "PathDef;r", 
                        "Task;r", 
                        "Action;r", 
                        "App;r"
                    ]
                }, 
                "trainee": {
                    "modules": [
                        "Video", 
                        "Inbox", 
                        "HasSkills", 
                        "HasTasks", 
                        "studentview"
                    ], 
                    "capabilities": [
                        "Config;r", 
                        "VideoInfo2;r"
                    ]
                }
            }
          ]
        }

        ldecl = {
          "transform-t": 
          {
            "!": {":": {
              "&": "makemap",
              "value": {
                "&": "map_core",
                "list": "^@.combinedroles",
                "t": {":": [
                  "^@.item",
                  {
                    "&": "reduce",
                    "list": "^@.roleinfos",
                    "accum": {},
                    "rolename": "^@.item",
                    "t": {":": {
                      "roles":  {         
                        "!": "^@.mergearrs-t",
                        "attribname": "roles"
                      },
                      "modules":  {         
                        "!": "^@.mergearrs-t",
                        "attribname": "modules"
                      },
                      "capabilities":  {         
                        "!": "^@.mergearrs-t",
                        "attribname": "capabilities"
                      }
                    }}
                  }
                ]}
              }
            }},
            "combinedroles": {
              "&": "removedupstrarr_core",
              "list": {
                "&": "reduce",
                "list": "^@.roleinfos",
                "accum": [],
                "t": {":": 
                  [
                    "&&",
                    "^@.accum",
                    {
                      "&": "keys",
                      "map": "^@.item"
                    }
                  ]
                }
              }
            },
            "mergearrs-t": {":": {
              "&": "quicksort_core",
              "list": {
                "&": "removedupstrarr_core",
                "list": [
                  "&&",
                  ["^@", "accum", "^@.attribname"],
                  ["^@", "item", "^@.rolename", "^@.attribname"]
                ]
              }
            }}
          },
          "requires": ["map_core", "removedupstrarr_core", "quicksort_core"]
        }

        llib = s.compilelib([ldecl], [lcoredist], False)
        
#         print(llib["lib"])
#         
        result = s.evaluate(lsource, ldecl["transform-t"], llib["lib"])
        
        print result

    import cProfile

    p = cProfile.Profile()
    
    p.enable()
    p.runcall(slow)
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