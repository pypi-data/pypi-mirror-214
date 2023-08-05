"""Exec module for managing EC2 spot instance requests."""
from typing import Dict
from typing import List

__func_alias__ = {"list_": "list"}


async def get(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    filters: List = None,
) -> Dict:
    """
    Get a spot instance request resource from AWS. Supply one of the inputs as the filter.

    Args:
        name (str):
            The name of the Idem state.

        resource_id (str, Optional):
            ID of the spot instance request.

    Returns:
        Dict[str, Any]:
            Returns spot instance request in present format

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.ec2.spot_instance_request.get name="my_resource"

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.spot_instance_request.get
                - kwargs:
                    name: my_resource
    """
    result = dict(comment=[], ret=None, result=True)
    boto3_filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=[{"name": "spot-instance-request-id", "values": [resource_id]}]
    )
    ret = await hub.exec.boto3.client.ec2.describe_spot_instance_requests(
        ctx=ctx,
        Filters=boto3_filters,
    )
    if not ret.get("ret", {}).get("SpotInstanceRequests"):
        result["comment"].append(
            hub.tool.aws.comment_utils.get_empty_comment(
                resource_type="aws.ec2.spot_instance_request", name=name
            )
        )
        return result

    resource = ret["ret"]["SpotInstanceRequests"][0]
    if len(ret["ret"]["SpotInstanceRequests"]) > 1:
        result["comment"].append(
            f"More than one aws.ec2.spot_instance_request resource was found. Use resource {resource.get('SpotInstanceRequestId')}"
        )

    result["ret"] = hub.tool.aws.ec2.conversion_utils.convert_raw_sir_to_present(
        resource
    )
    return result


async def list_(hub, ctx, name: str = None, filters: List = None) -> Dict:
    """
    Get a list of spot instance request resources from AWS. Supply one of the inputs as the filter.

    Args:
        name (str, Optional):
            The name of the Idem state.

        filters (list[str, str], Optional):
            One or more filters: for example, tag :<key>, tag-key. A complete list of filters can be found at
            https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ec2.html#EC2.Client.describe_spot_instance_requests

    Returns:
        Dict[str, Any]:
            Returns spot instance request list in present format

    Examples:
        Calling this exec module function from the cli with filters

        .. code-block:: bash

            idem exec aws.ec2.spot_instance_request.list name="my_resource" filters=[{'name': 'name', 'values': ['resource-name']}]

        Using in a state:

        .. code-block:: yaml

            my_unmanaged_resource:
              exec.run:
                - path: aws.ec2.spot_instance_request.list
                - kwargs:
                    name: my_resource
                    filters:
                        - name: 'name'
                          values: ['resource-name']
    """
    result = dict(comment=[], ret=[], result=True)
    boto3_filters = hub.tool.aws.search_utils.convert_search_filter_to_boto3(
        filters=filters
    )
    ret = await hub.exec.boto3.client.ec2.describe_spot_instance_requests(
        ctx,
        Filters=boto3_filters,
    )
    if not ret["result"]:
        result["comment"] += list(ret["comment"])
        result["result"] = False
        return result
    if not ret["ret"]["SpotInstanceRequests"]:
        result["comment"].append(
            hub.tool.aws.comment_utils.list_empty_comment(
                resource_type="aws.ec2.spot_instance_requests", name=name
            )
        )
        return result
    for spot_instance_request in ret["ret"]["SpotInstanceRequests"]:
        result["ret"].append(
            hub.tool.aws.ec2.conversion_utils.convert_raw_sir_to_present(
                spot_instance_request=spot_instance_request
            )
        )
    return result
