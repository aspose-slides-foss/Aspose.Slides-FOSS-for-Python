from __future__ import annotations
from abc import ABC, abstractmethod
from typing import overload, TYPE_CHECKING, Any

from datetime import timedelta

if TYPE_CHECKING:
    from .IHeadingPair import IHeadingPair

class IDocumentProperties(ABC):
    """Represents properties of a presentation."""
    @property
    def app_version(self) -> str:
        """Returns the app version. Read-only ."""
        ...

    @property
    def name_of_application(self) -> str:
        """Returns or sets the name of the application. Read/write ."""
        ...

    @name_of_application.setter
    def name_of_application(self, value: str):
        ...

    @property
    def company(self) -> str:
        """Returns or sets the company property. Read/write ."""
        ...

    @company.setter
    def company(self, value: str):
        ...

    @property
    def manager(self) -> str:
        """Returns or sets the manager property. Read/write ."""
        ...

    @manager.setter
    def manager(self, value: str):
        ...

    @property
    def presentation_format(self) -> str:
        """Returns or sets the intended format of a presentation. Read/write ."""
        ...

    @presentation_format.setter
    def presentation_format(self, value: str):
        ...

    @property
    def shared_doc(self) -> bool:
        """Determines whether the presentation is shared between multiple people. Read/write ."""
        ...

    @shared_doc.setter
    def shared_doc(self, value: bool):
        ...

    @property
    def application_template(self) -> str:
        """Returns or sets the template of a application. Read/write ."""
        ...

    @application_template.setter
    def application_template(self, value: str):
        ...

    @property
    def total_editing_time(self) -> timedelta:
        """Total editing time of a presentation. Read/write ."""
        ...

    @total_editing_time.setter
    def total_editing_time(self, value: timedelta):
        ...

    @property
    def title(self) -> str:
        """Returns or sets the title of a presentation. Read/write ."""
        ...

    @title.setter
    def title(self, value: str):
        ...

    @property
    def subject(self) -> str:
        """Returns or sets the subject of a presentation. Read/write ."""
        ...

    @subject.setter
    def subject(self, value: str):
        ...

    @property
    def author(self) -> str:
        """Returns or sets the author of a presentation. Read/write ."""
        ...

    @author.setter
    def author(self, value: str):
        ...

    @property
    def keywords(self) -> str:
        """Returns or sets the keywords of a presentation. Read/write ."""
        ...

    @keywords.setter
    def keywords(self, value: str):
        ...

    @property
    def comments(self) -> str:
        """Returns or sets the comments of a presentation. Read/write ."""
        ...

    @comments.setter
    def comments(self, value: str):
        ...

    @property
    def category(self) -> str:
        """Returns or sets the category of a presentation. Read/write ."""
        ...

    @category.setter
    def category(self, value: str):
        ...

    @property
    def created_time(self) -> Any:
        """Returns the date a presentation was created. Values are in UTC. Read/write ."""
        ...

    @created_time.setter
    def created_time(self, value: Any):
        ...

    @property
    def last_saved_time(self) -> Any:
        """Returns the date a presentation was last modified. Values are in UTC.P Read-only in case of Presentation.DocumentProperties (because it will be updated internally while IPresentation object saving process). Can be changed via DocumentProperties instance returning by method Please see the example in method summary."""
        ...

    @last_saved_time.setter
    def last_saved_time(self, value: Any):
        ...

    @property
    def last_printed(self) -> Any:
        """Returns the date when a presentation was printed last time. Read/write ."""
        ...

    @last_printed.setter
    def last_printed(self, value: Any):
        ...

    @property
    def last_saved_by(self) -> str:
        """Returns or sets the name of a last person who modified a presentation. Read/write ."""
        ...

    @last_saved_by.setter
    def last_saved_by(self, value: str):
        ...

    @property
    def revision_number(self) -> int:
        """Returns or sets the presentation revision number. Read/write ."""
        ...

    @revision_number.setter
    def revision_number(self, value: int):
        ...

    @property
    def content_status(self) -> str:
        """Returns or sets the content status of a presentation. Read/write ."""
        ...

    @content_status.setter
    def content_status(self, value: str):
        ...

    @property
    def content_type(self) -> str:
        """Returns or sets the content type of a presentation. Read/write ."""
        ...

    @content_type.setter
    def content_type(self, value: str):
        ...

    @property
    def hyperlink_base(self) -> str:
        """Returns or sets the HyperlinkBase document property. Read/write ."""
        ...

    @hyperlink_base.setter
    def hyperlink_base(self, value: str):
        ...

    @property
    def scale_crop(self) -> bool:
        """Indicates the display mode of the document thumbnail. Set this element to true to enable scaling of the document thumbnail to the display. Set this element to false to enable cropping of the document thumbnail to show only sections that fits the display. Read/write ."""
        ...

    @scale_crop.setter
    def scale_crop(self, value: bool):
        ...

    @property
    def links_up_to_date(self) -> bool:
        """Indicates whether hyperlinks in a document are up-to-date. Set this element to true to indicate that hyperlinks are updated. Set this element to false to indicate that hyperlinks are outdated. Read/write ."""
        ...

    @links_up_to_date.setter
    def links_up_to_date(self, value: bool):
        ...

    @property
    def hyperlinks_changed(self) -> bool:
        """Specifies that one or more hyperlinks in this part were updated exclusively in this part by a producer. The next producer to open this document shall update the hyperlink relationships with the new hyperlinks specified in this part. Read/write ."""
        ...

    @hyperlinks_changed.setter
    def hyperlinks_changed(self, value: bool):
        ...

    @property
    def slides(self) -> int:
        """Specifies the total number of slides in a presentation document. Read-only ."""
        ...

    @property
    def hidden_slides(self) -> int:
        """Specifies the number of hidden slides in a presentation document. Read-only ."""
        ...

    @property
    def notes(self) -> int:
        """Specifies the number of slides in a presentation containing notes. Read-only ."""
        ...

    @property
    def paragraphs(self) -> int:
        """Specifies the total number of paragraphs found in a document if applicable. Read-only ."""
        ...

    @property
    def words(self) -> int:
        """Specifies the total number of words contained in a document. Read-only ."""
        ...

    @property
    def multimedia_clips(self) -> int:
        """Specifies the total number of sound or video clips that are present in the document. Read-only ."""
        ...

    @property
    def titles_of_parts(self) -> list[str]:
        """Specifies the title of each document part. These parts are not document parts but conceptual representations of document sections. Read-only ."""
        ...

    @property
    def heading_pairs(self) -> list[IHeadingPair]:
        """Indicates the grouping of document parts and the number of parts in each group. Read-only ."""
        ...

    @property
    def count_of_custom_properties(self) -> int:
        """Returns the number of custom properties actually contained in a collection. Read-only ."""
        ...

    @overload
    def get_custom_property_value(self, name, value) -> None:
        ...

    @overload
    def get_custom_property_value(self, name, value) -> None:
        ...

    @overload
    def get_custom_property_value(self, name, value) -> None:
        ...

    @overload
    def get_custom_property_value(self, name, value) -> None:
        ...

    @overload
    def get_custom_property_value(self, name, value) -> None:
        ...

    @overload
    def get_custom_property_value(self, name, value) -> None:
        ...


    @overload
    def set_custom_property_value(self, name, value) -> None:
        ...

    @overload
    def set_custom_property_value(self, name, value) -> None:
        ...

    @overload
    def set_custom_property_value(self, name, value) -> None:
        ...

    @overload
    def set_custom_property_value(self, name, value) -> None:
        ...

    @overload
    def set_custom_property_value(self, name, value) -> None:
        ...

    @overload
    def set_custom_property_value(self, name, value) -> None:
        ...
    def get_custom_property_name(self, index) -> str:
        ...
    def remove_custom_property(self, name) -> bool:
        ...
    def contains_custom_property(self, name) -> bool:
        ...
    def clear_custom_properties(self) -> None:
        ...
    def clear_built_in_properties(self) -> None:
        ...


