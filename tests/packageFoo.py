"""
a minimal package store and accessor
"""

import hotswapping


_package_store = {
    'doom': [
        'doom-1.0', 'doom-1.1', 'doom-1.2'
    ]
}


def _split(package):
    return package.split('-')


def _get_path_for_package(package):
    return '/vol/{}/{}/main.py'.format(*_split(package))


class PackageFoo(hotswapping.DaoI):

    def get_all(self, base_name, **kwargs):
        return _package_store.get(base_name, list())

    def resolve(self, packages):
        return [_get_path_for_package(p) for p in packages]

    def split(self, package):
        return _split(package)

    def compare_packages(self, lhs, rhs):
        if lhs == rhs:
            return 0
        lhs_base_name, lhs_version = (_split(lhs) + ['0'])[:2]
        rhs_base_name, rhs_version = (_split(rhs) + ['0'])[:2]
        if lhs_base_name != rhs_base_name:
            return lhs_base_name > rhs_base_name
        l_v = [int(_) for _ in lhs_version.split('.')]
        r_v = [int(_) for _ in rhs_version.split('.')]
        l_v.extend([0] * (max(len(l_v), len(r_v)) - len(l_v)))
        r_v.extend([0] * (max(len(l_v), len(r_v)) - len(r_v)))
        if l_v == r_v:
            return 0
        return 1 if l_v > r_v else -1
