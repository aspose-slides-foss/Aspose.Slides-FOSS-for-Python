from __future__ import annotations
from .IBehaviorProperty import IBehaviorProperty


# Internal registry of predefined properties
_PREDEFINED: dict[str, BehaviorProperty] = {}


def _make(name: str) -> BehaviorProperty:
    """Create and register a predefined property."""
    bp = BehaviorProperty.__new__(BehaviorProperty)
    bp._value = name
    bp._is_custom = False
    _PREDEFINED[name] = bp
    return bp


class BehaviorProperty(IBehaviorProperty):
    """Represent property types for animation behavior. Follows the list of properties from https://msdn.microsoft.com/en-us/library/dd949052(v=office.15).aspx and https://msdn.microsoft.com/en-us/library/documentformat.openxml.presentation.attributename(v=office.15).aspx"""

    def __init__(self):
        self._value = ''
        self._is_custom = True

    @property
    def value(self) -> str:
        """Value of the property"""
        return self._value

    @property
    def is_custom(self) -> bool:
        """Shows if this property does not belong to the predefined properties list in the specification: https://msdn.microsoft.com/en-us/library/dd949052(v=office.15).aspx"""
        return self._is_custom

    # ---- position / transform ----

    @property
    def ppt_x(self) -> BehaviorProperty:
        """Represents 'ppt_x' property"""
        return _PREDEFINED['ppt_x']

    @property
    def ppt_y(self) -> BehaviorProperty:
        """Represents 'ppt_y' property"""
        return _PREDEFINED['ppt_y']

    @property
    def ppt_w(self) -> BehaviorProperty:
        """Represents 'ppt_w' property"""
        return _PREDEFINED['ppt_w']

    @property
    def ppt_h(self) -> BehaviorProperty:
        """Represents 'ppt_h' property"""
        return _PREDEFINED['ppt_h']

    @property
    def ppt_c(self) -> BehaviorProperty:
        """Represents 'ppt_c' property"""
        return _PREDEFINED['ppt_c']

    @property
    def ppt_r(self) -> BehaviorProperty:
        """Represents 'ppt_r' property"""
        return _PREDEFINED['ppt_r']

    @property
    def x_shear(self) -> BehaviorProperty:
        """Represents 'xshear' property"""
        return _PREDEFINED['xshear']

    @property
    def y_shear(self) -> BehaviorProperty:
        """Represents 'yshear' property"""
        return _PREDEFINED['yshear']

    @property
    def image(self) -> BehaviorProperty:
        """Represents 'image' property"""
        return _PREDEFINED['image']

    @property
    def scale_x(self) -> BehaviorProperty:
        """Represents 'ScaleX' property"""
        return _PREDEFINED['ScaleX']

    @property
    def scale_y(self) -> BehaviorProperty:
        """Represents 'ScaleY' property"""
        return _PREDEFINED['ScaleY']

    @property
    def r(self) -> BehaviorProperty:
        """Represents 'r' property"""
        return _PREDEFINED['r']

    @property
    def fill_color(self) -> BehaviorProperty:
        """Represents 'fillcolor' property"""
        return _PREDEFINED['fillcolor']

    # ---- style ----

    @property
    def style_opacity(self) -> BehaviorProperty:
        """Represents 'style.opacity' property"""
        return _PREDEFINED['style.opacity']

    @property
    def style_rotation(self) -> BehaviorProperty:
        """Represents 'style.rotation' property"""
        return _PREDEFINED['style.rotation']

    @property
    def style_visibility(self) -> BehaviorProperty:
        """Represents 'style.visibility' property"""
        return _PREDEFINED['style.visibility']

    @property
    def style_color(self) -> BehaviorProperty:
        """Represents 'style.color' property"""
        return _PREDEFINED['style.color']

    @property
    def style_font_size(self) -> BehaviorProperty:
        """Represents 'style.fontSize' property"""
        return _PREDEFINED['style.fontSize']

    @property
    def style_font_weight(self) -> BehaviorProperty:
        """Represents 'style.fontWeight' property"""
        return _PREDEFINED['style.fontWeight']

    @property
    def style_font_style(self) -> BehaviorProperty:
        """Represents 'style.fontStyle' property"""
        return _PREDEFINED['style.fontStyle']

    @property
    def style_font_family(self) -> BehaviorProperty:
        """Represents 'style.fontFamily' property"""
        return _PREDEFINED['style.fontFamily']

    @property
    def style_text_effect_emboss(self) -> BehaviorProperty:
        """Represents 'style.textEffectEmboss' property"""
        return _PREDEFINED['style.textEffectEmboss']

    @property
    def style_text_shadow(self) -> BehaviorProperty:
        """Represents 'style.textShadow' property"""
        return _PREDEFINED['style.textShadow']

    @property
    def style_text_transform(self) -> BehaviorProperty:
        """Represents 'style.textTransform' property"""
        return _PREDEFINED['style.textTransform']

    @property
    def style_text_decoration_underline(self) -> BehaviorProperty:
        """Represents 'style.textDecorationUnderline' property"""
        return _PREDEFINED['style.textDecorationUnderline']

    @property
    def style_text_effect_outline(self) -> BehaviorProperty:
        """Represents 'style.textEffectOutline' property"""
        return _PREDEFINED['style.textEffectOutline']

    @property
    def style_text_decoration_line_through(self) -> BehaviorProperty:
        """Represents 'style.textDecorationLineThrough' property"""
        return _PREDEFINED['style.textDecorationLineThrough']

    @property
    def style_s_rotation(self) -> BehaviorProperty:
        """Represents 'style.sRotation' property"""
        return _PREDEFINED['style.sRotation']

    # ---- imageData ----

    @property
    def image_data_crop_top(self) -> BehaviorProperty:
        """Represents 'imageData.cropTop' property"""
        return _PREDEFINED['imageData.cropTop']

    @property
    def image_data_crop_bottom(self) -> BehaviorProperty:
        """Represents 'imageData.cropBottom' property"""
        return _PREDEFINED['imageData.cropBottom']

    @property
    def image_data_crop_left(self) -> BehaviorProperty:
        """Represents 'imageData.cropLeft' property"""
        return _PREDEFINED['imageData.cropLeft']

    @property
    def image_data_crop_right(self) -> BehaviorProperty:
        """Represents 'imageData.cropRight' property"""
        return _PREDEFINED['imageData.cropRight']

    @property
    def image_data_gain(self) -> BehaviorProperty:
        """Represents 'imageData.gain' property"""
        return _PREDEFINED['imageData.gain']

    @property
    def image_data_blacklevel(self) -> BehaviorProperty:
        """Represents 'imageData.blacklevel' property"""
        return _PREDEFINED['imageData.blacklevel']

    @property
    def image_data_gamma(self) -> BehaviorProperty:
        """Represents 'imageData.gamma' property"""
        return _PREDEFINED['imageData.gamma']

    @property
    def image_data_grayscale(self) -> BehaviorProperty:
        """Represents 'imageData.grayscale' property"""
        return _PREDEFINED['imageData.grayscale']

    @property
    def image_data_chromakey(self) -> BehaviorProperty:
        """Represents 'imageData.chromakey' property"""
        return _PREDEFINED['imageData.chromakey']

    # ---- fill ----

    @property
    def fill_on(self) -> BehaviorProperty:
        """Represents 'fill.on' property"""
        return _PREDEFINED['fill.on']

    @property
    def fill_type(self) -> BehaviorProperty:
        """Represents 'fill.type' property"""
        return _PREDEFINED['fill.type']

    @property
    def fill_color_(self) -> BehaviorProperty:
        """Represents 'fill.color' property"""
        return _PREDEFINED['fill.color']

    @property
    def fill_opacity(self) -> BehaviorProperty:
        """Represents 'fill.opacity' property"""
        return _PREDEFINED['fill.opacity']

    @property
    def fill_color2(self) -> BehaviorProperty:
        """Represents 'fill.color2' property"""
        return _PREDEFINED['fill.color2']

    @property
    def fill_method(self) -> BehaviorProperty:
        """Represents 'fill.method' property"""
        return _PREDEFINED['fill.method']

    @property
    def fill_opacity2(self) -> BehaviorProperty:
        """Represents 'fill.opacity2' property"""
        return _PREDEFINED['fill.opacity2']

    @property
    def fill_angle(self) -> BehaviorProperty:
        """Represents 'fill.angle' property"""
        return _PREDEFINED['fill.angle']

    @property
    def fill_focus(self) -> BehaviorProperty:
        """Represents 'fill.focus' property"""
        return _PREDEFINED['fill.focus']

    @property
    def fill_focus_position_x(self) -> BehaviorProperty:
        """Represents 'fill.focusposition.x' property"""
        return _PREDEFINED['fill.focusposition.x']

    @property
    def fill_focus_position_y(self) -> BehaviorProperty:
        """Represents 'fill.focusposition.y' property"""
        return _PREDEFINED['fill.focusposition.y']

    @property
    def fill_focus_size_x(self) -> BehaviorProperty:
        """Represents 'fill.focussize.x' property"""
        return _PREDEFINED['fill.focussize.x']

    @property
    def fill_focus_size_y(self) -> BehaviorProperty:
        """Represents 'fill.focussize.y' property"""
        return _PREDEFINED['fill.focussize.y']

    # ---- stroke ----

    @property
    def stroke_on(self) -> BehaviorProperty:
        """Represents 'stroke.on' property"""
        return _PREDEFINED['stroke.on']

    @property
    def stroke_color(self) -> BehaviorProperty:
        """Represents 'stroke.color' property"""
        return _PREDEFINED['stroke.color']

    @property
    def stroke_weight(self) -> BehaviorProperty:
        """Represents 'stroke.weight' property"""
        return _PREDEFINED['stroke.weight']

    @property
    def stroke_opacity(self) -> BehaviorProperty:
        """Represents 'stroke.opacity' property"""
        return _PREDEFINED['stroke.opacity']

    @property
    def stroke_line_style(self) -> BehaviorProperty:
        """Represents 'stroke.linestyle' property"""
        return _PREDEFINED['stroke.linestyle']

    @property
    def stroke_dash_style(self) -> BehaviorProperty:
        """Represents 'stroke.dashstyle' property"""
        return _PREDEFINED['stroke.dashstyle']

    @property
    def stroke_fill_type(self) -> BehaviorProperty:
        """Represents 'stroke.filltype' property"""
        return _PREDEFINED['stroke.filltype']

    @property
    def stroke_src(self) -> BehaviorProperty:
        """Represents 'stroke.src' property"""
        return _PREDEFINED['stroke.src']

    @property
    def stroke_color2(self) -> BehaviorProperty:
        """Represents 'stroke.color2' property"""
        return _PREDEFINED['stroke.color2']

    @property
    def stroke_image_size_x(self) -> BehaviorProperty:
        """Represents 'stroke.imagesize.x' property"""
        return _PREDEFINED['stroke.imagesize.x']

    @property
    def stroke_image_size_y(self) -> BehaviorProperty:
        """Represents 'stroke.imagesize.y' property"""
        return _PREDEFINED['stroke.imagesize.y']

    @property
    def stroke_start_arrow(self) -> BehaviorProperty:
        """Represents 'stroke.startArrow' property"""
        return _PREDEFINED['stroke.startArrow']

    @property
    def stroke_end_arrow(self) -> BehaviorProperty:
        """Represents 'stroke.endArrow' property"""
        return _PREDEFINED['stroke.endArrow']

    @property
    def stroke_start_arrow_width(self) -> BehaviorProperty:
        """Represents 'stroke.startArrowWidth' property"""
        return _PREDEFINED['stroke.startArrowWidth']

    @property
    def stroke_start_arrow_length(self) -> BehaviorProperty:
        """Represents 'stroke.startArrowLength' property"""
        return _PREDEFINED['stroke.startArrowLength']

    @property
    def stroke_end_arrow_width(self) -> BehaviorProperty:
        """Represents 'stroke.endArrowWidth' property"""
        return _PREDEFINED['stroke.endArrowWidth']

    @property
    def stroke_end_arrow_length(self) -> BehaviorProperty:
        """Represents 'stroke.endArrowLength' property"""
        return _PREDEFINED['stroke.endArrowLength']

    # ---- shadow ----

    @property
    def shadow_on(self) -> BehaviorProperty:
        """Represents 'shadow.on' property"""
        return _PREDEFINED['shadow.on']

    @property
    def shadow_type(self) -> BehaviorProperty:
        """Represents 'shadow.type' property"""
        return _PREDEFINED['shadow.type']

    @property
    def shadow_color(self) -> BehaviorProperty:
        """Represents 'shadow.color' property"""
        return _PREDEFINED['shadow.color']

    @property
    def shadow_color2(self) -> BehaviorProperty:
        """Represents 'shadow.color2' property"""
        return _PREDEFINED['shadow.color2']

    @property
    def shadow_opacity(self) -> BehaviorProperty:
        """Represents 'shadow.opacity' property"""
        return _PREDEFINED['shadow.opacity']

    @property
    def shadow_offset_x(self) -> BehaviorProperty:
        """Represents 'shadow.offset.x' property"""
        return _PREDEFINED['shadow.offset.x']

    @property
    def shadow_offset_y(self) -> BehaviorProperty:
        """Represents 'shadow.offset.y' property"""
        return _PREDEFINED['shadow.offset.y']

    @property
    def shadow_offset_2x(self) -> BehaviorProperty:
        """Represents 'shadow.offset2.x' property"""
        return _PREDEFINED['shadow.offset2.x']

    @property
    def shadow_offset_2y(self) -> BehaviorProperty:
        """Represents 'shadow.offset2.y' property"""
        return _PREDEFINED['shadow.offset2.y']

    @property
    def shadow_origin_x(self) -> BehaviorProperty:
        """Represents 'shadow.origin.x' property"""
        return _PREDEFINED['shadow.origin.x']

    @property
    def shadow_origin_y(self) -> BehaviorProperty:
        """Represents 'shadow.origin.y' property"""
        return _PREDEFINED['shadow.origin.y']

    @property
    def shadow_matrix_xto_x(self) -> BehaviorProperty:
        """Represents 'shadow.matrix.xtox' property"""
        return _PREDEFINED['shadow.matrix.xtox']

    @property
    def shadow_matrix_xto_y(self) -> BehaviorProperty:
        """Represents 'shadow.matrix.xtoy' property"""
        return _PREDEFINED['shadow.matrix.xtoy']

    @property
    def shadow_matrix_yto_x(self) -> BehaviorProperty:
        """Represents 'shadow.matrix.ytox' property"""
        return _PREDEFINED['shadow.matrix.ytox']

    @property
    def shadow_matrix_yto_y(self) -> BehaviorProperty:
        """Represents 'shadow.matrix.ytoy' property"""
        return _PREDEFINED['shadow.matrix.ytoy']

    @property
    def shadow_matrix_perspective_x(self) -> BehaviorProperty:
        """Represents 'shadow.matrix.perspectiveX' property"""
        return _PREDEFINED['shadow.matrix.perspectiveX']

    @property
    def shadow_matrix_perspective_y(self) -> BehaviorProperty:
        """Represents 'shadow.matrix.perspectiveY' property"""
        return _PREDEFINED['shadow.matrix.perspectiveY']

    # ---- skew ----

    @property
    def skew_on(self) -> BehaviorProperty:
        """Represents 'skew.on' property"""
        return _PREDEFINED['skew.on']

    @property
    def skew_offset_x(self) -> BehaviorProperty:
        """Represents 'skew.offset.x' property"""
        return _PREDEFINED['skew.offset.x']

    @property
    def skew_offset_y(self) -> BehaviorProperty:
        """Represents 'skew.offset.y' property"""
        return _PREDEFINED['skew.offset.y']

    @property
    def skew_origin_x(self) -> BehaviorProperty:
        """Represents 'skew.origin.x' property"""
        return _PREDEFINED['skew.origin.x']

    @property
    def skew_origin_y(self) -> BehaviorProperty:
        """Represents 'skew.origin.y' property"""
        return _PREDEFINED['skew.origin.y']

    @property
    def skew_matrix_xto_x(self) -> BehaviorProperty:
        """Represents 'skew.matrix.xtox' property"""
        return _PREDEFINED['skew.matrix.xtox']

    @property
    def skew_matrix_xto_y(self) -> BehaviorProperty:
        """Represents 'skew.matrix.xtoy' property"""
        return _PREDEFINED['skew.matrix.xtoy']

    @property
    def skew_matrix_yto_x(self) -> BehaviorProperty:
        """Represents 'skew.matrix.ytox' property"""
        return _PREDEFINED['skew.matrix.ytox']

    @property
    def skew_matrix_yto_y(self) -> BehaviorProperty:
        """Represents 'skew.matrix.ytoy' property"""
        return _PREDEFINED['skew.matrix.ytoy']

    @property
    def skew_matrix_perspective_x(self) -> BehaviorProperty:
        """Represents 'skew.matrix.perspectiveX' property"""
        return _PREDEFINED['skew.matrix.perspectiveX']

    @property
    def skew_matrix_perspective_y(self) -> BehaviorProperty:
        """Represents 'skew.matrix.perspectiveY' property"""
        return _PREDEFINED['skew.matrix.perspectiveY']

    # ---- extrusion ----

    @property
    def extrusion_on(self) -> BehaviorProperty:
        """Represents 'extrusion.on' property"""
        return _PREDEFINED['extrusion.on']

    @property
    def extrusion_type(self) -> BehaviorProperty:
        """Represents 'extrusion.type' property"""
        return _PREDEFINED['extrusion.type']

    @property
    def extrusion_render(self) -> BehaviorProperty:
        """Represents 'extrusion.render' property"""
        return _PREDEFINED['extrusion.render']

    @property
    def extrusion_view_point_origin_x(self) -> BehaviorProperty:
        """Represents 'extrusion.viewpointorigin.x' property"""
        return _PREDEFINED['extrusion.viewpointorigin.x']

    @property
    def extrusion_view_point_origin_y(self) -> BehaviorProperty:
        """Represents 'extrusion.viewpointorigin.y' property"""
        return _PREDEFINED['extrusion.viewpointorigin.y']

    @property
    def extrusion_view_point_x(self) -> BehaviorProperty:
        """Represents 'extrusion.viewpoint.x' property"""
        return _PREDEFINED['extrusion.viewpoint.x']

    @property
    def extrusion_view_point_y(self) -> BehaviorProperty:
        """Represents 'extrusion.viewpoint.y' property"""
        return _PREDEFINED['extrusion.viewpoint.y']

    @property
    def extrusion_view_point_z(self) -> BehaviorProperty:
        """Represents 'extrusion.viewpoint.z' property"""
        return _PREDEFINED['extrusion.viewpoint.z']

    @property
    def extrusion_plane(self) -> BehaviorProperty:
        """Represents 'extrusion.plane' property"""
        return _PREDEFINED['extrusion.plane']

    @property
    def extrusion_skew_angle(self) -> BehaviorProperty:
        """Represents 'extrusion.skewangle' property"""
        return _PREDEFINED['extrusion.skewangle']

    @property
    def extrusion_skew_amt(self) -> BehaviorProperty:
        """Represents 'extrusion.skewamt' property"""
        return _PREDEFINED['extrusion.skewamt']

    @property
    def extrusion_back_depth(self) -> BehaviorProperty:
        """Represents 'extrusion.backdepth' property"""
        return _PREDEFINED['extrusion.backdepth']

    @property
    def extrusion_fore_depth(self) -> BehaviorProperty:
        """Represents 'extrusion.foredepth' property"""
        return _PREDEFINED['extrusion.foredepth']

    @property
    def extrusion_orientation_x(self) -> BehaviorProperty:
        """Represents 'extrusion.orientation.x' property"""
        return _PREDEFINED['extrusion.orientation.x']

    @property
    def extrusion_orientation_y(self) -> BehaviorProperty:
        """Represents 'extrusion.orientation.y' property"""
        return _PREDEFINED['extrusion.orientation.y']

    @property
    def extrusion_orientation_z(self) -> BehaviorProperty:
        """Represents 'extrusion.orientation.z' property"""
        return _PREDEFINED['extrusion.orientation.z']

    @property
    def extrusion_orientation_angle(self) -> BehaviorProperty:
        """Represents 'extrusion.orientationangle' property"""
        return _PREDEFINED['extrusion.orientationangle']

    @property
    def extrusion_color(self) -> BehaviorProperty:
        """Represents 'extrusion.color' property"""
        return _PREDEFINED['extrusion.color']

    @property
    def extrusion_rotation_angle_x(self) -> BehaviorProperty:
        """Represents 'extrusion.rotationangle.x' property"""
        return _PREDEFINED['extrusion.rotationangle.x']

    @property
    def extrusion_rotation_angle_y(self) -> BehaviorProperty:
        """Represents 'extrusion.rotationangle.y' property"""
        return _PREDEFINED['extrusion.rotationangle.y']

    @property
    def extrusion_lock_rotation_center(self) -> BehaviorProperty:
        """Represents 'extrusion.lockrotationcenter' property"""
        return _PREDEFINED['extrusion.lockrotationcenter']

    @property
    def extrusion_auto_rotation_center(self) -> BehaviorProperty:
        """Represents 'extrusion.autorotationcenter' property"""
        return _PREDEFINED['extrusion.autorotationcenter']

    @property
    def extrusion_rotation_center_x(self) -> BehaviorProperty:
        """Represents 'extrusion.rotationcenter.x' property"""
        return _PREDEFINED['extrusion.rotationcenter.x']

    @property
    def extrusion_rotation_center_y(self) -> BehaviorProperty:
        """Represents 'extrusion.rotationcenter.y' property"""
        return _PREDEFINED['extrusion.rotationcenter.y']

    @property
    def extrusion_rotation_center_z(self) -> BehaviorProperty:
        """Represents 'extrusion.rotationcenter.z' property"""
        return _PREDEFINED['extrusion.rotationcenter.z']

    @property
    def extrusion_color_mode(self) -> BehaviorProperty:
        """Represents 'extrusion.colormode' property"""
        return _PREDEFINED['extrusion.colormode']

    def get_or_create_by_value(self, property_value) -> BehaviorProperty:
        if property_value in _PREDEFINED:
            return _PREDEFINED[property_value]
        bp = BehaviorProperty()
        bp._value = property_value
        bp._is_custom = True
        _PREDEFINED[property_value] = bp
        return bp


# Register all predefined properties at module load
for _name in [
    'ppt_x', 'ppt_y', 'ppt_w', 'ppt_h', 'ppt_c', 'ppt_r',
    'xshear', 'yshear', 'image', 'ScaleX', 'ScaleY', 'r', 'fillcolor',
    'style.opacity', 'style.rotation', 'style.visibility', 'style.color',
    'style.fontSize', 'style.fontWeight', 'style.fontStyle', 'style.fontFamily',
    'style.textEffectEmboss', 'style.textShadow', 'style.textTransform',
    'style.textDecorationUnderline', 'style.textEffectOutline',
    'style.textDecorationLineThrough', 'style.sRotation',
    'imageData.cropTop', 'imageData.cropBottom', 'imageData.cropLeft',
    'imageData.cropRight', 'imageData.gain', 'imageData.blacklevel',
    'imageData.gamma', 'imageData.grayscale', 'imageData.chromakey',
    'fill.on', 'fill.type', 'fill.color', 'fill.opacity', 'fill.color2',
    'fill.method', 'fill.opacity2', 'fill.angle', 'fill.focus',
    'fill.focusposition.x', 'fill.focusposition.y',
    'fill.focussize.x', 'fill.focussize.y',
    'stroke.on', 'stroke.color', 'stroke.weight', 'stroke.opacity',
    'stroke.linestyle', 'stroke.dashstyle', 'stroke.filltype', 'stroke.src',
    'stroke.color2', 'stroke.imagesize.x', 'stroke.imagesize.y',
    'stroke.startArrow', 'stroke.endArrow',
    'stroke.startArrowWidth', 'stroke.startArrowLength',
    'stroke.endArrowWidth', 'stroke.endArrowLength',
    'shadow.on', 'shadow.type', 'shadow.color', 'shadow.color2',
    'shadow.opacity', 'shadow.offset.x', 'shadow.offset.y',
    'shadow.offset2.x', 'shadow.offset2.y',
    'shadow.origin.x', 'shadow.origin.y',
    'shadow.matrix.xtox', 'shadow.matrix.xtoy',
    'shadow.matrix.ytox', 'shadow.matrix.ytoy',
    'shadow.matrix.perspectiveX', 'shadow.matrix.perspectiveY',
    'skew.on', 'skew.offset.x', 'skew.offset.y',
    'skew.origin.x', 'skew.origin.y',
    'skew.matrix.xtox', 'skew.matrix.xtoy',
    'skew.matrix.ytox', 'skew.matrix.ytoy',
    'skew.matrix.perspectiveX', 'skew.matrix.perspectiveY',
    'extrusion.on', 'extrusion.type', 'extrusion.render',
    'extrusion.viewpointorigin.x', 'extrusion.viewpointorigin.y',
    'extrusion.viewpoint.x', 'extrusion.viewpoint.y', 'extrusion.viewpoint.z',
    'extrusion.plane', 'extrusion.skewangle', 'extrusion.skewamt',
    'extrusion.backdepth', 'extrusion.foredepth',
    'extrusion.orientation.x', 'extrusion.orientation.y', 'extrusion.orientation.z',
    'extrusion.orientationangle', 'extrusion.color',
    'extrusion.rotationangle.x', 'extrusion.rotationangle.y',
    'extrusion.lockrotationcenter', 'extrusion.autorotationcenter',
    'extrusion.rotationcenter.x', 'extrusion.rotationcenter.y',
    'extrusion.rotationcenter.z', 'extrusion.colormode',
]:
    _make(_name)
