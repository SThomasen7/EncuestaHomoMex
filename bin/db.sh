#!/bin/bash

set -Eeuo pipefail

# Sanity check command line options

usage(){
  echo "Usage: $0 [create|destroy|reset|dump]"
}

if [ $# -ne 1 ]; then
  usage
  exit 1
fi

case $1 in
  "create")
    sqlite3 var/HomoMex.sqlite3 < sql/schema.sql
    sqlite3 var/HomoMex.sqlite3 < sql/data.sql
    ;;

  "destroy")
    rm -rf var/HomoMex.sqlite3
    ;;

  "reset")
    rm -rf var/HomoMex.sqlite3
    sqlite3 var/HomoMex.sqlite3 < sql/schema.sql
    sqlite3 var/HomoMex.sqlite3 < sql/data.sql
    ;;

  "dump")
    sqlite3 -batch -line var/HomoMex.sqlite3 'SELECT * FROM users'
    sqlite3 -batch -line var/HomoMex.sqlite3 'SELECT * FROM response'
    ;;

  *)
    usage
    exit1
    ;;
esac
