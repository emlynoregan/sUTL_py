import unittest
import sUTL
import json
import urllib2

class Tests(unittest.TestCase):
    def deepEqual(self, aMAS1, aMAS2, maxdepth=100):
        retval = False

        if maxdepth:
            retval = type(aMAS1) == type(aMAS2)
            if retval:
                if isinstance(aMAS1, dict):
                    retval = len(aMAS1.keys()) == len(aMAS2.keys())
                    if retval:
                        for lkey in aMAS1.keys():
                            retval = lkey in aMAS2 and self.deepEqual(aMAS1[lkey], aMAS2[lkey], maxdepth-1)
                            if not retval:
                                break
                elif isinstance(aMAS1, (list, tuple, set)):
                    retval = len(aMAS1) == len(aMAS2)
                    if retval:
                        for lindex, litem in enumerate(aMAS1):
                            retval = self.deepEqual(litem, aMAS2[lindex], maxdepth-1)
                            if not retval:
                                break
                else:
                    retval = aMAS1 == aMAS2
            
        return retval
    
    def test_Fail(self):
        ljsonDecls = GetDeclarations()
        
        lfailDecl = {
            "name": "failtest",
            "language": "sUTL0",
            "transform-t":   
            {
              "!": "#*.tests_tst",
              "tests": {"'": [
                {
                  "name": "this one fails",
                  "test-t": False
                }
              ]}
            },
            "requires": [
              "tests_tst"
            ]
          }
        
        lresult = EvaluateTransform(lfailDecl, ljsonDecls)
        
        if not lresult:
            raise Exception("Failed to fail")

    _source = {
            "updated": 1438517599342400, 
            "apkey": "2a02d608-6431-40aa-b0b2-91bf5f48cd84", 
            "stored": 1438313529667260, 
            "eventkeyid": "3a300a90-eca4-e101-383d-6bfd5990d791", 
            "key": "244de280-a01a-c5da-4162-ced9775246a5", 
            "clientkey": "82b25cfa-f0ec-4f44-9209-77cbd98edd6a", 
            "docalt": [1, 2, [3, 4]], 
            "invalid": False, 
            "document": {
                "description": "stuff", 
                "themeindex": 6, 
                "eventkeyid": "3a300a90-eca4-e101-383d-6bfd5990d791", 
                "published": True, 
                "type": "Metric_update", 
                "name": "thingo"
            }, 
            "type": "CachedObject", 
            "indexnames": [
                "82B25CFA-F0EC-4F44-9209-77CBD98EDD6A-Metric"
            ], 
            "objecttype": "Metric"
        }

    def test_1(self):
        ljsonDecls = GetDeclarations()
   
        ldecl = {
            "requires": [
                "addmaps_core", 
                "removekeys_core"
            ], 
            "transform-t": {
                "!": "^*.addmaps_core", 
                "map2": {
                    "__meta__": {
                        "!": "^*.removekeys_core", 
                        "map": "^$", 
                        "keys": [
                            "document"
                        ]
                    }
                }, 
                "map1": "^$.document"
            }, 
            "language": "sUTL0"
        }
          
        lexpected = {
          "description": "stuff",
          "themeindex": 6,
          "eventkeyid": "3a300a90-eca4-e101-383d-6bfd5990d791",
          "published": True,
          "__meta__": {
            "docalt": [
              1,
              2,
              [
                3,
                4
              ]
            ],
            "updated": 1438517599342400,
            "apkey": "2a02d608-6431-40aa-b0b2-91bf5f48cd84",
            "invalid": False,
            "stored": 1438313529667260,
            "eventkeyid": "3a300a90-eca4-e101-383d-6bfd5990d791",
            "key": "244de280-a01a-c5da-4162-ced9775246a5",
            "clientkey": "82b25cfa-f0ec-4f44-9209-77cbd98edd6a",
            "type": "CachedObject",
            "indexnames": [
              "82B25CFA-F0EC-4F44-9209-77CBD98EDD6A-Metric"
            ],
            "objecttype": "Metric"
          },
          "type": "Metric_update",
          "name": "thingo"
        }
          
        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
          
        self.assertTrue(self.deepEqual(lresult, lexpected), "lresult: %s" % json.dumps(lresult))

    def test_2(self):
        ljsonDecls = GetDeclarations()

        ldecl = {
            "transform-t": "^$.indexnames.1", 
            "language": "sUTL0"
        }

        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                None
            )
        
        lexpected = None

        self.assertTrue(self.deepEqual(lresult, lexpected), "lresult: %s" % json.dumps(lresult))

    def test_3(self):
        ljsonDecls = GetDeclarations()
   
        ldecl = {
            "requires": [
                "removekeys_core"
            ], 
            "transform-t": {
                        "!": "^*.removekeys_core", 
                        "map": "#$", 
                        "keys": [
                            "document",
                            "updated",
                            "apkey",
                            "key",
                            "clientkey",
                            "invalid",
                            "indexnames",
                            "docalt"
                        ]
                    },
            "language": "sUTL0"
        }
          
        lexpected = {
            "stored": 1438313529667260, 
            "eventkeyid": "3a300a90-eca4-e101-383d-6bfd5990d791", 
            "type": "CachedObject", 
            "objecttype": "Metric"
        }
         
        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
          
        self.assertTrue(self.deepEqual(lresult, lexpected), "lresult: %s" % json.dumps(lresult))

    def test_4(self):
        ljsonDecls = GetDeclarations()
 
        ldecl = {
            "requires": [
                "isinlist_core"
            ], 
            "transform-t": {
                        "!": "^*.isinlist_core", 
                        "list": {"&": "keys", "map": "^$"}, 
                        "item": 
                            "document"
                        
                    },
            "language": "sUTL0"
        }
        
        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        if not lresult:
            raise Exception("Failed: %s" % lresult)

    def test_5(self):
        ljsonDecls = GetDeclarations()
 
        ldecl = {
            "requires": [
                "filter_core"
            ], 
            "transform-t": {
                        "!": "^*.filter_core", 
                        "list": {"&": "keys", "map": "^$"}, 
                        "filter-t": True
                    },
            "language": "sUTL0"
        }
        
        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        if not lresult:
            raise Exception("Failed: %s" % lresult)

    def test_6(self):
        ljsonDecls = GetDeclarations()
 
        ldecl = {
            "transform-t": {
                "&": "reduce", 
                "list": {"&": "keys", "map": "^$"}, 
                "accum": "",
                "t": {"'": 
                  {
                    "&": "+",
                    "a": "^@.item",
                    "b": "^@.accum"
                  }
                }
            }, 
            "language": "sUTL0"
        }
        
        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        lexpected = "objecttypeindexnamestypedocumentinvaliddocaltclientkeykeyeventkeyidstoredapkeyupdated"
        
        self.assertTrue(self.deepEqual(lresult, lexpected), "lresult: %s" % json.dumps(lresult))

    def test_7(self):
        ljsonDecls = GetDeclarations()
        
        lfilterDecl =   {
            "name": "testfilter",
            "language": "sUTL0",
            "transform-t": 
            {
              "&": "reduce",
              "list": "^@.list",
              "accum": [],
              "t": {"'": [
                "&&",
                "^@.accum",
                {
                  "&": "if",
                  "cond": {"'": 
                    {"''": "^@.filter-t"}
                  },
                  "true": ["^@.item"],
                  "false": []
                }
              ]}
            }
          }
        
        ljsonDecls.append([lfilterDecl])

 
        ldecl = {
            "requires": [
                "testfilter"
            ], 
            "transform-t": {
                "!": "^*.testfilter", 
                "list": {"&": "keys", "map": "^$"}, 
                "filter-t": {"'": {
                    "&": "=",
                    "a": "^@.item",
                    "b": "stored"
                }}
            },
            "language": "sUTL0"
        }
        
        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        lexpected = [
          "stored"
        ]
        
        self.assertTrue(self.deepEqual(lresult, lexpected), "lresult: %s" % json.dumps(lresult))

    def test_8(self):
        ljsonDecls = GetDeclarations()

        ldecl = {
          "language": "sUTL0",
          "transform-t": {
            "&": "if",
            "cond": [],
            "true": 1,
            "false": 0
          }
        }

        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        lexpected = 0
        
        self.assertTrue(self.deepEqual(lresult, lexpected), "lresult: %s" % json.dumps(lresult))
        
    def test_9(self):
        ljsonDecls = GetDeclarations()

        lreduceDecl =   {
            "name": "testreduce",
            "language": "sUTL0",
            "transform-t": 
            {
              "&": "if",
              "cond": "^@.list",
              "true": { "'": {
                "!": "^*.testreduce",
                "list": {
                  "!": "^*.tail_core_emlynoregan_com",
                  "list": "^@.list"
                },
                "t": "^@.t",
                "accum": {
                  "!": "^@.t",
                  "item": {
                    "!": "^*.head_core_emlynoregan_com",
                    "list": "^@.list"
                  },
                  "accum": "^@.accum"
                }
              }},
              "false": {
                "'": "^@.accum"
              }
            },
            "requires": [
              "testreduce", 
              "head_core_emlynoregan_com", 
              "tail_core_emlynoregan_com"
            ]
          }
        
        ljsonDecls.append([lreduceDecl])


        ldecl = {
            "requires": [
                "testreduce"
            ], 
            "transform-t": {
                "!": "^*.testreduce", 
                "list": {"&": "keys", "map": "^$"}, 
                "accum": "",
                "t": {"'": [ "&+", "^@.item", "^@.accum"]}
            }, 
            "language": "sUTL0"
        }
        


        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        lexpected = "objecttypeindexnamestypedocumentinvaliddocaltclientkeykeyeventkeyidstoredapkeyupdated"
        
        self.assertTrue(self.deepEqual(lresult, lexpected), "lresult: %s" % json.dumps(lresult))
        
    def test_10(self):
        ljsonDecls = GetDeclarations()

        lreduceDecl =   {
            "name": "testcond",
            "language": "sUTL0",
            "transform-t": 
            {
              "&": "if",
              "cond": "^@.list",
              "true": { "'": True },
              "false": { "'": False }
            },
            "requires": [
            ]
          }
        
        ljsonDecls.append([lreduceDecl])


        ldecl = {
            "requires": [
                "testcond"
            ], 
            "transform-t": {
                "!": "^*.testcond", 
                "list": {"&": "keys", "map": "^$"}
            }, 
            "language": "sUTL0"
        }
        


        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        lexpected = True
        
        self.assertTrue(self.deepEqual(lresult, lexpected), "lresult: %s" % json.dumps(lresult))

    def test_11(self):
        ljsonDecls = GetDeclarations()

        ldecl = {
            "transform-t": {"&": "keys", "map": "^$"}, 
            "language": "sUTL0"
        }

        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        lexpected = [
          "updated",
          "apkey",
          "stored",
          "eventkeyid",
          "key",
          "clientkey",
          "docalt",
          "invalid",
          "document",
          "type",
          "indexnames",
          "objecttype"
        ]

        
        self.assertTrue(self.deepEqual(lresult, lexpected), "lresult: %s" % json.dumps(lresult))

    def test_12(self):
        ljsonDecls = GetDeclarations()

        ldecl = {
          "transform-t": {"'": {
            "a": "^$.updated", 
            "b": {"''": "^$.updated"}
          }}, 
          "language": "sUTL0"
        }

        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        lexpected = {
          "a": "^$.updated",
          "b": 1438517599342400
        }

        self.assertTrue(self.deepEqual(lresult, lexpected), "lresult: %s" % json.dumps(lresult))

    def test_13(self):
        ljsonDecls = GetDeclarations()
  
        ldecl = {
            "requires": [
                "zip_core"
            ], 
            "transform-t": {
                "!": "^*.zip_core", 
                "list": [[1, 2], [3, 4]]
            }, 
            "language": "sUTL0"
        }
  
        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
          
        lexpected = [[1, 3], [2, 4]]
  
        self.assertTrue(self.deepEqual(lresult, lexpected), "lresult: %s" % json.dumps(lresult))

    def test_14(self):
        ljsonDecls = GetDeclarations()

        ldecl = {
            "requires": [
                "count_core"
            ], 
            "transform-t": {
              "&": "<",
              "a": 0,
              "b": {
                "!": "^*.count_core",
                "obj": [[],[]]
              }
            }, 
            "language": "sUTL0"
        }

        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        lexpected = False
        self.assertTrue(self.deepEqual(lresult, lexpected), "lresult: %s" % json.dumps(lresult))

    def test_15(self):
        ljsonDecls = GetDeclarations()

        ldecl = {
            "transform-t": "^$", 
            "language": "sUTL0"
        }

        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        self.assertTrue(self.deepEqual(lresult, self._source), "lresult: %s" % json.dumps(lresult))

    def test_16(self):
        ljsonDecls = GetDeclarations()

        ldecl = {
            "transform-t": {
                "&": "len",
                "list": [1, 2]
            },
            "language": "sUTL0"
        }

        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        self.assertEqual(2, lresult)

    def test_17(self):
        ljsonDecls = GetDeclarations()

        ldecl = {
          "language": "sUTL0",
          "transform-t": {
            "!": "#*.foldone",
            "lists": [[1], [2]],
            "list": [3, 4]
          },
          "requires": [
            "foldone"
          ]
        }

        lexpected = [
          [
            1,
            3
          ],
          [
            2,
            4
          ]
        ]
        
        lresult = EvaluateTransform(
                ldecl,
                ljsonDecls,
                self._source
            )
        
        self.assertEqual(lexpected, lresult)
        
def EvaluateTransform(aDecl, aLibDecls, aSource = None):
    llibresult = sUTL.compilelib([aDecl], aLibDecls, True)
    
    llib = {}
    if "fail" in llibresult:
        raise Exception("Libraries failed tests: %s" % llibresult["fail"])
    elif "lib" in llibresult:
        llib = llibresult["lib"]
        
    lresult = sUTL.evaluate(aSource, aDecl.get("transform-t"), llib)
    
    return lresult

def GetDeclarations():
    ljsonDecls = []
    ljsonCoreString = urllib2.urlopen("http://emlynoregan.github.io/sUTL-spec/sUTL_core.json").read()
    ljsonDecls.append(json.loads(ljsonCoreString))
    return ljsonDecls

def GetCoreTests():
    ljsonCoreTestsString = urllib2.urlopen("http://emlynoregan.github.io/sUTL-spec/sUTL_coretests.json").read()
     
    return json.loads(ljsonCoreTestsString)
    
        
def AddTests(aGetDeclarationsF = GetDeclarations, aGetCoreTestsF = GetCoreTests):
    ljsonDecls = aGetDeclarationsF()
     
    ljsonCoreTests = aGetCoreTestsF()
         
    for lindex, lsUTLdeclaration in enumerate(ljsonCoreTests):
        ltestName = lsUTLdeclaration.get("name", str(lindex))
         
        def GetTestFunction():
            ldecl = lsUTLdeclaration
            def TheTestFunction(self):
                print json.dumps(ldecl)
                lresult = EvaluateTransform(ldecl, ljsonDecls)
 
                if lresult:
                    # tests are failed here
                    raise Exception("Failed: %s" % lresult)
            return TheTestFunction
             
        ltestFunction = GetTestFunction()
        ltestFunction.__name__ = str("test_%s" % ltestName)
        setattr(Tests, "test_%s" % ltestName, ltestFunction )
 
