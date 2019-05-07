{%- for user in pillar.outpost.users %}
outpost_user_{{ user.username }}:
  user.present:
    - name: {{ user.username }}
    - uid: {{ user.uid }}
    - home: {{ user.homedir }}
    - shell: {{ user.shell }}
    - createhome: true
    - fullname: "{{ user.displayname.decode('utf-8') }}"
    - gid_from_name: true
    {%- if user.groups is defined %}
    - groups:
    {%- for group in user.groups %}
        - {{ group.name }}
    {%- endfor %}
    {%- endif %}
    - require:
        - group: outpost_group_{{ user.username }}
    {%- for group in user.groups %}
        - group: outpost_group_{{ group.name }}
    {%- endfor %}

{%- if user.public_keys is iterable %}
outpost_user_{{ user.username }}_ssh_key:
  ssh_auth.present:
    - user: {{ user.username }}
    - names:
{%- for key in user.public_keys %}
      - {{ key.key }}
{%- endfor %}
    - require:
      - user: outpost_user_{{ user.username }}
{%- endif %}
{%- endfor %}
