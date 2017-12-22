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
