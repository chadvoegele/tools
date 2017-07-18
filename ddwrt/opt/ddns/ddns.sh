#!/bin/sh
# DynDNS Updater Script, with HTTPS/SSL Support
# This example uses Google's HTTPS/SSL URL update method to update the IP for hostname.example.com. This script runs in an endless loop set to the UPDATE_INTERVAL which is currently 1 minutes.
# Edit the settings section to match your DynDNS provider, including the DDNS URL which will be unique for each provider.
# See also: https://www.dd-wrt.com/wiki/index.php/DDNS_-_How_to_setup_Custom_DDNS_settings_using_embedded_inadyn_-_HOWTO#Custom_.28URL_Updates.29
# And: http://www.dd-wrt.com/wiki/index.php/Useful_Scripts#DynDNS_Updates_Using_Curl_.28with_HTTPS.2FSSL_Support.29
# alfer@fusebin.com
# cavoegele@gmail.com

if [ -z $DDNS_DOMAIN ] || [ -z $DDNS_USERNAME ] || [ -z $DDNS_PASSWORD ]; then
  echo "DDNS_DOMAIN, DDNS_USERNAME, DDNS_PASSWORD must be set"
  exit 1
fi
UPDATE_INTERVAL=${UPDATE_INTERVAL:-60}
DDNS_HOST=${DDNS_HOST:-domains.google.com}

LOG_FILE=/var/log/ddns.log
CA_BUNDLE=/opt/ddns/cacert.pem  # https://curl.haxx.se/docs/caextract.html

CURL_CMD="curl --silent --show-error --cacert /opt/ddns/cacert.pem --tlsv1.1 https://$DDNS_USERNAME:$DDNS_PASSWORD@$DDNS_HOST/nic/update?hostname=$DDNS_DOMAIN"

while sleep $UPDATE_INTERVAL
do
  CURRENT_TIME=`date`
  CURRENT_WAN_IP=`nvram get wan_ipaddr`
  LAST_WAN_IP=`nvram get wan_ipaddr_last`
  DNS_IP=`nslookup $DDNS_DOMAIN 8.8.8.8 | grep -A 1 $DDNS_DOMAIN | awk 'FNR==2{print $3}'` 2>> $LOG_FILE

  # Check if IP Address has changed from last locally stored IP
  if [ -z $LAST_WAN_IP ] || [ $CURRENT_WAN_IP != $LAST_WAN_IP ]; then
    echo "$CURRENT_TIME: IP has changed from $LAST_WAN_IP to $CURRENT_WAN_IP" >> $LOG_FILE
    nvram set wan_ipaddr_last=$CURRENT_WAN_IP
    nvram commit
    echo "$CURRENT_TIME: Updating DynDNS Service" >> $LOG_FILE
    (echo "$CURRENT_TIME: Running $CURL_CMD" | sed "s/$DDNS_PASSWORD/...REDACTED.../") >> $LOG_FILE
    $CURL_CMD 1>> $LOG_FILE 2>&1
    echo "" >> $LOG_FILE

  # Check if IP Address has changed from what DNS is reporting
  elif [ -z $DNS_IP ] || [ $CURRENT_WAN_IP != $DNS_IP ]; then
    echo "$CURRENT_TIME: DNS IP not up to date, currently: $DNS_IP, but our IP is $CURRENT_WAN_IP" >> $LOG_FILE
    echo "$CURRENT_TIME: Updating DynDNS Service" >> $LOG_FILE
    (echo "$CURRENT_TIME: Running $CURL_CMD" | sed "s/$DDNS_PASSWORD/...REDACTED.../") >> $LOG_FILE
    $CURL_CMD 1>> $LOG_FILE 2>&1
    echo "" >> $LOG_FILE

  else
    echo "$CURRENT_TIME: DNS IP up to date!" >> $LOG_FILE
  fi

done
