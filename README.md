**Requirements**

    git clone https://github.com/xeroc/python-bitsharesrpc
    cd python-bitsharesrpc
    python setup install    # (optionally with parameter --user fo non-root installations)

**Configuration**

An example configuration can be found in `config-sample.py`:

    url    = "http://127.0.0.1:19988/rpc"
    user   = 'username'
    passwd = 'pwd'
    unlock = "unlockPwd"
    wallet = "default"
