# ======================================================================================================================
#        File:  bugs.py
#     Project:  B Bug Tracker
# Description:  Simple bug tracker
#      Author:  Jared Julien <jaredjulien@exsystems.net>
#   Copyright:  (c) 2010-2011 Michael Diamond <michael@digitalgemstones.com>
#               (c) 2022-2023 Jared Julien <jaredjulien@exsystems.net>
# ---------------------------------------------------------------------------------------------------------------------
"""b's business logic and programatic API."""

# ======================================================================================================================
# Import Statements
# ----------------------------------------------------------------------------------------------------------------------
import os
import re
import shutil
import subprocess
import hashlib
import time
import logging
from datetime import datetime
from typing import Dict, List

import yaml
from rich import print, box
from rich.console import group
from rich.panel import Panel
from rich.table import Table

from b import exceptions, migrations




# ======================================================================================================================
# Tracker Class
# ----------------------------------------------------------------------------------------------------------------------
class Tracker:
    """A set of bugs, issues, and tasks, both finished and unfinished, for a given repository.

    The list's file is read from disk when initialized. The items can be written back out to disk with the write()
    function.

    You can specify any taskdir you want, but the intent is to work from the cwd and therefore anything calling this
    class ought to handle that change (normally to the repo root)
    """

    def __init__(self, bugsdir: str, user: str, editor: str):
        """Initialize by reading the task files, if they exist."""
        self.user = user
        self.editor = editor

        def climb_tree(reference) -> str:
            working = os.getcwd()
            while True:
                test = os.path.join(working, reference)
                if os.path.exists(test):
                    return test

                # Step up one directory.
                new = os.path.dirname(working)
                if new == working:
                    # Bail out if we're at the top of the tree.
                    return reference
                working = new

        bugsdir = os.path.expanduser(bugsdir)
        self.bugsdir = bugsdir if os.path.isabs(os.path.expanduser(bugsdir)) else climb_tree(bugsdir)


# ----------------------------------------------------------------------------------------------------------------------
    def _get_bug(self, prefix: str) -> Dict[str, any]:
        ids = self._list_ids()
        matched = [id for id in ids if id.startswith(prefix)]
        if len(matched) == 1:
            id = matched[0]
            with open(self._get_bug_path(id), 'r') as handle:
                data = yaml.safe_load(handle)
            data['id'] = id
            return data

        elif len(matched) == 0:
            raise exceptions.UnknownPrefix(prefix)

        else:
            # More than one match.
            raise exceptions.AmbiguousPrefix(prefix)


# ----------------------------------------------------------------------------------------------------------------------
    def _all_bugs(self) -> List[Dict[str, any]]:
        return [self._get_bug(id) for id in self._list_ids()]


# ----------------------------------------------------------------------------------------------------------------------
    def _write(self, bug: Dict[str, any]):
        """Flush the finished and unfinished tasks to the files on disk."""
        if not os.path.exists(self.bugsdir):
            raise exceptions.NotInitialized('No bugs directory found for the current directory')

        def str_presenter(dumper, data):
            if len(data.splitlines()) > 1:  # check for multiline string
                return dumper.represent_scalar('tag:yaml.org,2002:str', data, style='|')
            return dumper.represent_scalar('tag:yaml.org,2002:str', data)
        yaml.representer.SafeRepresenter.add_representer(str, str_presenter)

        # Start with a list of keys from the schema sorted in our preferred order.
        keys = [
            'title',
            'type',
            'open',
            'author',
            'entered',
            'owner',
            'details',
            'paths',
            'comments',
            'reproduce',
            'expected',
            'actual',
            'stacktrace',
            'environment',
            'problem',
            'fix',
            'what',
            'why',
            'how',
            'accepted'
        ]

        # Add any additional keys into the list at the end and warn users about schema violations too.
        for key in bug.keys():
            if key ==  'id':
                continue
            if key not in keys:
                logging.warning('Bug contains key "%s" which is not part of the schema.  Retaining.', key)
                keys.append(key)

        # Generate a new dict with values for the bug in the sorted order of keys.
        # In newer Python, the dicts are automatically OrderedDict's.
        sorted = dict((key, bug.get(key)) for key in keys if key in bug)

        # Finally, write the now sorted bug contents to disc.
        filename = self._get_bug_path(bug['id'])
        with open(filename, 'w') as handle:
            yaml.safe_dump(sorted, handle, sort_keys=False)


# ----------------------------------------------------------------------------------------------------------------------
    def _get_bug_path(self, full_id):
        """Returns the directory and file path to the details specified by id."""
        return os.path.join(self.bugsdir, full_id + ".bug.yaml")


# ----------------------------------------------------------------------------------------------------------------------
    def _list_ids(self) -> List[str]:
        return [file.split('.', 1)[0] for file in os.listdir(self.bugsdir) if file.endswith('.bug.yaml')]


# ----------------------------------------------------------------------------------------------------------------------
    def _prefixes(self) -> Dict[str, str]:
        prefixes = {}
        ids = self._list_ids()
        for id in ids:
            for idx in range(1, len(id)):
                prefix = id[:idx]
                matches = [id for id in ids if id.startswith(prefix)]
                if len(matches) == 1:
                    prefixes[id] = prefix
                    break
        return prefixes


# ----------------------------------------------------------------------------------------------------------------------
    def _users_list(self):
        """Returns a mapping of usernames to the number of open bugs assigned to that user."""
        counts = {}
        for bug in self._all_bugs():
            owner = bug.get('owner')
            if owner not in counts:
                counts[owner] = 0
            if bug['open']:
                counts[owner] += 1
        return dict(sorted(list(counts.items()), key=lambda count: count[1], reverse=True))


# ----------------------------------------------------------------------------------------------------------------------
    def _get_user(self, user, force=False):
        """Given a user prefix, returns the appropriate username, or fails if the correct user cannot be identified.

        'me' is a special username which maps to the username specified when constructing the Bugs.  'Nobody' (and
        prefixes of 'Nobody') is a special username which maps internally to the empty string, indicating no assignment.
        If force is true, the user 'Nobody' is used.  This is unadvisable, avoid forcing the username 'Nobody'.

        If force is true, it assumes user is not a prefix and should be assumed to exist already.
        """
        if user.lower() == 'me':
            return self.user

        if user.lower() == 'nobody':
            return None

        users = self._users_list().keys()
        if not force:
            if user not in users:
                usr = user.lower()
                matched = [u for u in users if u and u.lower().startswith(usr)]
                if len(matched) > 1:
                    raise exceptions.AmbiguousUser(user, matched)
                if len(matched) == 0:
                    raise exceptions.UnknownUser(user)
                user = matched[0]
            # Needed twice, since users can also type a prefix of "Nobody"
            if user == 'Nobody':
                return ''
        else:  # we're forcing a new username
            if '|' in user:
                raise exceptions.InvalidInput("Usernames cannot contain '|'.")
        return user


# ----------------------------------------------------------------------------------------------------------------------
    def _launch_editor(self, path: str) -> None:
        """Open the specified file in the editor specified by the user.

        Arguments:
            path: The path to the file to be edited.
        """
        subprocess.call("%s \"%s\"" % (self.editor, path), shell=True)



# ----------------------------------------------------------------------------------------------------------------------
    def initialize(self, force: bool):
        """Initialize a new bugs directory at the current working directory."""
        # Warn the user about creating a bugs directory if one was already found in a folder above.
        # Using the "-f" argument to "force" the creation will put a new bugs directory here too.
        if os.path.exists(self.bugsdir) and not force:
            message = f'Bugs directory already exists at {self.bugsdir} - use -f to force creation here'
            raise exceptions.AlreadyInitialized(message)

        # Attempt to make the directory as specified, if it exists the exception will be morphed into AlreadyExists.
        try:
            os.makedirs(self.bugsdir)
        except OSError as error:
            raise exceptions.AlreadyInitialized('Bugs directory already exists in this exact location') from error

        print(f'Initialized a bugs directory at "{os.path.abspath(self.bugsdir)}"')


# ----------------------------------------------------------------------------------------------------------------------
    def list_templates(self, only_defaults: bool = False, only_custom: bool = False) -> Dict[str, str]:
        """Return a dictionary of available templates that can be used to create new bugs.

        Arguments:
            only_defaults: Indicates that only the default templates from within the b tool should be returned - none of
                the custom templates from the .bugs directory.

        Returns:
            A dictionary where keys correspond to the names of the available templates and the values are the paths to
            the corresponding template file(s).
        """
        assert not (only_defaults and only_custom)
        templates = {}

        def add_templates(base):
            directory = os.path.join(base, 'templates')
            if not os.path.exists(directory):
                return
            for template in os.listdir(directory):
                path = os.path.join(directory, template)
                name = template.rsplit('.', 2)[0]
                templates[name] = path

        # Start with a list of templates from the template folder within this `b` package.
        if not only_custom:
            add_templates(os.path.dirname(__file__))

        # Include/override with templates from the project directory when specified.
        if not only_defaults:
            add_templates(os.path.expanduser(str(self.bugsdir)))

        return templates


# ----------------------------------------------------------------------------------------------------------------------
    def customize_template(self, template: str) -> None:
        """Copy the specified template from the tool directory into the project '.bugs' directory and open the editor.
        """
        available = self.list_templates(only_defaults=True)
        if template not in available:
            message = f'The specified default template "{template}" does not exist.'
            message += '\nInvoke `b templates -d` for a list of templates available for customization.'
            raise exceptions.InvalidInput(message)
        source = available[template]
        destination_dir = os.path.join(os.path.expanduser(str(self.bugsdir)), 'templates')
        destination = os.path.join(destination_dir, os.path.basename(source))
        if os.path.exists(destination):
            raise exceptions.InvalidCommand(f'The specified template "{template}" already exists at {destination}.')
        os.makedirs(destination_dir, exist_ok=True)
        shutil.copyfile(source, destination)
        self._launch_editor(destination)


# ----------------------------------------------------------------------------------------------------------------------
    def edit_template(self, template: str) -> None:
        """Open the specified custom template for editing.

        Arguments:
            template: The CUSTOM template name to be edited.
        """
        available = self.list_templates(only_custom=True)
        if template not in available:
            message = f'Custom template {template} does not exit.'
            message += '\nPerhaps you meant to create a custom template (-c) instead?'
            raise exceptions.InvalidInput(message)
        path = available[template]
        self._launch_editor(path)


# ----------------------------------------------------------------------------------------------------------------------
    def id(self, prefix):
        """Given a prefix, returns the full id of that bug."""
        print(self._get_bug(prefix)['id'])


# ----------------------------------------------------------------------------------------------------------------------
    def add(self, title: str, template: str, self_owner: bool):
        """Adds a new bug to the list.

        Arguments:
            title: Title text giving a summarized description of this new bug.
            template: Name of the template file (can be found using the `templates` command) to use for this new bug.
            self_owner: True if the current user should be set at the owner for this new bug.  If False, then no owner
                will be assigned.
        """
        # Add the new detail file from template.
        templates = self.list_templates()
        try:
            template_path = templates[template]
        except KeyError as error:
            message = f'Template "{template}" does not exist - use `template` command to view available templates'
            raise exceptions.TemplateError(message) from error

        # Load YAML from template.
        with open(template_path, 'r') as handle:
            bug = yaml.safe_load(handle)

        # Generate a unique hash for a new ID.
        existing = self._list_ids()
        while True:
            full_id = hashlib.sha1(str(time.time()).encode('utf-8')).hexdigest()
            if full_id not in existing:
                break

        # Populate default attributes.
        bug['id'] = full_id
        bug['title'] = title
        bug['entered'] = datetime.now().astimezone().isoformat()
        bug['author'] = self.user
        bug['open'] = True

        if self_owner:
            bug['owner'] = self.user

        self._write(bug)

        prefix = self._prefixes()[full_id]
        short_task_id = "[bold cyan]%s[/]:[yellow]%s[/]" % (prefix, full_id[len(prefix):])
        print(f"Added bug {short_task_id}")

        return full_id


# ----------------------------------------------------------------------------------------------------------------------
    def rename(self, prefix, title):
        """Renames the bug.

        If more than one task matches the prefix an AmbiguousPrefix exception will be raised, unless the prefix is the
        entire ID of one task.

        If no tasks match the prefix an UnknownPrefix exception will be raised.
        """
        bug = self._get_bug(prefix)
        if title.startswith('s/') or title.startswith('/'):
            title = re.sub('^s?/', '', title).rstrip('/')
            find, _, repl = title.partition('/')
            title = re.sub(find, repl, bug['title'])

        bug['title'] = title
        self._write(bug)


# ----------------------------------------------------------------------------------------------------------------------
    def assign(self, prefix, user, force=False):
        """Specifies a new owner of the bug.  Tries to guess the correct user, or warns if it cannot find an appropriate
        user.

        Using the -f flag will create a new user with that exact name, it will not try to guess, or warn the user.
        """
        bug = self._get_bug(prefix)
        user = self._get_user(user, force)

        if user is None:
            if 'owner' in bug:
                del bug['owner']
            print(f"Unassigned {prefix}: '{bug['title']}'")

        else:
            bug['owner'] = user
            print(f"Assigned {prefix}: '{bug['title']}' to {user}")

        self._write(bug)



# ----------------------------------------------------------------------------------------------------------------------
    def edit(self, prefix):
        """Allows the user to edit the details of the specified bug"""
        bug = self._get_bug(prefix)
        path = self._get_bug_path(bug['id'])
        self._launch_editor(path)


# ----------------------------------------------------------------------------------------------------------------------
    def comment(self, prefix, text):
        """Allows the user to add a comment to the bug without launching an editor.

        If they have a username set, the comment will show who made it."""
        bug = self._get_bug(prefix)

        # Add a new comments section to the bug if it doesn't already exist.
        if 'comments' not in bug:
            bug['comments'] = []

        # Append this comment to the bug.
        bug['comments'].append({
            'author': self.user,
            'date': datetime.now().astimezone().isoformat(),
            'text': text
        })

        # Write the bug back to file.
        self._write(bug)


# ----------------------------------------------------------------------------------------------------------------------
    def resolve(self, prefix):
        """Marks a bug as resolved"""
        bug = self._get_bug(prefix)
        bug['open'] = False
        self._write(bug)


# ----------------------------------------------------------------------------------------------------------------------
    def reopen(self, prefix):
        """Reopens a bug that was previously resolved"""
        bug = self._get_bug(prefix)
        bug['open'] = True
        self._write(bug)


# ----------------------------------------------------------------------------------------------------------------------
    def details(self, prefix):
        """Provides additional details on the requested bug.

        Metadata (like owner, and creation time) which are not stored in the details file are displayed along with the
        details.

        Sections with no content are not displayed.
        """
        bug = self._get_bug(prefix)

        is_open = bug.pop('open', True)
        type = bug.pop('type', 'Bug')
        color = 'red' if is_open else 'green'
        title = f"[{color}]{type}: {bug.pop('title')}[/]"

        @group()
        def chunks():
            id = bug.pop('id')
            yield f"Status: [{color}]{'Open' if is_open else 'Resolved'}"
            yield f"ID: [bold cyan]{prefix}[/]:[yellow]{id[len(prefix):]}"
            yield f"Entered on: {bug.pop('entered', '*unknown*')} by {bug.pop('author', '*unknown*')}"

            if 'owner' in bug:
                yield f"Owned by: [magenta]{bug.pop('owner')}"

            comments = bug.pop('comments', [])

            for key, value in bug.items():
                if isinstance(value, list):
                    value = '\n'.join(value)
                yield Panel(value, title=key.title())

            if comments:
                table = Table(title='Comments')
                table.add_column('Date')
                table.add_column('User')
                table.add_column('Text')

                for comment in comments:
                    table.add_row(str(comment['date']), comment['author'], comment['text'].strip())
                yield table

        print(Panel.fit(chunks(), title=title, title_align='left'))


# ----------------------------------------------------------------------------------------------------------------------
    def users(self):
        """Prints a list of users along with their number of open bugs."""
        table = Table(box=box.SIMPLE_HEAD)

        table.add_column('Username', justify='right', header_style='blue', style='blue')
        table.add_column('Open Bugs', header_style='magenta', style='magenta')

        for (user, count) in self._users_list().items():
            table.add_row(user or "*unassigned*", str(count))

        print(table)


# ----------------------------------------------------------------------------------------------------------------------
    def list(self, is_open=True, owner='*', grep='', alpha=False, chrono=False, truncate=0):
        """Lists all bugs, applying the given filters"""
        if not os.path.exists(self.bugsdir):
            raise exceptions.NotInitialized('No bugs directory found - use `init` command first')

        prefixes = self._prefixes()

        if owner != '*':
            owner = self._get_user(owner)

        filtered = [bug for bug in self._all_bugs()
                    if bug['open'] == is_open
                    and (owner == '*' or owner == bug.get('owner'))
                    and (grep == '' or grep.lower() in bug['title'].lower())]

        if len(filtered) > 0:
            plen = max([len(prefixes[bug['id']]) for bug in filtered])
        else:
            plen = 0

        if alpha:
            filtered = sorted(filtered, key=lambda x: x.title.lower())

        if chrono:
            filtered = sorted(filtered, key=lambda bug: bug['entered'])

        for bug in filtered:
            line = '[bold cyan]%s[/bold cyan] - %s' % (prefixes[bug['id']].rjust(plen), bug['title'])
            if 0 < truncate < len(line):
                line = line[:truncate - 4] + '...'
            print(line)

        out = f"Found {len(filtered)} "
        out += 'open' if is_open else 'resolved'
        out += f" bug{'' if len(filtered) == 1 else 's'}"
        if owner != '*':
            out += f" owned by {'Nobody' if owner == '' else owner}"
        if grep:
            out += f' whose title contains {grep}'
        print(out)


# ----------------------------------------------------------------------------------------------------------------------
    def migrate(self) -> None:
        """Migrate the current bugs directory to the latest version."""
        migrations.details_to_markdown(self.bugsdir)
        migrations.details_to_yaml(self.bugsdir)
        migrations.move_details_to_bugs_root(self.bugsdir)
        migrations.bug_dict_into_yaml_details(self.bugsdir)




# End of File
