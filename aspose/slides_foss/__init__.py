# Enums
from .BackgroundType import BackgroundType
from .BevelPresetType import BevelPresetType
from .BulletType import BulletType
from .CameraPresetType import CameraPresetType
from .ColorType import ColorType
from .FillBlendMode import FillBlendMode
from .FillType import FillType
from .FontAlignment import FontAlignment
from .GradientDirection import GradientDirection
from .GradientShape import GradientShape
from .LightRigPresetType import LightRigPresetType
from .LightingDirection import LightingDirection
from .LineAlignment import LineAlignment
from .LineArrowheadLength import LineArrowheadLength
from .LineArrowheadStyle import LineArrowheadStyle
from .LineArrowheadWidth import LineArrowheadWidth
from .LineCapStyle import LineCapStyle
from .LineDashStyle import LineDashStyle
from .LineJoinStyle import LineJoinStyle
from .LineStyle import LineStyle
from .MaterialPresetType import MaterialPresetType
from .NullableBool import NullableBool
from .NumberedBulletStyle import NumberedBulletStyle
from .Orientation import Orientation
from .PatternStyle import PatternStyle
from .PictureFillMode import PictureFillMode
from .PresetColor import PresetColor
from .PresetShadowType import PresetShadowType
from .RectangleAlignment import RectangleAlignment
from .SchemeColor import SchemeColor
from .ShapeType import ShapeType
from .SlideLayoutType import SlideLayoutType
from .SourceFormat import SourceFormat
from .TableStylePreset import TableStylePreset
from .TextAlignment import TextAlignment
from .TextAnchorType import TextAnchorType
from .TextAutofitType import TextAutofitType
from .TextCapType import TextCapType
from .TextShapeType import TextShapeType
from .TextStrikethroughType import TextStrikethroughType
from .TextUnderlineType import TextUnderlineType
from .TextVerticalType import TextVerticalType
from .TileFlip import TileFlip

# Interfaces
from .IAdjustValue import IAdjustValue
from .IAdjustValueCollection import IAdjustValueCollection
from .IAnimationTimeLine import IAnimationTimeLine
from .IAutoShape import IAutoShape
from .IBackground import IBackground
from .IBackgroundEffectiveData import IBackgroundEffectiveData
from .IBasePortionFormat import IBasePortionFormat
from .IBaseShapeLock import IBaseShapeLock
from .IBaseSlide import IBaseSlide
from .IBulkTextFormattable import IBulkTextFormattable
from .IBulletFormat import IBulletFormat
from .ICamera import ICamera
from .ICell import ICell
from .ICellCollection import ICellCollection
from .ICellFormat import ICellFormat
from .IColorFormat import IColorFormat
from .IColumn import IColumn
from .IColumnCollection import IColumnCollection
from .IComment import IComment
from .ICommentAuthor import ICommentAuthor
from .ICommentAuthorCollection import ICommentAuthorCollection
from .ICommentCollection import ICommentCollection
from .IConnector import IConnector
from .IDocumentProperties import IDocumentProperties
from .IEffectFormat import IEffectFormat
from .IEffectParamSource import IEffectParamSource
from .IFillFormat import IFillFormat
from .IFillParamSource import IFillParamSource
from .IFontData import IFontData
from .IFonts import IFonts
from .IGeometryShape import IGeometryShape
from .IGlobalLayoutSlideCollection import IGlobalLayoutSlideCollection
from .IGradientFormat import IGradientFormat
from .IGradientStop import IGradientStop
from .IGradientStopCollection import IGradientStopCollection
from .IGraphicalObject import IGraphicalObject
from .IGroupShape import IGroupShape
from .IGroupShapeLock import IGroupShapeLock
from .IHeadingPair import IHeadingPair
from .IHyperlinkContainer import IHyperlinkContainer
from .IImage import IImage
from .IImageCollection import IImageCollection
from .ILayoutSlide import ILayoutSlide
from .ILayoutSlideCollection import ILayoutSlideCollection
from .ILightRig import ILightRig
from .ILineFillFormat import ILineFillFormat
from .ILineFormat import ILineFormat
from .ILineParamSource import ILineParamSource
from .ILoadOptions import ILoadOptions
from .IMasterLayoutSlideCollection import IMasterLayoutSlideCollection
from .IMasterSlide import IMasterSlide
from .IMasterSlideCollection import IMasterSlideCollection
from .INotesSize import INotesSize
from .INotesSlide import INotesSlide
from .INotesSlideHeaderFooterManager import INotesSlideHeaderFooterManager
from .INotesSlideManager import INotesSlideManager
from .IPPImage import IPPImage
from .IParagraph import IParagraph
from .IParagraphCollection import IParagraphCollection
from .IParagraphFormat import IParagraphFormat
from .IPatternFormat import IPatternFormat
from .IPictureFillFormat import IPictureFillFormat
from .IPictureFrame import IPictureFrame
from .IPictureFrameLock import IPictureFrameLock
from .IPortion import IPortion
from .IPortionCollection import IPortionCollection
from .IPortionFormat import IPortionFormat
from .IPresentation import IPresentation
from .IPresentationComponent import IPresentationComponent
from .IRow import IRow
from .IRowCollection import IRowCollection
from .ISection import ISection
from .IShape import IShape
from .IShapeBevel import IShapeBevel
from .IShapeCollection import IShapeCollection
from .IShapeFrame import IShapeFrame
from .ISlide import ISlide
from .ISlideCollection import ISlideCollection
from .ISlideComponent import ISlideComponent
from .ISlideShowTransition import ISlideShowTransition
from .ISlidesPicture import ISlidesPicture
from .ITable import ITable
from .ITableFormat import ITableFormat
from .ITextFrame import ITextFrame
from .ITextFrameFormat import ITextFrameFormat
from .IThreeDFormat import IThreeDFormat
from .IThreeDParamSource import IThreeDParamSource

# Concrete classes
from .AdjustValue import AdjustValue
from .AdjustValueCollection import AdjustValueCollection
from .AutoShape import AutoShape
from .Background import Background
from .BaseHandoutNotesSlideHeaderFooterManager import BaseHandoutNotesSlideHeaderFooterManager
from .BasePortionFormat import BasePortionFormat
from .BaseShapeLock import BaseShapeLock
from .BaseSlide import BaseSlide
from .BulletFormat import BulletFormat
from .Camera import Camera
from .Cell import Cell
from .CellCollection import CellCollection
from .CellFormat import CellFormat
from .ColorFormat import ColorFormat
from .Column import Column
from .ColumnCollection import ColumnCollection
from .Comment import Comment
from .CommentAuthor import CommentAuthor
from .CommentAuthorCollection import CommentAuthorCollection
from .CommentCollection import CommentCollection
from .Connector import Connector
from .DocumentProperties import DocumentProperties
from .EffectFormat import EffectFormat
from .FillFormat import FillFormat
from .FontData import FontData
from .Fonts import Fonts
from .GeometryShape import GeometryShape
from .GlobalLayoutSlideCollection import GlobalLayoutSlideCollection
from .GradientFormat import GradientFormat
from .GradientStop import GradientStop
from .GradientStopCollection import GradientStopCollection
from .GraphicalObject import GraphicalObject
from .GraphicalObjectLock import GraphicalObjectLock
from .GroupShape import GroupShape
from .GroupShapeLock import GroupShapeLock
from .HeadingPair import HeadingPair
from .Image import Image
from .ImageCollection import ImageCollection
from .Images import Images
from .LayoutSlide import LayoutSlide
from .LayoutSlideCollection import LayoutSlideCollection
from .LightRig import LightRig
from .LineFillFormat import LineFillFormat
from .LineFormat import LineFormat
from .MasterLayoutSlideCollection import MasterLayoutSlideCollection
from .MasterSlide import MasterSlide
from .MasterSlideCollection import MasterSlideCollection
from .NotesSize import NotesSize
from .NotesSlide import NotesSlide
from .NotesSlideHeaderFooterManager import NotesSlideHeaderFooterManager
from .NotesSlideManager import NotesSlideManager
from .PPImage import PPImage
from .PVIObject import PVIObject
from .Paragraph import Paragraph
from .ParagraphCollection import ParagraphCollection
from .ParagraphFormat import ParagraphFormat
from .PatternFormat import PatternFormat
from .Picture import Picture
from .PictureFillFormat import PictureFillFormat
from .PictureFrame import PictureFrame
from .PictureFrameLock import PictureFrameLock
from .Portion import Portion
from .PortionCollection import PortionCollection
from .PortionFormat import PortionFormat
from .Presentation import Presentation
from .Row import Row
from .RowCollection import RowCollection
from .Shape import Shape
from .ShapeBevel import ShapeBevel
from .ShapeCollection import ShapeCollection
from .ShapeFrame import ShapeFrame
from .Slide import Slide
from .SlideCollection import SlideCollection
from .Table import Table
from .TableFormat import TableFormat
from .TextFrame import TextFrame
from .TextFrameFormat import TextFrameFormat
from .ThreeDFormat import ThreeDFormat


# Subpackages
from . import drawing

try:
    from . import effects
except TypeError:
    pass

try:
    from . import export
except TypeError:
    pass

try:
    from . import theme
except TypeError:
    pass

try:
    from . import animation
except TypeError:
    pass

try:
    from . import charts
except TypeError:
    pass

try:
    from . import slideshow
except TypeError:
    pass


__all__ = [
    # Enums
    'BackgroundType',
    'BevelPresetType',
    'BulletType',
    'CameraPresetType',
    'ColorType',
    'FillBlendMode',
    'FillType',
    'FontAlignment',
    'GradientDirection',
    'GradientShape',
    'LightRigPresetType',
    'LightingDirection',
    'LineAlignment',
    'LineArrowheadLength',
    'LineArrowheadStyle',
    'LineArrowheadWidth',
    'LineCapStyle',
    'LineDashStyle',
    'LineJoinStyle',
    'LineStyle',
    'MaterialPresetType',
    'NullableBool',
    'NumberedBulletStyle',
    'Orientation',
    'PatternStyle',
    'PictureFillMode',
    'PresetColor',
    'PresetShadowType',
    'RectangleAlignment',
    'SchemeColor',
    'ShapeType',
    'SlideLayoutType',
    'SourceFormat',
    'TableStylePreset',
    'TextAlignment',
    'TextAnchorType',
    'TextAutofitType',
    'TextCapType',
    'TextShapeType',
    'TextStrikethroughType',
    'TextUnderlineType',
    'TextVerticalType',
    'TileFlip',
    # Interfaces
    'IAdjustValue',
    'IAdjustValueCollection',
    'IAnimationTimeLine',
    'IAutoShape',
    'IBackground',
    'IBackgroundEffectiveData',
    'IBasePortionFormat',
    'IBaseShapeLock',
    'IBaseSlide',
    'IBulkTextFormattable',
    'IBulletFormat',
    'ICamera',
    'ICell',
    'ICellCollection',
    'ICellFormat',
    'IColorFormat',
    'IColumn',
    'IColumnCollection',
    'IComment',
    'ICommentAuthor',
    'ICommentAuthorCollection',
    'ICommentCollection',
    'IConnector',
    'IDocumentProperties',
    'IEffectFormat',
    'IEffectParamSource',
    'IFillFormat',
    'IFillParamSource',
    'IFontData',
    'IFonts',
    'IGeometryShape',
    'IGlobalLayoutSlideCollection',
    'IGradientFormat',
    'IGradientStop',
    'IGradientStopCollection',
    'IGraphicalObject',
    'IGroupShape',
    'IGroupShapeLock',
    'IHeadingPair',
    'IHyperlinkContainer',
    'IImage',
    'IImageCollection',
    'ILayoutSlide',
    'ILayoutSlideCollection',
    'ILightRig',
    'ILineFillFormat',
    'ILineFormat',
    'ILineParamSource',
    'ILoadOptions',
    'IMasterLayoutSlideCollection',
    'IMasterSlide',
    'IMasterSlideCollection',
    'INotesSize',
    'INotesSlide',
    'INotesSlideHeaderFooterManager',
    'INotesSlideManager',
    'IPPImage',
    'IParagraph',
    'IParagraphCollection',
    'IParagraphFormat',
    'IPatternFormat',
    'IPictureFillFormat',
    'IPictureFrame',
    'IPictureFrameLock',
    'IPortion',
    'IPortionCollection',
    'IPortionFormat',
    'IPresentation',
    'IPresentationComponent',
    'IRow',
    'IRowCollection',
    'ISection',
    'IShape',
    'IShapeBevel',
    'IShapeCollection',
    'IShapeFrame',
    'ISlide',
    'ISlideCollection',
    'ISlideComponent',
    'ISlideShowTransition',
    'ISlidesPicture',
    'ITable',
    'ITableFormat',
    'ITextFrame',
    'ITextFrameFormat',
    'IThreeDFormat',
    'IThreeDParamSource',
    # Concrete classes
    'AdjustValue',
    'AdjustValueCollection',
    'AutoShape',
    'Background',
    'BaseHandoutNotesSlideHeaderFooterManager',
    'BasePortionFormat',
    'BaseShapeLock',
    'BaseSlide',
    'BulletFormat',
    'Camera',
    'Cell',
    'CellCollection',
    'CellFormat',
    'ColorFormat',
    'Column',
    'ColumnCollection',
    'Comment',
    'CommentAuthor',
    'CommentAuthorCollection',
    'CommentCollection',
    'Connector',
    'DocumentProperties',
    'EffectFormat',
    'FillFormat',
    'FontData',
    'Fonts',
    'GeometryShape',
    'GlobalLayoutSlideCollection',
    'GradientFormat',
    'GradientStop',
    'GradientStopCollection',
    'GraphicalObject',
    'GraphicalObjectLock',
    'GroupShape',
    'GroupShapeLock',
    'HeadingPair',
    'Image',
    'ImageCollection',
    'Images',
    'LayoutSlide',
    'LayoutSlideCollection',
    'LightRig',
    'LineFillFormat',
    'LineFormat',
    'MasterLayoutSlideCollection',
    'MasterSlide',
    'MasterSlideCollection',
    'NotesSize',
    'NotesSlide',
    'NotesSlideHeaderFooterManager',
    'NotesSlideManager',
    'PPImage',
    'PVIObject',
    'Paragraph',
    'ParagraphCollection',
    'ParagraphFormat',
    'PatternFormat',
    'Picture',
    'PictureFillFormat',
    'PictureFrame',
    'PictureFrameLock',
    'Portion',
    'PortionCollection',
    'PortionFormat',
    'Presentation',
    'Row',
    'RowCollection',
    'Shape',
    'ShapeBevel',
    'ShapeCollection',
    'ShapeFrame',
    'Slide',
    'SlideCollection',
    'Table',
    'TableFormat',
    'TextFrame',
    'TextFrameFormat',
    'ThreeDFormat',
    # Subpackages
    'animation',
    'charts',
    'drawing',
    'effects',
    'export',
    'slideshow',
    'theme',
]
