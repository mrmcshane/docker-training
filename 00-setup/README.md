# Setup


## Installation

You will need several things installed to use docker correctly (on a mac):
- brew
- git
- virtualbox
- docker


### Brew

We will be using the [brew](https://brew.sh/) repo manager:

Now it's a terrible idea to run a random ruby file from the internet to install software, but it's the default/easiest install instructions:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```
To do this securely, you should download the file from github and read through it to understand what it's doing before running it.

### Git

Install git
```
brew install git
```

### Virtualbox

Install virtualbox:
```
brew update
brew tap caskroom/cask
brew cask install virtualbox
brew install docker
```

### Docker

Install docker:
```
brew install docker
```

## Docker Hub

To store your docker images, you will need a [Docker Hub](https://hub.docker.com) account.

There are other image repositories, but this one is the one we will use.


## Check docker is running

You can run `docker ps` to see the list of containers running on docker.

If the command runs successfully, docker is running.


