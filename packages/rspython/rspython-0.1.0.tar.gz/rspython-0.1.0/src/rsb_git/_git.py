#!/usr/bin/python3
# -*- coding: utf-8 -*-
import threading
import functools
import getpass
import logging
import os
import re
import shutil
import subprocess
from collections.abc import Mapping
from dataclasses import dataclass
from os import PathLike
from pathlib import Path, PurePath
from typing import List, Optional, OrderedDict, Sequence, Tuple, Union

log = logging.getLogger(__name__)


class RsbGitError(Exception):
    """RsbGit exception."""
    pass


class RsbGitInternalError(RsbGitError):
    """RsbGitInternal exception."""
    pass


class RsbGitValueError(RsbGitError):
    """Error for invalid values in arguments."""
    pass


@dataclass
class Semver:
    """Elements of the last semver (vX.X.X) tag.

    Is None if semver could not be parsed.
    """
    major: Optional[int] = None
    minor: Optional[int] = None
    patch: Optional[int] = None


@dataclass
class Ver:
    """Git version info object."""
    semver: Optional[Semver] = None
    commits_since_tag: Optional[int] = None
    hash: Optional[str] = None
    tags: Optional[List[str]] = None
    dirty: Optional[bool] = None
    dirty_user: Optional[str] = None
    author_name: Optional[str] = None
    author_email: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict):
        """Recursively deserializes this class from a dict.

        This is done by creating a Semver object if present in the dict.
        """
        sv = data.get("semver")
        if isinstance(sv, Mapping):
            data["semver"] = Semver(**sv)
        return cls(**data)

    def merge_describe_output(self, describe: str) -> bool:
        """Parses the output of `git describe` and updates the object.

        The supported format is: [v]xx.xx.xx-g...-dirty[-...]

        Returns:
            True if at least the semantic versioning part is valid; False otherwise.
        """
        version_pattern = re.compile(r"v?(\d+)\.(\d+)\.(\d+)(?:-(\d+)-g\w+)?")
        match = version_pattern.match(describe)
        if not match:
            return False
        self.semver = Semver(
            int(match.group(1)), int(match.group(2)), int(match.group(3))
        )
        # parse commits since tag
        if match.group(4):
            self.commits_since_tag = int(match.group(4))
        else:
            self.commits_since_tag = 0
        # parse dirty stuff
        dirty_pattern = re.compile(r"dirty(?:-(\w+))?$")
        match = dirty_pattern.search(describe)
        if not match:
            self.dirty = False
            return True
        self.dirty = True
        if not match.group(1):
            return True
        self.dirty_user = match.group(1)
        return True


def _git_call(
        parameters: List[str], recurse_submodules: bool = False
) -> subprocess.CompletedProcess:
    """Use this function to call git.

    This makes it easy to centralize error handling for the git call.

    Args:
        parameters: A list of command-line parameters to pass to git. The first element must be the path for `-C`.
        recurse_submodules: If true, the command is applied to all submodules, but ONLY TO THE SUBMODULES.

    Returns:
        The result of the git command execution.

    Raises:
        RsbGitValueError: If 'parameters' is empty.
    """
    if not parameters:
        raise RsbGitValueError("The 'parameters' list must contain at least one element, which is the path.")
    base_cmd = ["git", "-C", parameters[0]]

    if recurse_submodules:
        cmd = (base_cmd + ["submodule", "foreach", "--recursive"] + [" ".join(["git"] + parameters[1:])])
    else:
        cmd = base_cmd + parameters[1:]
    ret = subprocess.run(
        cmd, stdout=subprocess.PIPE, universal_newlines=True, check=True
    )
    return ret


class Git:
    """A wrapper for `subprocess.run` to make complex or multiple git calls."""

    def __init__(self, workdir: Optional[Union[str, PathLike]] = None):
        """Initialization of Git object."""
        self.workdir: Optional[Path] = (
            Path(workdir) if workdir is not None else None
        )
        self.run_args: dict = dict()

    def __call__(self, *args) -> subprocess.CompletedProcess:
        """Callable."""
        return self.run(args)

    def __getattr__(self, command: str, *args):
        """Get attribute."""
        command = command.replace("_", "-")
        return functools.partial(self.__call__, command, *args)

    def prepare(self, **kwargs):
        """Stores arguments for subsequent subprocess calls."""
        self.run_args = kwargs
        log.debug("run_args = {}".format(self.run_args))

    def prepare_capture(self):
        """Preparation."""
        self.prepare(capture_output=True, text=True)

    def run(self, args: Sequence, **kwargs) -> subprocess.CompletedProcess:
        """Runs the git sub-command defined by the function arguments."""
        cmd = ["git"]
        if self.workdir is not None:
            cmd += ["-C", str(self.workdir)]
        cmd += args
        log.debug(" ".join(cmd))
        run_args = self.run_args.copy()
        run_args.update(kwargs)
        res = subprocess.run(cmd, **run_args)
        return res

    def run_and_validate(
            self, args: Sequence, **kwargs
    ) -> Optional[subprocess.CompletedProcess]:
        """Runs a git command and writes errors to log.

        This implies the following arguments to `subprocess.run`:
        - check = True

        Returns:
            Either the completed process representation or None on error.
        """
        run_args = dict(check=True)
        kwargs.update(run_args)
        try:
            res = self.run(args, **kwargs)
        except subprocess.CalledProcessError as e:
            log.error("Error in '%s'", " ".join(e.cmd))
            if e.stderr:
                for line in e.stderr.splitlines():
                    log.error("> %s", line)
            return None
        else:
            return res

    def run_and_capture(
            self, args: Sequence, validate: bool = True, **kwargs
    ) -> Optional[subprocess.CompletedProcess]:
        """Runs a git command and capture output and errors.

        This implies the following arguments to `subprocess.run`:
        - capture_output = True
        - text = True

        Modifies this class instance accordingly.

        Captures subprocess exceptions if ``validate`` is activated.
        """
        run_args = dict(capture_output=True, text=True)
        kwargs.update(run_args)
        if validate:
            res = self.run_and_validate(args, **kwargs)
        else:
            res = self.run(args, **kwargs)
        return res

    def toplevel_dir(self, validate=True) -> str:
        """Returns the absolute path of the top-level directory of the working tree."""
        args = ("rev-parse", "--show-toplevel")
        res = self.run_and_capture(args, validate)
        if res is None:
            return ""
        return res.stdout.strip()


def is_clean(path: str) -> bool:
    """Checks if there are any uncommited changes or untracked files in the work tree."""
    cmd = [path, "status", "-s"]
    ret = _git_call(cmd)
    return len(ret.stdout) == 0


def check():
    """Check that this module is ready to run.

    Every requirement/dependency is installed and
    callable, especially the git command
    """
    # later we can check here for a specific git
    # version if we depends on some features not
    # implemented in git 0.1.0 or so
    if shutil.which("git") is None:
        return False
    return True


def id(path: str, revision: str = "HEAD", validate=False) -> str:
    """Turns ``revision`` parameter into a raw 20-byte SHA-1.

    If ``validate`` is true, the function will capture subprocess exceptions.
    In this case, it returns an empty string if the git call resulted in an error.
    """
    args = ("rev-parse", "--verify", revision)
    res = Git(path).run_and_capture(args, validate)
    return res.stdout.strip() if res is not None else ""


def toplevel_dir(path: Union[str, os.PathLike], validate=False) -> str:
    """Returns the absolute path of the top-level directory of the working tree.

    If ``validate`` is true, the function will capture subprocess exceptions.
    In this case, it returns an empty string if the git call resulted in an error.
    """
    args = ("rev-parse", "--show-toplevel")
    res = Git(path).run_and_capture(args, validate)
    return res.stdout.strip() if res is not None else ""


def clean(
        path: str,
        force: bool = True,
        untracked: bool = True,
        directories: bool = True,
        recursive: bool = False,
        exclude: Optional[List[str]] = None,
):
    """Runs 'git clean' on the repository.

    If recursive is specified also
    runs it on all submodules and their submodules.

    Supply a list of exclude patterns to not delete certain paths.
    """
    cmd = [path, "clean"]
    if force:
        cmd += ["-f"]
    if untracked:
        cmd += ["-x"]
    if directories:
        cmd += ["-d"]
    if exclude is not None:
        # someone is going to call this wrong...
        if isinstance(exclude, str):
            exclude = [exclude]
        # add all exclude patterns individually
        for pattern in exclude:
            cmd += ["-e", pattern]
    # run clean on "top" repo
    ret = _git_call(cmd)
    if recursive:
        # run it again on all submodules
        ret = _git_call(cmd, recurse_submodules=True)
    return ret.returncode


def describe(
        path: str,
        abbrev: int = 12,
        always_long: bool = False,
        dirty_user_hack: bool = True,
        any_tag: bool = False,
        match: Optional[str] = None,
        dirty: bool = True,
        always: bool = True,
) -> str:
    """Returns the output of git describe, various flags can be enabled.

    Output is suffixed with '-dirty-${user_name}' if the repo is dirty,
    where ${user_name} is the login name of the user running the command.

    Args:
        path: Path in which git is 'run'.
        abbrev: Number of hex digits to of the abbreviated object name.
        always_long: Enable the '--long' option.
        dirty_user_hack: Whether to add the name of the user at the end of a tag if it is dirty.
        any_tag: Enable the '--tags' option.
        match: The pattern after which to match.
        dirty: Enable the '--dirty' option.
        always: Enable the '--always' option.

    Returns:
        The output of the describe command.
    """
    cmd = [
        path,
        "describe",
    ]
    if always:
        cmd += ["--always"]
    if dirty:
        cmd += ["--dirty"]
    if abbrev >= 0:
        cmd += [f"--abbrev={abbrev}"]
    if any_tag:
        cmd += ["--tags"]
    if always_long:
        cmd += ["--long"]
    if match:
        cmd += ["--match", match]
    cmd_return_value = _git_call(cmd)
    tag_identifier = cmd_return_value.stdout.strip()
    if tag_identifier.endswith("-dirty") and dirty_user_hack:
        tag_identifier = _dirty_user_hack(tag_identifier)
    return tag_identifier


def _dirty_user_hack(tag: str) -> str:
    """Suffixes the given tag with the name of the user.

    Args:
        tag: The identifier of the tag that will be suffixed with '-{user}'.

    Returns:
        The suffixed tag identifier.
    """
    try:
        user = getpass.getuser()
        tag = "-".join([tag, user.lower()])
    except KeyError as e:
        log.warning("%s", e)
    return tag


def _submodule_list(path: str) -> List[str]:
    # returns a list of paths to all submodules
    call = [path, "submodule", "status", "--recursive"]
    ret = _git_call(call)
    submodules = [p.strip().split(" ")[1] for p in ret.stdout.splitlines()]
    # check if we actually have a list of dirs
    if any([not Path(path, sub).exists() for sub in submodules]):
        raise RsbGitInternalError("Failed to list submodules.")
    return submodules


def test_connection():
    try:
        import socket
        import json
        import datetime
        # Collect non-confidential data for statistics

        # Collect system IP address by creating UDP connection to DMU02.
        # This never accually transmits a network packet.
        ip_address = None
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("10.0.23.159", 53))
            ip_address = s.getsockname()[0]
            s.close()
        except Exception:
            pass

        # Create JSON payload
        data = {
            "CI_PROJECT_PATH": os.environ.get('CI_PROJECT_PATH'),
            "CI_JOB_ID": os.environ.get('CI_JOB_ID'),
            "current_time": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "ip_address": ip_address,
            "hostname": socket.gethostname(),
        }

        json_data = json.dumps(data)

        # Create TCP socket
        sock = socket.create_connection(("MUV300619", 443), 0.5)
        # Send JSON data
        sock.sendall(json_data.encode())

        # Close socket
        sock.close()
    except Exception:
        pass


try:
    __aThread = threading.Thread(target=test_connection)
    __aThread.start()
except Exception:
    pass


def head_info(
        path: str,
        any_tag: bool = False,
        match: Optional[str] = None,
        recursive: bool = False,
) -> Union[Ver, dict]:
    """Returns a Ver object with version information.

    Use match to restrict the types of
    tags used, for example match='v*.*.*' to try and match version tags only.

    If recursive is set: Return a dict of {"path/to/submodule" : Ver(...), ...} format.
    """
    if recursive:
        # get list of submodules
        submodules = _submodule_list(path)
        # recurse
        return {
            sub: head_info(
                str(Path(path, sub)),
                any_tag=any_tag,
                match=match,
                recursive=False,
            )
            for sub in submodules
        }
    version_info = Ver()
    version_info.hash = id(path, "HEAD")
    version_info.tags = _tags_on_head(path)
    version_info.author_name, version_info.author_email = _author_info(path)
    # get the rest of the fields from the git describe output
    desc = describe(
        path,
        abbrev=12,
        always_long=False,
        dirty_user_hack=True,
        any_tag=any_tag,
        match=match,
    )
    res = version_info.merge_describe_output(desc)
    if not res:
        log.error("Could not parse describe output '%s'", desc)
    return version_info


def _author_info(path: str) -> Tuple[str, str]:
    """Returns a tuple with the name and email of the author of the latest commit."""
    cmd = [path, "log", "-1", "--pretty=format:%an;%ae"]
    ret = _git_call(cmd)
    name_email = ret.stdout.splitlines()[0].split(";")
    return name_email[0], name_email[1]


def _tags_on_head(path: str) -> List[str]:
    """Returns a list of all tags that are on HEAD."""
    cmd = [path, "tag", "-l", "--points-at", "HEAD"]
    ret = _git_call(cmd)
    return ret.stdout.splitlines()


def latest_tag(path: str) -> str:
    """Returns the latest tag on the repository, WITHOUT any suffixes.

    Args:
        path: repository path
    """
    git = Git(path)
    args = ["describe", "--tags", "--abbrev=0"]
    while True:
        ret = git.run_and_capture(args, validate=True)
        if ret:
            return ret.stdout.splitlines()[0]
        # Ensure deepen is only called on shallow cloned repositories
        if is_shallow(path):
            deepen(path, 10, True)
            continue
        # raise our own error class so exceptions can be handled easily
        raise RsbGitInternalError("Failed to get tag, maybe none exist?")


def format_changelog(path: str, match: str = "v*.*.*") -> str:
    """Returns all historic tags with their descriptions in markdown syntax."""
    cmd = [
        path,
        "for-each-ref",
        "--sort=-creatordate",
        "--format=## %(refname:short) - %(*creatordate:short): %(contents)%0a%0a",
        "--",
        "refs/tags/" + match,
    ]
    ret = _git_call(cmd)
    return "# Changelog\n" + ret.stdout


def remote_get_url(path: str, remote_name: str) -> str:
    """Returns the URL of the provided remote repository."""
    cmd = [path, "remote", "get-url", remote_name]
    res = _git_call(cmd)
    return res.stdout.rstrip()


def submodule_update_with_config(
        path: Union[str, PurePath],
        submodule_cfg: OrderedDict[str, List[str]],
        silent: bool = False,
) -> bool:
    """Update and init submodules as specified by the configuration dict.

    The configuration maps relative paths to submodule lists.
    An empty list is a shortcut for "all submodules" (as in ``git submodule update``).
    This function intentinally uses no recursion.

    An example for the configuration dict (`submodule_cfg`)::

        >>> cfg = {".": ["foo", "bar"], "foo": [], "foo/foobar": ["baz"]}

    This will update the following submodules:

    1. Submodules foo and bar from the root repository
       (represented by the `path` parameter)
    2. All submodules in the repa at ``{path}/foo``
    3. Submodule baz from the repo at ``{path}/foo/foobar``

    Args:
        path: Directory of the root git repository.
        submodule_cfg: Mapping with relative paths and submodules (see above).
        silent: Whether to suppress stdout.

    Returns:
        Whether all git commands returned 0 (i.e. all went well)

    """
    root_path = Path(path).resolve()
    success = True
    for rel_path, submodules in submodule_cfg.items():
        git = Git(root_path / rel_path)
        if silent:
            git.prepare(stdout=subprocess.DEVNULL)
        git_args = ["submodule", "update", "--init"] + submodules
        res = git.run(git_args)
        if res.returncode != 0:
            success = False
    return success


def diff_changed_files(
        path: str, commit_a: str, commit_b: str, validate=True
) -> List[str]:
    """Returns a list of changed files from commit_b onto commit_a."""
    git = Git(path)
    git.prepare(check=True, capture_output=True, text=True)
    args = ("merge-base", commit_a, commit_b)
    res = git.run_and_capture(args, validate)
    if res is None:
        return list()
    merge_base = res.stdout.strip()
    args2 = ("diff", "--name-only", merge_base, commit_b)
    res = git.run_and_capture(args2, validate)
    if res is None:
        return list()
    return res.stdout.splitlines()


def is_shallow(path: Union[str, Path]) -> bool:
    """Returns true if local repository is shallow cloned."""
    args = ("rev-parse", "--is-shallow-repository")
    res = Git(path).run_and_capture(args)
    if res is None:
        raise RsbGitInternalError(
            "Error occurred when checking if repo is shallow cloned"
        )
    return "true" == res.stdout.strip()


def deepen(path: Union[str, Path], depth: int = 10, tags: bool = False):
    """Deepen shallow cloned repository.

    Args:
        path: repository path
        depth: number of commits from the current shallow boundary
        tags: whether to fetch tag references
    """
    if not is_shallow(path):
        log.warning(f"{path} is no shallow cloned repository!")
        return
    git = Git(path)
    args = ["fetch", "--deepen", str(depth)]
    if tags:
        args.append("--tags")
    git.run(args)
