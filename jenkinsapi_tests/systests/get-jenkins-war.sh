#!/bin/sh
#JENKINS_WAR_URL="http://mirrors.jenkins-ci.org/war/latest/jenkins.war"
if [[ -z $1 ]]; then
    JENKINS_WAR_URL="http://mirrors.jenkins-ci.org/war-stable/latest/jenkins.war"
else
    JENKINS_WAR_URL=$1
fi

wget -O jenkins.war $JENKINS_WAR_URL
