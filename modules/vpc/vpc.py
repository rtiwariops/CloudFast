from fastapi import APIRouter, HTTPException
from fastapi.openapi import docs
import boto3
import botocore
import os
from pydantic import BaseModel
import yaml

router = APIRouter()

class VpcNotFound(BaseModel):
    message: str
    error_code: int

@router.post("/create_vpc", responses={200: {"model": VpcNotFound},
                                                404: {"model": VpcNotFound},
                                                500: {"model": VpcNotFound}})
async def create_vpc():
    try:
        with open(os.path.normpath(os.getcwd() + "/modules/vpc/vpc.yml")) as f:
            config = yaml.safe_load(f)
            cloud_provider = config["vpc_config"]["provider"]
            vpc_name = config["vpc_config"]["vars"]["vpc_name"]
            cidr_block = config["vpc_config"]["vars"]["cidr_block"]
            if cloud_provider == "AWS":
                access_key_id = os.environ['AWS_ACCESS_KEY_ID']
                secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
                region_name = os.environ['AWS_REGION']
                ec2_client = boto3.client('ec2',
                                        aws_access_key_id=access_key_id,
                                        aws_secret_access_key=secret_access_key,
                                        region_name=region_name)
            elif cloud_provider == "azure":
                # Code for creating a VPC in Azure
                raise NotImplementedError("Creating a VPC in Azure is not implemented")
            elif cloud_provider == "gcp":
                # Code for creating a VPC in GCP
                raise NotImplementedError("Creating a VPC in GCP is not implemented")
            else:
                raise ValueError(f"Unsupported cloud provider: {cloud_provider}")
                
            try:
                response = ec2_client.create_vpc(CidrBlock=cidr_block)
                vpc_id = response['Vpc']['VpcId']
                ec2_client.create_tags(Resources=[vpc_id], Tags=[{'Key': 'Name', 'Value': vpc_name}])
                return {"vpc_id": vpc_id}
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
    except FileNotFoundError as e:
        print(e)
        print(os.getcwd())
        print(os.path.normpath(os.getcwd() + "/module/vpc/vpc.yml"))
        raise HTTPException(status_code=404, detail="vpc.yml file not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except NotImplementedError as e:
        raise HTTPException(status_code=501, detail=str(e))


@router.delete("/delete_vpc/{vpc_id}", responses={200: {"model": VpcNotFound},
                                                404: {"model": VpcNotFound},
                                                500: {"model": VpcNotFound}})
async def delete_vpc(vpc_id: str):
    try:
        with open(os.path.normpath(os.getcwd() + "/modules/vpc/vpc.yml")) as f:
            config = yaml.safe_load(f)
            cloud_provider = config["vpc_config"]["provider"]
        if cloud_provider == "AWS":
            access_key_id = os.environ['AWS_ACCESS_KEY_ID']
            secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
            region_name = os.environ['AWS_REGION']

            ec2_client = boto3.client('ec2',
                                    aws_access_key_id=access_key_id,
                                    aws_secret_access_key=secret_access_key,
                                    region_name=region_name)
            try:
                ec2_client.delete_vpc(VpcId=vpc_id)
                return {"message": f"VPC {vpc_id} deleted successfully.", "error_code": 200}
            except botocore.exceptions.ClientError as e:
                if e.response['Error']['Code'] == 'InvalidVpcID.NotFound':
                    raise HTTPException(status_code=404, detail="VPC not found")
                else:
                    raise HTTPException(status_code=500, detail=str(e))
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="config.yml file not found")
    except KeyError as e:
        raise HTTPException(status_code=400, detail=f"{e} env variable is not set.")


