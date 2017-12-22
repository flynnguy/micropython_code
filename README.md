# micropython_code
Repo to hold all my misc. micropython code

# Secrets Management
So that I don't commit all my secrets into github, I have a file `secrets.json`
where I keep all of my secrets. I can then load it in with the following snippet:

```python
with open('secrets.json') as fp:
    secrets = ujson.loads(fp.read())

```

I've included a `example_secrets.py` file to give you an idea of what yours
should look like. You can then access it like so:

```python
print(secrets['wifi']['ssid'])
```

# Flashing ESP8266
The Makefile has a target to flash the esp8266 firmware. To use, download the
firmware (use `make download` on a mac) and set the `ESP_FIRMWARE` to the
location of the file. Also set your `ESP_PORT`. See examples below to change for
one time use.
```bash
$ make flash_esp8266
$ ESP_PORT=/dev/tty.wchusbserial1420 make flash_esp8266
```
