{%- if pillar.outpost is defined %}
include:
 - outpost.groups
 - outpost.users
{%- endif %}
