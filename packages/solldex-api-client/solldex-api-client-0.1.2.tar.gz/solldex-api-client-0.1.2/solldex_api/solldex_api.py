import logging
import requests
from tenacity import retry, stop_after_attempt, wait_fixed
from typing import Dict, Union

class SolldexAPI:
    """
    A Python interface to interact with the Solldex API.
    """

    def __init__(self, token: str):
        """
        Initializes a new instance of the SolldexAPI class.

        Args:
            token: The authorization token for the Solldex API.
        """
        self.base_url = 'https://api.solldex.com.br/v1'
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'Authorization': f'Bearer {token}'
        }

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def recepcionar_lote(self, data: Dict[str, Union[str, int, Dict]]) -> Dict:
        """
        Makes a POST request to the 'recepcionar-lote-rps' endpoint of the Solldex API.

        Args:
            data: The request body data.

        Returns:
            The response from the Solldex API.
        """
        url = f'{self.base_url}/recepcionar-lote-rps'
        try:
            response = requests.post(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f'Request to {url} failed: {e}')
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def consultar_lote(self, data: Dict[str, Union[str, int]]) -> Dict:
        """
        Makes a GET request to the 'consulta-lote' endpoint of the Solldex API.

        Args:
            data: The request parameters.

        Returns:
            The response from the Solldex API.
        """
        url = f'{self.base_url}/consulta-lote'
        try:
            response = requests.get(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f'Request to {url} failed: {e}')
            raise

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def consultar_rps(self, data: Dict[str, Union[str, int]]) -> Dict:
        """
        Makes a GET request to the 'consulta-rps' endpoint of the Solldex API.

        Args:
            data: The request parameters.

        Returns:
            The response from the Solldex API.
        """
        url = f'{self.base_url}/consulta-rps'
        try:
            response = requests.get(url, headers=self.headers, json=data)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            logging.error(f'Request to {url} failed: {e}')
            raise
