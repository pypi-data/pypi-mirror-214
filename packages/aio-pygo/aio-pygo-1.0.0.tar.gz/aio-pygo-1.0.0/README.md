# Pygo

Pygo is fully typed & zero dependency Python library that enables you to code in a Go-like fashion. It brings some of the key features from the Go programming language such as goroutines and channels.

## Features

- **Goroutines**: Execute functions concurrently using asyncio coroutines.
- **Channels**: Enable communication and synchronization between coroutines using channels.
- **Select Statement**: Choose the first ready communication operation from multiple channels.
- **Time Management**: Schedule and manage timed operations using channels.
- **Deferring**: Defer operations using a context manager.

## Installation

To install Pygo, you can use pip:

```shell
pip install aio-pygo
```

## Usage

### Goroutines

```python
from asyncio import run
from python-go import go

async def worker():
    # some async operations
    ...

async def main():
    # Start a goroutine
    go(worker())

    # Continue with the main execution
    print("Main thread continues...")

if __name__ == "__main__":
    run(main())
```

### Channels

```python
from asyncio import run
from python-go import Chan

async def main():
    # Create a channel
    ch = Chan[str]()

    # Send data to the channel
    ch.send("Hello, Pygo!")

    # Receive data from the channel
    data = ch.receive()
    print(data)

if __name__ == "__main__":
    run(main())
```

### And more

To help you get started with Pygo, we provide a [collection of examples](https://github.com/GaelLnz/pygo/examples). These examples showcase various use cases and demonstrate how to leverage the features of Pygo in your projects.

## Testing

The Pygo library is 100% tested. To run the tests, you can use the following command:

```shell
make test
```

## Comming up next

Here's a list of features that we may implement in the near future:

* context management
* dedicated python compiler to allow multiprocessed coroutines

## Contributions

Contributions to Pygo are welcome! If you find a bug, have a suggestion, or want to contribute new features or improvements, please create an issue or submit a pull request on the [GitHub repository](https://github.com/GaelLnz/pygo).

## License

Pygo is licensed under the GPL 3.0 License. See the [LICENSE](LICENSE) file for more details.

---

Thank you for using Pygo. We hope this library enhances your concurrent and asynchronous programming experience in Python. Happy coding!