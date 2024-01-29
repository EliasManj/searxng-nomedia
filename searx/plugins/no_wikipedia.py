# SPDX-License-Identifier: AGPL-3.0-or-later
# lint: pylint
"""A plugin to remove wikipedia results from search.

Enable in ``settings.yml``:

.. code:: yaml

  enabled_plugins:
    ..
    - 'No Wikipedia'

"""

import re
from flask_babel import gettext
from httpx import HTTPError
from searx.network import get
from searx import settings

default_on = True

name = gettext("No Wikipedia")
'''Translated name of the plugin'''

plugin_id = 'no_wikipedia'

description = gettext(
    "This plugin removes all results from wikipedia"
)
'''Translated description of the plugin.'''

preference_section = 'query'
'''The preference section where the plugin is shown.'''

query_keywords = ['no-wikipedia']
'''Query keywords shown in the preferences.'''

query_examples = ''
'''Query examples shown in the preferences.'''

# Regex for exit node addresses in the list.
reg = re.compile(r"(?<=ExitAddress )\S+")

def pre_search(request, search):
    return True

def on_result(request, search, result):
    if "url" in result:
        if "wikipedia.org" in result["url"]:
            return False
    return True