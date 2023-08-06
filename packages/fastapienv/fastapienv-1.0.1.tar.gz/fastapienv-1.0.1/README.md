# Your Module

A Python module that creates a Python environment and generates FastAPI boilerplate code.

This Module can even run your project as soon as it creates entire environment Make sure to use other parameters.

## Installation

You can install the module using pip:

## Usage

To use the module, import it and call the `createFastApiEnvironment` function:

```python
import fastapienv

# for creating just python environment and fast api boiler plate code
createFastApiEnvironment('{{your_prefered_env_name}}')

# here is the example for all the options provided in my module
createFastApiEnvironment("myenv", activate_env=True, start_server=True, server_host="localhost", server_port=8000, server_reload=True)

# activate_env will activate the environment after creating it.
# start_server will start the fast api server using uvicorn.
# server_host will be used to give the ip address or host name.
# server_port will be used to change the port number at which your fast api server should run
# server_reload will be used for dynamic reloading of your server if any changes happens to your files.

```
