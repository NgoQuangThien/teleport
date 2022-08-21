# TELEPORT
##	Create role
```
kind: role
metadata:
  name: owner_access
spec:
  allow:
    logins:
    - root
    node_labels:
      owner: '{{external.owner}}'
    rules:
    - resources:
      - event
      verbs:
      - list
      - read
    - resources:
      - session
      verbs:
      - read
      - list
      where: contains(session.participants, user.metadata.name)
  deny:
    logins:
    - guest
  options:
    cert_format: standard
    create_host_user: false
    desktop_clipboard: true
    desktop_directory_sharing: true
    enhanced_recording:
    - command
    - network
    forward_agent: false
    max_session_ttl: 24h0m0s
    pin_source_ip: false
    port_forwarding: true
    record_session:
      default: best_effort
      desktop: true
version: v5
```
```
kind: role
metadata:
  name: groups_access
spec:
  allow:
    logins:
    - '{{internal.logins}}'
    node_labels:
      groups: '{{external.servers_groups}}'
    rules:
    - resources:
      - event
      verbs:
      - list
      - read
    - resources:
      - session
      verbs:
      - read
      - list
      where: contains(session.participants, user.metadata.name)
  deny:
    logins:
    - guest
  options:
    cert_format: standard
    create_host_user: false
    desktop_clipboard: true
    desktop_directory_sharing: true
    enhanced_recording:
    - command
    - network
    forward_agent: false
    max_session_ttl: 24h0m0s
    pin_source_ip: false
    port_forwarding: true
    record_session:
      default: best_effort
      desktop: true
version: v5
```
```
kind: role
metadata:
  name: ips_access
spec:
  allow:
    logins:
    - '{{internal.logins}}'
    node_labels:
      ips: '{{external.ips}}'
    rules:
    - resources:
      - event
      verbs:
      - list
      - read
    - resources:
      - session
      verbs:
      - read
      - list
      where: contains(session.participants, user.metadata.name)
  deny:
    logins:
    - guest
  options:
    cert_format: standard
    create_host_user: false
    desktop_clipboard: true
    desktop_directory_sharing: true
    enhanced_recording:
    - command
    - network
    forward_agent: false
    max_session_ttl: 24h0m0s
    pin_source_ip: false
    port_forwarding: true
    record_session:
      default: best_effort
      desktop: true
version: v5
```
##	Set user traits (on console of Teleport master)
```
tctl get user/<user_name> > user.yaml
```
```
vim user.yaml
```
####	Add the following below the "spec" field (edit content as desired)
```
  traits:
    logins:
    - ubuntu
    owner:
    - test
    servers_groups:
    - k8s
    ips:
    - 10.10.0.200
```
```
tctl create -f user.yaml
```