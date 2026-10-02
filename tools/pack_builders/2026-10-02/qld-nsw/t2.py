import sys, traceback
from auto import *
from qb import T, TW, S
for a in sys.argv[1:]:
    code, _, opts = a.partition(":")
    kw = eval("dict(" + opts + ")") if opts else {}
    try: report(build(code, kw.pop("name", None), **kw))
    except SystemExit as ex: print("##", code, "FAIL", ex)
    except Exception as ex: print("##", code, "ERR", repr(ex)); traceback.print_exc(limit=2)
