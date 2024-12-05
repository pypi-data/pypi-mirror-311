
"""
Utils
"""

from crocodile.core import List as L
from crocodile.file_management import P, randstr, PLike
from crocodile.meta import Terminal
# import crocodile.environment as env
import machineconfig
from rich.text import Text
from rich.panel import Panel
from rich.console import Console
from rich.syntax import Syntax
import platform
import subprocess
from typing import Optional, Union, TypeVar, Iterable


LIBRARY_ROOT = P(machineconfig.__file__).resolve().parent  # .replace(P.home().to_str().lower(), P.home().str)
REPO_ROOT = LIBRARY_ROOT.parent.parent
PROGRAM_PATH = (P.tmp().joinpath("shells/python_return_command") + (".ps1" if platform.system() == "Windows" else ".sh")).create(parents_only=True)
CONFIG_PATH = P.home().joinpath(".config/machineconfig")
INSTALL_VERSION_ROOT = CONFIG_PATH.joinpath("cli_tools_installers/versions")
INSTALL_TMP_DIR = P.tmp(folder="tmp_installers")

DEFAULTS_PATH = P.home().joinpath("dotfiles/machineconfig/defaults.ini")


T = TypeVar("T")


def choose_cloud_interactively() -> str:
    print("Listing Remotes ... ")
    tmp = Terminal().run("rclone listremotes").op_if_successfull_or_default(strict_returcode=False)
    # consider this: remotes = Read.ini(P.home().joinpath(".config/rclone/rclone.conf")).sections()
    if isinstance(tmp, str):
        remotes: list[str] = L(tmp.splitlines()).apply(lambda x: x.replace(":", "")).list

    else: raise ValueError(f"Got {tmp} from rclone listremotes")
    if len(remotes) == 0:
        raise RuntimeError("You don't have remotes. Configure your rclone first to get cloud services access.")
    cloud: str=choose_one_option(msg="WHICH CLOUD?", options=list(remotes), default=remotes[0], fzf=True)
    return cloud


def sanitize_path(a_path: P) -> P:
    path = P(a_path)
    if path.as_posix().startswith("/home"):
        if platform.system() == "Windows":  # path copied from Linux to Windows
            path = P.home().joinpath(*path.parts[3:])  # exlcude /home/username
            assert path.exists(), f"File not found: {path}"
            print(f"\n{'--' * 50}\n🔗 Mapped `{a_path}` ➡️ `{path}`\n{'--' * 50}\n")
        elif platform.system() == "Linux" and P.home().as_posix() not in path.as_posix():  # copied from Linux to Linux with different username
            path = P.home().joinpath(*path.parts[3:])  # exlcude /home/username (three parts: /, home, username)
            assert path.exists(), f"File not found: {path}"
            print(f"\n{'--' * 50}\n🔗 Mapped `{a_path}` ➡️ `{path}`\n{'--' * 50}\n")
    elif path.as_posix().startswith("C:"):
        if platform.system() == "Linux":  # path copied from Windows to Linux
            xx = str(a_path).replace("\\", "/")
            path = P.home().joinpath(*P(xx).parts[3:])  # exlcude C:\Users\username
            assert path.exists(), f"File not found: {path}"
            print(f"\n{'--' * 50}\n🔗 Mapped `{a_path}` ➡️ `{path}`\n{'--' * 50}\n")
        elif platform.system() == "Windows" and P.home().as_posix() not in path.as_posix():  # copied from Windows to Windows with different username
            path = P.home().joinpath(*path.parts[2:])
            assert path.exists(), f"File not found: {path}"
            print(f"\n{'--' * 50}\n🔗 Mapped `{a_path}` ➡️ `{path}`\n{'--' * 50}\n")
    return path.expanduser().absolute()


def match_file_name(sub_string: str, search_root: Optional[P] = None) -> P:
    """Look up current directory for file name that matches the passed substring."""
    search_root_obj = search_root if search_root is not None else P.cwd()
    search_root_obj = search_root_obj.absolute()
    print(f"Searching for {sub_string} in {search_root_obj}")

    search_root_objects = search_root_obj.search("*", not_in=["links", ".venv", ".git", ".idea", ".vscode", "node_modules", "__pycache__"])
    search_results: L[P] = L([a_search_root_obj.search(f"*{sub_string}*", r=True) for a_search_root_obj in search_root_objects]).reduce(lambda x, y: x + y)  # type: ignore
    search_results = search_results.filter(lambda x: x.suffix in (".py", ".sh", ".ps1"))

    if len(search_results) == 1:
        path_obj = search_results.list[0]
    elif len(search_results) > 1:
        msg = "Search results are ambiguous or non-existent, choose manually:"
        print(msg)
        choice = choose_one_option(msg=msg, options=search_results.list, fzf=True)
        path_obj = P(choice)
    else:
        # let's do a final retry with sub_string.small()
        sub_string_small = sub_string.lower()
        if sub_string_small != sub_string:
            print("Retrying with small letters")
            return match_file_name(sub_string=sub_string_small)
        from git.repo import Repo
        from git.exc import InvalidGitRepositoryError
        try:
            repo = Repo(search_root_obj, search_parent_directories=True)
            repo_root_dir = P(repo.working_dir)
            if repo_root_dir != search_root_obj:  # may be user is in a subdirectory of the repo root, try with root dir.
                print("Retrying with root repo instea of cwd")
                return match_file_name(sub_string=sub_string, search_root=repo_root_dir)
            else:
                search_root_obj = repo_root_dir
        except InvalidGitRepositoryError:
            pass

        if check_tool_exists(tool_name="fzf"):
            try:
                print("Trying with fd ...")
                fzf_cmd = f"cd '{search_root_obj}'; fd --type f --strip-cwd-prefix | fzf --filter={sub_string}"
                search_res = subprocess.run(fzf_cmd, stdout=subprocess.PIPE, text=True, check=True, shell=True).stdout.split("\n")[:-1]
            except subprocess.CalledProcessError as cpe:
                print(f"Failed at fzf search with {sub_string} in {search_root_obj}.\n{cpe}")
                msg = f"\n{'--' * 50}\n💥 Path {sub_string} does not exist. No search results\n{'--' * 50}\n"
                raise FileNotFoundError(msg) from cpe

            if len(search_res) == 1: return search_root_obj.joinpath(search_res[0])
            else:
                print("Tring with raw fzf search ...")
                try:
                    # res = subprocess.run(f"cd '{search_root_obj}'; fzf --query={sub_string}", check=True, stdout=subprocess.PIPE, text=True, shell=True).stdout.strip()
                    res = subprocess.run(f"cd '{search_root_obj}'; fd | fzf --query={sub_string}", check=True, stdout=subprocess.PIPE, text=True, shell=True).stdout.strip()
                except subprocess.CalledProcessError as cpe:
                    print(f"Failed at fzf search with {sub_string} in {search_root_obj}. {cpe}")
                    msg = f"\n{'--' * 50}\n💥 Path {sub_string} does not exist. No search results\n{'--' * 50}\n"
                    raise FileNotFoundError(msg) from cpe
                return search_root_obj.joinpath(res)

        msg = f"\n{'--' * 50}\n💥 Path {sub_string} does not exist. No search results\n{'--' * 50}\n"
        raise FileNotFoundError(msg)
    print(f"\n{'--' * 50}\n🔗 Matched `{sub_string}` ➡️ `{path_obj}`\n{'--' * 50}\n")
    return path_obj


def choose_one_option(options: Iterable[T], header: str="", tail: str="", prompt: str="", msg: str="",
                      default: Optional[T] = None, fzf: bool=False, custom_input: bool=False) -> T:
    choice_key = display_options(msg=msg, options=options, header=header, tail=tail, prompt=prompt,
                                 default=default, fzf=fzf, multi=False, custom_input=custom_input)
    assert not isinstance(choice_key, list)
    return choice_key


def choose_multiple_options(options: Iterable[T], header: str="", tail: str="", prompt: str="", msg: str="",
                            default: Optional[T] = None, custom_input: bool=False) -> list[T]:
    choice_key = display_options(msg=msg, options=options, header=header, tail=tail, prompt=prompt,
                                 default=default, fzf=True, multi=True,
                                 custom_input=custom_input)
    if isinstance(choice_key, list): return choice_key
    return [choice_key]


def display_options(msg: str, options: Iterable[T], header: str="", tail: str="", prompt: str="",
                    default: Optional[T] = None, fzf: bool=False, multi: bool=False, custom_input: bool=False) -> Union[T, list[T]]:
    # TODO: replace with https://github.com/tmbo/questionary  # also see https://github.com/charmbracelet/gum
    tool_name = "fzf"
    options_strings: list[str] = [str(x) for x in options]
    default_string = str(default) if default is not None else None
    if fzf and check_tool_exists(tool_name):
        from pyfzf.pyfzf import FzfPrompt
        fzf_prompt = FzfPrompt()
        nl = "\n"
        choice_string_multi: list[str] = fzf_prompt.prompt(choices=options_strings, fzf_options=("--multi" if multi else "") + f' --prompt "{prompt.replace(nl, " ")}" ')  # --border-label={msg.replace(nl, ' ')}")
        # --border=rounded doens't work on older versions of fzf installed at Ubuntu 20.04
        if not multi:
            try:
                choice_one_string = choice_string_multi[0]
                choice_idx = options_strings.index(choice_one_string)
                return list(options)[choice_idx]
            except IndexError as ie:
                print(f"{options=}, {choice_string_multi=}")
                print(choice_string_multi)
                raise ie
        choice_idx_s = [options_strings.index(x) for x in choice_string_multi]
        return [list(options)[x] for x in choice_idx_s]
    else:
        console = Console()
        if default is not None:
            assert default in options, f"Default `{default}` option not in options `{list(options)}`"
            default_msg = Text(" <<<<-------- DEFAULT", style="bold red")
        else: default_msg = Text("")
        txt = Text("\n" + msg + "\n")
        for idx, key in enumerate(options):
            txt = txt + Text(f"{idx:2d} ", style="bold blue") + str(key) + (default_msg if default is not None and default == key else "") + "\n"
        txt_panel = Panel(txt, title=header, subtitle=tail, border_style="bold red")
        console.print(txt_panel)
        if default is not None:
            choice_string = input(f"{prompt}\nEnter option number or hit enter for default choice: ")
        else: choice_string = input(f"{prompt}\nEnter option number: ")

        if choice_string == "":
            if default_string is None:
                print("Default option not available!")
                return display_options(msg=msg, options=options, header=header, tail=tail, prompt=prompt, default=default, fzf=fzf, multi=multi, custom_input=custom_input)
            choice_idx = options_strings.index(default_string)
            assert default is not None, "🧨 Default option not available!"
            choice_one: T = default
        else:
            try:
                choice_idx = int(choice_string, base=10)
                choice_one = list(options)[choice_idx]
            except IndexError as ie:  # i.e. converting to integer was successful but indexing failed.
                if choice_string in options_strings:  # string input
                    choice_idx = options_strings.index(choice_one)  # type: ignore #TODO: fix this
                    choice_one = list(options)[choice_idx]
                elif custom_input: return str(choice_string)  # type: ignore #TODO: fix this
                else: raise ValueError(f"Unknown choice. {choice_string}") from ie
            except TypeError as te:  # int(choice_string) failed due to # either the number is invalid, or the input is custom.
                if choice_string in options_strings:  # string input
                    choice_idx = options_strings.index(choice_one)  # type: ignore #TODO: fix this
                    choice_one = list(options)[choice_idx]
                elif custom_input:
                    return choice_string  # type: ignore #TODO: fix this
                else: raise ValueError(f"Unknown choice. {choice_string}") from te
        print(f"{choice_idx}: {choice_one}", "<<<<-------- CHOICE MADE")
        if multi: return [choice_one]
    return choice_one


def symlink_func(this: P, to_this: P, prioritize_to_this: bool=True):
    """helper function. creates a symlink from `this` to `to_this`.
    What can go wrong?
    depending on this and to_this existence, one will be prioretized depending on overwrite value.
    True means this will potentially be overwritten (depending on whether to_this exists or not)
    False means to_this will potentially be overwittten."""
    this = P(this).expanduser().absolute()
    to_this = P(to_this).expanduser().absolute()
    if this.is_symlink(): this.delete(sure=True)  # delete if it exists as symblic link, not a concrete path.
    if this.exists():  # this is a problem. It will be resolved via `overwrite`
        if prioritize_to_this is True:  # it *can* be deleted, but let's look at target first.
            if to_this.exists():  # this exists, to_this as well. to_this is prioritized.
                this.append(f".orig_{randstr()}", inplace=True)  # rename is better than deletion
            else: this.move(path=to_this)  # this exists, to_this doesn't. to_this is prioritized.
        elif prioritize_to_this is False:  # don't sacrefice this, sacrefice to_this.
            if to_this.exists(): this.move(path=to_this, overwrite=True)  # this exists, to_this as well, this is prioritized.   # now we are readly to make the link
            else: this.move(path=to_this)  # this exists, to_this doesn't, this is prioritized.
    else:  # this doesn't exist.
        if not to_this.exists(): to_this.touch()  # we have to touch it (file) or create it (folder)
    try:
        # print(f"Linking {this} ➡️ {to_this}")
        P(this).symlink_to(target=to_this, verbose=True, overwrite=True)
    except Exception as ex: print(f"Failed at linking {this} ➡️ {to_this}.\nReason: {ex}")


def symlink_copy(this: P, to_this: P, prioritize_to_this: bool=True):
    this = P(this).expanduser().absolute()
    to_this = P(to_this).expanduser().absolute()
    if this.is_symlink(): this.delete(sure=True)  # delete if it exists as symblic link, not a concrete path.
    if this.exists():  # this is a problem. It will be resolved via `overwrite`
        if prioritize_to_this is True:  # it *can* be deleted, but let's look at target first.
            if to_this.exists():  # this exists, to_this as well. to_this is prioritized.
                this.append(f".orig_{randstr()}", inplace=True)  # rename is better than deletion
            else: this.move(path=to_this)  # this exists, to_this doesn't. to_this is prioritized.
        elif prioritize_to_this is False:  # don't sacrefice this, sacrefice to_this.
            if to_this.exists(): this.move(path=to_this, overwrite=True)  # this exists, to_this as well, this is prioritized.   # now we are readly to make the link
            else: this.move(path=to_this)  # this exists, to_this doesn't, this is prioritized.
    else:  # this doesn't exist.
        if not to_this.exists(): to_this.touch()  # we have to touch it (file) or create it (folder)
    try:
        to_this.copy(path=this, overwrite=True, verbose=True)
    except Exception as ex: print(f"Failed at linking {this} ➡️ {to_this}.\nReason: {ex}")


def get_shell_script_executing_python_file(python_file: str, func: Optional[str] = None, ve_name: str="ve", strict_execution: bool=True):
    if func is None: exec_line = f"""python {python_file}"""
    else: exec_line = f"""python -m fire {python_file} {func}"""
    shell_script = f"""
. $HOME/scripts/activate_ve {ve_name}
echo "Executing {exec_line}"
{exec_line}
deactivate || true
"""

    if strict_execution:
        if platform.system() == "Windows": shell_script = """$ErrorActionPreference = "Stop" """ + "\n" + shell_script
        if platform.system() == "Linux": shell_script = "set -e" + "\n" + shell_script

    if platform.system() == "Linux": shell_script = "#!/bin/bash" + "\n" + shell_script  # vs #!/usr/bin/env bash
    return shell_script


def get_shell_script(shell_script: str):
    if platform.system() == "Linux": suffix = ".sh"
    elif platform.system() == "Windows": suffix = ".ps1"
    else: raise NotImplementedError(f"Platform {platform.system()} not implemented.")
    shell_file = P.tmp().joinpath("tmp_scripts", "shell", randstr() + suffix).create(parents_only=True).write_text(shell_script)
    return shell_file


def get_shell_file_executing_python_script(python_script: str, ve_name: str, verbose: bool=True):
    if verbose:
        python_script = f"""
code = r'''{python_script}'''
try:
    from machineconfig.utils.utils import print_code
    print_code(code=code, lexer="python", desc="Python Script")
except ImportError: print(code)
""" + python_script
    python_file = P.tmp().joinpath("tmp_scripts", "python", randstr() + ".py").create(parents_only=True).write_text(python_script)
    shell_script = get_shell_script_executing_python_file(python_file=python_file.to_str(), ve_name=ve_name)
    shell_file = get_shell_script(shell_script)
    return shell_file


def write_shell_script(program: str, desc: str="", preserve_cwd: bool=True, display: bool=True, execute: bool=False):
    if preserve_cwd:
        if platform.system() == "Windows":
            program = "$orig_path = $pwd\n" + program + "\ncd $orig_path"
        else:
            program = 'orig_path=$(cd -- "." && pwd)\n' + program + '\ncd "$orig_path" || exit'
    if display:
        print(f"Executing {PROGRAM_PATH}")
        print_code(code=program, lexer="shell", desc=desc)
    PROGRAM_PATH.create(parents_only=True).write_text(program)
    if execute:
        Terminal().run(f". {PROGRAM_PATH}", shell="powershell").print_if_unsuccessful(desc="Executing shell script", strict_err=True, strict_returncode=True)
    return None


def print_code(code: str, lexer: str, desc: str=""):
    if lexer == "shell":
        if platform.system() == "Windows": lexer = "powershell"
        elif platform.system() == "Linux": lexer = "sh"
        else: raise NotImplementedError(f"lexer {lexer} not implemented for system {platform.system()}")
    console = Console()
    console.print(Panel(Syntax(code=code, lexer=lexer), title=desc), style="bold red")


# def get_latest_version(url: str) -> None:
#     # not yet used, consider, using it.
#     import requests
#     import json
#     url = f"https://api.github.com/repos/{url.split('github.com/')[1]}/releases/latest"
#     # Replace {owner} and {repo} with the actual owner and repository name
#     response = requests.get(url, timeout=10)
#     if response.status_code == 200:
#         data = json.loads(response.text)
#         latest_version = data["tag_name"]
#         print("Latest release version:", latest_version)
#     else: print("Error:", response.status_code)


def check_tool_exists(tool_name: str, install_script: Optional[str] = None) -> bool:
    """This is the CLI equivalent of `install_n_import` function of crocodile. """
    if platform.system() == "Windows":
        tool_name = tool_name.replace(".exe", "") + ".exe"

    if platform.system() == "Windows": cmd = "where.exe"
    elif platform.system() == "Linux": cmd = "which"
    else: raise NotImplementedError(f"platform {platform.system()} not implemented")

    try:
        _tmp = subprocess.check_output([cmd, tool_name], stderr=subprocess.DEVNULL)
        res: bool=True
    except (subprocess.CalledProcessError, FileNotFoundError):
        res = False
    if res is False and install_script is not None:
        print(f"Installing {tool_name} ...")
        Terminal().run(install_script, shell="powershell").print()
        return check_tool_exists(tool_name=tool_name, install_script=None)
    return res


def get_ssh_hosts() -> list[str]:
    from paramiko import SSHConfig
    c = SSHConfig()
    c.parse(open(P.home().joinpath(".ssh/config").to_str(), encoding="utf-8"))
    return list(c.get_hostnames())
def choose_ssh_host(multi: bool=True): return display_options(msg="", options=get_ssh_hosts(), multi=multi, fzf=True)


def check_dotfiles_version_is_beyond(commit_dtm: str, update: bool=False):
    dotfiles_path = str(P.home().joinpath("dotfiles"))
    from git import Repo
    repo = Repo(path=dotfiles_path)
    last_commit = repo.head.commit
    dtm = last_commit.committed_datetime
    from datetime import datetime  # make it tz unaware
    dtm = datetime(dtm.year, dtm.month, dtm.day, dtm.hour, dtm.minute, dtm.second)
    res =  dtm > datetime.fromisoformat(commit_dtm)
    if res is False and update is True:
        print(f"Updating dotfiles because {dtm} < {datetime.fromisoformat(commit_dtm)}")
        from machineconfig.scripts.python.cloud_repo_sync import main
        main(cloud=None, path=dotfiles_path)
    return res


def build_links(target_paths: list[tuple[PLike, str]], repo_root: PLike):
    """Build symboic links from various relevant paths (e.g. data) to `repo_root/links/<name>` to facilitate easy access from
    tree explorer of the IDE.
    """
    target_dirs_filtered: list[tuple[P, str]] = []
    for a_dir, a_name in target_paths:
        a_dir_obj = P(a_dir).resolve()
        if not a_dir_obj.exists():
            a_dir_obj.mkdir(parents=True, exist_ok=True)
        target_dirs_filtered.append((a_dir_obj, a_name))

    import git
    repo = git.Repo(repo_root, search_parent_directories=True)
    root_maybe = repo.working_tree_dir
    assert root_maybe is not None
    repo_root_obj = P(root_maybe)
    tmp_results_root = P.home().joinpath("tmp_results", "tmp_data", repo_root_obj.name)
    tmp_results_root.mkdir(parents=True, exist_ok=True)
    target_dirs_filtered.append((tmp_results_root, "tmp_results"))

    for a_target_path, a_name in target_dirs_filtered:
        links_path = repo_root_obj.joinpath("links", a_name)
        links_path.symlink_to(target=a_target_path)


def wait_for_jobs_to_finish(root: P, pattern: str, wait_for_n_jobs: int, max_wait_minutes: float) -> bool:
    wait_finished: bool=False
    import time
    t0 = time.time()
    while not wait_finished:
        parts = root.search(pattern, folders=False, r=False)
        counter  =  len(parts)
        if counter == wait_for_n_jobs:
            wait_finished = True
            print(f"{counter} Jobs finished. Exiting.")
            return True
        if (time.time() - t0) > 60 * max_wait_minutes:
            print(f"Waited for {max_wait_minutes} minutes. Exiting.")
            return False
        print(f"{counter} Jobs finished. Waiting for {wait_for_n_jobs - counter} / {wait_for_n_jobs} jobs to finish, sleeping for 60 seconds.")
        time.sleep(60)
    return False


if __name__ == '__main__':
    # import typer
    # typer.run(check_tool_exists)
    pass
