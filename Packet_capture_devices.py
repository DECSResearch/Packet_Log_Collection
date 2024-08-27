import subprocess
import re


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
    tcpdump_data = []
    current_entry = {}

    for line in lines:
        line=line.lstrip()
        basic_info_match = re.match(
            r'(\d{2}:\d{2}:\d{2}\.\d{6}) (\S+) +(\S+) +IP.+proto (\S+) \(\d+\), length (\d+)\)', line)
        #ip_match = re.match(r'(\S+)\.(\S+) > (\S+)\.(\S+): Flags \[(.+)\]', line)
        ip_match = re.match(r'(\S+) > (\S+): Flags \[(.+)\]', line)
        if basic_info_match:
            if current_entry:
                tcpdump_data.append(current_entry)
                current_entry = {}

            current_entry['timestamp'] = basic_info_match.group(1)
            current_entry['interface'] = basic_info_match.group(2)
            current_entry['direction'] = basic_info_match.group(3)
            current_entry['protocol'] = basic_info_match.group(4)
            current_entry['length'] = basic_info_match.group(5)
        elif ip_match:
            
            if ip_match:
                current_entry['src_ip'] = ip_match.group(1)
                current_entry['dst_ip'] = ip_match.group(2)
                current_entry['flags'] = "["+ip_match.group(3)
        else:
            continue
    if current_entry:
        tcpdump_data.append(current_entry)

    for entry in tcpdump_data:
        print(f"Timestamp: {entry['timestamp']}")
        print(f"Interface: {entry['interface']}")
        print(f"Direction: {entry['direction']}")
        print(f"Source IP: {entry['src_ip']}")
        print(f"Destination IP: {entry['dst_ip']}")
        print(f"Protocol: {entry['protocol']}")
        print(f"Packet Length: {entry['length']}")
        print(f"Flags: {entry['flags']}")
        print("-" * 40)
    print(count)



#run_tcpdump()
read_file()
	
