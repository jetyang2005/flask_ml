
import sys
sys.path.insert(0, '')

import yaml

f = open('/Users/yangwm/log/elastalert/samples/test.yml')
x = yaml.load(f)

print type(x)
print x