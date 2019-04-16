import time

from tasks import test_add, test_lol

result = test_add.delay(1,2)
t      = test_lol.delay(1,2,3,4,'lol')

print 'Task finished? {}'.format(result.ready())
print 'Task result: {}'.format(result.result)

time.sleep(5)

print 'Task finished? {}'.format(result.ready())
print 'Task result: {}'.format(result.result)
