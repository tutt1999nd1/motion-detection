import sys
if len(sys.argv) == 3:
    program, cam_id, src = sys.argv
    print('cam_id: ',cam_id)
    print('src: ',src)
else:
    print('You must give an environment, and an action!')