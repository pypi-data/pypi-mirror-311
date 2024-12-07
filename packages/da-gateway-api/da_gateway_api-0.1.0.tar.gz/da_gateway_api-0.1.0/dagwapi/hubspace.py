from typing import Any, Dict, List, Tuple

from loguru import logger as LOGGER

from dagwapi.utils import helper


# --------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------
class _HubspaceGateway():
    """
    Interface to Hubspace devices
    """
    def __init__(self, gateway_url: str):
        self._base_url = f'{gateway_url}/hubspace'
        LOGGER.debug(f'HubspaceGateway.__init__() - {self._base_url}')
        if not helper.is_gateway_available(self._base_url):
            raise RuntimeError('Unable to connect to gateway. Down?')

    def discover(self) -> List[Dict[str,Any]]:
        """
        Discover Hubspace devices on local network

        Returns:
            List[Dict]: Device information
                ```
                {
                    'child': item[0], 
                    'model': item[1], 
                    'device_id': item[2], 
                    'device_class': item[3],
                    'friendly_name': item[4],
                    'functions' : List[Dict[str, Any]]
                }
                ```
        """
        url = f'{self._base_url}/discover'
        resp_json = helper.call_api(url)
        device_list = resp_json['value']        
        return device_list
        
    # def getChildInfoById(self, child_id: str) -> HubspaceDevice:
    def getChildInfoById(self, child_id: str) -> Tuple[str,str,str,str,str]:
        """
        Get device attributes based on child_id

        Args:
            child_id (str): GUID identifying child entry

        Returns:
            Device: child_id, model, device_id, device_class, friendly_name
        """
        url = f'{self._base_url}/child_by_id/{child_id}'
        resp_json = helper.call_api(url)
        # device: HubspaceDevice = HubspaceDevice(resp_json['value'])
        # return device
        child = resp_json['value']['child']
        model = resp_json['value']['model']
        device_id = resp_json['value']['device_id']
        device_class = resp_json['value']['device_class']
        friendly_name = resp_json['value']['friendly_name']

        return child, model, device_id, device_class, friendly_name

    def getDebugInfo(self, child_id: str) -> Dict[str,str]:
        """
        Get device info

        Args:
            child_id (str): GUID identifying child entry

        Returns:
            Dict[str,str]: Device information
            ```
            {
                "metadeviceId": guid,
                "values": {
                    "functionClass": name, 
                    "value": value,
                    "lastUpdateTime: timeStamp,
                }
            }
            ```
        Note:
            functionClass values are: 
            - power, timer, led-configuration
            - wifi-ssid, wifi-rssi, wifi-steady-state, wifi-setup-state, wifi-mac-address
            - ble-mac-address
            - geo-coordinates, scheduler-flags
            - available, visible, direct

        """
        url = f'{self._base_url}/debug_info/{child_id}'
        resp_json = helper.call_api(url)

        return resp_json['value']

    def getState(self, child_id: str, desired_state_name: str) -> Any:
        """
        Get specified state (i.e. power, ...) value

        Args:
            child_id (str): GUID identifying child entry
            desired_state_name (str): aka functionClass
            
        Returns:
            Any: value of target function class

        Note:
            desired_state_name / functionClass is one of:
            - power, timer, led-configuration
            - wifi-ssid, wifi-rssi, wifi-steady-state, wifi-setup-state, wifi-mac-address
            - ble-mac-address
            - geo-coordinates, scheduler-flags
            - available, visible, direct

        """
        url = f'{self._base_url}/state/{child_id}?desired_state_name={desired_state_name}'
        resp_json = helper.call_api(url)

        return resp_json['value']

    def setState(self, child_id: str, desired_state_name: str, state: any, instance_field: str = None) -> Any:
        """
        Set specified state (i.e. power, ...) value

        Args:
            child_id (str): GUID identifying child entry
            desired_state_name (str): aka functionClass
            state (any): Target state, type depends on function class
            instance_field: (str): Optional, if device has more than 1 instance (i.e. dual power switch)
            
        Returns:
            Any: value of target function class

        Note:
            desired_state_name / functionClass is one of:
            - power, timer, led-configuration
            - wifi-ssid, wifi-rssi, wifi-steady-state, wifi-setup-state, wifi-mac-address
            - ble-mac-address
            - geo-coordinates, scheduler-flags
            - available, visible, direct

        """
        query=f'desired_state_name={desired_state_name}&state={state}'
        if instance_field is not None:
            query += f'&instance_field[{instance_field}]'

        url=f'{self._base_url}/state/{child_id}?{query}'
        resp_json = helper.call_api(url,is_post=True)

        return resp_json['value']


    def getStateInstance(self, child_id: str, desired_state_name: str, function_instance: str) -> Any:
        query=f'desired_state_name={desired_state_name}&function_instance={function_instance}'
        url = f'{self._base_url}/state_instance/{child_id}?{query}'

        resp_json = helper.call_api(url)

        return resp_json['value']

    def setStateInstance(self, child_id: str, desired_state_name: str, function_instance: str, state: str) -> Any:
        query=f'desired_state_name={desired_state_name}&function_instance={function_instance}&state={state}'
        url = f'{self._base_url}/state_instance/{child_id}?{query}'
        
        resp_json = helper.call_api(url, is_post=True)

        return resp_json['value']
