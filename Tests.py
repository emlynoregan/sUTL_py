import unittest
import sUTL
import json
import io
import os
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

def EvaluateTransform(aDecl, aLibDecls):
    llibresult = sUTL.compilelib([aDecl], aLibDecls, True)
    
    llib = {}
    if "fail" in llibresult:
        raise Exception("Libraries failed tests: %s" % llibresult["fail"])
    elif "lib" in llibresult:
        llib = llibresult["lib"]
        
    lresult = sUTL.evaluate(None, aDecl.get("transform-t"), llib)
    
    return lresult

def GetDeclarations():
    ljsonDecls = []
    ljsonCoreString = urllib2.urlopen("http://emlynoregan.github.io/sUTL-spec/sUTL_core.json").read()
    ljsonDecls.append(json.loads(ljsonCoreString))
    return ljsonDecls
        
def AddTests():
    ljsonDecls = GetDeclarations()
     
    ljsonCoreTestsString = urllib2.urlopen("http://emlynoregan.github.io/sUTL-spec/sUTL_coretests.json").read()
     
    ljsonCoreTests = json.loads(ljsonCoreTestsString)
     
    for lindex, lsUTLdeclaration in enumerate(ljsonCoreTests):
        ltestName = lsUTLdeclaration.get("name", str(lindex))
         
        def GetTestFunction():
            ldecl = lsUTLdeclaration
            def TheTestFunction(self):
                lresult = EvaluateTransform(ldecl, ljsonDecls)
 
                if lresult:
                    # tests are failed here
                    raise Exception("Failed: %s" % lresult)
            return TheTestFunction
             
        ltestFunction = GetTestFunction()
        ltestFunction.__name__ = str("test_%s" % ltestName)
        setattr(Tests, "test_%s" % ltestName, ltestFunction )
 
AddTests()        
