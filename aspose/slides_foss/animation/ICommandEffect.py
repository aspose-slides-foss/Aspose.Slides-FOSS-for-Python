from __future__ import annotations
from abc import ABC, abstractmethod
from typing import TYPE_CHECKING
from .IBehavior import IBehavior

if TYPE_CHECKING:
    from .BehaviorAdditiveType import BehaviorAdditiveType
    from .CommandEffectType import CommandEffectType
    from .IBehaviorPropertyCollection import IBehaviorPropertyCollection
    from ..IShape import IShape
    from .ITiming import ITiming
    from ..NullableBool import NullableBool

class ICommandEffect(IBehavior, ABC):
    """Represents a command effect for an animation behavior."""
    @property
    @abstractmethod
    def type(self) -> CommandEffectType:
        """Defines command effect type of behavior. Read/write ."""
        ...
    @type.setter
    @abstractmethod
    def type(self, value: CommandEffectType):
        ...
    @property
    @abstractmethod
    def command_string(self) -> str:
        """Defines command string. Read/write ."""
        ...
    @command_string.setter
    @abstractmethod
    def command_string(self, value: str):
        ...
    @property
    @abstractmethod
    def shape_target(self) -> IShape:
        """Defines shape target of command effect. Read/write ."""
        ...
    @shape_target.setter
    @abstractmethod
    def shape_target(self, value: IShape):
        ...
    @property
    @abstractmethod
    def as_i_behavior(self) -> IBehavior:
        """Allows to get base IBehavior interface. Read-only ."""
        ...
    @property
    @abstractmethod
    def accumulate(self) -> NullableBool:
        ...
    @accumulate.setter
    @abstractmethod
    def accumulate(self, value: NullableBool):
        ...
    @property
    @abstractmethod
    def additive(self) -> BehaviorAdditiveType:
        ...
    @additive.setter
    @abstractmethod
    def additive(self, value: BehaviorAdditiveType):
        ...
    @property
    @abstractmethod
    def properties(self) -> IBehaviorPropertyCollection:
        ...
    @property
    @abstractmethod
    def timing(self) -> ITiming:
        ...
    @timing.setter
    @abstractmethod
    def timing(self, value: ITiming):
        ...