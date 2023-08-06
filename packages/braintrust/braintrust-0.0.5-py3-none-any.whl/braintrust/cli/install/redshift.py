import json
import logging
import re
import textwrap
from hashlib import md5

import boto3


_redhshift = boto3.client("redshift")
_redshift_serverless = boto3.client("redshift-serverless")
_iam = boto3.client("iam")
_logger = logging.getLogger("braintrust.install.redshift")

TABLE_NAME = "braintrust_logs"


def build_parser(subparsers, parents):
    parser = subparsers.add_parser(
        "redshift", help="Setup Redshift to ingest from BrainTrust (Kafka)", parents=parents
    )

    parser.add_argument("name", help="Name of the Redshift cluster (or namespace) to create or update")
    parser.add_argument(
        "--create", help="Create the Redshift instance if it does not exist", action="store_true", default=False
    )
    parser.add_argument("--serverless", help="Use Serverless Redshift", action="store_true", default=False)
    parser.add_argument("--iam-role", help="IAM Role that can read from Kafka", default=None)
    parser.add_argument(
        "--iam-policy", help="Inline IAM policy permitting access to Kafka", default="BrainTrustMSKReadPolicy"
    )
    parser.add_argument(
        "--msk-cluster-arn",
        help="The ARN of a specific MSK cluster to allow access to. If this flag is unspecified, Redshift can read from any MSK cluster in this AWS account",
        default=None,
        required=True,
    )
    parser.add_argument(
        "--msk-topic-name",
        help="The name of a specific MSK topic to map into Redshift. The policy will allow access to all topics in the cluster, to support future topics",
        default="braintrust",
    )
    parser.add_argument(
        "--schema-name",
        help="The name of a Redshift schema to create that maps to the Kafka cluster",
        default="braintrust_streaming",
    )

    parser.set_defaults(func=main)


def main(args):
    if args.create:
        raise NotImplementedError("Creating Redshift clusters is not yet supported")

    if args.msk_topic_name.lower() != args.msk_topic_name:
        raise ValueError("Kafka topic names must be lowercase (b/c of Redshift case sensitivity issues)")

    role_name = args.iam_role or ("bt-redshift-" + md5(args.msk_cluster_arn.encode("utf-8")).hexdigest())
    role = None
    try:
        role = _iam.get_role(RoleName=role_name)
    except _iam.exceptions.NoSuchEntityException:
        pass

    if role is None:
        _logger.info("Creating IAM Role %s", role_name)
        role = _iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(
                {
                    "Version": "2012-10-17",
                    "Statement": [
                        {
                            "Effect": "Allow",
                            "Principal": {"Service": "redshift.amazonaws.com"},
                            "Action": "sts:AssumeRole",
                        }
                    ],
                }
            ),
            Description="BrainTrust Redshift Kafka Reader",
        )

    role_policy = None
    try:
        role_policy = _iam.get_role_policy(RoleName=role_name, PolicyName=args.iam_policy)
    except _iam.exceptions.NoSuchEntityException:
        pass

    # See definitions here: https://docs.aws.amazon.com/msk/latest/developerguide/iam-access-control.html
    msk_cluster_arn = args.msk_cluster_arn
    account_info, path = msk_cluster_arn.rsplit(":", 1)
    cluster_ident, cluster_name, cluster_uuid = path.split("/")
    if cluster_ident != "cluster":
        raise ValueError(f"Invalid MSK cluster ARN: {msk_cluster_arn}")

    # Allow access to all topics
    msk_topic_arn = f"{account_info}:topic/{cluster_name}/{cluster_uuid}/*"

    if role_policy is None:
        _logger.info(f"Creating inline IAM Policy {args.iam_policy} on {role_name}")

        policy = {
            "Version": "2012-10-17",
            "Statement": [
                {
                    "Sid": "MSKIAMpolicy",
                    "Effect": "Allow",
                    "Action": ["kafka-cluster:ReadData", "kafka-cluster:DescribeTopic", "kafka-cluster:Connect"],
                    "Resource": [
                        msk_cluster_arn,
                        msk_topic_arn,
                    ],
                },
                {"Sid": "MSKPolicy", "Effect": "Allow", "Action": ["kafka:GetBootstrapBrokers"], "Resource": "*"},
            ],
        }
        role_policy = _iam.put_role_policy(
            RoleName=role_name, PolicyName=args.iam_policy, PolicyDocument=json.dumps(policy)
        )

    role_arn = role["Role"]["Arn"]
    if args.serverless:
        namespace = _redshift_serverless.get_namespace(namespaceName=args.name)
        if namespace is None:
            raise ValueError(f"Serverless Redshift namespace {args.name} does not exist")

        existing_roles = [re.search(r"iamRoleArn=(.*)(,|\))", d).group(1) for d in namespace["namespace"]["iamRoles"]]
        if role_arn not in existing_roles:
            _logger.info("Adding IAM Role %s to Serverless Redshift namespace %s", role_arn, args.name)
            _redshift_serverless.update_namespace(namespaceName=args.name, iamRoles=existing_roles + [role_arn])
    else:
        raise NotImplementedError("Only Serverless Redshift is currently supported")

    #    if args.serverless:
    #        workgroup = None
    #        next_token = {}
    #        while workgroup is None:
    #            workgroups = _redshift_serverless.list_workgroups(**next_token)
    #            for wg in workgroups["workgroups"]:
    #                if wg["namespaceName"] == args.name:
    #                    workgroup = wg
    #                    break
    #
    #            if "nextToken" in workgroups:
    #                next_token = {"nextToken": workgroups["nextToken"]}
    #            else:
    #                break
    #        print(workgroup)
    #
    #        def get_credentials(database=None):
    #            kwargs = {}
    #            if database:
    #                kwargs["dbName"] = database
    #            return _redshift_serverless.get_credentials(workgroupName=args.name, **kwargs)
    #
    #    else:
    #        raise NotImplementedError("Only Serverless Redshift is currently supported")

    print(
        textwrap.dedent(
            f"""
        The CLI does not yet support running the setup queries against Redshift. Often, Redshift
        is not accessible from the public internet. You can run queries by visiting the SQL workbench,
        e.g. https://us-east-1.console.aws.amazon.com/sqlworkbench (fill in your region appropriately).

        Once connected, run the following commands to complete the setup process:

        CREATE EXTERNAL SCHEMA "{args.schema_name}"
            FROM MSK
            IAM_ROLE  '{role['Role']['Arn']}'
            AUTHENTICATION iam
            CLUSTER_ARN '{msk_cluster_arn}';


        CREATE MATERIALIZED VIEW "{TABLE_NAME}" AUTO REFRESH YES AS
            SELECT "kafka_partition",
            "kafka_offset",
            "kafka_timestamp_type",
            "kafka_timestamp",
            "kafka_key",
            JSON_PARSE("kafka_value") as data,
            "kafka_headers"
            FROM "{args.schema_name}"."{args.msk_topic_name}";"""
        )
    )
