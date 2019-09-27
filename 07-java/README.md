# docker-mkdocs

This is a multistage docker manifest that automatically builds and deploys your documentation on mkdocs-material.

It performs a `git clone` on your documentation repo and builds the static HTML, copying the static HTML to a minimal nginx image to only take up around ~21MB in size (depending on your docs). 

The documentation repo can be specified in the Dockerfile:
```
ARG docs_repo=https://github.com/mrmcshane/ns1.ovh.git
```
Or as an argument at build time:
```
docker build . -t mrmcshane/mkdocs --build-arg docs_repo=https://github.com/mrmcshane/ns1.ovh.git
```


Many thanks to:

- [mkdocs](https://github.com/mkdocs/mkdocs)
- [mkdics-material](https://github.com/squidfunk/mkdocs-material)
- [Docker - Multistage Builds](https://docs.docker.com/develop/develop-images/multistage-build/)
- [Nginx](https://hub.docker.com/_/nginx)