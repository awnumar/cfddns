## Usage

### From command line:

```
./cfddns.py zone record email api_key
```
```
./cfddns.py example.com ssh.example.com me@example.com 0123456789abcdef
```

You are able to add this to your system's crontab file to schedule the update procedure to run regularly. See [usage](https://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/) and [commands](https://crontab.guru/).

### From script:

```
# Returns timestamp on success, None on failure.
cfddns.update(zone, record, email, api_key)
```
```
cfddns.update("example.com", "ssh.example.com", "me@example.com", "0123456789abcdef")
```
