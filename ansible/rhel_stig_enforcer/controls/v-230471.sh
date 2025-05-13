#!/bin/bash

set -e

# Recursively chmod /etc/audit/rules.d to ensure files do not have a mode more permissive than 0640
chmod 0640 -R /etc/audit/rules.d
chmod 0640 /etc/audit/auditd.conf
chmod 0640 /etc/audit/rules.d/*
