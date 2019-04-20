#!/bin/bash

. ./group7_openrc.sh; ansible-playbook --ask-become-pass deploy_nectar.yaml -i inventory/inventory.ini