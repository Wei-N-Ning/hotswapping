
import importlib
import os
import re
import stat
import sys
import time
import types


class ModuleDescriptor(object):

    def __init__(self):
        self.fs_path = ''
        self.fs_mtime = ''
        self.birth_time = ''
        self.deprecated = True


def create_descriptor_from_fs(path):
    if not os.path.isfile(path):
        return None
    m = ModuleDescriptor()
    m.birth_time = time.time()
    m.fs_mtime = os.stat(path)[stat.ST_MTIME]
    m.fs_path = path
    m.deprecated = False
    return m


class SearchRuleI(object):

    def search(self, m):
        """

        Args:
            m (ModuleDescriptor):

        Returns:
            str: module path
        """
        raise NotImplementedError()


class TimerRuleI(object):

    def retire(self, m):
        """

        Args:
            m (ModuleDescriptor):

        Returns:
            bool: True if the given module descriptor is retired; False otherwise
        """
        raise NotImplementedError()


class NewerSemanticVersion(SearchRuleI):

    def __init__(self, check_existence=False):
        self.check_existence = check_existence

    @staticmethod
    def iter_dir(dir_path):
        for fn in os.listdir(dir_path):
            yield fn, os.path.abspath(os.path.join(dir_path, fn))

    @staticmethod
    def exists(p):
        return os.path.exists(p)

    @staticmethod
    def compare_versions(lhs, rhs):
        regex = '^(\d+)\.(\d+)\.(\d+)$'
        _ = re.match(regex, lhs)
        l = [int(n) for n in _.groups()] if _ is not None else [0, 0, 0]
        _ = re.match(regex, rhs)
        r = [int(n) for n in _.groups()] if _ is not None else [0, 0, 0]
        if l > r:
            return 1
        if l < r:
            return -1
        return 0

    def search(self, m):
        regex = '^(.+)/(\d+\.\d+\.\d+)/(.*)$'
        r = re.match(regex, m.fs_path)
        if r is None:
            return ''
        dir_, ver_, rel_path = r.groups()
        max_ver = ver_
        p_max_ver = ''
        for fn, p in self.iter_dir(dir_):
            if self.compare_versions(fn, max_ver) == 1:
                max_ver = fn
                p_max_ver = p
        if max_ver == ver_:
            return ''
        ret = os.path.abspath(os.path.join(p_max_ver, rel_path))
        if self.check_existence and self.exists(ret) is False:
            return ''
        return ret


class MaxAge(TimerRuleI):

    def __init__(self, max_age):
        self.max_age = max_age

    @staticmethod
    def age(m):
        return time.time() - m.birth_time

    def retire(self, m):
        if self.age(m) >= self.max_age:
            m.deprecated = True
            return True
        return False


def renew(m, search_rule, timer_rule):
    """
    Can modify the incoming module descriptor

    Args:
        m (ModuleDescriptor):
        search_rule (SearchRuleI):
        timer_rule (TimerRuleI):

    Returns:
        ModuleDescriptor: a renewed ModuleDescriptor or None; in the first case the given ModuleDescriptor is marked
            deprecated
    """
    if not timer_rule.retire(m):
        return None

    path = search_rule.search(m)
    if not path:
        m.deprecated = False
        return None

    ret = create_descriptor_from_fs(path)
    if not ret:
        m.deprecated = False
        return None

    return ret


def load(m):
    """
    Can modify the incoming module descriptor

    Args:
        m (ModuleDescriptor):

    Returns:
        types.ModuleType:
    """

    class SysPathManip(object):

        def __init__(self, dir_path):
            self.dir_path = dir_path

        def __enter__(self):
            sys.path.insert(0, self.dir_path)

        def __exit__(self, exc_type, exc_val, exc_tb):
            sys.path = sys.path[1:]

    path = m.fs_path
    search_path = os.path.dirname(path)
    dot_path = os.path.basename(path).replace('.py', '')
    with SysPathManip(search_path):
        try:
            return importlib.import_module(dot_path)
        except Exception, e:
            return None


def unload(m):
    return 0
