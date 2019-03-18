#!/bin/sh -i

DATA_DIR=$(grep 'DATA_DIR' .env | cut -d'=' -f2)

## CONFIG LOCAL ENV
echo "[*] Config local environment..."
alias vault='docker-compose -f docker-compose-infra.yml exec vault vault "$@"'
export VAULT_ADDR=http://127.0.0.1:8200

## INIT VAULT
echo "[*] Init vault..."
vault operator init -address=${VAULT_ADDR} | sed $'s,\x1b\\[[0-9;]*[a-zA-Z],,g' | tee "$DATA_DIR/keys.txt"
export VAULT_TOKEN=$(grep 'Initial Root Token:' "$DATA_DIR/keys.txt" | awk '{print substr($NF, 1, length($NF)-1)}')

## UNSEAL VAULT
echo "[*] Unseal vault..."
vault operator unseal -address=${VAULT_ADDR} $(grep 'Key 1:' "$DATA_DIR/keys.txt" | awk '{print $NF}')
vault operator unseal -address=${VAULT_ADDR} $(grep 'Key 2:' "$DATA_DIR/keys.txt" | awk '{print $NF}')
vault operator unseal -address=${VAULT_ADDR} $(grep 'Key 3:' "$DATA_DIR/keys.txt" | awk '{print $NF}')

## AUTH
echo "[*] Auth..."
vault login -address=${VAULT_ADDR} token=${VAULT_TOKEN}

## CREATE BACKUP TOKEN
echo "[*] Create backup token..."
vault auth enable -address=${VAULT_ADDR} userpass
vault token create -address=${VAULT_ADDR} -display-name="backup_token" | awk '/token/{i++}i==2' | awk '{print "backup_token: " $2}' >> "$DATA_DIR/keys.txt"

## SAVE TOKEN IN ENV
uname_out="$(uname -s)"
case "${uname_out}" in
    Linux*)
        sed -e "s/<VAULT_TOKEN>/$(grep 'Initial Root Token:' "$DATA_DIR/keys.txt" | awk '{print substr($NF, 1, length($NF)-1)}')/g" .env
    ;;
    Darwin*)
        sed -i '' -e "s/<VAULT_TOKEN>/$(grep 'Initial Root Token:' "$DATA_DIR/keys.txt" | awk '{print substr($NF, 1, length($NF)-1)}')/g" .env
    ;;
    * )
        echo "[*] Can not set vault token. Set it yourself in .env file."
     ;;
esac
