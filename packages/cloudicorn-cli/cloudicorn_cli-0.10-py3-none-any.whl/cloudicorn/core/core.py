#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import sys
import yaml
import hcl
import shutil
import time
from fuzzywuzzy import fuzz
import tempfile
from subprocess import Popen, PIPE
import requests
from collections import OrderedDict
import re
import hashlib
import string
import random
from pathlib import Path
from copy import deepcopy
import pkgutil
from base64 import b64encode, b64decode
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes

from git import Repo, Remote, InvalidGitRepositoryError
import time
from datetime import datetime, timedelta


PACKAGE = "cloudicorn"
LOG = True
DEBUG = False

def download_progress(url, filename, w=None):
    if w == None:
        rows, columns = os.popen('stty size', 'r').read().split()
        w = int(columns) - 5

    with open(filename, "wb") as f:
        response = requests.get(url, stream=True)
        total_length = response.headers.get('content-length')

        if total_length is None:  # no content length header
            f.write(response.content)
        else:
            dl = 0
            total_length = int(total_length)
            for data in response.iter_content(chunk_size=4096):
                dl += len(data)
                f.write(data)
                done = int(w * dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (w-done)))
                sys.stdout.flush()

    print("")
    
def list_cloud_extensions():
    for x in ("aws", "azurerm", "opentofu", "gcp"):
        exists = check_cloud_extension(x)
        yield x, exists

def check_cloud_extension(which):

    try:
        pkgutil.resolve_name("cloudicorn_{}".format(which))
        return True
    except:
        return False

        
def get_cloudicorn_cachedir(salt, cleanup=True):
    current_date_slug = datetime.today().strftime('%Y-%m-%d')

    slug = hashlib.sha224("{}{}".format(
        get_random_string(64), salt).encode('utf-8')).hexdigest()
    wdir_root = os.path.expanduser('~/.cache/cloudicorn/')

    wdir_d = os.path.join(wdir_root, current_date_slug)

    if not os.path.isdir(wdir_root):
        os.makedirs(wdir_root)

    if not os.path.isdir(wdir_d):
        # first time today cloudicorn has been run, clean up past cache
        if cleanup:
            clean_cache(wdir_root, 30)

    wdir_p = os.path.join(wdir_d, slug)
    os.makedirs(wdir_p)

    return wdir_p


def get_random_string(length):
    # choose from all lowercase letter
    l1 = string.ascii_lowercase + string.ascii_uppercase
    result_str = ''.join(random.choice(l1) for i in range(length))
    return str(result_str)


def anyof(needles, haystack):
    for n in needles:
        if n in haystack:
            return True

    return False


def hcldump(obj):
    hcls = ""
    for f in hcldumplines(obj):
        hcls = "{}{}".format(hcls, f)

    return hcls


def recursive_dict_set(d, parts, val):
    if len(parts) == 1:
        d[parts[0]] = val
    else:
        if parts[0] not in d:
            d[parts[0]] = {}
            recursive_dict_set(d[parts[0]], parts[1:], val)
            return


class HclDumpException(Exception):
    pass


HCL_KEY_RE = r"^\w+$"


def hcldumplines(obj, recursions=0):
    nextrecursion = recursions+1
    if recursions == 0 and type(obj) != dict:
        raise HclDumpException("Top level object must be a dictionary")

    if type(obj) in (dict,  OrderedDict):
        if recursions > 0:
            yield "   "*(recursions-1)+'{\n'
        for k, v in obj.items():
            if type(k) != str:
                raise HclDumpException(
                    "dictionary keys can only contain letters, numbers and underscores")

            matches = re.findall(HCL_KEY_RE, k)
            if len(matches) == 0:
                raise HclDumpException(
                    "dictionary keys can only contain letters, numbers and underscores")
            yield '{}{} = '.format("   "*recursions, k)
            yield from hcldumplines(v, nextrecursion)
            yield "{}\n".format(" "*recursions)
        if recursions > 0:
            yield "   "*(recursions-1)+'}\n'
    elif type(obj) == list:
        yield '{}['.format(" "*recursions)

        i = 0
        m = len(obj)-1
        while i <= m:
            yield from hcldumplines(obj[i], nextrecursion)
            if i < m:
                yield ","
            i += 1
        yield ']\n'
    elif type(obj) in (int, float):
        yield obj

    elif type(obj) == str:
        yield '"'+obj+'"'


def stylelog(s):
    if type(s) is str:
        s = s.replace("<b>", "\033[1m")
        s = s.replace("<u>", "\033[4m")
        s = s.replace("</u>", "\033[0;0m")
        s = s.replace("</b>", "\033[0;0m")
    return s

def log(s):
    if LOG == True:
        print(stylelog(s))

def debug(s):
    if DEBUG == True:
        print(stylelog(s))


def run(cmd, splitlines=False, env=os.environ, raise_exception_on_fail=False, cwd='.'):
    # you had better escape cmd cause it's goin to the shell as is
    proc = Popen([cmd], stdout=PIPE, stderr=PIPE,
                 universal_newlines=True, shell=True, env=env, cwd=cwd)
    out, err = proc.communicate()
    if splitlines:
        out_split = []
        for line in out.split("\n"):
            line = line.strip()
            if line != '':
                out_split.append(line)
        out = out_split

    exitcode = int(proc.returncode)

    if raise_exception_on_fail and exitcode != 0:
        raise Exception("Running {} resulted in return code {}, below is stderr: \n {}".format(
            cmd, exitcode, err))

    return (out, err, exitcode)


def runshow(cmd, env=os.environ, cwd='.', stdout = sys.stdout, stderr = sys.stderr):
    # you had better escape cmd cause it's goin to the shell as is

    if LOG != True:
        stdout = None
        strerr = None

    proc = Popen([cmd], stdout=stdout, stderr=stderr,
                 shell=True, env=env, cwd=cwd)
    proc.communicate()

    exitcode = int(proc.returncode)

    return exitcode


def flatwalk_up(haystack, needle, bottom_up=True):
    spl = needle.split("/")
    needle_parts = [spl.pop(0)]
    for s in spl:
        add = os.path.join(needle_parts[-1], s)
        needle_parts.append(add)

    needle_parts.insert(0, "")

    if not bottom_up:
        # top down
        needle_parts = sorted(needle_parts, reverse=True)

    for n in needle_parts:
        l = os.listdir(os.path.join(haystack, n))
        for i in sorted(l):
            if os.path.isfile(os.path.join(haystack,n,i)):
                yield (os.path.join(haystack,n), i)


    # for (folder, fn) in results:
    #     debug((folder, fn))
    #     yield (folder, fn)


def flatwalk(path):
    paths = []
    for (folder, b, c) in os.walk(path):
        for fn in c:
            paths.append((folder, fn))
            
    for folder, fn in sorted(paths):
        yield (folder, fn)


def clean_cache(d, olderthan_days=30):
    cutoff = (time.time()) - olderthan_days * 86400
    for fn in os.scandir(d):
        p = os.path.join(d, fn.name)
        if os.path.isdir(p):
            if os.path.getmtime(p) < cutoff:
                shutil.rmtree(p)


def dir_is_git_repo(dir):
    if not os.path.isdir(dir):
        return False
    try:
        repo = Repo(dir)
        return True

    except InvalidGitRepositoryError:
        pass

    return False


def git_rootdir(dir="."):
    if dir_is_git_repo(dir):
        return dir
    else:
        # print (wdir)
        oneup = os.path.abspath(dir+'/../')
        if oneup != "/":
            # print ("trying {}".format(oneup))
            return git_rootdir(oneup)
        else:
            # not a git repository
            return None


def git_check(wdir='.'):

    git_root = git_rootdir(wdir)

    if git_root == None:
        return 0

    f = "{}/.git/FETCH_HEAD".format(os.path.abspath(git_root))

    if os.path.isfile(f):
        '''
         make sure this is not a freshly cloned repo with no FETCH_HEAD
        '''
        last_fetch = int(os.stat(f).st_mtime)
        diff = int(time.time() - last_fetch)
    else:
        # if the repo is a fresh clone, there is no FETCH_HEAD
        # so set time diff to more than a minute to force a fetch
        diff = 61

    repo = Repo(git_root)

    assert not repo.bare

    remote_names = []

    # fetch at most once per minute
    for r in repo.remotes:
        remote_names.append(r.name)
        if diff > 60:
            remote = Remote(repo, r.name)
            remote.fetch()

    # check what branch we're on
    branch = repo.active_branch.name

    origin_branch = None
    for ref in repo.git.branch('-r').split('\n'):
        for rn in remote_names:
            if "{}/{}".format(rn, branch) in ref:
                origin_branch = ref.strip()
                break

    if origin_branch == None:
        # no remote branch to compare to
        return 0

    # check if local branch is ahead and /or behind remote branch
    command = "git -C {} rev-list --left-right --count \"{}...{}\"".format(
        git_root, branch, origin_branch)
    # print command
    (ahead_behind, err, exitcode) = run(command, raise_exception_on_fail=True)
    ahead_behind = ahead_behind.strip().split("\t")
    ahead = int(ahead_behind[0])
    behind = int(ahead_behind.pop())

    if behind > 0:
        sys.stderr.write("")
        sys.stderr.write(
            "GIT ERROR: You are on branch {} and are behind the remote.  Please git pull and/or merge before proceeding.  Below is a git status:".format(branch))
        sys.stderr.write("")
        (status, err, exitcode) = run("git -C {} status ".format(git_root))
        sys.stderr.write(status)
        sys.stderr.write("")
        return (-1)
    else:

        CLOUDICORN_GIT_DEFAULT_BRANCH = os.getenv(
            'CLOUDICORN_GIT_DEFAULT_BRANCH', 'master')

        if branch != CLOUDICORN_GIT_DEFAULT_BRANCH:
            '''
                in this case assume we're on a feature branch
                if the FB is behind master then issue a warning
            '''
            command = "git -C {} branch -vv | grep {} ".format(
                git_root, CLOUDICORN_GIT_DEFAULT_BRANCH)
            (origin_master, err, exitcode) = run(command)
            if exitcode != 0:
                '''
                In this case the git repo does not contain CLOUDICORN_GIT_DEFAULT_BRANCH, so I guess assume that we're 
                on the default branch afterall and that we're up to date persuant to the above code
                '''
                return 0

            for line in origin_master.split("\n"):
                if line.strip().startswith(CLOUDICORN_GIT_DEFAULT_BRANCH):
                    origin = line.strip().split('[')[1].split('/')[0]

            assert origin != None

            command = "git -C {} rev-list --left-right --count \"{}...{}/{}\"".format(
                git_root, branch, origin, CLOUDICORN_GIT_DEFAULT_BRANCH)
            (ahead_behind, err, exitcode) = run(command)
            ahead_behind = ahead_behind.strip().split("\t")
            ahead = int(ahead_behind[0])
            behind = int(ahead_behind.pop())

            command = "git -C {} rev-list --left-right --count \"{}...{}\"".format(
                git_root, branch, CLOUDICORN_GIT_DEFAULT_BRANCH)
            (ahead_behind, err, exitcode) = run(command)
            ahead_behind = ahead_behind.strip().split("\t")
            local_ahead = int(ahead_behind[0])
            local_behind = int(ahead_behind.pop())

            if behind > 0:
                sys.stderr.write("")
                sys.stderr.write("GIT WARNING: Your branch, {}, is {} commit(s) behind {}/{}.\n".format(
                    branch, behind, origin, CLOUDICORN_GIT_DEFAULT_BRANCH))
                sys.stderr.write("This action may clobber new changes that have occurred in {} since your branch was made.\n".format(
                    CLOUDICORN_GIT_DEFAULT_BRANCH))
                sys.stderr.write("It is recommended that you stop now and merge or rebase from {}\n".format(
                    CLOUDICORN_GIT_DEFAULT_BRANCH))
                sys.stderr.write("\n")

                if ahead != local_ahead or behind != local_behind:
                    sys.stderr.write("")
                    sys.stderr.write("INFO: your local {} branch is not up to date with {}/{}\n".format(
                        CLOUDICORN_GIT_DEFAULT_BRANCH, origin, CLOUDICORN_GIT_DEFAULT_BRANCH))
                    sys.stderr.write("HINT:")
                    sys.stderr.write("git checkout {} ; git pull ; git checkout {}\n".format(
                        CLOUDICORN_GIT_DEFAULT_BRANCH, branch))
                    sys.stderr.write("\n")

                answer = input(
                    "Do you want to continue anyway? [y/N]? ").lower()

                if answer != 'y':
                    log("")
                    log("Aborting due to user input")
                    exit()

        return 0


class WrongPasswordException(Exception):
    pass


class MissingEncryptionPassphrase(Exception):
    pass


class NoRemoteState(Exception):
    pass


class RemoteStateKeyNotFound(Exception):
    pass



class ErrorParsingYmlVars(Exception):
    pass


class HclParseException(Exception):
    pass


class Project():

    def __init__(self,
                 git_filtered=False,
                 conf_marker="project.yml",
                 inpattern=".hclt",
                 project_vars={},
                 wdir=None
                 ):

        if wdir == None:
            wdir = os.getcwd()
        self.wdir = wdir
        self.inpattern = inpattern
        self.component_dir = None
        self.vars = None
        self.parse_messages = []
        self.linked_projects = None

        self.components = None
        self.git_filtered = git_filtered
        self.conf_marker = conf_marker
        self.remotestates = None
        # all used to decrypt, first used to re encrypt
        self.passphrases = []
        self.project_vars = project_vars

    @property
    def project_root(self):
        return os.path.abspath(self.wdir)

    # verify that the cwd or wdir contains a project.yml
    def check_project_dir(self):
        f = os.path.join(self.project_root, self.conf_marker)
        if os.path.isfile(f):
            return True
        
        return False
    
    # given a component path, walk up filesystem looking for project.yml
    def find_project_root(self, component=None):
        haystack = self.project_root
        
        if component == None:
            haystack = "/"
            component = self.project_root

        d = os.path.join(haystack, component)
        if os.path.isdir(d):
            # called from outside of project
            for (folder, fn) in flatwalk_up(haystack, component, False):
                if fn == self.conf_marker:
                    apath = os.path.abspath(folder)
                    relpath = os.path.relpath(component, apath)
                    return apath, relpath
        else:
            # called from subdir of project
            apath, relpath = self.find_project_root()
            d = os.path.join(apath, component)
            if os.path.isdir(d):
                return apath, component

        raise ProjectException("Could not find project root given component path {}".format(component))
    
    def set_passphrases(self, passphrases=[]):
        if type(passphrases) == str:
            self.passphrases = [passphrases]
        elif type(passphrases) == list:
            self.passphrases = passphrases
        else:
            raise ProjectException("set_passphrases: must provide a string or list of strings")
        

    def set_tf_dir(self, dir):
        self.tf_dir = dir

    def set_component_dir(self, dir):
        
        self.component_dir = dir
        
        cdir_slug = dir.replace('/', '_')
        tf_wdir_p = get_cloudicorn_cachedir(self.project_root+cdir_slug)

        tf_wdir = '{}/{}'.format(tf_wdir_p, cdir_slug)
        os.makedirs(tf_wdir)

        debug("setting tf_wdir to {}".format(tf_wdir))
        self.set_tf_dir(tf_wdir)

        self.component = None
        self.vars = None

    def check_hclt_file(self, path):
        only_whitespace = True
        with open(path, 'r') as lines:
            for line in lines:
                # debug("##{}##".format(line.strip()))
                if line.strip() != "":
                    only_whitespace = False
                    break
        # debug(only_whitespace)

        if not only_whitespace:
            with open(path, 'r') as fp:
                try:
                    obj = hcl.load(fp)
                except:
                    raise HclParseException(
                        "FATAL: An error occurred while parsing {}\nPlease verify that this file is valid hcl syntax".format(path))

        return only_whitespace

    def check_parsed_file(self, require_tfstate_store_block=False):
        # this function makes sure that self.outstring contains a legit hcl file with a remote state config
        obj = hcl.loads(self.out_string)

        debug(obj)
        required = ["inputs", "source"]

        if require_tfstate_store_block:
            required.append("tfstate_store")

        missing = []
        for r in required:

            try:
                d = obj[r]
            except KeyError:
                missing.append(r)

        if len(missing) > 0:
            return "Component missing block(s): {}.".format(", ".join(missing))

        return True

    def format_hclt_file(self, path):
        log("Formatting {}".format(path))
        only_whitespace = self.check_hclt_file(path)
        if not only_whitespace:
            cmd = "cat \"{}\" | terraform fmt -".format(path)
            (out, err, exitcode) = run(cmd, raise_exception_on_fail=True)

            with open(path, 'w') as fh:
                fh.write(out)

    def example_commands(self, command):
        log("")

        for which, component, match in self.get_components():
            if match:
                s = "{} {} {}".format(PACKAGE, command, component)
                if which == "bundle":
                    s = "{} {} <u><b>{}</u>".format(PACKAGE,
                                                    command, component)

                log(s)
        log("")

   # def get_filtered_components(wdir, filter):

    def get_components(self):
        if self.components == None:
            self.components = []
            filtered = []
            if self.git_filtered:
                (out, err, exitcode) = run(
                    "git status -s -uall", raise_exception_on_fail=True)
                for line in out.split("\n"):
                    p = line.split(" ")[-1]
                    if len(p) > 3:
                        filtered.append(os.path.dirname(p))

            d = self.project_root
            for (dirpath, filename) in flatwalk(d):
                dirpath = dirpath[len(d)+1:]
                if filename in ['component.hclt', "bundle.yml"] and len(dirpath) > 0:
                    which = "component"
                    if filename == "bundle.yml":
                        which = "bundle"
                    if self.git_filtered:
                        match = False
                        for f in filtered:
                            if f.startswith(dirpath):
                                match = True
                                break
                        self.components.append((which, dirpath, match))

                    else:
                        self.components.append((which, dirpath, True))

        return self.components

    def component_type(self, component):
        for which, c, match in self.get_components():
            if c == component:
                return which

        return None

    def get_bundle(self, wdir):
        components = []

        debug("")
        debug("get_bundle wdir {}".format(wdir))

        for c in self.get_components():
            if c[1] == wdir:
                # exclude bundle from self
                continue
            if c[1].startswith(wdir):
                components.append(c[1])

                debug("get_bundle  {}".format(c))
        debug("")
                    
        bundleyml = '{}/{}/{}'.format(self.project_root, wdir, "bundle.yml")

        with open(bundleyml, 'r') as fh:
            d = yaml.load(fh, Loader=yaml.FullLoader)

        try:
            order = d['order']
        except:
            return components

        if type(order) != list:
            return components

        reordered_components = []
        for i in order:
            if "*" not in i:
                # look for exact match
                x = os.path.join(wdir, i)
                if x in components:
                    reordered_components.append(x)
                else:
                    raise ComponentException(f"Batch Error: no such component: {x} (recheck bundle.yml)")

            else:
                for c in components:
                    if c in reordered_components:
                        continue
                    if self.component_type(c) == "component":
                        relpath = c[len(wdir)+1:]

                        match = False
                        if i == relpath:
                            match = True

                        # start and end wildcards
                        elif i[-1] == "*" and i[0] == "*":
                            if i[1:-1] in relpath:
                                match = True

                        elif i[-1] == "*":
                            if relpath.startswith(i[0:-1]):
                                match = True
                        elif i[0] == "*":
                            if relpath.endswith(i[1:]):
                                match = True

                        if match:
                            reordered_components.append(c)
                        

        return reordered_components
    
    def check_hclt_files(self):
        for f in self.get_files():
            debug("check_hclt_files() checking {}".format(f))
            self.check_hclt_file(f)

    def get_files(self):
        # project_root = self.get_project_root(self.component_dir)
        for (folder, fn) in flatwalk_up(self.project_root, self.component_dir):
            if fn.endswith(self.inpattern):
                yield "{}/{}".format(folder, fn)

    def parse_items(self, trynum=0):
        # parse item values
        for k, v in self.vars.items():
            self.vars[k] = self.parse(v)

        problems = []

        for k, v in self.vars.items():
            if "${" in v:
                msg = self.check_parsed_text(v)
                if msg != "":
                    problems.append("File {}, cannot parse value of \"{}\"".format(
                        os.path.relpath(self.var_sources[k]), k))
                    for line in msg.split("\n"):
                        problems.append(line)

        if len(problems) > 0 and trynum < 5:
            return self.parse_items(trynum+1)

        return problems

    def get_yml_vars(self):
        if self.vars == None:
            self.var_sources = {}
            # project_root = self.get_project_root(self.component_dir)
            self.vars = {}
            for (folder, fn) in flatwalk_up(self.project_root, self.component_dir):
                if fn.endswith('.yml'):

                    with open(r'{}/{}'.format(folder, fn)) as fh:
                        d = yaml.load(fh, Loader=yaml.FullLoader)
                        if type(d) == dict:
                            for k, v in d.items():
                                if type(v) in (str, int, float, dict):
                                    self.vars[k] = v
                                    self.var_sources[k] = '{}/{}'.format(
                                        folder, fn)

            # special vars
            self.vars["PROJECT_ROOT"] = self.project_root
            self.vars["COMPONENT_PATH"] = self.component_path
            self.vars["COMPONENT_DIRNAME"] = self.component_path.split("/")[-1]
            try:
                self.vars["CLOUDICORN_INSTALL_PATH"] = os.path.dirname(
                    os.path.abspath(os.readlink(__file__)))
            except OSError:
                self.vars["CLOUDICORN_INSTALL_PATH"] = os.path.dirname(
                    os.path.abspath(__file__))

            problems = self.parse_items()

            if len(problems) > 0:

                for line in problems:
                    if line != "":
                        sys.stderr.write("\n"+line)
                sys.stderr.write("\n")
                sys.stderr.write("\n")
                raise ErrorParsingYmlVars(" ".join(problems))

    @property
    def tfstate_file(self):
        return "{}/terraform.tfstate".format(self.tf_dir)

    def set_component_instance(self):
        if self.component == None:
            obj = hcl.loads(self.hclfile)
            self.component = Component(
                args=obj,
                dir=self.component_dir,
                tfstate_file=self.tfstate_file,
                tf_dir=self.tf_dir)

    def setup_component_source(self):
        self.set_component_instance()
        self.componentsource = self.component.get_source_instance()

    def setup_component_file_overrides(self):
        base = os.path.join(self.project_root, self.component_dir)
        for (d, fn) in flatwalk(base):
            if fn.endswith(".hclt"):
                continue
            if fn.endswith(".hcl"):
                continue

            dest = os.path.join(self.tf_dir, d[len(base)+1:])

            if not os.path.isdir(dest):
                # raise Exception(dest, base, d, fn, self.tf_dir)
                os.makedirs(dest)

            shutil.copy(os.path.join(d, fn), dest)

            # os.copy.copy(self.component_dir, self.tf_dir)

    def setup_component_tfstore(self):
        self.set_component_instance()
        self.componenttfstore = None
        obj = hcl.loads(self.hclfile)

        if "tfstate_store" in obj:

            crs = self.component.get_tfstate_store_instance()

            if crs.is_encrypted:
                if self.passphrases == []:
                    raise MissingEncryptionPassphrase(
                        "Remote state for component is encrypted, you must provide a decryption passphrase")
                crs.set_passphrases(self.passphrases)
                crs.decrypt()

            self.componenttfstore = crs

        else:
            # touch tfstate
            Path(self.tfstate_file).touch()

    def get_linked_project(self, linked_project_name):
        if self.get_linked_projects():
            if linked_project_name not in self.linked_projects:
                raise NoSuchLinkedProjectException(
                    "'{}': No such linked project".format(linked_project_name))

            if "source_instance" not in self.linked_projects[linked_project_name]:
                source = self.linked_projects[linked_project_name]

                if "repo" in source:
                    i = LinkedProjectSourceGit(args=source)
                    targetdir = get_cloudicorn_cachedir(
                        json.dumps(source)+linked_project_name)
                    tfdir = get_cloudicorn_cachedir(json.dumps(source)+"tfdir")

                elif "path" in source:
                    i = LinkedProjectSourcePath(args=source)
                    targetdir = get_cloudicorn_cachedir(
                        source["path"]+linked_project_name)
                    tfdir = get_cloudicorn_cachedir(source["path"]+"tfdir")

                else:
                    raise ProjectException(
                        "No handler for LinkedProjectSource")

                self.linked_projects[linked_project_name]["source_instance"] = i

                # fetch into a dir
                p = Project(git_filtered=False, wdir=targetdir,
                            project_vars=self.project_vars)
                p.set_tf_dir(tfdir)

                self.linked_projects[linked_project_name]["project_instance"] = p
                i.set_targetdir(targetdir)
                i.fetch()

            return self.linked_projects[linked_project_name]

    # def get_linked_project_source_instance(self, name):
    #         return self.linked_projects[name]["source_instance"]

    def get_linked_projects(self):
        self.get_yml_vars()
        if self.linked_projects == None:

            if "project_links" not in self.vars:
                return False
            self.linked_projects = {}

            for k, v in self.vars["project_links"].items():
                self.linked_projects[k] = v

        return True

    @property
    def component_inputs(self):
        obj = hcl.loads(self.hclfile)
        # lazy-resolve component_inputs here

        inputs = obj["inputs"]

        if "component_inputs" in obj:
            lp = self.get_linked_projects()

            for k, v in obj["component_inputs"].items():

                from_lp = False
                which = None
                if "." in k:
                    # key is buried in a block
                    which = k.split(".")[-1]
                    if "_" in which:
                        which = which.split("_")[-1]

                elif "_" in k:
                    which = k.split("_")[-1]

                else:
                    which = k

                if lp:
                    parts = v.split(":")
                    cdir = parts[1]

                    if len(parts) == 3:
                        # definitely a linked project
                        from_lp = True
                        lp_name = parts[0]
                        which = parts[2]
                    if len(parts) == 2:
                        # might be from linked project
                        if parts[0] in self.linked_projects:
                            from_lp = True
                            lp_name = parts[0]

                if from_lp:
                    si = self.get_linked_project(lp_name)

                    p = si["project_instance"]
                    p.set_component_dir(cdir)
                    t = p.component_type(component=cdir)
                    p.save_parsed_component()

                    if t != "component":
                        raise ComponentException(
                            tfstate_file, k, v, t, cdir, p.tf_dir, lp_name, p.wdir, which)
                    tfstate_file = p.tfstate_file
                else:
                    d = tempfile.mkdtemp()
                    tfstate_file = "{}/terraform.tfstate".format(d)

                    project = deepcopy(self)
                    project.git_filtered = False
                    project.components = None  # reset component cache

                    if ":" in v:
                        which = v.split(":")[-1]
                        v = v.split(":")[0]

                    project.set_component_dir(v)
                    t = project.component_type(component=v)

                    if t != "component":
                        raise ComponentException(
                            "component_inputs key {} = \"{}\" must point to a component".format(k, v))

                    project.set_tf_dir(d)
                    project.save_parsed_component()

                if not os.path.isfile(tfstate_file):
                    raise ComponentException(
                        "Missing terraform.tfstate file for component_inputs key {} = \"{}\"".format(k, v))

                try:
                    with open(tfstate_file, 'r') as fh:
                        tfstate = json.load(fh)
                except:
                    raise ComponentException("No tfstate for component: {} (have you applied this component?)".format(v))

                try:

                    val = tfstate["outputs"][which]["value"]
                    if "." in k:  # key is buried in a block
                        parts = k.split(".")
                        recursive_dict_set(inputs, parts, val)
                    else:
                        inputs[k] = val
                except KeyError:
                    # raise ComponentException(which, tfstate_file, k, v, t, cdir, p.tf_dir, lp_name, p.wdir)
                    raise ComponentException(
                        "component_inputs {} No such output in component {}".format(which, v))

        for k in cloud_cred_keys():
            if k in os.environ:
                inputs[k.lower()] = os.environ[k]

        return inputs

    def save_parsed_component(self):
        self.setup_component_tfstore()
        with open(self.outfile, 'w') as fh:
            fh.write(self.hclfile)

    @property
    def outfile(self):
        return "{}/{}".format(self.root_wdir, "component.hcl")

    @property
    def component_path(self):
        return self.component_dir
    
    @property
    def root_wdir(self):
        tf_wdir = self.tf_dir
        if not os.path.isdir(tf_wdir):
            os.makedirs(tf_wdir)

        return tf_wdir

    def get_template(self):
        self.templates = OrderedDict()
        for f in self.get_files():
            data = u""
            with open(f, 'r') as lines:
                for line in lines:
                    data += line
                self.templates[os.path.basename(f)] = {
                    "filename": f,
                    "data": data
                }

    def parse(self, obj):
        if type(obj) == str:
            return self.parsetext(obj)
        elif type(obj) == dict:
            for k, v in obj.items():
                obj[k] = self.parse(v)

        return obj

    def parsetext(self, s):

        # self.project_vars
        for (k, v) in self.project_vars.items():
            s = s.replace('${' + k + '}', v)

        # self.vars
        for (k, v) in self.vars.items():
            if type(v) == str:
                s = s.replace('${' + k + '}', v)

        # ENV VARS
        for (k, v) in os.environ.items():
            s = s.replace('${' + k + '}', v)

        return s

    def check_parsed_text(self, s):
        regex = r"\$\{(.+?)\}"

        # now make sure that all vars have been replaced
        # exclude commented out lines from check
        linenum = 0
        msg = ""
        lines = s.split("\n")
        for line in lines:
            linenum += 1
            try:
                if line.strip()[0] != '#':

                    matches = re.finditer(regex, line)

                    for matchNum, match in enumerate(matches):
                        miss = match.group()

                        if len(lines) > 1:
                            msg += "line {}:".format(linenum)
                        msg += "\n   No substitution found for {}".format(miss)

                        lim = 80
                        near_matches = {}
                        for k in self.vars.keys():
                            ratio = fuzz.ratio(miss, k)
                            if ratio >= lim:
                                near_matches[k] = ratio

                        for k in os.environ.keys():
                            ratio = fuzz.ratio(miss, k)
                            if ratio >= lim:
                                near_matches[k] = ratio

                        for k, ratio in near_matches.items():
                            msg += "\n   ==>  Perhaps you meant ${"+k+"}?"

                        msg += "\n"

            except IndexError:  # an empty line has no first character ;)
                pass

        # debug(msg)
        return msg

    def parse_component(self):

        if not self.check_project_dir():
            raise ProjectException("{} does not appear to be a cloudicorn project".format(self.project_root))

        self.check_hclt_files()
        self.get_yml_vars()
        self.get_template()

        self.out_string = u""

        self.parse_messages = []

        for fn, d in self.templates.items():
            parsed = self.parsetext(d['data'])
            msg = self.check_parsed_text(parsed)
            if msg != "":
                self.parse_messages.append(
                    "File: {}".format(os.path.relpath(d['filename'])))
                self.parse_messages.append(msg)

            self.out_string += parsed
            self.out_string += "\n"

    @property
    def parse_status(self):
        if len(self.parse_messages) == 0:
            return True

        return "\n".join([u"Could not substitute all variables in templates 😢"] + self.parse_messages)

    @property
    def hclfile(self):
        self.parse_component()
        return self.out_string


class ProjectException(Exception):
    pass


class ComponentException(Exception):
    pass


class Component():

    def __init__(self, args, dir, tfstate_file, tf_dir) -> None:
        self.args = args
        self.dir = dir
        self.tfstate_file = tfstate_file
        self.outputs = None
        self.tf_dir = tf_dir

    def set_dir(self, dir):
        self.dir = dir

    def set_tfstate_file(self, tfstate_file):
        self.tfstate_file = tfstate_file

    def get_source_instance(self):
        if "source" not in self.args:
            raise ComponentException("No source block specified in component")
        source = self.args["source"]

        if type(source) == str and source == "null":
            cs = ComponentSourceNull(args=source)

        elif "repo" in source:

            cs = ComponentSourceGit(args=source)

        elif "path" in source:
            cs = ComponentSourcePath(args=source)

        else:
            raise ComponentException(
                "No ComponentSource handler for component")

        # fetch into tf_wdir
        cs.set_targetdir(self.tf_dir)
        cs.fetch()
        return cs

    def get_tfstate_store_instance(self):
        tfstate_file = self.tfstate_file
        if "tfstate_store" not in self.args:
            raise ComponentException(
                "tfstate_store block specified in component")
        tfstate_store = self.args["tfstate_store"]

        # instanciate TfStateStore
        if "bucket" in tfstate_store:
            from cloudicorn_aws import TfStateStoreAwsS3
            crs = TfStateStoreAwsS3(args=tfstate_store, localpath=tfstate_file)
        elif "storage_account" in tfstate_store:
            from cloudicorn_azurerm import TfStateStoreAzureStorage
            crs = TfStateStoreAzureStorage(
                args=tfstate_store, localpath=tfstate_file)
        elif "path" in tfstate_store:
            crs = TfStateStoreFilesystem(
                args=tfstate_store, localpath=tfstate_file)
        else:
            raise ComponentException("No TfStateStore handler for component")

        crs.fetch()
        return crs

    def get_outputs(self):
        if self.outputs == None:

            if not os.path.isfile(self.tfstate_file):
                raise ComponentException(
                    "Cannot read tfstate for component, {} : no such file".format(self.tfstate_file))

            with open(self.tfstate_file, 'r') as fh:
                o = json.load(fh)

            self.outputs = o["outputs"]

    def get_output(self, k):
        self.get_outputs()

        if k not in self.outputs:
            raise ComponentException(
                "{}: No such output for component".format(k))

        return self.outputs[k]["value"]

    def get_output_keys(self):
        self.get_outputs()
        return list(self.outputs.keys())


class ComponentSourceException(Exception):
    pass


class ComponentSource():
    def __init__(self, args) -> None:
        self.args = args

    def set_targetdir(self, targetdir):
        if not os.path.isdir(targetdir):
            os.makedirs(targetdir)

        self.targetdir = targetdir

    def fetch(self):
        raise ComponentSourceException("not implemented here")

    @property
    def tdir(self):
        return self.targetdir


class ComponentSourceNull(ComponentSource):
    def fetch(self):
        pass


class ComponentSourcePath(ComponentSource):

    def fetch(self):
        if "path" not in self.args:
            raise ComponentSourceException("path not present in source block")

        xp = os.path.expanduser(self.args["path"])
        if not os.path.isdir(xp):
            raise ComponentSourceException(
                "No such directory: {}".format(xp))

        shutil.copytree(xp, self.targetdir, dirs_exist_ok=True)


class ComponentSourceGit(ComponentSource):
    def fetch(self):
        if "repo" not in self.args:
            raise ComponentSourceException("repo not present in source block")

        if dir_is_git_repo(self.args["repo"]):
            # local path was provided, handy for local testing without commit/push
            subdir = self.args["repo"]
            if "path" in self.args:

                subdir = "{}/{}".format(subdir, self.args["path"])
                if not os.path.isdir(subdir):
                    raise ComponentSourceException("No such path {} in repo: {}".format(
                        self.args["path"], self.args["repo"]))

            shutil.copytree(subdir, self.targetdir, dirs_exist_ok=True)

        else:
            t = tempfile.mkdtemp()
            try:
                if "tag" in self.args:
                    if "*" in self.args["tag"]:
                        repo = Repo.clone_from(self.args["repo"], t)
                        tag = self.args["tag"].replace("*", "")

                        found = False
                        tags = []

                        for T in repo.tags:
                            tags.append(str(T))

                        tags.sort(reverse=True)
                        for T in tags:
                            if tag in str(T):
                                repo.git.checkout(T)
                                found = True
                                break

                        if not found:
                            raise ComponentSourceException("Error cloning git repo {}, no tag matching {}, repo contains these tags: {}".format(
                                self.args["repo"], self.args["tag"], ", ".join(tags)))

                    else:
                        Repo.clone_from(
                            self.args["repo"], t, branch=self.args["tag"], depth=1)
                elif "branch" in self.args:
                    Repo.clone_from(self.args["repo"], t,
                                    branch=self.args["branch"], depth=1)
                else:
                    Repo.clone_from(self.args["repo"], t, depth=1)

            except Exception:
                shutil.rmtree(t)
                raise ComponentSourceException(
                    "Error cloning git repo {}".format(self.args["repo"]))

            if "path" in self.args:

                subdir = "{}/{}".format(t, self.args["path"])
                if not os.path.isdir(subdir):
                    shutil.rmtree(t)
                    raise ComponentSourceException("No such path {} in repo: {}".format(
                        self.args["path"], self.args["repo"]))

                shutil.copytree(subdir, self.targetdir, dirs_exist_ok=True)

            else:
                shutil.copytree(t, self.targetdir, dirs_exist_ok=True)

            shutil.rmtree(t)


class LinkedProjectSourcePath(ComponentSourcePath):
    pass


class LinkedProjectSourceGit(ComponentSourceGit):
    pass

# class TfStateReader():

#     def __init__(self):
#         self.components = {}

#     def load(self, component):
#         if component not in self.components.values():
#             # implement here
#             pass

#     def value(self, component, key):
#         self.load(component)

#         try:
#             value = self.components[component][key]["value"]
#         except KeyError:
#             msg = "ERROR: State key \"{}\" not found in component {}\nKey must be one of: {}".format(key, component, ", ".join(self.components[component].keys()))
#             raise RemoteStateKeyNotFound(msg)

#         return value


class TfStateStore():

    def __init__(self, args, localpath) -> None:
        self.args = args
        self.localpath = localpath
        self.passphrases = []
        self.fetched = False

        def unpad(s): return s[:-ord(s[len(s) - 1:])]

    def set_passphrases(self, passphrases=[]):
        self.passphrases = passphrases

    def encrypt(self) -> bool:
        if self.passphrases == []:
            raise Exception("No passphrase given")

        with open(self.localpath, 'r') as fh:
            content = fh.read()

        private_key = hashlib.sha256(
            self.passphrases[0].encode("utf-8")).digest()

        def pad(s): return s + (AES.block_size - len(s) %
                                AES.block_size) * chr(AES.block_size - len(s) % AES.block_size)
        padded = pad(content)
        iv = get_random_bytes(AES.block_size)
        cipher = AES.new(private_key, AES.MODE_CBC, iv)

        ciphertext = cipher.encrypt(bytes(padded.encode('utf-8')))

        with open(self.localpath, 'w') as fh:
            json.dump({
                'ciphertext':  b64encode(ciphertext).decode('utf-8'),
                'iv': b64encode(iv).decode('utf-8')}, fh)

        return True

    def decrypt(self) -> bool:
        if self.passphrases == []:
            raise Exception("No passphrase given")

        with open(self.localpath, 'r') as fh:
            obj = json.load(fh)

        def unpad(s): return s[:-ord(s[len(s) - 1:])]

        iv = b64decode(obj['iv'])
        ciphertext = b64decode(obj['ciphertext'])

        for passphrase in self.passphrases:
            private_key = hashlib.sha256(passphrase.encode("utf-8")).digest()

            cipher = AES.new(private_key, AES.MODE_CBC, iv)

            plaintext = unpad(cipher.decrypt(ciphertext))

            if len(plaintext) > 0:

                try:
                    plaintext = plaintext.decode("utf-8")
                    with open(self.localpath, "w") as fh:
                        fh.write(plaintext)

                    return True
                except:
                    continue

        raise WrongPasswordException("Wrong decryption passphrase")

    @property
    def is_encrypted(self):

        if os.path.isfile(self.localpath):
            with open(self.localpath, 'r') as fh:
                try:
                    obj = json.load(fh)
                except json.JSONDecodeError:
                    return False
                except Exception as e:
                    raise Exception(self.localpath, e)

            if "ciphertext" in obj:
                return True


        return False

    def push(self):
        raise Exception("not implemented here")

    def fetch(self):
        raise Exception("not implemented here")

    @property
    def localpath_exists(self):
        return os.path.isfile(self.localpath)




class TfStateStoreFilesystem(TfStateStore):
    def push(self):
        if not self.localpath_exists:
            return False

        tf_path = self.args["path"]

        if not os.path.isdir(os.path.dirname(tf_path)):
            os.makedirs(os.path.dirname(tf_path))

        shutil.copy(self.localpath, tf_path)

    def fetch(self):
        tf_path = self.args["path"]

        if os.path.isfile(tf_path):
            shutil.copy(tf_path, self.localpath)


class NoSuchLinkedProjectException(Exception):
    pass


class MissingCredsException(Exception):
    pass

def cloud_cred_keys():
    l = []
    if check_cloud_extension("aws"):
        from cloudicorn_aws import aws_sts_cred_keys, aws_cred_keys
        l.extend(aws_sts_cred_keys())
        l.extend(aws_cred_keys())

    if check_cloud_extension("azurerm"):
        from cloudicorn_azurerm import azurerm_sp_cred_keys
        l.extend(azurerm_sp_cred_keys())

    return list(set(l))

def assert_env_vars(required):
    missing = []
    for c in required:
        val = os.environ.get(c, None)
        if val == None:
            missing.append(c)

    if len(missing) == 0:
        return True

    return missing



