# TurboREST

TurboREST is a REST API framework for Python 3.7+.

## Installation

```bash
pip install turborest
```

## Usage

```python
from turborest import Client

def main():
    client = Client(format="json")
    client.get("https://api.bytesentinel.io/test")
```

## Authentication

```python
from turborest import Client

def main():
    auth = ("Bearer", "xyz")
    client = Client(format="json", auth=auth)
    client.get("https://api.bytesentinel.io/test")
```

## Proxy

```python
from turborest import Client

def main():
    proxy = "http://localhost:8080"
    client = Client(format="json", proxy=proxy)
    client.get("https://api.bytesentinel.io/test")
```

## Advanced Options

```python
from turborest import Client

def main():
    proxy = "http://localhost:8080"
    endpoint = "https://api.bytesentinel.io/test"
    auth = ("Bearer", "xyz")
    client = Client(format="json", proxy=proxy, auth=auth)
    client.set_user_agent("TestAgent/1.0.0")
    client.set_success(print)
    client.set_header("X-Test", "Test")
    res = client.get(endpoint)

    print(res.status_code)
```

## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

### MIT License

```text
MIT License

TurboREST - A REST API framework for Python 3.7+.

...
    
```
