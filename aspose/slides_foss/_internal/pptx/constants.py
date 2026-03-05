"""
XML namespace constants for PPTX format.

Defines all XML namespaces used in PowerPoint Open XML documents.
"""

from __future__ import annotations

# Namespace URIs
NAMESPACES = {
    # PresentationML namespace (main presentation elements)
    'p': 'http://schemas.openxmlformats.org/presentationml/2006/main',

    # DrawingML namespace (shapes, text, effects)
    'a': 'http://schemas.openxmlformats.org/drawingml/2006/main',

    # Relationships namespace (in XML content, e.g., r:id attributes)
    'r': 'http://schemas.openxmlformats.org/officeDocument/2006/relationships',

    # Package relationships namespace (in .rels files)
    'pr': 'http://schemas.openxmlformats.org/package/2006/relationships',

    # Content types namespace
    'ct': 'http://schemas.openxmlformats.org/package/2006/content-types',

    # Core properties namespace (Dublin Core)
    'cp': 'http://schemas.openxmlformats.org/package/2006/metadata/core-properties',
    'dc': 'http://purl.org/dc/elements/1.1/',
    'dcterms': 'http://purl.org/dc/terms/',

    # Extended properties namespace
    'ep': 'http://schemas.openxmlformats.org/officeDocument/2006/extended-properties',

    # VML namespace (legacy vector markup)
    'v': 'urn:schemas-microsoft-com:vml',

    # Office namespace
    'o': 'urn:schemas-microsoft-com:office:office',

    # Chart namespace
    'c': 'http://schemas.openxmlformats.org/drawingml/2006/chart',

    # Diagram namespace
    'dgm': 'http://schemas.openxmlformats.org/drawingml/2006/diagram',

    # Picture namespace
    'pic': 'http://schemas.openxmlformats.org/drawingml/2006/picture',

    # Math namespace
    'm': 'http://schemas.openxmlformats.org/officeDocument/2006/math',

    # Microsoft Office extensions (2010+)
    'p14': 'http://schemas.microsoft.com/office/powerpoint/2010/main',
    'p15': 'http://schemas.microsoft.com/office/powerpoint/2012/main',
    'a14': 'http://schemas.microsoft.com/office/drawing/2010/main',

    # Markup Compatibility namespace
    'mc': 'http://schemas.openxmlformats.org/markup-compatibility/2006',
}


class NS:
    """
    Namespace helper class providing formatted namespace strings.

    Use NS.P for "{http://...}tagname" style lookups.
    """

    # Formatted namespace strings for lxml element access
    P = f"{{{NAMESPACES['p']}}}"        # PresentationML: {http://...}
    A = f"{{{NAMESPACES['a']}}}"        # DrawingML
    R = f"{{{NAMESPACES['r']}}}"        # Document relationships
    PR = f"{{{NAMESPACES['pr']}}}"      # Package relationships
    CT = f"{{{NAMESPACES['ct']}}}"      # Content types
    C = f"{{{NAMESPACES['c']}}}"        # Charts
    PIC = f"{{{NAMESPACES['pic']}}}"    # Pictures

    @classmethod
    def get(cls, prefix: str) -> str:
        """
        Get formatted namespace string by prefix.

        Args:
            prefix: Namespace prefix (e.g., 'p', 'a', 'r').

        Returns:
            Formatted namespace string like "{http://...}".

        Raises:
            KeyError: If prefix not found.
        """
        return f"{{{NAMESPACES[prefix]}}}"


# Common element names with namespaces
class Elements:
    """Common PPTX element names with full namespace qualification."""

    # Presentation elements
    PRESENTATION = f"{NS.P}presentation"
    SLD_ID_LST = f"{NS.P}sldIdLst"
    SLD_ID = f"{NS.P}sldId"
    SLD_MASTER_ID_LST = f"{NS.P}sldMasterIdLst"
    SLD_MASTER_ID = f"{NS.P}sldMasterId"
    SLD_SZ = f"{NS.P}sldSz"
    NOTES_SZ = f"{NS.P}notesSz"

    # Slide elements
    SLD = f"{NS.P}sld"
    C_SLD = f"{NS.P}cSld"
    SP_TREE = f"{NS.P}spTree"

    # Shape elements
    SP = f"{NS.P}sp"
    NV_SP_PR = f"{NS.P}nvSpPr"
    C_NV_PR = f"{NS.P}cNvPr"
    SP_PR = f"{NS.P}spPr"
    TX_BODY = f"{NS.P}txBody"

    # DrawingML elements
    A_P = f"{NS.A}p"           # Paragraph
    A_R = f"{NS.A}r"           # Run
    A_T = f"{NS.A}t"           # Text
    A_XFRM = f"{NS.A}xfrm"     # Transform
    A_OFF = f"{NS.A}off"       # Offset
    A_EXT = f"{NS.A}ext"       # Extents

    # Fill elements
    A_NO_FILL = f"{NS.A}noFill"
    A_SOLID_FILL = f"{NS.A}solidFill"
    A_GRAD_FILL = f"{NS.A}gradFill"
    A_PATT_FILL = f"{NS.A}pattFill"
    A_BLIP_FILL = f"{NS.A}blipFill"
    A_GRP_FILL = f"{NS.A}grpFill"

    # Color elements
    A_SRGB_CLR = f"{NS.A}srgbClr"
    A_SCHEME_CLR = f"{NS.A}schemeClr"
    A_PRST_CLR = f"{NS.A}prstClr"
    A_SYS_CLR = f"{NS.A}sysClr"
    A_HLS_CLR = f"{NS.A}hlsClr"
    A_SCR_GB_CLR = f"{NS.A}scrgbClr"

    # Gradient elements
    A_GS_LST = f"{NS.A}gsLst"
    A_GS = f"{NS.A}gs"
    A_LIN = f"{NS.A}lin"
    A_PATH = f"{NS.A}path"
    A_TILE_RECT = f"{NS.A}tileRect"

    # Pattern elements
    A_FG_CLR = f"{NS.A}fgClr"
    A_BG_CLR = f"{NS.A}bgClr"

    # Text elements
    A_BODY_PR = f"{NS.A}bodyPr"
    A_LST_STYLE = f"{NS.A}lstStyle"
    A_R_PR = f"{NS.A}rPr"
    A_P_PR = f"{NS.A}pPr"
    A_END_PARA_RPR = f"{NS.A}endParaRPr"
    A_HIGHLIGHT = f"{NS.A}highlight"
    A_U_LN_TX = f"{NS.A}uLnTx"
    A_U_LN = f"{NS.A}uLn"
    A_U_FILL_TX = f"{NS.A}uFillTx"
    A_U_FILL = f"{NS.A}uFill"
    A_DEF_R_PR = f"{NS.A}defRPr"
    A_TAB_LST = f"{NS.A}tabLst"
    A_LN_SPC = f"{NS.A}lnSpc"
    A_SPC_BEF = f"{NS.A}spcBef"
    A_SPC_AFT = f"{NS.A}spcAft"
    A_SPC_PCT = f"{NS.A}spcPct"
    A_SPC_PTS = f"{NS.A}spcPts"
    A_BU_NONE = f"{NS.A}buNone"
    A_BU_CHAR = f"{NS.A}buChar"
    A_BU_AUTO_NUM = f"{NS.A}buAutoNum"
    A_BU_FONT = f"{NS.A}buFont"
    A_BU_SZ_PCT = f"{NS.A}buSzPct"
    A_BU_SZ_PTS = f"{NS.A}buSzPts"
    A_BU_CLR = f"{NS.A}buClr"
    A_BU_CLR_TX = f"{NS.A}buClrTx"
    A_BU_FONT_TX = f"{NS.A}buFontTx"
    A_BU_SZ_TX = f"{NS.A}buSzTx"
    A_BU_BLIP = f"{NS.A}buBlip"
    A_LATIN = f"{NS.A}latin"
    A_EA = f"{NS.A}ea"
    A_CS = f"{NS.A}cs"
    A_SYM = f"{NS.A}sym"

    # Autofit elements
    A_NO_AUTOFIT = f"{NS.A}noAutofit"
    A_SP_AUTO_FIT = f"{NS.A}spAutoFit"
    A_NORM_AUTOFIT = f"{NS.A}normAutofit"

    # Text warp element
    A_PRST_TX_WARP = f"{NS.A}prstTxWarp"

    # Line elements
    A_LN = f"{NS.A}ln"
    A_PRST_DASH = f"{NS.A}prstDash"
    A_CUST_DASH = f"{NS.A}custDash"
    A_ROUND = f"{NS.A}round"
    A_BEVEL = f"{NS.A}bevel"
    A_MITER = f"{NS.A}miter"
    A_HEAD_END = f"{NS.A}headEnd"
    A_TAIL_END = f"{NS.A}tailEnd"

    # 3D elements
    A_SCENE_3D = f"{NS.A}scene3d"
    A_SP_3D = f"{NS.A}sp3d"
    A_CAMERA = f"{NS.A}camera"
    A_LIGHT_RIG = f"{NS.A}lightRig"
    A_BEVEL_T = f"{NS.A}bevelT"
    A_BEVEL_B = f"{NS.A}bevelB"
    A_CONTOUR_CLR = f"{NS.A}contourClr"
    A_EXTRUSION_CLR = f"{NS.A}extrusionClr"
    A_ROT = f"{NS.A}rot"
    A_EFFECT_LST = f"{NS.A}effectLst"
    A_EFFECT_DAG = f"{NS.A}effectDag"
    A_EXT_LST = f"{NS.A}extLst"

    # Effect elements (children of effectLst, in OOXML order)
    A_BLUR = f"{NS.A}blur"
    A_FILL_OVERLAY = f"{NS.A}fillOverlay"
    A_GLOW = f"{NS.A}glow"
    A_INNER_SHDW = f"{NS.A}innerShdw"
    A_OUTER_SHDW = f"{NS.A}outerShdw"
    A_PRST_SHDW = f"{NS.A}prstShdw"
    A_REFLECTION = f"{NS.A}reflection"
    A_SOFT_EDGE = f"{NS.A}softEdge"

    # Table elements
    A_GRAPHIC = f"{NS.A}graphic"
    A_GRAPHIC_DATA = f"{NS.A}graphicData"
    A_TBL = f"{NS.A}tbl"
    A_TBL_PR = f"{NS.A}tblPr"
    A_TBL_GRID = f"{NS.A}tblGrid"
    A_GRID_COL = f"{NS.A}gridCol"
    A_TR = f"{NS.A}tr"
    A_TC = f"{NS.A}tc"
    A_TC_PR = f"{NS.A}tcPr"
    A_TBL_STYLE = f"{NS.A}tblStyle"
    A_TABLE_STYLE_ID = f"{NS.A}tableStyleId"

    # Table border elements
    A_LN_L = f"{NS.A}lnL"
    A_LN_R = f"{NS.A}lnR"
    A_LN_T = f"{NS.A}lnT"
    A_LN_B = f"{NS.A}lnB"
    A_LN_TL_TO_BR = f"{NS.A}lnTlToBr"
    A_LN_BL_TO_TR = f"{NS.A}lnBlToTr"

    # GraphicFrame elements
    P_GRAPHIC_FRAME = f"{NS.P}graphicFrame"
    P_NV_GRAPHIC_FRAME_PR = f"{NS.P}nvGraphicFramePr"
    P_C_NV_GRAPHIC_FRAME_PR = f"{NS.P}cNvGraphicFramePr"
    A_GRAPHIC_FRAME_LOCKING = f"{NS.A}graphicFrameLocking"
    P_NV_PR = f"{NS.P}nvPr"
    P_XFRM = f"{NS.P}xfrm"

    # Table URI
    TABLE_URI = 'http://schemas.openxmlformats.org/drawingml/2006/table'

    # DrawingML txBody (for table cells)
    A_TX_BODY = f"{NS.A}txBody"


# Unit conversion constants
EMU_PER_POINT = 12700  # 1 point = 12700 EMUs (914400 EMU/inch / 72 points/inch)
ROTATION_UNIT = 60000  # OOXML stores rotation in 60000ths of a degree


# Common attribute names
class Attributes:
    """Common PPTX attribute names."""

    # With namespace (e.g., r:id)
    R_ID = f"{NS.R}id"
    R_EMBED = f"{NS.R}embed"

    # Without namespace
    ID = 'id'
    NAME = 'name'
    CX = 'cx'
    CY = 'cy'
    X = 'x'
    Y = 'y'
