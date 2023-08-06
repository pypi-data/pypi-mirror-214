# ------------------------------------------------------------------------------
#  es7s/core
#  (c) 2022-2023 A. Shavykin <0.delameter@gmail.com>
# ------------------------------------------------------------------------------

import io
import os
from collections.abc import Iterable

from .path import RESOURCE_DIR
from .. import APP_NAME


class DemoHilightNumText:
    @classmethod
    def open(cls) -> io.StringIO:
        import pkg_resources
        return io.StringIO(
            pkg_resources.resource_string(
                APP_NAME, os.path.join(RESOURCE_DIR, 'demo', "demo-text.txt")
            ).decode()
        )


class DemoGradients:
    @classmethod
    def open(cls) -> Iterable[io.StringIO]:
        import pkg_resources
        n = 0
        while True:
            try:
                n += 1
                yield io.StringIO(
                    pkg_resources.resource_string(
                        APP_NAME, os.path.join(RESOURCE_DIR, 'demo', f"demo-gradient-{n}.ggr")
                    ).decode()
                )
            except FileNotFoundError:
                if n == 1:
                    raise
                break
