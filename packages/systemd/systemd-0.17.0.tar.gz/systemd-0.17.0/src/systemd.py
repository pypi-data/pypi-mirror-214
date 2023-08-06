import warnings

from cysystemd import (
    reader, sd_daemon, sd_id128, sd_journal, async_reader, daemon, journal,
    package_info, version_info, author_info, author_email, license,
    __version__, __author__
)

__all__ = (
    "reader", "sd_daemon", "sd_id128", "sd_journal", "async_reader", "daemon",
    "journal", "__author__", "__version__", "author_info", "license",
    "package_info", "version_info",
)


warnings.warn(
    "This package has been renamed to cysystemd, please use this instead.",
    DeprecationWarning
)
