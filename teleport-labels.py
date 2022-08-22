import os
import sys
import yaml
import subprocess

file_path = '/etc/teleport.labels'


def read_yaml(path):
    with open(path) as f:
        yaml_content = os.path.expandvars(f.read())
        return yaml.safe_load(yaml_content)


def get_network_interfaces():
    # find the network interfaces present on the system
    interfaces_details = []
    not_real = ['lo', 'docker', 'veth', 'br', 'bond']

    interfaces = subprocess.check_output("ls /sys/class/net", shell=True)
    interfaceString = str(interfaces)
    interfaceString = interfaceString[2:-3]
    interfaces = interfaceString.split('\\n')

    tmp = interfaces.copy()
    for interface in tmp:
        for item in not_real:
            if item in interface: 
                interfaces.remove(interface)
                break

    for interface in interfaces:
        interface_out = subprocess.check_output(["ip", "addr", "show", interface])
        interfaces_output = str(interface_out)
        ip_addr_out = interfaces_output[interfaces_output.find("inet") + 5:]
        ip_addr = ip_addr_out[:ip_addr_out.find(" ")]

        if ip_addr != "":
            interfaces_details.append(ip_addr.split('/')[0])
    return interfaces_details



if __name__ == '__main__':
    labels = read_yaml(file_path)
    key = sys.argv[1]
    result = str()
    if key == 'ips':
        result = str(get_network_interfaces())
    elif key in labels:
        result = str(labels[key])
    if result != "":
        result = result.replace("[", "")
        result = result.replace("]", "")
    print(result.lower())
