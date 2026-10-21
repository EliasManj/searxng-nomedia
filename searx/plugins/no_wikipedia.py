# SPDX-License-Identifier: AGPL-3.0-or-later
"""A plugin to remove Wikipedia results from search.

Enable in ``settings.yml``:

.. code:: yaml

   plugins:
     searx.plugins.no_wikipedia.SXNGPlugin:
       active: true

"""

import typing as t

from flask_babel import gettext  # pyright: ignore[reportUnknownVariableType]

from searx.plugins import Plugin, PluginInfo

if t.TYPE_CHECKING:
    from searx.search import SearchWithPlugins
    from searx.extended_types import SXNG_Request
    from searx.result_types import Result
    from searx.plugins import PluginCfg


@t.final
class SXNGPlugin(Plugin):
    """Removes all results from wikipedia.org."""

    id = "no_wikipedia"

    def __init__(self, plg_cfg: "PluginCfg") -> None:
        super().__init__(plg_cfg)
        self.info = PluginInfo(
            id=self.id,
            name=gettext("No Wikipedia"),
            description=gettext("Removes all results from Wikipedia."),
            preference_section="general",
        )

    def on_result(self, request: "SXNG_Request", search: "SearchWithPlugins", result: "Result") -> bool:
        if result.parsed_url and "wikipedia.org" in result.parsed_url.netloc:
            return False
        return True