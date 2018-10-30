{%- for user in pillar.outpost.users %}
outpost_group_{{ user.username }}:
  group.present:
    - name: {{ user.username }}
    - gid: {{ user.uid }}
{%- endfor %}
{%- for group in pillar.outpost.groups %}
outpost_group_{{ group.name }}:
  group.present:
    - name: {{ group.name }}
    - gid: {{ group.gid }}
{%- endfor %}
