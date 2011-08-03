import json
from xml.etree.ElementTree import XML

from fabric.api import env, local, prefix, put, sudo

import keep

# recommended distribution command:
#   $ fab load_config:settings.json deploy
#
# where settings.json is a path to a file that looks something like this:
#   {
#     "hosts": ["myself@stagingserver.library.emory.edu"], # where we'll ssh/scp
#     "sudo_user": "keep", # the user we'll sudo into to do stuff
#     "extract_path": "/path/to/sites/keep" # where we'll extract the webapp
#   }
#
# if the new version doesn't work, you can revert symlinks with:
#   $ fab load_config:settings.json revert

# env targets

def _base_env():
    """Configure basic env."""
    env.version = keep.__version__
    env.svn_rev = None
    env.svn_rev_tag = ''
    env.svn_url = None
_base_env()

def _svn_env():
    """Try to infer some env from local svn checkout."""
    svn_info = XML(local('svn info --xml', capture=True))
    env.svn_rev = svn_info.find('entry').get('revision')
    env.svn_rev_tag = '-r' + env.svn_rev
    env.svn_url = svn_info.find('entry/url').text
try:
    if keep.__version_info__[-1]:
        _svn_env()
except:
    pass

def _env_paths():
    """Set some env paths based on previously-generated env."""
    env.build_dir = 'keep-%(version)s%(svn_rev_tag)s' % env
    env.tarball = 'keep-%(version)s%(svn_rev_tag)s.tar.bz2' % env
_env_paths()

def load_config(file):
    """Load fab env variables from a local JSON file."""
    with open(file) as f:
        config = json.load(f)
    env.update(config)

# misc helpers

def _sudo(*args, **kwargs):
    """Wrapper for sudo, using a default user in env."""
    if 'user' not in kwargs and 'sudo_user' in env:
        kwargs = kwargs.copy()
        kwargs['user'] = env.sudo_user
    return sudo(*args, **kwargs)

# local build functions

def _fetch_source_from_svn():
    """Fetch the source from svn to avoid accidentally including local
    changes."""
    local('mkdir -p build')
    local('rm -rf build/%(build_dir)s' % env)
    local('svn export -r %(svn_rev)s %(svn_url)s@%(svn_rev)s build/%(build_dir)s' % env)

def _package_source():
    """Create a tarball of the source tree."""
    local('mkdir -p dist')
    local('tar cjf dist/%(tarball)s -C build %(build_dir)s' % env)

# remote functions

def _copy_tarball():
    """Copy the source tarball to the target server."""
    put('dist/%(tarball)s' % env,
        '/tmp/%(tarball)s' % env)

def _extract_tarball():
    """Extract the remote source tarball in the appropriate directory."""
    _sudo('cp /tmp/%(tarball)s %(extract_path)s/%(tarball)s' % env)
    _sudo('tar xjf %(extract_path)s/%(tarball)s -C %(extract_path)s' % env)

def _create_virtualenv():
    """Construct and configure a remote virtualenv."""
    _sudo('virtualenv --no-site-packages %(extract_path)s/%(build_dir)s/env' % env)
    with prefix('source %(extract_path)s/%(build_dir)s/env/bin/activate' % env):
        _sudo('pip install -r %(extract_path)s/%(build_dir)s/pip-install-req.txt' % env)
        _sudo('pip install mysql-python psycopg2==2.4.1') # system reqs, but not strictly sw reqs

def _collect_remote_config():
    """Copy configuration files into the remote source tree."""
    _sudo('cp %(extract_path)s/localsettings.py %(extract_path)s/%(build_dir)s/keep/localsettings.py' % env)

def _update_links():
    """Update current/previous symlinks."""
    _sudo('''if [ -h %(extract_path)s/current ]; then
               rm -f %(extract_path)s/previous;
               mv %(extract_path)s/current %(extract_path)s/previous;
             fi''' % env)
    _sudo('ln -sf %(build_dir)s %(extract_path)s/current' % env)

# bring it all together

def deploy():
    """Deploy the application from source control to a remote server."""
    _fetch_source_from_svn()
    _package_source()
    _copy_tarball()
    _extract_tarball()
    _create_virtualenv()
    _collect_remote_config()
    _update_links()

def revert():
    """Back out the current version, updating remote symlinks to point back
    to the stored previous one."""
    _sudo('[ -h %(extract_path)s/previous ]' % env) # only if previous link exists
    _sudo('rm -f %(extract_path)s/current' % env)
    _sudo('ln -s $(readlink %(extract_path)s/previous) %(extract_path)s/current' % env)
    _sudo('rm %(extract_path)s/previous' % env)
    
def clean_local():
    """Remove local files created during deployment."""
    local('rm -rf dist build')

def clean_remote():
    """Remove the deployed application from the remote server."""
    _sudo('rm -rf %(extract_path)s/%(build_dir)s %(extract_path)s/%(tarball)s' % env)
