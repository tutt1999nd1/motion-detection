import sys
if len(sys.argv) == 3:
    program, environment, action = sys.argv
    print('enviroment: ',environment)
    print('action: ',action)
else:
    print('You must give an environment, and an action!')