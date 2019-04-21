#!/bin/bash

export ANSIBLE_HOST_KEY_CHECKING=False
. ./group7_openrc.sh; ansible-playbook --ask-become-pass deploy_applications.yaml -i inventory/hosts.ini