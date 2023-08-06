# SolldexAPI Python Client

This repository contains a Python client for interacting with the Solldex API. The client supports making requests to the following endpoints:

- Recepcionar Lote RPS
- Consultar Lote
- Consultar RPS

## Features

- Simple and intuitive interface for making requests to the Solldex API.
- Built-in retry logic using the Tenacity library, with up to 3 retry attempts and a 2 second wait between each attempt.
- Error logging for better debugging and maintenance.

## Installation

You can install the SolldexAPI Python Client via pip:

```bash
pip install solldex-api-client==0.1.0
```


## Usage

To use the SolldexAPI client, you'll need to import the SolldexAPI class and initialize it with your API token:

```python
from solldex_api import SolldexAPI

api = SolldexAPI('your-token-here')
```

Once you've done that, you can make requests to the Solldex API using the `recepcionar_lote`, `consultar_lote`, and `consultar_rps` methods:

```python
# Make a request to the Recepcionar Lote RPS endpoint
response = api.recepcionar_lote({
  'data_emissao': 'date',
  'prestador': {
    'cnpj': 'string',
    'inscricao_municipal': 'number',
    'codigo_municipio': 'number'
  },
  # Additional data...
})

# Make a request to the Consultar Lote endpoint
response = api.consultar_lote({
  'protocolo': 'number',
  'cnpj': 'number',
  'inscricao_municipal': 'number',
  'codigo_municipio': 'number'
})

# Make a request to the Consultar RPS endpoint
response = api.consultar_rps({
  'numero': 'number',
  'serie': 'number',
  'tipo': 'number',
  'cnpj': 'number',
  'inscricao_municipal': 'number',
  'codigo_municipio': 'number'
})
```

## Error Handling

The SolldexAPI client uses the Tenacity library to provide built-in retry logic for requests. If a request fails, the client will automatically retry it up to 3 times, with a 2 second wait between each attempt.

If a request continues to fail after 3 attempts, the client will log the error and raise a `requests.RequestException` exception.
