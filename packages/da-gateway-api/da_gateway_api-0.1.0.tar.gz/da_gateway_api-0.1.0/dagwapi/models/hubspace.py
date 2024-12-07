import json
import threading
from dataclasses import dataclass
from typing import Any, Dict, List

import dt_tools.net.net_helper as nh
from loguru import logger as LOGGER

from dagwapi.hubspace import _HubspaceGateway
from dagwapi.utils.helper import SingletonMeta

lock = threading.Lock()

# --------------------------------------------------------------------------------------
@dataclass
class HubspaceDevice():
    """
    Represents a hubspace device for calls from DAGatewayWeb

    """
    gateway: _HubspaceGateway
    device_dict: Dict[str,str]
    _debug_dict: Dict[str, Any] = None
    _wifi_ip_address: str = None
    _func_instances: List = None

    @property
    def eye_catcher(self) -> str:
        token = f'[{self.device_class}]-{self.friendly_name}'   
        token = f'{token:20}'
        return token
    
    @property
    def debug_dict(self) -> Dict[str, Any]:
        if self._debug_dict is None:
            # Lazy load
            LOGGER.debug(f'{self.eye_catcher}: Lazy load debug info.')
            self._debug_dict = self.gateway.getDebugInfo(self.child_id)
        
        return self._debug_dict
    @property
    def child_id(self) -> str:
        """
        Unique id representing a hubspace device

        Returns:
            str: GUID string
        """
        return self.device_dict['child']
    
    @property
    def model(self) -> str:
        return self.device_dict['model']
    
    @property
    def device_id(self) -> str:
        """
        Unique ID representing component for this child

        Returns:
            str: GUID string
        """
        return self.device_dict['device_id']
    
    @property
    def device_class(self) -> str:
        """
        Class of device

        Returns:
            str: Class ex (switch, plug, fan,...)
        """
        return self.device_dict['device_class']
    
    @property
    def friendly_name(self) -> str:
        return self.device_dict['friendly_name']

    @property
    def func_list(self) -> List[Dict[str, Any]]:
        if self.debug_dict.get('metadeviceId') == self.child_id:
            return self.debug_dict.get('values')
    
    @property
    def wifi_ssid(self):
        return self._get_debug_field('wifi-ssid')

    @property
    def wifi_mac_address(self):
        return self._get_debug_field('wifi-mac-address')

    @property
    def wifi_ip_address(self):
        if self._wifi_ip_address is None or self._wifi_ip_address == '1.1.1.1':
            try:
                self._wifi_ip_address = nh.get_ip_from_mac(self.wifi_mac_address)
            except Exception:
                self._wifi_ip_address = '1.1.1.1'
            LOGGER.debug(f'{self.eye_catcher}: Lazy load wifi_ip_address [{self._wifi_ip_address}]')

        return self._wifi_ip_address

    @property
    def available(self) -> bool:
        is_available = self._get_debug_field('available')
        return is_available

    @property
    def bluetooth_mac_address(self) -> bool:
        return  self._get_debug_field('ble-mac-address')

    @property
    def instances(self) -> List[str]:
        """Return list of (toggle) instances for this HubspaceSwitchDevice"""
        if self._func_instances is None:
            self._func_instances = []
            # debug_info = self._hs.getDebugInfo(self.child_id)
            LOGGER.debug(f'{self.eye_catcher}: debug_info: {self.debug_dict}\n')
            func_dict: Dict[str, Any] = None
            if self.debug_dict.get('metadeviceId') == self.child_id:
                for func_dict in self.debug_dict.get('values'):
                    LOGGER.debug(f'{self.eye_catcher}: func_dict: {func_dict}\n')
                    if func_dict.get('functionClass') == 'toggle':
                        func_instance = func_dict.get('functionInstance')
                        LOGGER.debug(f'{self.eye_catcher}: func_instance: {func_instance}\n')
                        if func_instance is not None:
                            if func_instance not in self._func_instances:
                                self._func_instances.append(func_instance)

            LOGGER.debug(f'{self.eye_catcher}: {len(self._func_instances)} lazy loaded.')

        return self._func_instances

    def turn_on(self, instance_name: str = None) -> bool:
        """Turn on switch (or switch instance)"""
        instance_str = '' if instance_name is None else f'[{instance_name}]' 
        LOGGER.debug(f'{self.eye_catcher}: turn_on {instance_str}')
        power_state = self.get_power_state(instance_name)
        if power_state is None:
            raise KeyError(f'{self.friendly_name} {instance_str} not found/valid.')

        if power_state == "off":
            if instance_name:
                self.gateway.setStateInstance(self.child_id, 'toggle', instance_name, "on")
            else:
                self.gateway.setState(self.child_id, 'power', "on")
            LOGGER.debug(f'{self.eye_catcher}: sent on request.')
        else:
            LOGGER.warning(f'{self.eye_catcher}: {instance_str} already turned on.')

        return True
    
    def turn_off(self, instance_name: str = None) -> bool:
        """Turn of switch (or switch instance)"""
        instance_str = '' if instance_name is None else f'[{instance_name}]' 
        LOGGER.debug(f'{self.eye_catcher}: turn_off {instance_str}')
        power_state = self.get_power_state(instance_name)
        if power_state is None:
            raise KeyError(f'{self.eye_catcher}: not found/valid.')

        if power_state == "on":
            if instance_name:
                self.gateway.setStateInstance(self.child_id, 'toggle', instance_name, "off")
            else:
                self.gateway.setState(self.child_id, 'power', "off")
            LOGGER.debug(f'{self.eye_catcher}: sent off request.')
        else:
            LOGGER.warning(f'{self.eye_catcher}: {instance_str} already turned off.')

        return True


    def get_power_state(self, instance_name: str):
        """Get switch (or switch instance) power state (on/off)"""
        power_state = None
        if instance_name:
            if instance_name in self.instances:
                power_state = self.gateway.getStateInstance(self.child_id, 'toggle', instance_name )
        else:
            power_state = self.gateway.getState(self.child_id, 'power')

        return power_state

    def _get_debug_field(self, function_class: str, instance_name: str = None):
        ret_value = None
        if self.debug_dict.get('metadeviceId') == self.child_id:
            for value_dict in self.debug_dict.get('values'):
                if value_dict.get('functionClass') == function_class:
                    if instance_name is None or value_dict.get("functionInstance") == instance_name:
                        ret_value = value_dict.get('value')
                        break

        return ret_value
    
class HubspaceManager(metaclass=SingletonMeta):
    # _instance = None
    _initialized: bool = False
    _devices: list[HubspaceDevice] = None
    _gateway = _HubspaceGateway = None 
    _initialized = False
    # https://refactoring.guru/design-patterns/singleton/python/example#example-1

    
    def __init__(self, gateway_url: str):
        if not self._initialized:
            LOGGER.debug('Initializing HubspaceManager class')
            self._gateway = _HubspaceGateway(gateway_url)
            self._load_devices()
            self._initialized = True
    
    @property
    def is_initialized(self) -> bool:
        return self._initialized

    @property
    def devices(self) -> List[HubspaceDevice]:
        """Return list of HubspaceDevice"""
        if self._devices is None:
            self._load_devices()
        return self._devices

    def _load_devices(self):
        if self._devices is None:
            self._devices = []
            device_list = self._gateway.discover()
            for dev_dict in device_list:
                # debug_dict = self._gateway.getDebugInfo(dev_dict['child'])
                device: HubspaceDevice = HubspaceDevice(self._gateway, dev_dict) # , debug_dict)
                self._devices.append(device)

    def get_device(self, name_or_id: str) -> HubspaceDevice:
        """Return device associated with friendly name or child_id"""
        for dev in self.devices:
            if dev.friendly_name == name_or_id or dev.child_id == name_or_id:
                return dev

        LOGGER.error(f'Unable to locate device: {name_or_id}')
        return None
    
    def dump_devices(self, include_functions: bool = False):
        LOGGER.info('in dump_devices')
        if self._initialized:
            for device in self.devices:
                LOGGER.info('== Device ===================================================================')
                LOGGER.info(f'Child         : {device.child_id}')
                LOGGER.info(f'Available     : {device.available}')
                LOGGER.info(f'Model         : {device.model}')
                LOGGER.info(f'Device Id     : {device.device_id}')
                LOGGER.info(f'Device Class  : {device.device_class}')
                LOGGER.info(f'Friendly Name : {device.friendly_name}')
                LOGGER.info(f'BT Mac Addr   : {device.bluetooth_mac_address}')
                LOGGER.info(f'Wifi IP       : {device.wifi_ip_address}')
                LOGGER.info(f'Wifi MAC      : {device.wifi_mac_address}')
                LOGGER.info(f'Wifi SSID     : {device.wifi_ssid}')
                if include_functions:
                    func_cnt = 0
                    LOGGER.info('Functions     :')
                    for function in device.func_list:
                        func_cnt += 1
                        LOGGER.info(f'  {function}')
                LOGGER.info('')


if __name__ == "__main__":
    import dt_tools.logger.logging_helper as lh
    lh.configure_logger(log_level="INFO", log_format=lh.DEFAULT_DEBUG_LOGFMT)
    LOGGER.info('Create HubspaceMaager')
    hm = HubspaceManager('http://localhost:8900')
    hm.dump_devices()
    LOGGER.info('')
    LOGGER.info('done.')