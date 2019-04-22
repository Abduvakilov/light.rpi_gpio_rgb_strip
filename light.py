import logging

import voluptuous as vol


from homeassistant.components.light import (

    ATTR_RGB_COLOR, ATTR_HS_COLOR, SUPPORT_COLOR, Light,

    PLATFORM_SCHEMA)

from homeassistant.const import CONF_NAME

import homeassistant.helpers.config_validation as cv

import homeassistant.util.color as color_util



_LOGGER = logging.getLogger(__name__)

CONF_DAT = 'dat'
CONF_CLK = 'clk'

DEFAULT_NAME = 'RGB Strip'



PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({

    vol.Required(CONF_DAT): cv.positive_int,
    vol.Required(CONF_CLK): cv.positive_int,
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,

})





def setup_platform(hass, config, add_entities, discovery_info=None):

    """Set up RGB Strip with DAT and CLK."""

    from .rgbstrip import LEDStrip


    name = config.get(CONF_NAME)

    DAT = config.get(CONF_DAT)
    CLK = config.get(CONF_CLK)

    rgb_strip = LEDStrip(CLK, DAT)


    add_entities([RPIGPIORGBStrip(rgb_strip, name)], True)





class RPIGPIORGBStrip(Light):

    """Representation of a RGB light."""



    def __init__(self, rgb_strip, name):

        """Initialize the light."""

        self._rgb_strip = rgb_strip

        self._name = name

        # self._rgb_color = [255, 255, 255]

        self._hs = None

        self._is_on = False



    @property

    def should_poll(self):

        """Set up polling."""

        return True



    @property

    def name(self):

        """Return the name of the light."""

        return self._name


    @property

    def hs_color(self):

        """Read back the color of the light."""

        return self._hs



    @property

    def is_on(self):

        """Return True if entity is on."""

        return self._is_on



    @property

    def supported_features(self):

        """Flag supported features."""

        return SUPPORT_COLOR



    def update(self):

        """No need to update anything."""
        


    def turn_on(self, **kwargs):

        """Turn the device on."""

        # if ATTR_RGB_COLOR in kwargs:

        #     self._rgb_color = kwargs[ATTR_RGB_COLOR]

        
        self._hs = kwargs.get(ATTR_HS_COLOR) or self._hs or [0,0]

        rgb = color_util.color_hs_to_RGB(*self._hs)

        self._rgb_strip.setcolourrgb(rgb[0], rgb[1], rgb[2])

        self._is_on = True



    def turn_off(self, **kwargs):

        """Turn the device off."""

        self._rgb_strip.setcolouroff()
        
        self._is_on = False
        