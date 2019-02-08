import os
from parser import Manager

groups = os.getenv('GROUPS', '').split(' ')

man = Manager()
man.run(*groups)
man.save()
