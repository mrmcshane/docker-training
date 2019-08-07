# Database Container

How to build a database container.

The source for this can be found on my [github](https://github.com/mrmcshane/docker-training/tree/master/03-database-container).

We will be using the `mariadb/server` image. Documentation can be found [here](https://hub.docker.com/r/mariadb/server/).


## Volumes

As we want to run a databse, it could be a good idea to find a way not to lose the database when the container is stopped/destroyed. This is where volumes come in...

### Create a volume

```
docker volume create --name mariadb-data
```

It's that simple, and it will be around until you specifically destroy it.


### Attach the volume to a container

This is passed as the `-v` argument when running a container:

```
docker run -d -p 30066:3306 -v mariadb-data:/var/lib/mysql mariadb/server
```

This will spin up a `mariadb/server` container with the volume attached.

Delete the container you just spun up.


### Configuring MariaDB

We will want to at least configure the root password for mariadb or we wont be able to connect to or manage the instance.

Looking at the documentation, the root password can be set by configuring an environment variable `MARIADB_ROOT_PASSWORD` with a password on startup.

To configure an environment variable , we use the `-e` flag when spinning up a container:
```
docker run -d -p 30066:3306 -v mariadb-data:/var/lib/mysql -e MARIADB_ROOT_PASSWORD=pass mariadb/server
```

Now try and connect to the instance:
```
mysql -h 127.0.0.1 -P 30066 -u root -p
```

You will receive the error: `ERROR 1045 (28000): Access denied for user 'root'@'172.17.0.1' (using password: YES)`. This is because we previously spun up a mariadb instance with this volume, so even though we configured a root password in an environment variable, as it's a persistent volume it already has a mariadb installation configured.

#### Accessing the container

We will need to access the container directly to resolve this issue using the `docker exec -it` command. The full syntax is:
```
docker exec -it containerID command
```

So to access the shell of container `b24e5580d853`, we will use:
```
docker exec -it b24e5580d853 /bin/bash
```

As we have the volume mounted to the `/var/lib/mysql` directory, we need to remove all data in it to rebuild the container with our configurable database password:
```
rm -rf /var/lib/mysql/*
```

Exit the session as you would any other shell.

Stop the container with the incorrect mariadb config:
```
docker stop b24e5580d853
```

#### Re-configuring MariaDB

Now the incorrect installation has been removed from the volume, we can spin up the container again:
```
docker run -d -p 30066:3306 -v mariadb-data:/var/lib/mysql -e MARIADB_ROOT_PASSWORD=pass mariadb/server
```

Now try and connect to the instance:
```
mysql -h 127.0.0.1 -P 30066 -u root -p
```

Show all of the current databases:
```
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
+--------------------+
3 rows in set (0.00 sec)
```

#### Testing Persistence

Create a test database:
```
mysql> create database test1;
Query OK, 1 row affected (0.00 sec)
```
Confirm the test database is in place:
```
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| test1              |
+--------------------+
4 rows in set (0.00 sec)
```
Exit the session and delete the container.

Create a new instance, without specifying the password:
```
docker run -d -p 30066:3306 -v mariadb-data:/var/lib/mysql mariadb/server
```

As the mariadb installation is already in place, you should be able to log in again with the same password:
```
mysql -h 127.0.0.1 -P 30066 -u root -p
```

Show the databases:
```
mysql> show databases;
+--------------------+
| Database           |
+--------------------+
| information_schema |
| mysql              |
| performance_schema |
| test1              |
+--------------------+
4 rows in set (0.00 sec)
```