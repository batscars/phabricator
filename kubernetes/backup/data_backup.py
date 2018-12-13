#!/usr/bin/python3.5
import argparse
import sys
import logging
from kubernetes import client, config
from kubernetes.stream import stream

config.load_incluster_config()
k8s_coreapi = client.CoreV1Api()
logger = logging.getLogger("Metrics")
formatter = logging.Formatter('%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s')
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter
logger.addHandler(console_handler)
logger.setLevel(logging.DEBUG)


def exec_backup(namespace, label, command=["/bin/sh", "-c", "srv/phabricator/phabricator/bin/storage dump|gzip > /repos/backup.sql.gz"]):
    pods = k8s_coreapi.list_namespaced_pod(namespace=namespace, label_selector=label).items
    if len(pods) >= 1:
        pod = pods[0].metadata.name
        logger.info("phabricator pod name is " + str(pod))
    else:
        logger.error("No pod found in namespace {} with label {}".format(namespace, label))
        return
    logger.info("Start to backup phabricator data")
    flag = 0
    try:
        resp = stream(k8s_coreapi.connect_get_namespaced_pod_exec, pod, namespace,
                command=command,
                stderr=True, stdin=False,
                stdout=True, tty=False)
    except:
        flag = 1
        logger.error("Exec into pod %s in namespace %s error" % (pod, namespace))
    if flag == 0:
        logger.info("Backup phabricator data successfully")

def main():
    parser = argparse.ArgumentParser(description='phabricator data backup')
    parser.add_argument('-n', '--namespace', type=str, default="aitech", help='namespace current pod created in')
    parser.add_argument('-l', '--label', type=str, default="app=phabricator", required=False, help='label selector')
    args = parser.parse_args()
    namespace = args.namespace
    label = args.label
    exec_backup(namespace=namespace, label=label)


if __name__ == "__main__":
    main()