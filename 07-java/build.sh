#!/usr/bin/env bash

green='\033[32m';
no_colour='\033[0m';

echo -e "${green}[killing whatever is on port 80]${no_colour}"
docker kill $(docker ps -f publish=80 -q) # kill whatever is on port 80

echo -e "${green}[build docker image]${no_colour}"
docker build . -t java-test

echo -e "${green}[run docker image]${no_colour}"
docker run -d -p 80:80 -p 8443:8443 -p 8080:8080 java-test

echo -e "${green}[opening browser]${no_colour}"
/usr/bin/open -a "/Applications/Google Chrome.app" "http://localhost"
