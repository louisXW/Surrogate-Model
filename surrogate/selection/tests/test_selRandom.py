from surrogate.selection.tests.test_individuals import Individuals

individuals = Individuals()

from surrogate.selection.selRandom import selRandom

print '\nTest.selection: selRandom'
print '\tInput:  ind=\t' + '\t'.join(map(str, individuals)) + ''
out = selRandom(individuals=list(individuals), k=2)
print '\tOutput: out=\t' + '\t'.join(map(str, out)) + ''
