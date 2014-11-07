#!/bin/bash

#set -x
sudo='sudo -u'

while getopts ":h:m:p:r:u:" option;do
   case $option in    
     h) host=$OPTARG;;
     m) mount_point=$OPTARG;;
     p) path_remote=$OPTARG;;
     r) runas=$OPTARG;;
     u) remote_user=$OPTARG;;    
     ?) exit;;
   esac
done


if [ -z "$host" ] || [ -z "$mount_point" ] || [ -z "$path_remote" ] || [ -z "$runas" ] || [ -z "$remote_user" ]; then
   exit
fi

found=$(/bin/grep "$runas" /etc/passwd)
if [ "$found" == "0" ];then
   echo "User to runas does not exist."
   exit
fi   
if [ ! -d "$mount_point" ]; then
   echo "Mount point does not exist and needs to be created before remote path can be mounted."
   exit
fi   

if [ "$USER" == "$runas" ];then
   sudo=''
   runas=''
fi   

cmd="$sudo $runas sshfs ${remote_user}@${host}:${path_remote} $mount_point -o idmap=user -o allow_other"
echo "$cmd"
eval "$cmd"
