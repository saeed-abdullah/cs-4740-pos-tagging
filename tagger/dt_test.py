import DynamicTable

keys = ['verb', 'noun', 'adj']

v1 = {keys[0]: (.1, keys[1]), keys[1]: (.05, keys[2]), keys[2]: (.025, keys[0])}
v2 = {keys[0]: (.01, keys[2]), keys[1]: (.005, keys[0]), keys[2]: (.0025, keys[1])}
v3 = {keys[0]: (.001, keys[0]), keys[1]: (.0005, keys[1]), keys[2]: (.00025, keys[2])}

dt = DynamicTable.DynamicTable()

print 'testing updates'

print 'expecting output:\n'
print 'True'
print 'True'
print 'True\n'

print 'Received:\n'
print dt.update(v1)
print dt.update(v2)
print dt.update(v3)
print 'complete\n'

print 'testing last function'

print 'expecting output:\n'
print keys[1]
print keys[0]
print keys[2]+'\n'

print 'Received:\n'
print dt.last(0, keys[0])
print dt.last(1, keys[1])
print dt.last(2, keys[2])
print 'complete\n'

print 'testing prob function'

print 'expecting output:\n'
print '.05'
print '.0025'
print '.001\n'

print 'Received:\n'
print dt.prob(0, keys[1])
print dt.prob(1, keys[2])
print dt.prob(2, keys[0])
print 'complete\n'

print 'testing path function'

print 'expecting output:\n'
print [keys[0], keys[2], keys[0], keys[0]]
print [keys[1], keys[0], keys[1], keys[1]]
print [keys[2], keys[1], keys[2], keys[2]]
print ''

print 'Received:\n'
print dt.full_path(2, keys[0])
print dt.full_path(2, keys[1])
print dt.full_path(2, keys[2])
print 'complete\n'
