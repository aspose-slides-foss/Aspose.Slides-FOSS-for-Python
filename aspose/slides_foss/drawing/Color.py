from __future__ import annotations


class Color:
    """Represents an ARGB color, equivalent to System.Drawing.Color."""

    def __init__(self, a: int = 255, r: int = 0, g: int = 0, b: int = 0):
        self._a = a
        self._r = r
        self._g = g
        self._b = b

    @staticmethod
    def from_argb(a: int, r: int, g: int, b: int) -> Color:
        return Color(a, r, g, b)

    @property
    def r(self) -> int:
        return self._r

    @property
    def g(self) -> int:
        return self._g

    @property
    def b(self) -> int:
        return self._b

    @property
    def a(self) -> int:
        return self._a

    def __eq__(self, other):
        if not isinstance(other, Color):
            return NotImplemented
        return self._r == other._r and self._g == other._g and self._b == other._b and self._a == other._a

    def __repr__(self):
        if self._a == 255:
            return f"Color(r={self._r}, g={self._g}, b={self._b})"
        return f"Color(a={self._a}, r={self._r}, g={self._g}, b={self._b})"

    # Named color constants — populated after class definition
    alice_blue = None
    antique_white = None
    aqua = None
    aquamarine = None
    azure = None
    beige = None
    bisque = None
    black = None
    blanched_almond = None
    blue = None
    blue_violet = None
    brown = None
    burly_wood = None
    cadet_blue = None
    chartreuse = None
    chocolate = None
    coral = None
    cornflower_blue = None
    cornsilk = None
    crimson = None
    cyan = None
    dark_blue = None
    dark_cyan = None
    dark_goldenrod = None
    dark_gray = None
    dark_green = None
    dark_khaki = None
    dark_magenta = None
    dark_olive_green = None
    dark_orange = None
    dark_orchid = None
    dark_red = None
    dark_salmon = None
    dark_sea_green = None
    dark_slate_blue = None
    dark_slate_gray = None
    dark_turquoise = None
    dark_violet = None
    deep_pink = None
    deep_sky_blue = None
    dim_gray = None
    dodger_blue = None
    firebrick = None
    floral_white = None
    forest_green = None
    fuchsia = None
    gainsboro = None
    ghost_white = None
    gold = None
    goldenrod = None
    gray = None
    green = None
    green_yellow = None
    honeydew = None
    hot_pink = None
    indian_red = None
    indigo = None
    ivory = None
    khaki = None
    lavender = None
    lavender_blush = None
    lawn_green = None
    lemon_chiffon = None
    light_blue = None
    light_coral = None
    light_cyan = None
    light_goldenrod_yellow = None
    light_gray = None
    light_green = None
    light_pink = None
    light_salmon = None
    light_sea_green = None
    light_sky_blue = None
    light_slate_gray = None
    light_steel_blue = None
    light_yellow = None
    lime = None
    lime_green = None
    linen = None
    magenta = None
    maroon = None
    medium_aquamarine = None
    medium_blue = None
    medium_orchid = None
    medium_purple = None
    medium_sea_green = None
    medium_slate_blue = None
    medium_spring_green = None
    medium_turquoise = None
    medium_violet_red = None
    midnight_blue = None
    mint_cream = None
    misty_rose = None
    moccasin = None
    navajo_white = None
    navy = None
    old_lace = None
    olive = None
    olive_drab = None
    orange = None
    orange_red = None
    orchid = None
    pale_goldenrod = None
    pale_green = None
    pale_turquoise = None
    pale_violet_red = None
    papaya_whip = None
    peach_puff = None
    peru = None
    pink = None
    plum = None
    powder_blue = None
    purple = None
    red = None
    rosy_brown = None
    royal_blue = None
    saddle_brown = None
    salmon = None
    sandy_brown = None
    sea_green = None
    sea_shell = None
    sienna = None
    silver = None
    sky_blue = None
    slate_blue = None
    slate_gray = None
    snow = None
    spring_green = None
    steel_blue = None
    tan = None
    teal = None
    thistle = None
    tomato = None
    transparent = None
    turquoise = None
    violet = None
    wheat = None
    white = None
    white_smoke = None
    yellow = None
    yellow_green = None


# Initialize named colors (must be done after class definition due to forward reference)
Color.alice_blue = Color(255, 240, 248, 255)
Color.antique_white = Color(255, 250, 235, 215)
Color.aqua = Color(255, 0, 255, 255)
Color.aquamarine = Color(255, 127, 255, 212)
Color.azure = Color(255, 240, 255, 255)
Color.beige = Color(255, 245, 245, 220)
Color.bisque = Color(255, 255, 228, 196)
Color.black = Color(255, 0, 0, 0)
Color.blanched_almond = Color(255, 255, 235, 205)
Color.blue = Color(255, 0, 0, 255)
Color.blue_violet = Color(255, 138, 43, 226)
Color.brown = Color(255, 165, 42, 42)
Color.burly_wood = Color(255, 222, 184, 135)
Color.cadet_blue = Color(255, 95, 158, 160)
Color.chartreuse = Color(255, 127, 255, 0)
Color.chocolate = Color(255, 210, 105, 30)
Color.coral = Color(255, 255, 127, 80)
Color.cornflower_blue = Color(255, 100, 149, 237)
Color.cornsilk = Color(255, 255, 248, 220)
Color.crimson = Color(255, 220, 20, 60)
Color.cyan = Color(255, 0, 255, 255)
Color.dark_blue = Color(255, 0, 0, 139)
Color.dark_cyan = Color(255, 0, 139, 139)
Color.dark_goldenrod = Color(255, 184, 134, 11)
Color.dark_gray = Color(255, 169, 169, 169)
Color.dark_green = Color(255, 0, 100, 0)
Color.dark_khaki = Color(255, 189, 183, 107)
Color.dark_magenta = Color(255, 139, 0, 139)
Color.dark_olive_green = Color(255, 85, 107, 47)
Color.dark_orange = Color(255, 255, 140, 0)
Color.dark_orchid = Color(255, 153, 50, 204)
Color.dark_red = Color(255, 139, 0, 0)
Color.dark_salmon = Color(255, 233, 150, 122)
Color.dark_sea_green = Color(255, 143, 188, 143)
Color.dark_slate_blue = Color(255, 72, 61, 139)
Color.dark_slate_gray = Color(255, 47, 79, 79)
Color.dark_turquoise = Color(255, 0, 206, 209)
Color.dark_violet = Color(255, 148, 0, 211)
Color.deep_pink = Color(255, 255, 20, 147)
Color.deep_sky_blue = Color(255, 0, 191, 255)
Color.dim_gray = Color(255, 105, 105, 105)
Color.dodger_blue = Color(255, 30, 144, 255)
Color.firebrick = Color(255, 178, 34, 34)
Color.floral_white = Color(255, 255, 250, 240)
Color.forest_green = Color(255, 34, 139, 34)
Color.fuchsia = Color(255, 255, 0, 255)
Color.gainsboro = Color(255, 220, 220, 220)
Color.ghost_white = Color(255, 248, 248, 255)
Color.gold = Color(255, 255, 215, 0)
Color.goldenrod = Color(255, 218, 165, 32)
Color.gray = Color(255, 128, 128, 128)
Color.green = Color(255, 0, 128, 0)
Color.green_yellow = Color(255, 173, 255, 47)
Color.honeydew = Color(255, 240, 255, 240)
Color.hot_pink = Color(255, 255, 105, 180)
Color.indian_red = Color(255, 205, 92, 92)
Color.indigo = Color(255, 75, 0, 130)
Color.ivory = Color(255, 255, 255, 240)
Color.khaki = Color(255, 240, 230, 140)
Color.lavender = Color(255, 230, 230, 250)
Color.lavender_blush = Color(255, 255, 240, 245)
Color.lawn_green = Color(255, 124, 252, 0)
Color.lemon_chiffon = Color(255, 255, 250, 205)
Color.light_blue = Color(255, 173, 216, 230)
Color.light_coral = Color(255, 240, 128, 128)
Color.light_cyan = Color(255, 224, 255, 255)
Color.light_goldenrod_yellow = Color(255, 250, 250, 210)
Color.light_gray = Color(255, 211, 211, 211)
Color.light_green = Color(255, 144, 238, 144)
Color.light_pink = Color(255, 255, 182, 193)
Color.light_salmon = Color(255, 255, 160, 122)
Color.light_sea_green = Color(255, 32, 178, 170)
Color.light_sky_blue = Color(255, 135, 206, 250)
Color.light_slate_gray = Color(255, 119, 136, 153)
Color.light_steel_blue = Color(255, 176, 196, 222)
Color.light_yellow = Color(255, 255, 255, 224)
Color.lime = Color(255, 0, 255, 0)
Color.lime_green = Color(255, 50, 205, 50)
Color.linen = Color(255, 250, 240, 230)
Color.magenta = Color(255, 255, 0, 255)
Color.maroon = Color(255, 128, 0, 0)
Color.medium_aquamarine = Color(255, 102, 205, 170)
Color.medium_blue = Color(255, 0, 0, 205)
Color.medium_orchid = Color(255, 186, 85, 211)
Color.medium_purple = Color(255, 147, 112, 219)
Color.medium_sea_green = Color(255, 60, 179, 113)
Color.medium_slate_blue = Color(255, 123, 104, 238)
Color.medium_spring_green = Color(255, 0, 250, 154)
Color.medium_turquoise = Color(255, 72, 209, 204)
Color.medium_violet_red = Color(255, 199, 21, 133)
Color.midnight_blue = Color(255, 25, 25, 112)
Color.mint_cream = Color(255, 245, 255, 250)
Color.misty_rose = Color(255, 255, 228, 225)
Color.moccasin = Color(255, 255, 228, 181)
Color.navajo_white = Color(255, 255, 222, 173)
Color.navy = Color(255, 0, 0, 128)
Color.old_lace = Color(255, 253, 245, 230)
Color.olive = Color(255, 128, 128, 0)
Color.olive_drab = Color(255, 107, 142, 35)
Color.orange = Color(255, 255, 165, 0)
Color.orange_red = Color(255, 255, 69, 0)
Color.orchid = Color(255, 218, 112, 214)
Color.pale_goldenrod = Color(255, 238, 232, 170)
Color.pale_green = Color(255, 152, 251, 152)
Color.pale_turquoise = Color(255, 175, 238, 238)
Color.pale_violet_red = Color(255, 219, 112, 147)
Color.papaya_whip = Color(255, 255, 239, 213)
Color.peach_puff = Color(255, 255, 218, 185)
Color.peru = Color(255, 205, 133, 63)
Color.pink = Color(255, 255, 192, 203)
Color.plum = Color(255, 221, 160, 221)
Color.powder_blue = Color(255, 176, 224, 230)
Color.purple = Color(255, 128, 0, 128)
Color.red = Color(255, 255, 0, 0)
Color.rosy_brown = Color(255, 188, 143, 143)
Color.royal_blue = Color(255, 65, 105, 225)
Color.saddle_brown = Color(255, 139, 69, 19)
Color.salmon = Color(255, 250, 128, 114)
Color.sandy_brown = Color(255, 244, 164, 96)
Color.sea_green = Color(255, 46, 139, 87)
Color.sea_shell = Color(255, 255, 245, 238)
Color.sienna = Color(255, 160, 82, 45)
Color.silver = Color(255, 192, 192, 192)
Color.sky_blue = Color(255, 135, 206, 235)
Color.slate_blue = Color(255, 106, 90, 205)
Color.slate_gray = Color(255, 112, 128, 144)
Color.snow = Color(255, 255, 250, 250)
Color.spring_green = Color(255, 0, 255, 127)
Color.steel_blue = Color(255, 70, 130, 180)
Color.tan = Color(255, 210, 180, 140)
Color.teal = Color(255, 0, 128, 128)
Color.thistle = Color(255, 216, 191, 216)
Color.tomato = Color(255, 255, 99, 71)
Color.transparent = Color(0, 0, 0, 0)
Color.turquoise = Color(255, 64, 224, 208)
Color.violet = Color(255, 238, 130, 238)
Color.wheat = Color(255, 245, 222, 179)
Color.white = Color(255, 255, 255, 255)
Color.white_smoke = Color(255, 245, 245, 245)
Color.yellow = Color(255, 255, 255, 0)
Color.yellow_green = Color(255, 154, 205, 50)
