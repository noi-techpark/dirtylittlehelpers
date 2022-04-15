#!/bin/bash
set -euo pipefail

### configuration - START
#
# The description appearing near your inbound rule
MYSG_DESC="Home Peter Moser"
# Your current IP address (leave this if you want to find it automatically)
MYIP=$(curl -L http://ipecho.net/plain 2>/dev/null)
#
### configuration - END

echo "##### CHANGING CIDR ON HOMEOFFICE SECGROUPS WITH DESCRIPTION '$MYSG_DESC' #####"

MYNEWCIDR="$MYIP/32"

echo "#"
echo "# Your current remote IP is: $MYIP"
echo "#"

echo -n "# HTTP + HTTPS:"

MYOLDCIDR=$(aws ec2 describe-security-groups \
    --group-name generic-http-https-homeoffices \
    | jq --arg mysg_desc "$MYSG_DESC" '(.SecurityGroups[0].IpPermissions[0].IpRanges[] | select(.Description == $mysg_desc) | .CidrIp)' \
    | tr -d '"')


if [ "$MYNEWCIDR" = "$MYOLDCIDR" ]; then

    echo " IPs are the same... skipping!"

else

    echo " Changing IP from $MYOLDCIDR to $MYNEWCIDR..."

    aws ec2 revoke-security-group-ingress \
        --group-name generic-http-https-homeoffices \
        --ip-permissions IpProtocol=tcp,FromPort=80,ToPort=80,IpRanges="[{CidrIp=$MYOLDCIDR,Description=$MYSG_DESC}]" \
        IpProtocol=tcp,FromPort=443,ToPort=443,IpRanges="[{CidrIp=$MYOLDCIDR,Description=$MYSG_DESC}]" || true

    aws ec2 authorize-security-group-ingress \
        --group-name generic-http-https-homeoffices \
        --ip-permissions IpProtocol=tcp,FromPort=80,ToPort=80,IpRanges="[{CidrIp=$MYNEWCIDR,Description=$MYSG_DESC}]" \
        IpProtocol=tcp,FromPort=443,ToPort=443,IpRanges="[{CidrIp=$MYNEWCIDR,Description=$MYSG_DESC}]"

fi

echo -n "# SSH:"

MYOLDCIDR=$(aws ec2 describe-security-groups \
    --group-name generic-ssh-homeoffices \
    | jq --arg mysg_desc "$MYSG_DESC" '(.SecurityGroups[0].IpPermissions[0].IpRanges[] | select(.Description == $mysg_desc) | .CidrIp)' \
    | tr -d '"')

if [ "$MYNEWCIDR" = "$MYOLDCIDR" ]; then

    echo " IPs are the same... skipping!"

else

    echo " Changing IP from $MYOLDCIDR to $MYNEWCIDR..."


    aws ec2 revoke-security-group-ingress \
        --group-name generic-ssh-homeoffices \
        --ip-permissions IpProtocol=tcp,FromPort=22,ToPort=22,IpRanges="[{CidrIp=$MYOLDCIDR,Description=$MYSG_DESC}]" || true 

    aws ec2 authorize-security-group-ingress \
        --group-name generic-ssh-homeoffices \
        --ip-permissions IpProtocol=tcp,FromPort=22,ToPort=22,IpRanges="[{CidrIp=$MYNEWCIDR,Description=$MYSG_DESC}]" 

fi

echo -n "# RDS:"

MYOLDCIDR=$(aws ec2 describe-security-groups \
    --group-name generic-rds-homeoffices \
    | jq --arg mysg_desc "$MYSG_DESC" '(.SecurityGroups[0].IpPermissions[0].IpRanges[] | select(.Description == $mysg_desc) | .CidrIp)' \
    | tr -d '"')

if [ "$MYNEWCIDR" = "$MYOLDCIDR" ]; then

    echo " IPs are the same... skipping!"

else

    echo " Changing IP from $MYOLDCIDR to $MYNEWCIDR..."

    aws ec2 revoke-security-group-ingress \
        --group-name generic-rds-homeoffices \
        --ip-permissions IpProtocol=tcp,FromPort=5432,ToPort=5432,IpRanges="[{CidrIp=$MYOLDCIDR,Description=$MYSG_DESC}]" || true

    aws ec2 authorize-security-group-ingress \
        --group-name generic-rds-homeoffices \
        --ip-permissions IpProtocol=tcp,FromPort=5432,ToPort=5432,IpRanges="[{CidrIp=$MYNEWCIDR,Description=$MYSG_DESC}]" 
fi

echo "##### READY."
exit 0
