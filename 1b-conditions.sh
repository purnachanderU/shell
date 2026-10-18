#!/bin/bash
user_id=$(id -u)
if [ $user_id -ne 0 ]; then
    echo "You are not root. Please run as root."
    exit 1
fi
validate(){
    if [ $1 -ne 0 ]; then
        echo "{2} not installed"
        exit 1
    else
        echo "{2} installing"
    fi
}
echo "Installing nginx"
dnf install niginx -y

validate $? "nginx installation"

dnf install mysql -y
validate $? "mysql installation"

echo "still procceded"