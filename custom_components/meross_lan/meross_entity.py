"""
 Base-Common behaviour for all Meross-LAN entities

 actual HA custom platform entities will be derived like this:
 MerossLanSwitch(_MerossToggle, SwitchEntity)
"""
from __future__ import annotations

from homeassistant.helpers.typing import StateType
from homeassistant.helpers import device_registry as dr
from homeassistant.const import (
    STATE_ON, STATE_OFF,
)


from .merossclient import const as mc, get_productnameuuid
from .helpers import LOGGER
from .const import CONF_DEVICE_ID, DOMAIN


class MerossFakeEntity:
    """
    an 'abstract' class we'll use as a placeholder to reduce optional and/or
    disabled entities access overhead
    """
    enabled = False



# pylint: disable=no-member
class _MerossEntity:

    PLATFORM: str

    def __init__(self, device: 'MerossDevice', id: object, device_class: str):  # pylint: disable=unsubscriptable-object
        self._device = device
        self._id = id
        self._attr_device_class = device_class
        self._attr_state = None
        #self._attr_unit_of_measurement = CLASS_TO_UNIT_MAP.get(device_class)
        device.entities[id] = self
        async_add_devices = device.platforms.setdefault(self.PLATFORM)
        if async_add_devices is not None:
            async_add_devices([self])


    def __del__(self):
        LOGGER.debug("MerossEntity(%s) destroy", self.unique_id)
        return

    """
    @abstractmethod
    @property
    def enabled(self):
        pass

    @abstractmethod
    def async_write_ha_state(self):
        pass
    """

    @property
    def unique_id(self):
        return f"{self._device.device_id}_{self._id}"


    @property
    def name(self) -> str:
        return f"{self._device.descriptor.productname} - {self._attr_device_class}" if self._attr_device_class else self._device.descriptor.productname


    @property
    def device_info(self):
        _desc = self._device.descriptor
        return {
            "identifiers": {(DOMAIN, self._device.device_id)},
            "connections": {(dr.CONNECTION_NETWORK_MAC, _desc.macAddress)},
            "manufacturer": mc.MANUFACTURER,
            "name": _desc.productname,
            "model": _desc.productmodel,
            "sw_version": _desc.firmware.get(mc.KEY_VERSION)
            }


    @property
    def device_class(self) -> str | None:
        return self._attr_device_class

    """ moved to sensor to comply with HA development
    @property
    def unit_of_measurement(self) -> str | None:
        return self._attr_unit_of_measurement
    """

    @property
    def should_poll(self) -> bool:
        return False


    @property
    def available(self) -> bool:
        return self._attr_state is not None


    @property
    def assumed_state(self) -> bool:
        return False


    @property
    def state(self) -> StateType:
        return self._attr_state


    async def async_added_to_hass(self) -> None:
        return


    async def async_will_remove_from_hass(self) -> None:
        return


    def set_state(self, state: str):
        if self._attr_state != state:
            self._attr_state = state
            if self.hass and self.enabled:
                self.async_write_ha_state()


    def set_unavailable(self):
        self.set_state(None)


    @property
    def entryname(self) -> str: # ATTR friendly_name in HA api
        return (self.registry_entry.name if self.registry_entry is not None else None) or self.name


    """
    even though these are toggle/binary_sensor properties
    we provide a base-implement-all
    """
    @property
    def is_on(self) -> bool:
        return self._attr_state == STATE_ON


    def _set_onoff(self, onoff) -> None:
        self.set_state(STATE_ON if onoff else STATE_OFF)



class _MerossToggle(_MerossEntity):

    def __init__(self, device: 'MerossDevice', id: object, device_class: str, toggle_ns: str, toggle_key: str):
        super().__init__(device, id, device_class)
        self._toggle_ns = toggle_ns
        self._toggle_key = toggle_key


    async def async_turn_on(self, **kwargs) -> None:
        def _ack_callback():
            self.set_state(STATE_ON)

        self._device.request(
            self._toggle_ns,
            mc.METHOD_SET,
            {self._toggle_key: {mc.KEY_CHANNEL: self._id, mc.KEY_ONOFF: 1}},
            _ack_callback
        )


    async def async_turn_off(self, **kwargs) -> None:
        def _ack_callback():
            self.set_state(STATE_OFF)

        self._device.request(
            self._toggle_ns,
            mc.METHOD_SET,
            {self._toggle_key: {mc.KEY_CHANNEL: self._id, mc.KEY_ONOFF: 0}},
            _ack_callback
        )



class _MerossHubEntity(_MerossEntity):

    def __init__(self, subdevice: 'MerossSubDevice', id: object, device_class: str):
        super().__init__(
            subdevice.hub,
            id,
            device_class)
        self.subdevice = subdevice


    @property
    def name(self) -> str:
        name = get_productnameuuid(self.subdevice.type, self.subdevice.id)
        return f"{name} - {self._attr_device_class}" if self._attr_device_class else name


    @property
    def device_info(self):
        _id = self.subdevice.id
        _type = self.subdevice.type
        return {
            "via_device": (DOMAIN, self._device.device_id),
            "identifiers": {(DOMAIN, _id)},
            "manufacturer": mc.MANUFACTURER,
            "name": get_productnameuuid(_type, _id),
            "model": _type
            }


"""
 helper functions to 'commonize' platform setup/unload
"""
def platform_setup_entry(hass: object, config_entry: object, async_add_devices, platform: str):
    device_id = config_entry.data[CONF_DEVICE_ID]
    device = hass.data[DOMAIN].devices[device_id]
    device.platforms[platform] = async_add_devices
    async_add_devices([entity for entity in device.entities.values() if entity.PLATFORM is platform])
    LOGGER.debug("async_setup_entry device_id = %s - platform = %s", device_id, platform)

def platform_unload_entry(hass: object, config_entry: object, platform: str) -> bool:
    device_id = config_entry.data[CONF_DEVICE_ID]
    device = hass.data[DOMAIN].devices[device_id]
    device.platforms[platform] = None
    LOGGER.debug("async_unload_entry device_id = %s - platform = %s", device_id, platform)
    return True
