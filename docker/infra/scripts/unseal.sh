#!/bin/sh -i

DATA_DIR=$(grep 'DATA_DIR' .env | cut -d'=' -f2)

## CONFIG LOCAL ENV
echo "[*] Config local environment..."
alias vault='docker-compose -f docker-compose-infra.yml exec vault vault "$@"'
export VAULT_ADDR=http://127.0.0.1:8200

## UNSEAL VAULT
echo "[*] Unseal vault..."
vault operator unseal -address=${VAULT_ADDR} $(grep 'Key 1:' "$DATA_DIR/keys.txt" | awk '{print $NF}')
vault operator unseal -address=${VAULT_ADDR} $(grep 'Key 2:' "$DATA_DIR/keys.txt" | awk '{print $NF}')
vault operator unseal -address=${VAULT_ADDR} $(grep 'Key 3:' "$DATA_DIR/keys.txt" | awk '{print $NF}')
