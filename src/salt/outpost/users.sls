{%- for user in pillar.outpost.users %}
outpost_user_{{ user.username }}:
  user.present:
    - name: {{ user.username }}
    - uid: {{ user.uid }}
    - home: {{ user.homedir }}
    - createhome: true
    - fullname: {{ user.displayname }}
    - gid_from_name: true
    - require:
        - group: outpost_group_{{ user.username }}
    {%- for group in user.groups %}
        - group: outpost_group_{{ group.name }}
    {%- endfor %}
{%- endfor %}
