#!/usr/bin/env python3
# -*- coding:utf-8 -*-

"""
    @project: k8s-controller-sqs-autoscaler
    @component: core
    @copyright: © 2020 by vfabi
    @author: vfabi
    @support: vfabi
    @initial date:
    @license: this file is subject to the terms and conditions defined
        in file 'LICENSE', which is part of this source code package
    @description:
    @todo:
"""

import boto3
from time import sleep, time
from kubernetes import client, config
from log import logger


class SQSPoller:

    options = None
    sqs_client = None
    extensions_v1_beta1 = None
    last_message_count = None

    def __init__(self, options):
        self.options = options
        self.sqs_client = boto3.client('sqs')
        config.load_incluster_config()
        self.extensions_v1_beta1 = client.ExtensionsV1beta1Api()
        self.last_scale_up_time = time()
        self.last_scale_down_time = time()

    def message_count(self):
        response = self.sqs_client.get_queue_attributes(QueueUrl=self.options.sqs_queue_url, AttributeNames=['ApproximateNumberOfMessages'])
        return int(response['Attributes']['ApproximateNumberOfMessages'])

    def poll(self):
        message_count = self.message_count()
        t = time()
        if message_count >= self.options.scale_up_messages:
            if t - self.last_scale_up_time > self.options.scale_up_cool_down:
                self.scale_up()
                self.last_scale_up_time = t
            else:
                logger.debug("Waiting for scale-up cooldown")
        if message_count <= self.options.scale_down_messages:
            if t - self.last_scale_down_time > self.options.scale_down_cool_down:
                self.scale_down()
                self.last_scale_down_time = t
            else:
                logger.debug("Waiting for scale-down cooldown")

        sleep(self.options.poll_period)

    def scale_up(self):
        deployment = self.deployment()
        if deployment.spec.replicas < self.options.max_pods:
            logger.info("Scaling up")
            deployment.spec.replicas += 1
            self.update_deployment(deployment)
        elif deployment.spec.replicas > self.options.max_pods:
            self.scale_down()
        else:
            logger.info("Max pods reached")

    def scale_down(self):
        deployment = self.deployment()
        if deployment.spec.replicas > self.options.min_pods:
            logger.info("Scaling Down")
            deployment.spec.replicas -= 1
            self.update_deployment(deployment)
        elif deployment.spec.replicas < self.options.min_pods:
            self.scale_up()
        else:
            logger.info("Min pods reached")

    def deployment(self):
        logger.debug("Loading deployment: {} from namespace: {}".format(self.options.kubernetes_deployment, self.options.kubernetes_namespace))
        deployments = self.extensions_v1_beta1.list_namespaced_deployment(
            self.options.kubernetes_namespace,
            label_selector="app={}".format(self.options.kubernetes_deployment)
        )
        return deployments.items[0]

    def update_deployment(self, deployment):
        api_response = self.extensions_v1_beta1.patch_namespaced_deployment(
            name=self.options.kubernetes_deployment,
            namespace=self.options.kubernetes_namespace,
            body=deployment
        )
        logger.debug("Deployment updated. Status='%s'" % str(api_response.status))

    def run(self):
        options = self.options
        logger.debug("Starting poll for {} queue every {}s".format(options.sqs_queue_url, options.poll_period))
        while True:
            self.poll()
