import os

from django_python3_ldap.utils import format_search_filters


def group_membership_filter(ldap_fields):
    group = os.environ.get('DJANGO_LDAP_GROUP_MEMBERSHIP', None)
    if group:
        ldap_fields["groupMembership"] = group
    search_filters = format_search_filters(ldap_fields)
    return search_filters
