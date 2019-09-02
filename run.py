import os
from parser import Manager

groups = os.getenv('GROUPS', '').split(' ')

man = Manager()
man.run('3-Т3О-308Б-16',)
man.save()
