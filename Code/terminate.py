import os
print('running programs:')
os.system("ps -ef | grep python")
print('terminating...')
os.system("sudo killall python3")
print('remaining programs:')
os.system("ps -ef | grep python")
