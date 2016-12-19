import mango


uri = "mongodb://user:pwd@localhost:27017/tests"
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


print "select, is_many=True"
for each in mango.select(
    "tests",
    dict(status=True),
    is_many=True):
    print each
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
