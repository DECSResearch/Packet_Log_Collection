import subprocess
import re
from connection import *


def run_tcpdump():
    print('Running TCPdump ....')
    cmd = ['timeout','200','sudo','tcpdump','-i','any','-vvv','-x']
    try:
        f = open("output.txt", "w")
        proc1 = subprocess.run(cmd, stdout=f,timeout=4)
    except subprocess.TimeoutExpired:
        print('TCPdump Complete ....')
    
    f.close()


def read_file():
    f=open("output.txt","r")
    lines=f.readlines()
    tcpdump_data = []
    current_entry = {}
    payload_lines = []

    for line in lines:
        line=line.lstrip()
        basic_info_match = re.match(
            r'(\d{2}:\d{2}:\d{2}\.\d{6}) (\S+) +(\S+) +IP.+proto (\S+) \(\d+\), length (\d+)\)', line)
        #ip_match = re.match(r'(\S+)\.(\S+) > (\S+)\.(\S+): Flags \[(.+)\]', line)
        ip_match = re.match(r'(\S+) > (\S+): Flags \[(.+)\]', line)
        payload_match = re.match(r'^\s*0x[0-9a-f]{4}:\s+([0-9a-f\s]+)', line)
        if basic_info_match:
            if current_entry:
                current_entry['payload'] = ' '.join(payload_lines).replace(' ', '')
                tcpdump_data.append(current_entry)
                current_entry = {}
                payload_lines = []

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
            if payload_match:
                payload_lines.append(payload_match.group(1))
    if current_entry:
        current_entry['payload'] = ' '.join(payload_lines).replace(' ', '')
        tcpdump_data.append(current_entry)

    return tcpdump_data

    #for entry in tcpdump_data:
    #    print(f"Timestamp: {entry['timestamp']}")
    #    print(f"Interface: {entry['interface']}")
    #    print(f"Direction: {entry['direction']}")
    #    print(f"Source IP: {entry['src_ip']}")
    #    print(f"Destination IP: {entry['dst_ip']}")
    #    print(f"Protocol: {entry['protocol']}")
    #    print(f"Packet Length: {entry['length']}")
    #    print(f"Flags: {entry['flags']}")
    #    print(f"Payload: {entry['payload']}")
    #    print("-" * 40)

def write_to_mongo():
    for entry in tcpdump_data:
        a_document = {
            "timestamp": entry['timestamp'],
            "interface": entry['interface'],
            "direction": entry['direction'],
            "src_ip": entry['src_ip'],
            "dst_ip": entry['dst_ip'],
            "protocol": entry['protocol'],
            "length": entry['length'],
            "flags": entry['flags'],
            "payload": entry['payload']
        }
        collection.insert_one(a_document)


#run_tcpdump()
tcpdump_data = read_file()
write_to_mongo(tcpdump_data)







#Personal Access token- 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
	
