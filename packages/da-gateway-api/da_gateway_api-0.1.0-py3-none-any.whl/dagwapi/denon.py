from typing import Dict, List

from loguru import logger as LOGGER

from dagwapi.utils import helper
from dagwapi.models.denon import ReceiverConstants, ReceiverInfo, ReceiverStatus

# -----------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------
class DenonAPI():
    """
    Interface to the DAGateway service for Denon API
    """
    def __init__(self, gateway_url: str):
        self._base_url: str = f'{gateway_url}/denon'
        if not helper.is_gateway_available(self._base_url):
            raise RuntimeError('Unable to connect to gateway. Down?')

    #--------------------------------------------------------------
    def discover(self) -> List[Dict]:
        """
        Discover Denon receivers on local network

        Returns:
            List: List of receiver info dictionaries
            ```
            [
                {
                    "host": receiver.host,
                    "name": receiver.name,
                    "manufacturer": receiver.manufacturer,
                    "model_name": receiver.model_name,
                    "serial_number": receiver.serial_number,
                    "receiver_type": receiver.receiver_type,
                    "receiver_port": receiver.receiver_port,
                    "input_func_list": receiver.input_func_list,            
                },
                {...}, 
                ...
            ]
            ```
        """
        url = f'{self._base_url}/discover'        
        resp = helper.call_api(url)
        return resp['value']
    
    def info(self, host: str) -> ReceiverInfo:
        """
        Denon Receiver info

        Args:
            host (str): Denon Host (IP)

        Returns:
            ReceiverInfo object
        """        
        url = f'{self._base_url}/info/{host}'
        resp = helper.call_api(url)
        info_obj: ReceiverInfo = ReceiverInfo(resp['value'])
        return info_obj

    def status(self, host: str) -> ReceiverStatus:
        """
        Get status info for target receiver (host)

        Args:
            host (str): Host (ip)

        Returns:
            ReceiverStatus object
        """
        url = f'{self._base_url}/status/{host}'
        resp = helper.call_api(url)
        status_obj: ReceiverStatus = ReceiverStatus(resp['value'])
        return status_obj

    #--------------------------------------------------------------
    def turn_on(self, host: str) -> bool:
        """
        Turn on receiver

        Args:
            host (str): Receiver host (ip)

        Returns:
            bool: Device on = True else False
        """
        url = f'{self._base_url}/power_state/{host}?value={ReceiverConstants.POWER_ON}'
        resp = helper.call_api(url, is_post=True)
        power_state = resp['value']['power']
        if power_state.upper() != ReceiverConstants.POWER_ON:  
            LOGGER.error(f'Unable to turn receiver from {power_state} to {ReceiverConstants.POWER_ON}. GW: {resp.get("msg")}')
            return False
        return True
    
    def turn_off(self, host: str) -> bool:
        """
        Turn off receiver

        Args:
            host (str): Receiver host (ip)

        Returns:
            bool: Device off = True else False
        """
        url = f'{self._base_url}/power_state/{host}?value={ReceiverConstants.POWER_OFF}'
        resp = helper.call_api(url, is_post=True)
        power_state = resp['value']['power']
        if power_state.upper() not in [ReceiverConstants.POWER_OFF, ReceiverConstants.POWER_STANDBY]:
            LOGGER.error(f'Unable to turn receiver from {power_state} to {ReceiverConstants.POWER_OFF}. GW: {resp.get("msg")}')
            return False
        return True

    def get_power(self, host: str) -> str:
        """
        Receiver power state

        Args:
            host (str): Receiver host (ip)

        Returns:
            str: Receiver power state - "on" or "off"
        """
        url = f'{self._base_url}/status/{host}'
        resp = helper.call_api(url)
        return resp['value']['power']

    #--------------------------------------------------------------
    def whats_playing(self, host: str) -> str:
        """
        Get what's playing on the receiver

        Args:
            host (str): Receiver host (ip)

        Returns:
            str: Title of what's playing or None (if nothing is playing)
        """
        url = f'{self._base_url}/status/{host}'
        resp = helper.call_api(url)
        return resp['value']['title']

    #--------------------------------------------------------------
    def volume_up(self, host: str) -> float:
        """
        Turn up volume on reciever (incr of 5)

        Args:
            host (str): Receiver host (ip)

        Returns:
            float: resulting volume level
        """
        url = f'{self._base_url}/volume_up/{host}'
        resp = helper.call_api(url, is_post=True)
        return resp['value']['volume']

    def volume_down(self, host: str) -> float:
        """
        Turn down volume on reciever (incr of 5)

        Args:
            host (str): Receiver host (ip)

        Returns:
            float: resulting volume level
        """
        url = f'{self._base_url}/volume_down/{host}'
        resp = helper.call_api(url, is_post=True)
        return resp['value']['volume']

    def get_volume(self, host: str) -> float:
        """
        Get volume level on reciever

        Args:
            host (str): Receiver host (ip)

        Returns:
            float: resulting volume level
        """
        url = f'{self._base_url}/status/{host}'
        resp = helper.call_api(url)
        return resp['value']['volume']
    
    def set_volume(self, host: str, value: float) -> float:
        """
        Set volume level on receiver

        Args:
            host (str): Receiver host (ip)
            value (float): Target volume 
                Should be in the range of -80 to 18

        Returns:
            float: resulting volume level
        """
        ##  DEBUG WARNING CODE, must be removed when volume functions have been fully tested.
        if value >= 18:
            LOGGER.error(f'*** THROTTLE DenonAPI.set_volume() No way are we going to set the volume that high [{value}]')
            LOGGER.error(f'    Valid range is {ReceiverConstants.VOLUME_MIN} to {ReceiverConstants.VOLUME_MAX}.')
            raise RuntimeError('volume')
            return self.get_volume(host)
        
        url = f'{self._base_url}/volume/{host}?value={value:.1f}'
        # LOGGER.error(f'BYPASSING REQEST: {url}')
        # return self.get_volume(host)
        resp = helper.call_api(url, is_post=True)
        return resp['value']['volume']

    #--------------------------------------------------------------
    def toggle_mute(self, host: str) -> bool:
        """
        Toggle receiver mute state

        Args:
            host (str): Receiver host (ip)

        Returns:
            bool: resulting mute state (True or False)
        """        
        url = f'{self._base_url}/mute/toggle/{host}'
        resp = helper.call_api(url, is_post=True)
        return resp['value']['muted']

    def get_muted(self, host: str) -> bool:
        """
        Get receiver mute state

        Args:
            host (str): Receiver host (ip)

        Returns:
            bool: mute state (True or False)
        """        
        url = f'{self._base_url}/status/{host}'
        resp = helper.call_api(url)
        return resp['value']['muted']

    def set_muted(self, host: str, value: bool) -> bool:
        """
        Set receiver mute state

        Args:
            host (str): Receiver host (ip)
            value (bool): True (mute receiver) False (unmute receiver)

        Returns:
            bool: Resulting mute state (True-muted/False-unmuted)
        """
        url = f'{self._base_url}/mute/{host}?value={value}'
        resp = helper.call_api(url, is_post=True)
        return resp['value']['muted']

    #--------------------------------------------------------------
    def get_input_func(self, host: str) -> str:
        """
        Get receiver input source

        Args:
            host (str): Receiver host (ip)

        Returns:
            str: Resulting input source
        """
        url = f'{self._base_url}/input_func/{host}'
        resp = helper.call_api(url)
        return resp['value']['input_func']
        return self.status(host).input_func

    def set_input_func(self, host: str, value: str) -> str:
        """
        Set receiver input source

        Args:
            host (str): Receiver host (ip)
            value (str): Desired input source

        Returns:
            str: Resulting input source
        """
        url = f'{self._base_url}/input_func/{host}?value={value}'
        resp = helper.call_api(url, is_post=True)
        return resp['value']['input_func']

    def get_input_func_list(self, host: str) -> List[str]:
        """
        Get receiver input sources

        Args:
            host (str): Receiver host (ip)

        Returns:
            list: A list of valid receiver input sources
        """
        return self.info(host).info_dict


if __name__ == '__main__':
    import dt_tools.logger.logging_helper as lh    
    lh.configure_logger(log_level="DEBUG", log_format=lh.DEFAULT_CONSOLE_LOGFMT)
    
    denon = DenonAPI('http://localhost:8900')
    LOGGER.info('Discover receivers...')
    receivers = denon.discover()
    host = receivers[0]['host']
    LOGGER.info(f'Receiver(s) discovered: {receivers}')
    LOGGER.info('')
    LOGGER.info(f'Host selected: {host}')
    LOGGER.info('Info:')
    for key, val in denon.info(host).info_dict.items():
        LOGGER.info(f'- {key:12} {val}')
    LOGGER.info('')
    LOGGER.info('Status:')
    for key,val in denon.status(host).status_dict.items():
        LOGGER.info(f'- {key:12} {val}')
    
    # LOGGER.info('')
    # initial_power_state = denon.get_power(host)
    # LOGGER.info(f'Receiver is currently: {initial_power_state} ')
    # if initial_power_state == ReceiverConstants.POWER_ON:
    #     LOGGER.info('- turn off')
    #     denon.turn_off(host)
    #     time.sleep(2)
    #     LOGGER.info('- turn on')
    #     current_power_state = denon.turn_on(host)
    #     time.sleep(2)
    #     LOGGER.info(f'- Toggle mute. Now {denon.toggle_mute(host)}')
    #     time.sleep(2)
    #     LOGGER.info(f'- Toggle mute. Now {denon.toggle_mute(host)}')
    #     time.sleep(2)
    # else:
    #     LOGGER.info('- turn on')
    #     denon.turn_on(host)
    #     time.sleep(2)
    #     LOGGER.info(f'- Toggle mute. Now {denon.toggle_mute(host)}')
    #     time.sleep(2)
    #     LOGGER.info(f'- Toggle mute. Now {denon.toggle_mute(host)}')
    #     time.sleep(2)
    #     LOGGER.info('- turn off')
    #     denon.turn_off(host)
    #     time.sleep(2)

    # current_power_state = denon.get_power(host)
    # if initial_power_state != current_power_state:
    #     LOGGER.info(f'- Returning to initial power state [{initial_power_state}]')
    #     if initial_power_state == ReceiverConstants.POWER_ON:
    #         denon.turn_on(host)
    #     else:
    #         denon.turn_off(host)
    
    # LOGGER.info('- Insuring power is off before we exit.')
    # denon.turn_off(host)

    LOGGER.info('')
    LOGGER.info('Thats all!')
    