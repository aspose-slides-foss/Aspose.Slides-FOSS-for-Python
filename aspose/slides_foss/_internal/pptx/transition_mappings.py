"""
Mapping tables for slide transition types and their OOXML representations.

Maps between TransitionType enum values and XML element names, namespaces,
value classes, and direction attribute conversions.
"""

from __future__ import annotations

# Namespace URIs for transition elements
P_NS = 'http://schemas.openxmlformats.org/presentationml/2006/main'
P14_NS = 'http://schemas.microsoft.com/office/powerpoint/2010/main'
P15_NS = 'http://schemas.microsoft.com/office/powerpoint/2012/main'
P159_NS = 'http://schemas.microsoft.com/office/powerpoint/2015/09/main'
MC_NS = 'http://schemas.openxmlformats.org/markup-compatibility/2006'

P_PREFIX = f'{{{P_NS}}}'
P14_PREFIX = f'{{{P14_NS}}}'
P15_PREFIX = f'{{{P15_NS}}}'
P159_PREFIX = f'{{{P159_NS}}}'
MC_PREFIX = f'{{{MC_NS}}}'

# A transition element in one of these namespaces is an extension to
# ECMA-376.  PowerPoint writes it inside mc:AlternateContent: the element in an
# mc:Choice whose Requires names this prefix, and a plain fade in mc:Fallback
# for a reader that does not know the extension.
EXTENSION_PREFIXES = {P14_NS: 'p14', P15_NS: 'p15', P159_NS: 'p159'}

# ---------------------------------------------------------------
# TransitionType → (xml_tag, namespace_prefix, value_class_name)
# ---------------------------------------------------------------
# Standard (p: namespace) transitions
_STANDARD_TRANSITIONS = {
    'Blinds':     ('blinds',     P_PREFIX, 'OrientationTransition'),
    'Checker':    ('checker',    P_PREFIX, 'OrientationTransition'),
    'Circle':     ('circle',     P_PREFIX, 'EmptyTransition'),
    'Comb':       ('comb',       P_PREFIX, 'OrientationTransition'),
    'Cover':      ('cover',      P_PREFIX, 'EightDirectionTransition'),
    'Cut':        ('cut',        P_PREFIX, 'OptionalBlackTransition'),
    'Diamond':    ('diamond',    P_PREFIX, 'EmptyTransition'),
    'Dissolve':   ('dissolve',   P_PREFIX, 'EmptyTransition'),
    'Fade':       ('fade',       P_PREFIX, 'OptionalBlackTransition'),
    'Newsflash':  ('newsflash',  P_PREFIX, 'EmptyTransition'),
    'Plus':       ('plus',       P_PREFIX, 'EmptyTransition'),
    'Pull':       ('pull',       P_PREFIX, 'EightDirectionTransition'),
    'Push':       ('push',       P_PREFIX, 'SideDirectionTransition'),
    'Random':     ('random',     P_PREFIX, 'EmptyTransition'),
    'RandomBar':  ('randomBar',  P_PREFIX, 'OrientationTransition'),
    'Split':      ('split',      P_PREFIX, 'SplitTransition'),
    'Strips':     ('strips',     P_PREFIX, 'CornerDirectionTransition'),
    'Wedge':      ('wedge',      P_PREFIX, 'EmptyTransition'),
    'Wheel':      ('wheel',      P_PREFIX, 'WheelTransition'),
    'Wipe':       ('wipe',       P_PREFIX, 'SideDirectionTransition'),
    'Zoom':       ('zoom',       P_PREFIX, 'InOutTransition'),
}

# PowerPoint 2010+ transitions (p14: namespace)
_P14_TRANSITIONS = {
    'Vortex':       ('vortex',       P14_PREFIX, 'SideDirectionTransition'),
    'Switch':       ('switch',       P14_PREFIX, 'LeftRightDirectionTransition'),
    'Flip':         ('flip',         P14_PREFIX, 'LeftRightDirectionTransition'),
    'Ripple':       ('ripple',       P14_PREFIX, 'RippleTransition'),
    'Honeycomb':    ('honeycomb',    P14_PREFIX, 'EmptyTransition'),
    'Cube':         ('prism',        P14_PREFIX, 'SideDirectionTransition'),
    'Box':          ('prism',        P14_PREFIX, 'SideDirectionTransition'),
    'Rotate':       ('prism',        P14_PREFIX, 'SideDirectionTransition'),
    'Orbit':        ('prism',        P14_PREFIX, 'SideDirectionTransition'),
    'Doors':        ('doors',        P14_PREFIX, 'OrientationTransition'),
    'Window':       ('window',       P14_PREFIX, 'OrientationTransition'),
    'Ferris':       ('ferris',       P14_PREFIX, 'LeftRightDirectionTransition'),
    'Gallery':      ('gallery',      P14_PREFIX, 'LeftRightDirectionTransition'),
    'Conveyor':     ('conveyor',     P14_PREFIX, 'LeftRightDirectionTransition'),
    'Pan':          ('pan',          P14_PREFIX, 'SideDirectionTransition'),
    'Glitter':      ('glitter',      P14_PREFIX, 'GlitterTransition'),
    'Warp':         ('warp',         P14_PREFIX, 'InOutTransition'),
    'Flythrough':   ('flythrough',   P14_PREFIX, 'FlyThroughTransition'),
    'Flash':        ('flash',        P14_PREFIX, 'EmptyTransition'),
    'Shred':        ('shred',        P14_PREFIX, 'ShredTransition'),
    'Reveal':       ('reveal',       P14_PREFIX, 'RevealTransition'),
    'WheelReverse': ('wheelReverse', P14_PREFIX, 'WheelTransition'),
}

# Cube, Rotate, Box and Orbit are all one p14:prism element, told apart by two
# flags.  These are the values PowerPoint writes for each.
_PRISM_FLAGS = {
    'Cube':   {},
    'Rotate': {'isContent': '1'},
    'Box':    {'isInverted': '1'},
    'Orbit':  {'isContent': '1', 'isInverted': '1'},
}

# PowerPoint 2013+ preset transitions (p15: namespace)
_P15_PRESET_TYPES = {
    'FallOver':        'fallOver',
    'Drape':           'drape',
    'Curtains':        'curtains',
    'Wind':            'wind',
    'Prestige':        'prestige',
    'Fracture':        'fracture',
    'Crush':           'crush',
    'PeelOff':         'peelOff',
    'PageCurlDouble':  'pageCurlDbl',
    'PageCurlSingle':  'pageCurlSgl',
    'Airplane':        'airplane',
    'Origami':         'origami',
}

# Reverse mapping: p15 preset value → TransitionType value string
_P15_PRESET_REVERSE = {v: k for k, v in _P15_PRESET_TYPES.items()}

# Morph transition (uses p159 namespace per PowerPoint conventions)
MORPH_NS = P159_NS
MORPH_PREFIX = P159_PREFIX

# ---------------------------------------------------------------
# Combined mapping: TransitionType.value → (full_tag, value_class)
# ---------------------------------------------------------------

def get_transition_info(type_value: str):
    """Get (full_xml_tag, value_class_name, extra_attrs) for a TransitionType value.

    Returns None if the type is NONE or unknown.
    extra_attrs is a dict of additional attributes to set on the element.
    """
    if type_value == 'None':
        return None

    # Check standard transitions
    if type_value in _STANDARD_TRANSITIONS:
        tag_name, ns_prefix, cls_name = _STANDARD_TRANSITIONS[type_value]
        return (f'{ns_prefix}{tag_name}', cls_name, {})

    # Check p14 transitions
    if type_value in _P14_TRANSITIONS:
        tag_name, ns_prefix, cls_name = _P14_TRANSITIONS[type_value]
        extra = dict(_PRISM_FLAGS.get(type_value, {}))
        return (f'{ns_prefix}{tag_name}', cls_name, extra)

    # Check p15 preset transitions
    if type_value in _P15_PRESET_TYPES:
        prst_val = _P15_PRESET_TYPES[type_value]
        tag = f'{P15_PREFIX}prstTrans'
        return (tag, 'EmptyTransition', {'prst': prst_val})

    # Morph
    if type_value == 'Morph':
        tag = f'{P159_PREFIX}morph'
        return (tag, 'MorphTransition', {'option': 'byObject'})

    return None


def get_transition_type_from_element(elem) -> str | None:
    """Given a transition child XML element, return the TransitionType value string.

    Returns None if the element is not recognized.
    """
    tag = elem.tag

    # Check standard transitions
    for type_val, (tag_name, ns_prefix, _) in _STANDARD_TRANSITIONS.items():
        if tag == f'{ns_prefix}{tag_name}':
            return type_val

    # Check p14 transitions
    for type_val, (tag_name, ns_prefix, _) in _P14_TRANSITIONS.items():
        if tag == f'{ns_prefix}{tag_name}':
            # Special case: prism is Cube, Rotate, Box or Orbit by its flags
            if tag_name == 'prism':
                flags = {
                    name: '1' for name in ('isContent', 'isInverted')
                    if elem.get(name) in ('1', 'true')
                }
                for prism_type, prism_flags in _PRISM_FLAGS.items():
                    if prism_flags == flags:
                        return prism_type
            return type_val

    # Check p15 preset transitions
    if tag == f'{P15_PREFIX}prstTrans':
        prst = elem.get('prst', '')
        return _P15_PRESET_REVERSE.get(prst)

    # Check morph (p159 namespace per PowerPoint, also accept p14 for compat)
    if tag == f'{P159_PREFIX}morph' or tag == f'{P14_PREFIX}morph':
        return 'Morph'

    return None


# ---------------------------------------------------------------
# Direction value ↔ XML attribute mappings
# ---------------------------------------------------------------

SIDE_DIR_TO_XML = {
    'Left': 'l', 'Up': 'u', 'Down': 'd', 'Right': 'r',
}
SIDE_DIR_FROM_XML = {v: k for k, v in SIDE_DIR_TO_XML.items()}

EIGHT_DIR_TO_XML = {
    'Left': 'l', 'Up': 'u', 'Down': 'd', 'Right': 'r',
    'LeftDown': 'ld', 'LeftUp': 'lu', 'RightDown': 'rd', 'RightUp': 'ru',
}
EIGHT_DIR_FROM_XML = {v: k for k, v in EIGHT_DIR_TO_XML.items()}

CORNER_DIR_TO_XML = {
    'LeftDown': 'ld', 'LeftUp': 'lu', 'RightDown': 'rd', 'RightUp': 'ru',
}
CORNER_DIR_FROM_XML = {v: k for k, v in CORNER_DIR_TO_XML.items()}

CORNER_CENTER_DIR_TO_XML = {
    'LeftDown': 'ld', 'LeftUp': 'lu', 'RightDown': 'rd', 'RightUp': 'ru',
    'Center': 'center',
}
CORNER_CENTER_DIR_FROM_XML = {v: k for k, v in CORNER_CENTER_DIR_TO_XML.items()}

IN_OUT_DIR_TO_XML = {'In': 'in', 'Out': 'out'}
IN_OUT_DIR_FROM_XML = {v: k for k, v in IN_OUT_DIR_TO_XML.items()}

LEFT_RIGHT_DIR_TO_XML = {'Left': 'l', 'Right': 'r'}
LEFT_RIGHT_DIR_FROM_XML = {v: k for k, v in LEFT_RIGHT_DIR_TO_XML.items()}

ORIENTATION_TO_XML = {'Horizontal': 'horz', 'Vertical': 'vert'}
ORIENTATION_FROM_XML = {v: k for k, v in ORIENTATION_TO_XML.items()}

SPEED_TO_XML = {'Fast': 'fast', 'Medium': 'med', 'Slow': 'slow'}
SPEED_FROM_XML = {v: k for k, v in SPEED_TO_XML.items()}

PATTERN_TO_XML = {'Diamond': 'diamond', 'Hexagon': 'hexagon'}
PATTERN_FROM_XML = {v: k for k, v in PATTERN_TO_XML.items()}

SHRED_PATTERN_TO_XML = {'Strip': 'strip', 'Rectangle': 'rect'}
SHRED_PATTERN_FROM_XML = {v: k for k, v in SHRED_PATTERN_TO_XML.items()}

MORPH_TYPE_TO_XML = {'ByObject': 'byObject', 'ByWord': 'byWord', 'ByChar': 'byChar'}
MORPH_TYPE_FROM_XML = {v: k for k, v in MORPH_TYPE_TO_XML.items()}
