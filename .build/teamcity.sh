#!/usr/bin/env bash
#
# Auto Build testing script for TeamCity
#


WORKSPACE="."
REMOTE="/www/hev"

cp -av $REMOTE/hev.conf $WORKSPACE/
rm -rfv $REMOTE/*
cp -arv $WORKSPACE/* $REMOTE/
