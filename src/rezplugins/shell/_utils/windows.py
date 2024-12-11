# SPDX-License-Identifier: Apache-2.0
# Copyright Contributors to the Rez Project


import os
import re


def get_syspaths_from_registry():
    # Local import to avoid import errors on non-windows systems.
    import winreg

    paths = []

    path_query_keys = (
        (winreg.HKEY_LOCAL_MACHINE, 'SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Environment'),
        (winreg.HKEY_CURRENT_USER, 'Environment')
    )

    for root_key, sub_key in path_query_keys:
        try:
            with winreg.OpenKey(root_key, sub_key) as key:
                reg_value, _ = winreg.QueryValueEx(key, 'Path')
        except OSError:
            # Key does not exist
            pass
        else:
            expanded_value = winreg.ExpandEnvironmentStrings(reg_value)
            paths.extend(expanded_value.split(os.pathsep))

    return [x for x in paths if x]
