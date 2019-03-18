#!/bin/sh -i

DATA_DIR=$(grep 'DATA_DIR' .env | cut -d'=' -f2)

read -p "[?] Are you sure you want to remove all data (y/n)? " answer
case ${answer:0:1} in
    y|Y )
        echo "[*] Removing files..."
        echo "[+] Removing: $DATA_DIR/consul/"
        rm -rf "$DATA_DIR/consul/"
        echo "[+] Removing: $DATA_DIR/redis/"
		rm -rf "$DATA_DIR/redis/"
		echo "[+] Removing: $DATA_DIR/keys.txt"
		rm -f "$DATA_DIR/keys.txt"
		echo "[+] Removing: $DATA_DIR/logs/"
		rm -rf "$DATA_DIR/logs/"
    ;;
    * )
        echo "[*] Aborting..."
    ;;
esac
