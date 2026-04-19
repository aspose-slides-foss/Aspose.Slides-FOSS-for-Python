from __future__ import annotations
from typing import TYPE_CHECKING
from .Behavior import Behavior
from .IBehavior import IBehavior
from .ICommandEffect import ICommandEffect

if TYPE_CHECKING:
    from .CommandEffectType import CommandEffectType
    from ..IShape import IShape


class CommandEffect(Behavior, ICommandEffect):
    """Represent command effect behavior of effect."""

    def __init__(self):
        self._type_val = None
        self._command_str = ''
        self._shape_target = None

    @property
    def type(self) -> CommandEffectType:
        from .CommandEffectType import CommandEffectType
        if hasattr(self, '_elem') and self._elem is not None:
            val = self._elem.get('type')
            _map = {'evt': CommandEffectType.EVENT, 'call': CommandEffectType.CALL, 'verb': CommandEffectType.VERB}
            return _map.get(val, CommandEffectType.NOT_DEFINED)
        return self._type_val or CommandEffectType.NOT_DEFINED

    @type.setter
    def type(self, value: CommandEffectType):
        self._type_val = value

    @property
    def command_string(self) -> str:
        if hasattr(self, '_elem') and self._elem is not None:
            return self._elem.get('cmd', '')
        return self._command_str

    @command_string.setter
    def command_string(self, value: str):
        self._command_str = value
        if hasattr(self, '_elem') and self._elem is not None:
            self._elem.set('cmd', value)

    @property
    def shape_target(self) -> IShape:
        return self._shape_target

    @shape_target.setter
    def shape_target(self, value: IShape):
        self._shape_target = value

    @property
    def as_i_behavior(self) -> IBehavior:
        return self
