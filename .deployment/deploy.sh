#!/bin/bash

ENV_FILE=.env

DOMAIN=$1
EMAIL=$2

unset DJANGO_SECRET_KEY
unset POSTGRES_PASSWORD
unset POSTGRES_USER
unset POSTGRES_DB
unset LETSENCRYPT_EMAIL
unset FQDN

if [ -f $ENV_FILE ]; then
  echo "Loading saved environ"
  source $ENV_FILE
else
  if [ -z $EMAIL ]; then
    echo "Please specify a fully qualified domain name and an email address for Let's Encrypt"
    return 1 2>/dev/null
    exit 1
  fi
  echo "Creating environ"
  touch $ENV_FILE
fi

if [ -z $DJANGO_SECRET_KEY ]; then
  echo "Generating new DJANGO_SECRET_KEY"
  export DJANGO_SECRET_KEY=$(tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c50)
  echo "export DJANGO_SECRET_KEY=\"$DJANGO_SECRET_KEY\"" >> $ENV_FILE
fi
if [ -z $POSTGRES_PASSWORD ]; then
  echo "Generating new POSTGRES_PASSWORD"
  export POSTGRES_PASSWORD=$(tr -dc 'a-z0-9!@#$%^&*(-_=+)' < /dev/urandom | head -c25)
  echo "export POSTGRES_PASSWORD=\"$POSTGRES_PASSWORD\"" >> $ENV_FILE
fi
if [ -z $POSTGRES_USER ]; then
  export POSTGRES_USER=thedoubler
  echo "export POSTGRES_USER=\"$POSTGRES_USER\"" >> $ENV_FILE
fi
if [ -z $POSTGRES_DB ]; then
  export POSTGRES_DB=thedoubler
  echo "export POSTGRES_DB=\"$POSTGRES_DB\"" >> $ENV_FILE
fi
if [ -z $LETSENCRYPT_EMAIL ]; then
  export LETSENCRYPT_EMAIL=$EMAIL
  echo "export LETSENCRYPT_EMAIL=\"$LETSENCRYPT_EMAIL\"" >> $ENV_FILE
fi
if [ -z $FQDN ]; then
  export FQDN=$DOMAIN
  echo "export FQDN=\"$DOMAIN\"" >> $ENV_FILE
fi

echo "All environs loaded"
echo "You may now run docker-compose"
echo
echo "Hint: deploy: docker-compose up --build -d"
echo "Hint: shutdown: docker-compose down"
echo "Hint: update: docker-compose pull backend"
