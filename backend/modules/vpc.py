from fastapi import APIRouter, HTTPException
import boto3
import os
import yaml

router = APIRouter()

@router.post("/create_vpc")
async def create_vpc():
    # Read the config file
    with open("config.yml") as f:
        config = yaml.safe_load(f)
    cidr_block = config["cidr_block"]
    vpc_name = config["vpc_name"]
    cloud_provider = config["cloud_provider"]

    if cloud_provider == "aws":
        access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        region_name = os.environ['AWS_REGION']
        ec2_client = boto3.client('ec2',
                                 aws_access_key_id=access_key_id,
                                 aws_secret_access_key=secret_access_key,
                                 region_name=region_name)
    elif cloud_provider == "azure":
        # Code for creating a VPC in Azure
        pass
    elif cloud_provider == "gcp":
        # Code for creating a VPC in GCP
        pass
    else:
        raise ValueError(f"Unsupported cloud provider: {cloud_provider}")

    try:
        # Create a VPC
        response = ec2_client.create_vpc(CidrBlock=cidr_block)
        vpc_id = response['Vpc']['VpcId']
        # Add a name tag
        ec2_client.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': vpc_name}])
        return {"vpc_id": vpc_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.delete("/delete_vpc/{vpc_id}")
async def delete_vpc(vpc_id: str):
    # Read the config file
    with open("config.yml") as f:
        config = yaml.safe_load(f)
    cloud_provider = config["cloud_provider"]

    if cloud_provider == "aws":
        # Read AWS credentials from environment variables
        access_key_id = os.environ['AWS_ACCESS_KEY_ID']
        secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
        region_name = os.environ['AWS_REGION']

        ec2_client = boto3.client('ec2',
                                 aws_access_key_id=access_key_id,
                                 aws_secret_access_key=secret_access_key,
                                 region_name=region_name)
        try:
            # Delete the VPC
            ec2_client.delete_vpc(VpcId=vpc_id)
            return {"message": f"VPC {vpc_id} deleted successfully."}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
