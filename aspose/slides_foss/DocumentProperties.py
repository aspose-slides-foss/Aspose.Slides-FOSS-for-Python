from __future__ import annotations
from datetime import datetime, timedelta
from typing import overload, TYPE_CHECKING, Any
from .IDocumentProperties import IDocumentProperties

if TYPE_CHECKING:
    from .IHeadingPair import IHeadingPair

class DocumentProperties(IDocumentProperties):
    """Represents properties of a presentation."""

    def _init_internal(self, package, presentation_ref=None):
        """Initialize with OPC package and optional weak reference to Presentation."""
        self._package = package
        self._presentation_ref = presentation_ref
        self._core_part = None
        self._app_part = None
        self._custom_part = None

    def _ensure_core(self):
        if self._core_part is None:
            from ._internal.pptx.core_properties_part import CorePropertiesPart
            self._core_part = CorePropertiesPart(self._package)
        return self._core_part

    def _ensure_app(self):
        if self._app_part is None:
            from ._internal.pptx.app_properties_part import AppPropertiesPart
            self._app_part = AppPropertiesPart(self._package)
        return self._app_part

    def _ensure_custom(self):
        if self._custom_part is None:
            from ._internal.pptx.custom_properties_part import CustomPropertiesPart
            self._custom_part = CustomPropertiesPart(self._package)
        return self._custom_part

    # ── Core properties (via CorePropertiesPart) ──

    @property
    def title(self) -> str:
        """Returns or sets the title of a presentation. Read/write ."""
        return self._ensure_core().title or ''

    @title.setter
    def title(self, value: str):
        core = self._ensure_core()
        core.title = value
        core.mark_dirty()

    @property
    def subject(self) -> str:
        """Returns or sets the subject of a presentation. Read/write ."""
        return self._ensure_core().subject or ''

    @subject.setter
    def subject(self, value: str):
        core = self._ensure_core()
        core.subject = value
        core.mark_dirty()

    @property
    def author(self) -> str:
        """Returns or sets the author of a presentation. Read/write ."""
        return self._ensure_core().creator or ''

    @author.setter
    def author(self, value: str):
        core = self._ensure_core()
        core.creator = value
        core.mark_dirty()

    @property
    def keywords(self) -> str:
        """Returns or sets the keywords of a presentation. Read/write ."""
        return self._ensure_core().keywords or ''

    @keywords.setter
    def keywords(self, value: str):
        core = self._ensure_core()
        core.keywords = value
        core.mark_dirty()

    @property
    def comments(self) -> str:
        """Returns or sets the comments of a presentation. Read/write ."""
        return self._ensure_core().description or ''

    @comments.setter
    def comments(self, value: str):
        core = self._ensure_core()
        core.description = value
        core.mark_dirty()

    @property
    def category(self) -> str:
        """Returns or sets the category of a presentation. Read/write ."""
        return self._ensure_core().category or ''

    @category.setter
    def category(self, value: str):
        core = self._ensure_core()
        core.category = value
        core.mark_dirty()

    @property
    def content_status(self) -> str:
        """Returns or sets the content status of a presentation. Read/write ."""
        return self._ensure_core().content_status or ''

    @content_status.setter
    def content_status(self, value: str):
        core = self._ensure_core()
        core.content_status = value
        core.mark_dirty()

    @property
    def content_type(self) -> str:
        """Returns or sets the content type of a presentation. Read/write ."""
        return self._ensure_core().content_type or ''

    @content_type.setter
    def content_type(self, value: str):
        core = self._ensure_core()
        core.content_type = value
        core.mark_dirty()

    @property
    def last_saved_by(self) -> str:
        """Returns or sets the name of a last person who modified a presentation. Read/write ."""
        return self._ensure_core().last_modified_by or ''

    @last_saved_by.setter
    def last_saved_by(self, value: str):
        core = self._ensure_core()
        core.last_modified_by = value
        core.mark_dirty()

    @property
    def revision_number(self) -> int:
        """Returns or sets the presentation revision number. Read/write ."""
        rev = self._ensure_core().revision
        if rev:
            try:
                return int(rev)
            except ValueError:
                pass
        return 0

    @revision_number.setter
    def revision_number(self, value: int):
        core = self._ensure_core()
        core.revision = str(value)
        core.mark_dirty()

    @property
    def created_time(self) -> Any:
        """Returns the date a presentation was created. Values are in UTC. Read/write ."""
        return self._ensure_core().created

    @created_time.setter
    def created_time(self, value: Any):
        core = self._ensure_core()
        core.created = value
        core.mark_dirty()

    @property
    def last_saved_time(self) -> Any:
        """Returns the date a presentation was last modified. Values are in UTC. Read-only in case of Presentation.DocumentProperties (because it will be updated internally while IPresentation object saving process). Can be changed via DocumentProperties instance returning by method Please see the example in method summary."""
        return self._ensure_core().modified

    @last_saved_time.setter
    def last_saved_time(self, value: Any):
        core = self._ensure_core()
        core.modified = value
        core.mark_dirty()

    @property
    def last_printed(self) -> Any:
        """Returns the date when a presentation was printed last time. Read/write ."""
        return self._ensure_core().last_printed

    @last_printed.setter
    def last_printed(self, value: Any):
        core = self._ensure_core()
        core.last_printed = value
        core.mark_dirty()

    # ── App properties (via AppPropertiesPart) ──

    @property
    def app_version(self) -> str:
        """Returns the app version. Read-only ."""
        return self._ensure_app().app_version or ''

    @property
    def name_of_application(self) -> str:
        """Returns or sets the name of the application. Read/write ."""
        return self._ensure_app().application or ''

    @name_of_application.setter
    def name_of_application(self, value: str):
        app = self._ensure_app()
        app.application = value
        app.mark_dirty()

    @property
    def company(self) -> str:
        """Returns or sets the company property. Read/write ."""
        return self._ensure_app().company or ''

    @company.setter
    def company(self, value: str):
        app = self._ensure_app()
        app.company = value
        app.mark_dirty()

    @property
    def manager(self) -> str:
        """Returns or sets the manager property. Read/write ."""
        return self._ensure_app().manager or ''

    @manager.setter
    def manager(self, value: str):
        app = self._ensure_app()
        app.manager = value
        app.mark_dirty()

    @property
    def presentation_format(self) -> str:
        """Returns or sets the intended format of a presentation. Read/write ."""
        return self._ensure_app().presentation_format or ''

    @presentation_format.setter
    def presentation_format(self, value: str):
        app = self._ensure_app()
        app.presentation_format = value
        app.mark_dirty()

    @property
    def application_template(self) -> str:
        """Returns or sets the template of a application. Read/write ."""
        return self._ensure_app().template or ''

    @application_template.setter
    def application_template(self, value: str):
        app = self._ensure_app()
        app.template = value
        app.mark_dirty()

    @property
    def hyperlink_base(self) -> str:
        """Returns or sets the HyperlinkBase document property. Read/write ."""
        return self._ensure_app().hyperlink_base or ''

    @hyperlink_base.setter
    def hyperlink_base(self, value: str):
        app = self._ensure_app()
        app.hyperlink_base = value
        app.mark_dirty()

    @property
    def total_editing_time(self) -> timedelta:
        """Total editing time of a presentation. Read/write ."""
        minutes = self._ensure_app().total_time
        if minutes is not None:
            return timedelta(minutes=minutes)
        return timedelta(0)

    @total_editing_time.setter
    def total_editing_time(self, value: timedelta):
        app = self._ensure_app()
        app.total_time = int(value.total_seconds() / 60)
        app.mark_dirty()

    @property
    def shared_doc(self) -> bool:
        """Determines whether the presentation is shared between multiple people. Read/write ."""
        val = self._ensure_app().shared_doc
        return val if val is not None else False

    @shared_doc.setter
    def shared_doc(self, value: bool):
        app = self._ensure_app()
        app.shared_doc = value
        app.mark_dirty()

    @property
    def scale_crop(self) -> bool:
        """Indicates the display mode of the document thumbnail. Set this element to true to enable scaling of the document thumbnail to the display. Set this element to false to enable cropping of the document thumbnail to show only sections that fits the display. Read/write ."""
        val = self._ensure_app().scale_crop
        return val if val is not None else False

    @scale_crop.setter
    def scale_crop(self, value: bool):
        app = self._ensure_app()
        app.scale_crop = value
        app.mark_dirty()

    @property
    def links_up_to_date(self) -> bool:
        """Indicates whether hyperlinks in a document are up-to-date. Set this element to true to indicate that hyperlinks are updated. Set this element to false to indicate that hyperlinks are outdated. Read/write ."""
        val = self._ensure_app().links_up_to_date
        return val if val is not None else False

    @links_up_to_date.setter
    def links_up_to_date(self, value: bool):
        app = self._ensure_app()
        app.links_up_to_date = value
        app.mark_dirty()

    @property
    def hyperlinks_changed(self) -> bool:
        """Specifies that one or more hyperlinks in this part were updated exclusively in this part by a producer. The next producer to open this document shall update the hyperlink relationships with the new hyperlinks specified in this part. Read/write ."""
        val = self._ensure_app().hyperlinks_changed
        return val if val is not None else False

    @hyperlinks_changed.setter
    def hyperlinks_changed(self, value: bool):
        app = self._ensure_app()
        app.hyperlinks_changed = value
        app.mark_dirty()

    # ── Read-only statistics from app.xml ──

    @property
    def slides(self) -> int:
        """Returns the total number of slides in a presentation document. Read-only ."""
        return self._ensure_app().slides or 0

    @property
    def hidden_slides(self) -> int:
        """Returns the number of hidden slides in a presentation document. Read-only ."""
        return self._ensure_app().hidden_slides or 0

    @property
    def notes(self) -> int:
        """Returns the number of slides in a presentation containing notes. Read-only ."""
        return self._ensure_app().notes or 0

    @property
    def paragraphs(self) -> int:
        """Returns the total number of paragraphs found in a document if applicable. Read-only ."""
        return self._ensure_app().paragraphs or 0

    @property
    def words(self) -> int:
        """Returns the total number of words contained in a document. Read-only ."""
        return self._ensure_app().words or 0

    @property
    def multimedia_clips(self) -> int:
        """Returns the total number of sound or video clips that are present in the document. Read-only ."""
        return self._ensure_app().mm_clips or 0

    # ── Heading pairs and titles of parts ──

    @property
    def heading_pairs(self) -> list[IHeadingPair]:
        """Indicates the grouping of document parts and the number of parts in each group. Read-only ."""
        from .HeadingPair import HeadingPair
        result = []
        for hp_data in self._ensure_app().heading_pairs:
            hp = HeadingPair()
            hp._init_internal(hp_data.name, hp_data.count)
            result.append(hp)
        return result

    @property
    def titles_of_parts(self) -> list[str]:
        """Specifies the title of each document part. These parts are not document parts but conceptual representations of document sections. Read-only ."""
        return list(self._ensure_app().titles_of_parts)

    # ── Custom properties ──

    @property
    def count_of_custom_properties(self) -> int:
        """Returns the number of custom properties actually contained in a collection. Read-only ."""
        return self._ensure_custom().count







    def get_custom_property_value(self, *args, **kwargs) -> None:
        """Get a custom property value by name. The value is returned via the second argument (list)."""
        if len(args) >= 2:
            name = args[0]
            out = args[1]
            val = self._ensure_custom().get_value(name)
            if isinstance(out, list):
                out.clear()
                if val is not None:
                    out.append(val)







    def set_custom_property_value(self, *args, **kwargs) -> None:
        """Set a custom property value by name."""
        if len(args) >= 2:
            name = args[0]
            value = args[1]
            self._ensure_custom().set_value(name, value)

    def get_custom_property_name(self, index) -> str:
        return self._ensure_custom().get_name(index)

    def remove_custom_property(self, name) -> bool:
        return self._ensure_custom().remove(name)

    def contains_custom_property(self, name) -> bool:
        return self._ensure_custom().contains(name)

    def clear_custom_properties(self) -> None:
        self._ensure_custom().clear()

    # ── Built-in property operations ──

    def clear_built_in_properties(self) -> None:
        self._ensure_core().clear()
        self._ensure_app().clear()

    # ── Save ──

    def _save(self):
        """Serialize all loaded parts back to the package."""
        if hasattr(self, '_core_part') and self._core_part is not None:
            self._core_part.save()
        if hasattr(self, '_app_part') and self._app_part is not None:
            self._app_part.save()
        if hasattr(self, '_custom_part') and self._custom_part is not None:
            self._custom_part.save()

    # ── Not yet implemented ──



