#!/bin/bash

# Get acceptable options (i.e. the actions supported; e.g. GET,PUT,REPORT,etc)
# curl -X OPTIONS \
#      --user "$GUSER:$GPASS" \
#      -i \
#      "https://google.com/m8/carddav/principals/__uids__/$GUSER/lists/default/"

curl -X PROPFIND \
     --user "$GUSER:$GPASS" \
     -i \
     "https://google.com/m8/carddav/principals/__uids__/$GUSER/lists/default/"
echo " ----------- "

curl -X GET \
     --user "$GUSER:$GPASS" \
     -i \
     "https://google.com/m8/carddav/principals/__uids__/$GUSER/lists/default/62ea2f4088525c96"
echo " ----------- "

curl -X GET \
     --user "$GUSER:$GPASS" \
     -i \
     "https://google.com/m8/carddav/principals/__uids__/$GUSER/lists/default/12c7b5818badd1aa"
echo " ----------- "
