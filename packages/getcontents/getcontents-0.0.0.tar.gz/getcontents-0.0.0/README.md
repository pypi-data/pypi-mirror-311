# getcontents
A minimal HTTP/1.x client that is only used to deal with APIs.
It is not designed to be bulletproof or full-featured like requests.

```python
import asyncio

from getcontents import HTTPClient


async def main():
    async with HTTPClient('www.google.com', 80) as client:
        response = await client.send('GET /', data=b'')

        print(response.header)


if __name__ == '__main__':
    asyncio.run(main())
```

## License
MIT License
