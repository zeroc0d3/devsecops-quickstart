#!/usr/bin/env python3
from aws_cdk import core as cdk

from devsecops_quickstart.pipeline import CICDPipeline

app = cdk.App()
config = app.node.try_get_context("config")
general_config = config["general"]

developmentPipeline = CICDPipeline(
    app,
    id=f"{general_config['repository_name']}-cicd-development",
    general_config=general_config,
    stages_config=dict(filter(lambda item: item[0] == "dev", config["stage"].items())),
    env=cdk.Environment(
        account=general_config["toolchain_account"],
        region=general_config["toolchain_region"],
    ),
)

productionPipeline = CICDPipeline(
    app,
    id=f"{general_config['repository_name']}-cicd-production",
    general_config=general_config,
    stages_config=dict(
        filter(lambda item: item[0] in ["qa", "prod"], config["stage"].items())
    ),
    env=cdk.Environment(
        account=general_config["toolchain_account"],
        region=general_config["toolchain_region"],
    ),
)

app.synth()
