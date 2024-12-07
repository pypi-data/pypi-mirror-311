from dataclasses import dataclass
from loguru import logger as LOGGER
from typing import Any, Dict


# -----------------------------------------------------------------------------------
class ReceiverConstants:
    """
    Power, device and volume constants
    """
    # Power settings
    POWER_ON = "ON"
    POWER_OFF = "OFF"
    POWER_STANDBY = "STANDBY"
    # Device states
    DEVICE_ON = "on"
    DEVICE_OFF = "off"
    DEVICE_PLAYING = "playing"
    DEVICE_PAUSED = "paused"
    # Volume 
    VOLUME_MIN = -80.0
    VOLUME_MAX = 18.0
    VOLUME_DEFAULT = -55.0

# -----------------------------------------------------------------------------------
@dataclass
class ReceiverInfo():
    info_dict: Dict[str,Any]

    @property
    def host(self) -> str:
        """
        Receiver host (ip)

        Returns:
            str: ip address of the receiver
        """
        return self.info_dict.get('host','Unknown')
    
    @property
    def name(self) -> str:
        """
        Name of the receiver

        Returns:
            str: Friendly name of the receiver
        """
        return self.info_dict.get('name',None)
    
    @property
    def manufacturer(self) -> str:
        return self.info_dict.get('manufacturer','Unknown')
    
    @property
    def model_name(self) -> str:
        return self.info_dict.get('model_name','Unknown')
    
    @property
    def serial_number(self) -> str:
        return self.info_dict.get('serial_number','Unknown')
    
    @property
    def receiver_type(self) -> str:
        return self.info_dict.get('receiver_type','Unknown')
    
    @property
    def receiver_port(self) -> int:
        """
        Port receiver listening on.

        Returns:
            int: Port number
        """
        return self.info_dict.get('receiver_port','Unknown')
    
    @property
    def input_func_list(self) -> str:
        """
        List of input sources

        Returns:
            str: Input sources
        """
        return self.info_dict.get('input_func_list',['Unknown'])


# -----------------------------------------------------------------------------------
@dataclass
class ReceiverStatus():
    """
    Class representing current state of receiver

    ie. power, input source, volume, ...
    """
    status_dict: Dict[str,Any]

    @property
    def power(self) -> str:
        """
        Receiver power state

        Returns:
            str: ON, OFF, STANDBY
        """
        return self.status_dict.get('power','Unknown')
    
    @property
    def state(self) -> str:
        """
        Receiver state

        Returns:
            str: on, off, playing, paused
        """
        return self.status_dict.get('state','Unknown')
    
    @property
    def muted(self) -> bool:
        """
        Muted state

        Returns:
            bool: True if muted, False if unmuted
        """
        return self.status_dict.get('muted', False)
    
    @property
    def volume(self) -> float:
        """
        Receiver volume level

        Returns:
            float: Volume level in Denon values
                -80.0 (min) thru 18.0 (max) -99.0 if not valid.
        """
        return self.status_dict.get('volume',-99.0)
    
    @property
    def input_func(self) -> str:
        return self.status_dict.get('input_func','Unknown')
    
    @property
    def title(self) -> str:
        """
        Title of what's playing on receiver

        Returns:
            str: Title of what's playing, 'Unknown' if not valid
        """
        return self.status_dict.get('title','Unknown')
