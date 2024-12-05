# Mind Castle - Build a wall around your secrets

A universal store for your secret data. Don't delay securing you or your customer's data by deliberating over cloud secret stores. Mind Castle makes it easy to get started, and easy to switch between cloud secret stores.

Mind Castle currently supports:
- HashiCorp Vault
- AWS Secrets Manager
- In-memory and JSON stores that should only be used for testing/migration

## Architecture

Mind Castle comes in three parts:
- A unified interface for several secret stores.
- An SQLAlchemy column type that transparently stores and retrieves secrets for you.
- A migration tool to convert your existing DB column data into secrets.

Some other notes:
- Mind Castle is configured and secret stores are initialised at import time. That means env-vars used for configuration need to be defined when Mind Castle is imported.
- Mind Castle makes no attempt to manage secrets in memory. [Memory management](https://stackoverflow.com/questions/728164/securely-erasing-password-in-memory-python) in [Python](https://discuss.python.org/t/how-to-hide-or-remove-sensitive-data-from-getting-exposed-in-memory-dump/44526) is [futile](https://stackoverflow.com/questions/41509771/python-remove-password-from-memory), and if you need that level of control it's best to use another language.


## Install

`pip install mind-castle`


## Configure

You can configure Mind Castle by setting environment variables for your chosen secret store. To see what configuration options are required for each store:

```bash
$ python -m mind_castle

Mind-Castle - Shhhhh
====================
Available secret stores:

memory            - Required env vars: []
awssecretsmanager - Required env vars: ['MIND_CASTLE_AWS_REGION', 'MIND_CASTLE_AWS_ACCESS_KEY_ID', 'MIND_CASTLE_AWS_SECRET_ACCESS_KEY']
hashicorpvault    - Required env vars: ['MIND_CASTLE_VAULT_HOST', 'MIND_CASTLE_VAULT_PORT', 'MIND_CASTLE_VAULT_TOKEN']
json              - Required env vars: []
```

## Use

In your model file:

```python
from mind_castle.sqlalchemy import SecretData

class MyDBModel(Base):
    name = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.now)
    secret_data = Column(SecretData("hashicorpvault"))
```

Your secrets are now safely stored in Vault (or AWS, or anywhere else)!


## TODO

- Make migration script work for non-json columns
- Document migration
- Support deleting secrets when row is deleted
- Implement prefixes/folders for secrets
- Explain how secrets are stored
- Enforce tests on PR / branch protections