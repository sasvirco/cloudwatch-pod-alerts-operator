import kopf
import boto3
import logging
import datetime

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


@kopf.on.probe(id="now")
def get_current_timestamp(**kwargs):
    return datetime.datetime.utcnow().isoformat()


# @kopf.on.login(retries=5)
# def login_fn(**kwargs):
#    return kopf.login_via_client(**kwargs)


@kopf.on.create("crd.k8s.sas.io", "v1", "cwalerts")
def create_alarm(spec, meta, status, **kwargs):
    logging.info(f"Creating: {spec}")
    cw = boto3.client("cloudwatch", region_name="us-west-2")
    try:
        response = cw.put_metric_alarm(**spec)
        logging.info(response)
    except Exception as e:
        logging.error(e)


@kopf.on.update("crd.k8s.sas.io", "v1", "cwalerts")
def update_alarm(spec, old, new, diff, **_):
    logging.info(f"Updating: {spec}")
    cw = boto3.client("cloudwatch", region_name="us-west-2")
    try:
        response = cw.put_metric_alarm(**spec)
        logging.info(response)
    except Exception as e:
        logging.error(e)


@kopf.on.delete("crd.k8s.sas.io", "v1", "cwalerts")
def delete_alarm(spec, **_):
    logging.info(f"Deleting: {spec}")
    cw = boto3.client("cloudwatch", region_name="us-west-2")
    try:
        response = cw.delete_alarms(AlarmNames=[spec["AlarmName"]])
        logging.info(response)
    except Exception as e:
        logging.error(e)
