#!/bin/bash

set -e 

sudo chage -m 1 root

for user in $(ls /home); do chage -m 1 $user; done

