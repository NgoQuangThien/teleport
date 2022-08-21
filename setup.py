import os
import yaml


teleport_labels = '/etc/teleport.labels'
teleport_config = '/etc/teleport.yaml'
teleport_exec = '/usr/bin/teleport-labels.py'

LABELS = yaml.safe_load('''
- name: uptime
  command: [uptime, -p]
  period: 1m0s

- name: groups
  command: [/usr/bin/python3, /usr/bin/teleport-labels.py, groups]
  period: 1m0s

- name: owner
  command: [/usr/bin/python3, /usr/bin/teleport-labels.py, owner]
  period: 1m0s

- name: ips
  command: [/usr/bin/python3, /usr/bin/teleport-labels.py, ips]
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
    if not os.path.exists(teleport_labels):
        os.system('cp -f teleport.labels {0}'.format(teleport_labels))
    if not os.path.exists(teleport_exec):
        os.system('cp -f teleport-labels.py {0}'.format(teleport_exec))

    config = read_yaml(teleport_config)
    tmp = LABELS.copy()
    for x in tmp:
        for y in config['ssh_service']['commands']:
            if x == y:
                LABELS.remove(x)
                break

    config['ssh_service']['commands'].extend(LABELS)
    write_file(teleport_config, yaml.safe_dump(config))
