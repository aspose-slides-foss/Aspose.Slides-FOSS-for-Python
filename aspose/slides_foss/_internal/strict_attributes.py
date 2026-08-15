"""Refusing assignments to names the object has no property for.

Presentation content is expressed by assigning to properties, and Python
accepts an assignment to any name at all.  Without this, a misspelt property
name, or one belonging to a feature that is not implemented yet, is accepted
and then discarded when the object is written out: the call looks like it
worked and the setting is simply absent from the file.  That is
indistinguishable from a working call until somebody opens the result, and it
is the reason an unimplemented property is worse than a missing one.

Internal state is named with a leading underscore and is not affected.
"""

from __future__ import annotations


class StrictAttributes:
    """Mixin that turns an unknown property assignment into ``AttributeError``."""

    def __setattr__(self, name: str, value) -> None:
        if not name.startswith('_') and not hasattr(type(self), name):
            raise AttributeError(
                "%s has no property %r; the assignment would have been accepted "
                "and then silently discarded" % (type(self).__name__, name)
            )
        object.__setattr__(self, name, value)
