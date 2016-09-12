# sUTL_py
sUTL Universal Transform Language for Python

This is a python implementation of sUTL. See the [sUTL spec](https://github.com/emlynoregan/sUTL-spec) here.

Import sUTL like this:

    from sUTL_py import sUTL
  
Evaluate a transform like this:

    transform = {
        "&": "+",
        "a": "^@",
        "b": 5
    }
  
    source = 6
  
    result = sUTL.evaluate(source, transform, {})

    # here result is 11

To use library distributions, do the following:

1: Load the libraries. The following loads the core library.

    coreString = urllib2.urlopen("http://emlynoregan.github.io/sUTL-spec/sUTL_core.json").read()
    distributions = [json.loads(coreString)]

2: Add your transform to a declaration

    transform = {
        "&": "map_core",
        "list": "^@",
        "t": {":": {
            "&": "+",
            "a": "^@.item",
            "b": 1
        }}
    }

    declaration = {
      "transform-t": transform,
      "requires": ["map_core"]
    }

3: Compile a set of libraries from the distribution

    lib = sUTL.compilelib([declaration], distributions, false)
    
4: Evaluate your transform

    source = [1, 2, 3, 4]

    result = sUTL.evaluate(source, transform, lib)

    # here result is [2, 3, 4, 5]
