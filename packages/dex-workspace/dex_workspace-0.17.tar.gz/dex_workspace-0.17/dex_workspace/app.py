import sys 
import os 

sys.path.append(os.path.abspath(os.path.dirname(__file__)))

import os 
import sys
import subprocess 
import multiprocessing 
import requests
import socket
from threading import Thread,Event

try:
    multiprocessing.set_start_method('fork')
except:
    None
dirname = os.path.dirname(__file__)
python_path = sys.executable
backend_path = os.path.join(dirname, 'production', 'operator', 'app.py' )

def get_private_ip():
    hostname = socket.gethostname()
    private_ip = socket.gethostbyname(hostname)
    return private_ip

def return_ip():
    try:
        # Attempt to get the public IP
        public_ip = requests.get('https://api.ipify.org').text
        return public_ip
    except requests.RequestException:
        # If the public IP is not accessible, return the private IP
       return get_private_ip()
    
application_ip = get_private_ip()
private_mode = True

# start operator
def launch_operator():
    cmd = [python_path, 'app.py', '--app_ip', application_ip]

    work_dir = os.path.join(dirname, 'production', 'operator')

    sys_cmd = f'cd "{work_dir}" && {python_path} app.py --app_ip {application_ip}'

    process = subprocess.Popen(
        cmd, 
        cwd=os.path.join(dirname, 'production', 'operator'),
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,  # Line-buffered
        universal_newlines=True
    )

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            err = process.stderr.read()
            print(err)
            break

# info file that will be used 
info_content1 = """
const appIP = '{ip}'
"""

info_content2 = """
export {appIP,}
"""

# ultimately select public or private ip to access 
def select_ip():
    public_ip = return_ip()
    # test if public ip works 
    try:
        requests.get(f'http://{public_ip}:5678/get').json()
        return public_ip
    except:
        return get_private_ip()
    

# start frontend 
def start_frontend():
    # insert the backend path using private IP if the public IP does not work
    inserted_content = info_content1.format(ip=application_ip) + info_content2
    # put it in the file
    info_path = os.path.join(dirname, 'production', 'react-manage(1)','src','backend','otherInfo.js')
    with open(info_path, 'w') as file:
        file.write(inserted_content)
    folder_path = os.path.join(dirname,'production', 'react-manage(1)')
    # make a command to start running
    frontend_cmd = ['npm', 'run', 'dev', '--', '--host', application_ip , '--port', '10000']


    process = subprocess.Popen(
        frontend_cmd, 
        cwd=folder_path, 
        stdin=subprocess.PIPE, 
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1,  # Line-buffered
        universal_newlines=True
    )

    while True:
        output = process.stdout.readline()
        if output == '' and process.poll() is not None:
            err = process.stderr.read()
            print(err)
            break


def check1():
    from production.operator.operations.security import pwd_hash, save_pwd
    import getpass
    if pwd_hash == '':
        pwd = getpass.getpass('Set a password')
        if pwd =='':
            check1()
        else:
            save_pwd(pwd=pwd)
        sys.exit()

# ask the user what he/she wants to do
help_question = """
[1] Launch the platform 
[2] Reset Password
Enter the number:"""
def help_check():
    import getpass
    from production.operator.operations.security import save_pwd
    choice = input(help_question)
    if choice == '1':
        return
    # reset password
    if choice == '2':
        while True:
            pwd = getpass.getpass('Set a password')
            if pwd == '':
                continue
            save_pwd(pwd=pwd)
            break
    sys.exit()
    
help_check()
# ask about instructions

mode_question = """
[1] Private Mode: You and your collaborators can only connect to your workspace using private ip
[2] Public Mode: You and your collaborators can connect to your workspace using public ip

Enter the number you choose: 
"""

check1()

mode = int(input(mode_question))

if mode == 2:
    application_ip = return_ip() 
    private_mode = False

# launch the platform 

Thread(target=launch_operator, ).start()
Thread(target=start_frontend, ).start()

dashboard_link = f'http://{application_ip}:10000'

running_notif = "---------------------- Remeny Dex Platform Is Running ----------------------"
messsage = f"""
\033[32m{running_notif}\033[0m

You can access the platform dashboard at: {dashboard_link}

"""

print(messsage)


