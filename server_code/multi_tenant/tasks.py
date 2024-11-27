"""Functions for usertenant app architecture."""

import anvil.tables.query as q
from anvil.tables import app_tables

from ..helpers import print_timestamp


def upsert_role(usertenant, role_name):
    role = app_tables.roles.get(tenant=usertenant["tenant"], name=role_name)
    if not usertenant["roles"]:
        usertenant["roles"] = [role]
    elif role not in usertenant["roles"]:
        usertenant["roles"] = usertenant["roles"] + [role]
    return usertenant


def remove_role(usertenant, role_names):
    usertenant["roles"] = [
        i for i in usertenant["roles"] if i["name"] not in role_names
    ]
    if len(usertenant["roles"]) == 0:
        # Deal with a quirk of empty lists.
        usertenant["roles"] = None
    return usertenant


def populate_permissions(role_dict):
    """Populate the permissions table."""
    print_timestamp("populate_permissions")
    perm_list = []
    for key, val in role_dict.items():
        perm_list = perm_list + val

    perm_list = list(set(perm_list))
    if len(app_tables.permissions.search()) == 0:
        for perm in perm_list:
            app_tables.permissions.add_row(name=perm)


def populate_roles(tenant, role_dict):
    """Some basic roles."""
    print_timestamp("populate_roles")

    for key, val in role_dict.items():
        perm_rows = app_tables.permissions.search(name=q.any_of(*val))
        if len(perm_rows) == 0:
            populate_permissions(role_dict)
            perm_rows = app_tables.permissions.search(name=q.any_of(*val))

        is_it_there = app_tables.roles.get(name=key, tenant=tenant)
        if not is_it_there:
            app_tables.roles.add_row(
                name=key, tenant=tenant, permissions=list(perm_rows), can_edit=False
            )
    return app_tables.roles.search(tenant=tenant)
