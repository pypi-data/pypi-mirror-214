#!/usr/bin/env python3

import pymonetdb

conn = pymonetdb.connect(database='foo')
c = conn.cursor()

ret = c.execute("DROP TABLE IF EXISTS foo")
assert ret is None

ret = c.execute("CREATE TABLE foo(i INT)")
assert ret is None

ret = c.execute("INSERT INTO foo SELECT * FROM sys.generate_series(0,10)")
assert ret == 10

ret = c.execute("DELETE FROM foo WHERE i % 3 = 0")
assert ret == 4  # 0 3 6 9

ret = c.execute("SELECT * FROM foo")
assert ret == 6  # 1 2 4 5 7 8

