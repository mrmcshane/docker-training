# 0x - Secret Storage

We will be using vault in this example of how to do secret storage with containers.

**Note:** This is less of a task about learning docker than it is a basic example of using docker to host a basic python application with its secrets stored in vault.


## Docker Compose Config

It's a pretty basic compose file with two containers. One vault and one nginx:

```
version: '3'
services:
  vault:
    image: vault
    ports:
      - "8200:8200"
    networks:
      - network-secrets
    volumes:
      - vault-fs:/mnt/vault/file
      - ${PWD}/config.json:/home/vault/config.json
    cap_add:
      - IPC_LOCK
    command: /bin/sh -c "chown vault:vault /mnt/vault/file && /bin/vault server -config /home/vault/config.json"
  python:
    build: ./containers/orange-python
    ports:
      - "80:80"
    networks:
      - network-secrets
    environment:
      - VAULT_URL=http://vault:8200
      - VAULT_TOKEN={{ vault_token }}
volumes:
  vault-fs:
networks:
  network-secrets:
```

The main points are that we have two custom volumes attached to the vault container:

- vault-fs: contains the filesystem containing the secrets
- config.json: vault server configuration

The command that is run when the vault instance comes online ensures that the mounted volume has the correct permissions (as we don't run vault as root), and that the vault server starts up with the specified config file.

The vault token isn't specified here, but it will be given to you when you build the vault container for the first time. As the secret storage is on the volume, you can re-create the vault container and the token will work out of the box.

If you need to re-create the vault container from scratch, be sure to delete the volume.

## Create Secrets

Once vault comes online the first time, it will ask you how many key peices you want to generate, along with how many key peices will make up a full master key. In this example, just make them both `1`. Save both keys it provides.

**Note:** We will use the root token in this example, it's best practice to not use this and to create specific users for applications requiring access. That way you can create proper role based access control.

Then start a new secrets engine, we want to use `kv` (key:value), as this is the default for storing username/password combos.
Create this with the path `kv` (default), and then add a secret, in this example:
```
path:orange-python
key:username
value:password99
```

Add the root secret to the docker-compose file under the key `VAULT_TOKEN`:
```    
environment:
  - VAULT_URL=http://vault:8200
  - VAULT_TOKEN=s.dsOC6zOAiuCAhVkJnFoTQgYF
```
**Note:** I am storing this secret in github as it's part of the example, please never do this, even if it's a private repo. Best practice is to have the `VAULT_TOKEN` added in from an environment variable in your CI pipeline or something.


## Build the Containers

Using docker compose, force a build and run it in detached mode:
```
docker-compose up -d --build
```

## Testing

### Commandline

To test the secret is retreivable:
```
curl --header "X-Vault-Token:{{ vault_token }}" http://127.0.0.1:8200/v1/kv/data/orange-python | jq -r .data.data.username
```

You should receive the output
```
password99
```

### Browser

Visit the python app in a browser:
```
http://localhost/
```

You should see the vault data:
```
Vault Data: {'username': 'password99'}
```
