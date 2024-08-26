import subprocess


def run_tcpdump():
    print('Running TCPdump ....')
    cmd = ['timeout','2','sudo','tcpdump','-i','any','-vvv','-x']
    try:
        f = open("output.txt", "w")
        proc1 = subprocess.run(cmd, stdout=f,timeout=4)
    except subprocess.TimeoutExpired:
        print('TCPdump Complete ....')
    
    f.close()


def read_file():
    f=open("output.txt","r")
    lines=f.readlines()
    count=0
    for line in lines:
        count=count+1
    print(count)



run_tcpdump()
read_file()
	
