# 0x - Secret Storage

We will be using vault in this example of how to do secret storage with containers.



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
  nginx:
    image: "nginx:alpine"
    ports:
      - "80:80"
    networks:
      - network-secrets
volumes:
  vault-fs:
networks:
  network-secrets:
```

The main points are that we have two custom volumes attached to the vault container:

- vault-fs: contains the filesystem containing the secrets
- config.json: vault server configuration

The command that is run when the vault instance comes online ensures that the mounted volume has the correct permissions (as we don't run vault as root), and that the vault server starts up with the specified config file.



## Create Secrets

Once vault comes online the first time, it will ask you how many key peices you want to generate, along with how many key peices will make up a full master key. In this example, just make them both `1`. Save both keys it provides.

Note: We will use the root token in this example, it's best practice to not use this and to create sopecific users for applications requiring access. That way you can create proper role based access control.

Then start a new secrets engine, we want to use `kv` (key:value), as this is the default for storing username/password combos.
Create this with the path `kv` (default), and then add a secret, in this example:
```
path:nginx-secret
  key:username
  value:password99
```

## Testing - Retreive Secret

To test the secret is retreivable:
```
curl --header "X-Vault-Token:{{ root token }}" http://127.0.0.1:8200/v1/kv/data/nginx-secret | jq -r .data.data.username
```

You should receive the output
```
password99
```
