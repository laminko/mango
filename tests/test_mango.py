import sys
import os


"""
Mango Tester Script.
"""

current_path = os.path.dirname(
        os.path.dirname(
            os.path.abspath(__file__))
    )
# print current_path
sys.path.append(current_path)


import mango


uri_obj = dict()

if len(sys.argv) < 5:
    print "python test_mango.py user pwd dbname [port|d] [host|d]"
    print "NOTE: d = use default value"
    raise ValueError("Incorrect parameters")

args = sys.argv
if args[-2] == "d":
    args[-2] = "27017"
if args[-1] == "d":
    args[-1] = "localhost"

uri = "mongodb://{1}:{2}@{5}:{4}/{3}".format(*args)
print mango.init_db(uri)


print "Testing mango lib."


table = mango.get_table("tests")
print table


print "insert, is_many=False"
print mango.insert(
    "tests",
    dict(name="Tun Tun", status=True))
print mango.insert(
    "tests",
    dict(name="Mg Mg", status=True))


print "insert, is_many=True"
print mango.insert(
    "tests",
    [
        dict(name="Su Su", status=True),
        dict(name="Kyaw Kyaw", status=True)
    ],
    is_many=True)


print "select, is_many=False"
print mango.select(
    "tests",
    dict(status=True))


print "select, is_many=False, to_web2py_id=True"
print mango.select(
    "tests",
    dict(status=True),
    to_web2py_id=True)


print "select, is_many=True"
for each in mango.select(
    "tests",
    dict(status=True),
    is_many=True):
    print each
print


print "select, is_many=True, to_web2py_id=True"
for each in mango.select(
    "tests",
    dict(status=True),
    is_many=True,
    to_web2py_id=True):
    print each
print


print "count"
print mango.count('tests', dict(status=True))
print


print "update, is_many=False"
print mango.update(
    "tests",
    dict(name="Su Su"),
    dict(status=False))


print "update, is_many=True"
print mango.update(
    "tests",
    dict(status=True),
    dict(status=False),
    is_many=True)


print "delete, is_many=False"
print mango.delete(
    "tests",
    dict(name="Kyaw Kyaw"))


print "delete, is_many=True"
print mango.delete(
    "tests",
    dict(status=False),
    is_many=True)


print table.count()
