# QuickMQ

[![pipeline status](https://gitlab.ssec.wisc.edu/mdrexler/ssec_amqp/badges/main/pipeline.svg)](https://gitlab.ssec.wisc.edu/mdrexler/ssec_amqp/-/commits/main) [![coverage report](https://gitlab.ssec.wisc.edu/mdrexler/ssec_amqp/badges/main/coverage.svg)](https://gitlab.ssec.wisc.edu/mdrexler/ssec_amqp/-/commits/main) [![PyPI version shields.io](https://img.shields.io/pypi/v/quickmq.svg)](https://pypi.python.org/pypi/quickmq/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/quickmq.svg)](https://pypi.python.org/pypi/quickmq/)

An easy-to-use RabbitMQ client created for use at the SSEC.

## Table of Contents

* [Description](#description)
* [Installation](#installation)
* [Usage](#usage)
* [Author](#author)

## Description

QuickMQ is a high level RabbitMQ publisher made for the SSEC.

Current features:

* Multi-server publishing
* Publisher confirms
* Automatic reconnection
* Publishing message status

To see the requirements of this project check out the [reqs and specs doc](/docs/reqs-and-specs.md).

## Installation

### Installation Requirements

Python >= 3.6

QuickMQ is on [PyPi](https://pypi.org/project/quickmq/), so installation is easy using pip:

```bash
pip install --upgrade quickmq
```

To install from source (not usually necesasry).

```bash
git clone https://gitlab.ssec.wisc.edu/mdrexler/ssec_amqp.git
cd ssec_amqp
pip install .
```

## Usage

QuickMQ comes with an easy-to-use API.

Connect to servers:

```python3
import ssec_amqp.api as mq

mq.connect('server1', 'server2', user='username', password='password', exchange='satellite')
# Connects to the 'satellite' exchange on server1 and server2
```

Publish messages:

```python3
# continued from code block above

status = mq.publish({'payload': 'test'}, route_key='this.that')
# publish a message to all connected servers using a route key of 'this.that'

status # the status is returned as a dictionary
{'amqp://username@server1:5672//satellite': <DeliveryStatus.DELIVERED: "DELIVERED">, 'amqp://username@server2:5672//satellite': <DeliveryStatus.DROPPED: "DROPPED">}
```

> A DROPPED status means that the connection to the AMQP server is currently reconnecting.
> A REJECTED status means that the message was refused by the AMQP server.

Get status of current connections:

```python3
# continued from code block above

print(mq.status())
{'amqp://username@server1:5672//satellite': <ConnectionStatus.CONNECTED: "CONNECTED">, 'amqp://username@server2:5672//satellite': <ConnectionStatus.RECONNECTING: "RECONNECTING">}
```

You can also use the classes that drive the api directly.

```python3
from ssec_amqp import AmqpClient, AmqpConnection, DeliveryStatus

client = AmqpClient()

client.connect(AmqpConnection('server1', user='username', password='password'))

client.publish({'payload': 'test'})

client.disconnect()
```

## Author

Created/Maintained by [Max Drexler](mailto:mndrexler@wisc.edu).

## License

MIT License. See [LICENSE](/LICENSE) for more information.
