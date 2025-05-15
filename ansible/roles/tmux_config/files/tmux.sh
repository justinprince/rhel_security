# RHEL-08-020041 -- V-230349
if ["$PS1"]; then
  parent=$(ps -o ppid= -i $$)
  name=$(ps -o comm= -p $parent)
  case "$name" in (sshd|login) exec tmux ;; esac
fi

