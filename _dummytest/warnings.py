"""Emit warnings for unstable or pre-release versions."""

import warnings

from ._version import __version__
from .color import c


_PRE_RELEASE_TAGS = ("pre", "beta", "tomorrow")


class BaseDummytestWarning(UserWarning):
    """Base warning for all dummytest warnings."""


class PreReleaseWarning(BaseDummytestWarning):
    """Warned when using a pre-release version."""


class BetaWarning(BaseDummytestWarning):
    """Warned when using a beta version."""


class TomorrowWarning(BaseDummytestWarning):
    """Warned when using a tomorrow (nightly/unstable) version."""


class DeprecationWarning(BaseDummytestWarning):
    """Warned when using a deprecated feature."""


class ExperimentalWarning(BaseDummytestWarning):
    """Warned when using an experimental feature."""


class ConfigWarning(BaseDummytestWarning):
    """Warned when a configuration issue is detected."""


_TAG_TO_WARNING = {
    "pre": PreReleaseWarning,
    "beta": BetaWarning,
    "tomorrow": TomorrowWarning,
}


def _check_version_warnings():
    version_lower = __version__.lower()
    for tag in _PRE_RELEASE_TAGS:
        if tag in version_lower:
            msg = f"You are using dummytest {__version__}, which is a {tag} release. Use at your own risk."
            warnings.warn(c.yellow(msg), _TAG_TO_WARNING[tag], stacklevel=2)
            return
