from surrogate.selection.tests.test_individuals import Individuals

individuals = Individuals()

from surrogate.selection.selBest import selBest

print '\nTest.selection: selBest'
print '\tInput:  ind=\t' + '\t'.join(map(str, individuals)) + ''
out = selBest(individuals=list(individuals), k=2)
print '\tOutput: out=\t' + '\t'.join(map(str, out)) + ''
