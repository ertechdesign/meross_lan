"""Constants for the Meross IoT local LAN integration."""

from homeassistant import const as hac
from .merossclient import const as mc

DOMAIN = "meross_lan"

from homeassistant.components.switch import DOMAIN as PLATFORM_SWITCH
from homeassistant.components.sensor import DOMAIN as PLATFORM_SENSOR
from homeassistant.components.binary_sensor import DOMAIN as PLATFORM_BINARY_SENSOR
from homeassistant.components.light import DOMAIN as PLATFORM_LIGHT
from homeassistant.components.cover import DOMAIN as PLATFORM_COVER
from homeassistant.components.climate import DOMAIN as PLATFORM_CLIMATE

SERVICE_REQUEST = "request"

DND_ID = 'dnd' # entity (sub)id for the switch representing DNDMode

# ConfigEntry keys
CONF_DEVICE_ID = hac.CONF_DEVICE_ID
CONF_KEY = 'key'
CONF_PAYLOAD = hac.CONF_PAYLOAD
CONF_DEVICE_TYPE = "device_type"
CONF_HOST = hac.CONF_HOST

CONF_PROTOCOL = hac.CONF_PROTOCOL # protocol used to communicate with device
CONF_OPTION_AUTO = 'auto'
CONF_OPTION_MQTT = 'mqtt'
CONF_OPTION_HTTP = 'http'
CONF_PROTOCOL_OPTIONS = (
    CONF_OPTION_AUTO, # best-effort: tries whatever to connect
    CONF_OPTION_MQTT,
    CONF_OPTION_HTTP
)

CONF_POLLING_PERIOD = 'polling_period' # general device state polling or whatever
CONF_POLLING_PERIOD_MIN = 5
CONF_POLLING_PERIOD_DEFAULT = 30

CONF_TRACE = 'trace' # create a file with device info and communication tracing (only CONF_TRACE_TIMEOUT seconds then shut off)
CONF_TRACE_TIMEOUT = 600 # when starting a trace stop it and close the file after .. secs
CONF_TRACE_MAXSIZE = 65536 # or when MAXSIZE exceeded
CONF_TRACE_DIRECTORY = 'traces' # folder where to store traces
CONF_TRACE_FILENAME = '{}-{}.csv' # filename format: device_type-device_id.csv

CONF_TIME_ZONE = hac.CONF_TIME_ZONE # if set in config we'll force time_zone for devices

CONF_TIMESTAMP = mc.KEY_TIMESTAMP # this is a 'fake' conf param we'll add to config_entry when we want to force flush to storage

"""
 general working/configuration parameters (waiting to be moved to CONF_ENTRY)
"""
PARAM_UNAVAILABILITY_TIMEOUT = 20  # number of seconds since last inquiry to consider the device unavailable
PARAM_HEARTBEAT_PERIOD = 295 # whatever the connection state periodically inquire the device is there
PARAM_ENERGY_UPDATE_PERIOD = 55 # read energy consumption only every ... second
PARAM_HUBBATTERY_UPDATE_PERIOD = 3595 # read battery levels only every ... second
PARAM_HUBSENSOR_UPDATE_PERIOD = 55
PARAM_TIMEZONE_CHECK_PERIOD = 604800 # 1 week before retrying timezone updates
#PARAM_STALE_DEVICE_REMOVE_TIMEOUT = 60 # disable config_entry when device is offline for more than...
PARAM_GARAGEDOOR_TRANSITION_MAXDURATION = 60
PARAM_GARAGEDOOR_TRANSITION_MINDURATION = 10