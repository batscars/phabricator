#!/usr/bin/env bash
pod=$(kubectl get pod -n aitech | grep phabricator | awk '{print$1}')
echo $pod
kubectl exec -n aitech $pod -- /bin/bash -c "srv/phabricator/phabricator/bin/storage dump|gzip > /repos/backup.sql.gz"
