import os
import sys
import yaml


file_path = '/etc/teleport.labels'


def read_yaml(path):
    with open(path) as f:
        yaml_content = os.path.expandvars(f.read())
        return yaml.safe_load(yaml_content)


if __name__ == '__main__':
    labels = read_yaml(file_path)
    key = sys.argv[1]
    result = str()
    if key in labels:
        result = str(labels[key]).replace("'", "")
        result = result.replace("[", "")
        result = result.replace("]", "")
        print(result.lower())
    else:
        print()
