import os
from os import DirEntry
from pathlib import Path
import re
from collections import defaultdict
from dataclasses import dataclass
from itertools import chain
from enum import Enum
import logging
from typing import Sequence, cast

from .config_files import DirConfig, ConfigFiles


_LOG = logging.getLogger(__name__)


class GroupType(Enum):
    """Define the file group types."""
    MUST_PROTECT = 0
    MAY_WORK_ON = 1


@dataclass
class _Group():
    typ: GroupType

    dirs: dict[str, Path]

    files: dict[str, DirEntry]
    symlinks: dict[str, DirEntry]
    symlinks_by_abs_points_to: dict[str, list[DirEntry]]

    # For stats only
    num_directories: int = 0
    num_directory_symlinks: int = 0

    def add_entry_match(self, entry: DirEntry):
        """Abstract, but abstract and dataclass does not work with mypy. https://github.com/python/mypy/issues/500"""

@dataclass
class _IncludeMatchGroup(_Group):
    include: re.Pattern|None = None

    def add_entry_match(self, entry: DirEntry):
        if not self.include:
            self.files[entry.path] = entry
            return

        match = self.include.match(entry.name)
        _LOG.debug(" - include %s, match %s", self.include, match)

        if match:
            self.files[entry.path] = entry


@dataclass
class _ExcludeMatchGroup(_Group):
    exclude: re.Pattern|None = None

    def add_entry_match(self, entry: DirEntry):
        if not self.exclude:
            self.files[entry.path] = entry
            return

        match = self.exclude.match(entry.name)
        _LOG.debug(" - exclude %s, match %s", self.exclude, match)

        if not match:
            self.files[entry.path] = entry


class FileGroups():
    """Create six different groups of regular files and symlinks by collecting files under specified directories.

    Note that directory symlinks are followed for the specified arguments!, but never for any subdirectories.

    Config Files
    See `config_files` for description of config file format and arguments.

    Arguments:
        protect_dirs_seq: Directories in which (regular) files may not be deleted/modified.
            Directory may be a subdirectory of (or the same, for convenient globbing) as a work_dirs_seq directory.

        work_dirs_seq: Directories in which to potentially delete/rename/modify files.
            Directory may be a subdirectory of (or the same, for convenient globbing) as a protect_dirs_seq directory.

        protect_exclude: Exclude files matching regex in the protected files (does not apply to symlinks). Default: Include ALL.
            Note: Since these files are excluded from protection, it means they er NOT protected!
        work_include: ONLY include files matching regex in the may_work_on files (does not apply to symlinks). Default: Include ALL.

        config_files: Load config files. See config_files.ConfigFiles. Note that the default 'None' means use the `config_files.ConfigFiles` class with default arguments.
    """

    def __init__(
            self,
            protect_dirs_seq: Sequence[Path], work_dirs_seq: Sequence[Path],
            *,
            protect_exclude: re.Pattern|None = None, work_include: re.Pattern|None = None,
            config_files: ConfigFiles|None = None):
        super().__init__()

        self.config_files = config_files or ConfigFiles()
        self.config_files.load_config_dir_files()

        # Turn all paths into absolute paths with symlinks resolved, keep referrence to original argument for messages
        protect_dirs: dict[str, Path] = {os.path.abspath(os.path.realpath(kp)): kp for kp in protect_dirs_seq}

        work_dirs: dict[str, Path] = {}
        for input_work_dir in work_dirs_seq:
            real_dp = os.path.abspath(os.path.realpath(input_work_dir))
            if real_dp in protect_dirs:
                specified_protect_dir = protect_dirs[real_dp]

                if input_work_dir == specified_protect_dir:
                    _LOG.info("Ignoring 'work' dir '%s' which is also a 'protect' dir.", input_work_dir)
                    continue

                _LOG.info("Ignoring 'work' dir '%s' (from argument '%s') which is also a 'protect' dir (from argument '%s').", real_dp, input_work_dir, specified_protect_dir)
                continue

            work_dirs[real_dp] = input_work_dir

        self.must_protect = _ExcludeMatchGroup(GroupType.MUST_PROTECT, protect_dirs, {}, {}, defaultdict(list), exclude=protect_exclude)
        self.may_work_on = _IncludeMatchGroup(GroupType.MAY_WORK_ON, work_dirs, {}, {}, defaultdict(list), include=work_include)

        self.collect()

    def collect(self) -> None:
        """Split files into groups.

        E.g.:

            Given:

            top/d1
            top/d1/d1
            top/d1/d1/f1.jpg
            top/d1/d1/f2.jpg
            top/d1/d1/f2.JPG
            top/d1/d2
            top/d1/d2/f1.jpg
            top/d1/d2/f2.jpg
            top/d1/f1.jpg
            top/d1/f2.jpg
            top/d2
            top/d2/d1
            top/d2/d1/f1.jpg

            When: work_dirs_seq is [top, top/d1/d1]
            And: protect_dirs_seq is [top/d1]

            Then:

            Must protect:
            top/d1/d2/f1.jpg
            top/d1/d2/f2.jpg
            top/d1/f1.jpg
            top/d1/f2.jpg

            May work_on:
            top/d1/d1/f1.jpg
            top/d1/d1/f2.jpg
            top/d1/d1/f2.JPG
            top/d2/d1/f1.jpg

        This is called from __init__(), so there would normally be no need to call this explicitly.
        """

        checked_dirs: set[str] = set()

        def handle_entry(abs_dir_path: str, group: _Group, other_group: _Group, dir_config: DirConfig, entry: DirEntry):
            """Put entry in  the correct group. Call 'find_group' if entry is a directory."""
            if group.typ is GroupType.MAY_WORK_ON:
                # Check for match against configured protect patterns, if match, then the file must got to protect group instead
                pattern = dir_config.is_protected(entry)
                if pattern:
                    _LOG.debug("find %s - '%s' is protected by regex %s, assigning to group %s instead.", group.typ.name, entry.path, pattern, other_group.typ.name)
                    group, other_group = other_group, group

            if entry.is_dir(follow_symlinks=False):
                if entry.path in other_group.dirs:
                    _LOG.debug("find %s - '%s' is in '%s' dir list and not in '%s' dir list", group.typ.name, entry.path, other_group.typ.name, group.typ.name)
                    find_group(entry.path, other_group, group, dir_config)
                    return

                find_group(entry.path, group, other_group, dir_config)
                return

            if entry.name in self.config_files.conf_file_names:
                return

            if entry.is_symlink():
                # cast: https://github.com/python/mypy/issues/11964
                points_to = os.readlink(cast(str, entry))
                abs_points_to = os.path.normpath(os.path.join(abs_dir_path, points_to))

                if entry.is_dir(follow_symlinks=True):
                    _LOG.debug("find %s - '%s' -> '%s' is a symlink to a directory - ignoring", group.typ.name, entry.path, points_to)
                    group.num_directory_symlinks += 1
                    return

                group.symlinks[entry.path] = entry
                group.symlinks_by_abs_points_to[abs_points_to].append(entry)
                return

            _LOG.debug("find %s - entry name: %s", group.typ.name, entry.name)
            group.add_entry_match(entry)

        def find_group(abs_dir_path: str, group: _Group, other_group: _Group, parent_conf: DirConfig|None):
            """Recursively find all files belonging to 'group'"""
            _LOG.debug("find %s: %s", group.typ.name, abs_dir_path)
            if abs_dir_path in checked_dirs:
                _LOG.debug("directory already checked")
                return

            group.num_directories += 1
            dir_config = self.config_files.dir_config(Path(abs_dir_path), parent_conf)

            for entry in os.scandir(abs_dir_path):
                handle_entry(abs_dir_path, group, other_group, dir_config, entry)

            checked_dirs.add(abs_dir_path)

        for any_dir in sorted(chain(self.must_protect.dirs, self.may_work_on.dirs), key=lambda dd: len(Path(dd).parts)):
            parent_dir = Path(any_dir)
            while len(parent_dir.parts) > 1:
                parent_conf = self.config_files.per_dir_configs.get(parent_dir)
                if parent_conf:
                    break

                parent_dir = parent_dir.parent
            else:
                parent_conf = None

            if any_dir in self.must_protect.dirs:
                find_group(any_dir, self.must_protect, self.may_work_on, parent_conf)
            else:
                find_group(any_dir, self.may_work_on, self.must_protect, parent_conf)

    def dump(self):
        """Log collected files. This may be A LOT of output for large directories."""

        log = _LOG.getChild("dump")
        lvl = logging.DEBUG
        if not log.isEnabledFor(lvl):
            return

        log.log(lvl, "")

        log.log(lvl, "must protect:")
        for path in self.must_protect.files:
            log.log(lvl, "%s", path)
        log.log(lvl, "")

        log.log(lvl, "must protect symlinks:")
        for path in self.must_protect.symlinks:
            log.log(lvl, "%s -> %s", path, os.readlink(path))
        log.log(lvl, "")

        log.log(lvl, "must protect symlinks by absolute points to:")
        for abs_points_to, lnks in self.must_protect.symlinks_by_abs_points_to.items():
            log.log(lvl, "%s -> %s", lnks, abs_points_to)
        log.log(lvl, "")

        log.log(lvl, "may work on:")
        for path in self.may_work_on.files:
            log.log(lvl, "%s", path)
        log.log(lvl, "")

        log.log(lvl, "may work on symlinks:")
        for path in self.may_work_on.symlinks:
            log.log(lvl, "%s -> %s", path, os.readlink(path))
        log.log(lvl, "")

        log.log(lvl, "may work on symlinks by absolute points to:")
        for abs_points_to, lnks in self.may_work_on.symlinks_by_abs_points_to.items():
            log.log(lvl, "%s -> %s", lnks, abs_points_to)
        log.log(lvl, "")

        log.log(lvl, "")

    def stats(self):
        """Log collection numbers."""
        log = _LOG.getChild("stats")
        lvl = logging.INFO
        if not log.isEnabledFor(lvl):
            return

        log.log(lvl, "collected protect_directories: %s", self.must_protect.num_directories)
        log.log(lvl, "collected protect_directory_symlinks: %s", self.must_protect.num_directory_symlinks)
        log.log(lvl, "collected work_on_directories: %s", self.may_work_on.num_directories)
        log.log(lvl, "collected work_on_directory_symlinks: %s", self.may_work_on.num_directory_symlinks)

        log.log(lvl, "collected must_protect_files: %s", len(self.must_protect.files))
        log.log(lvl, "collected must_protect_symlinks: %s", len(self.must_protect.symlinks))
        log.log(lvl, "collected may_work_on_files: %s", len(self.may_work_on.files))
        log.log(lvl, "collected may_work_on_symlinks: %s", len(self.may_work_on.symlinks))
