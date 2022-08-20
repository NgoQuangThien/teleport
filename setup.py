import os
import yaml


teleport_labels = '/etc/teleport.labels'
teleport_config = '/etc/teleport.yaml'
teleport_exec = '/usr/bin/teleport-labels.py'

IP = yaml.safe_load('''
- name: ip
  command: [hostname, -I]
  period: 1m0s''')

UPTIME = yaml.safe_load('''
- name: uptime
  command: [uptime, -p]
  period: 1m0s''')

OTHER = yaml.safe_load('''
- name: group
  command: [/usr/bin/python3, /usr/bin/teleport-labels.py, groups]
  period: 1m0s

- name: owner
  command: [/usr/bin/python3, /usr/bin/teleport-labels.py, owner]
  period: 1m0s

- name: other
  command: [/usr/bin/python3, /usr/bin/teleport-labels.py, other]
  period: 1m0s''')


def read_yaml(path):
    with open(path) as f:
        yaml_content = os.path.expandvars(f.read())
        return yaml.safe_load(yaml_content)


def write_file(file_path, content):
    with open(file_path, 'w') as f:
        f.write(content)
    return True


if __name__ == '__main__':
    os.system('cp -f teleport.labels {0}'.format(teleport_labels))
    os.system('cp -f teleport-labels.py {0}'.format(teleport_exec))

    config = read_yaml(teleport_config)
    if IP not in config['ssh_service']['commands']:
        config['ssh_service']['commands'].extend(IP)
    if UPTIME not in config['ssh_service']['commands']:
        config['ssh_service']['commands'].extend(UPTIME)
    if OTHER not in config['ssh_service']['commands']:
        config['ssh_service']['commands'].extend(OTHER)

    write_file(teleport_config, yaml.safe_dump(config))

    os.system('systemctl restart teleport.service')
