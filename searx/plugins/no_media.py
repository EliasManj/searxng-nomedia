# SPDX-License-Identifier: AGPL-3.0-or-later
"""A plugin to remove mainstream media websites from search results.

Configure the list of blocked domains in ``settings.yml``:

.. code:: yaml

   no_media:
     - 'cnn.com'
     - 'bbc.com'
     ...

   plugins:
     searx.plugins.no_media.SXNGPlugin:
       active: true

"""

import typing as t

from flask_babel import gettext  # pyright: ignore[reportUnknownVariableType]

from searx import settings
from searx.plugins import Plugin, PluginInfo

if t.TYPE_CHECKING:
    import flask
    from searx.search import SearchWithPlugins
    from searx.extended_types import SXNG_Request
    from searx.result_types import Result
    from searx.plugins import PluginCfg

_media_list: list[str] = []


@t.final
class SXNGPlugin(Plugin):
    """Removes results from mainstream media websites configured in ``no_media``."""

    id = "no_media"

    def __init__(self, plg_cfg: "PluginCfg") -> None:
        super().__init__(plg_cfg)
        self.info = PluginInfo(
            id=self.id,
            name=gettext("No Media Plugin"),
            description=gettext("Removes all results from mainstream media websites."),
            preference_section="general",
        )

    def on_result(self, request: "SXNG_Request", search: "SearchWithPlugins", result: "Result") -> bool:
        if result.parsed_url:
            for domain in _media_list:
                if domain in result.parsed_url.netloc:
                    return False
        return True

    def init(self, app: "flask.Flask") -> bool:  # pylint: disable=unused-argument
        global _media_list  # pylint: disable=global-statement
        _media_list = settings.get(self.id, [])
        if not _media_list:
            return False
        return True
