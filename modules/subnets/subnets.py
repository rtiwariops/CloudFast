from fastapi import APIRouter, HTTPException
from fastapi.openapi import docs
import boto3
import botocore
import os
from pydantic import BaseModel
import yaml

router = APIRouter()

class SubnetNotFound(BaseModel):
    message: str
    error_code: int
    
@router.post("/create_subnets", responses={200: {"model": SubnetNotFound},
                                                404: {"model": SubnetNotFound},
                                                500: {"model": SubnetNotFound}})
async def create_subnets(vpc_id: str, num_subnets: int):
    try:
        with open(os.path.normpath(os.getcwd() + "/modules/vpc/vpc.yml")) as f:
            config = yaml.safe_load(f)
            cloud_provider = config["vpc_config"]["provider"]
            cidr_block = config["vpc_config"]["vars"]["cidr_block"]
            if cloud_provider == "AWS":
                access_key_id = os.environ['AWS_ACCESS_KEY_ID']
                secret_access_key = os.environ['AWS_SECRET_ACCESS_KEY']
                region_name = os.environ['AWS_REGION']
                ec2_client = boto3.client('ec2',
                                        aws_access_key_id=access_key_id,
                                        aws_secret_access_key=secret_access_key,
                                        region_name=region_name)
            else:
                raise ValueError(f"Unsupported cloud provider: {cloud_provider}")
                
            subnet_ids = []
            for i in range(num_subnets):
                subnet_cidr_block = calculate_subnet_cidr(cidr_block, i, num_subnets)
                response = ec2_client.create_subnet(VpcId=vpc_id, CidrBlock=subnet_cidr_block)
                subnet_id = response['Subnet']['SubnetId']
                subnet_ids.append(subnet_id)
            return {"subnet_ids": subnet_ids}
    except FileNotFoundError as e:
        print(os.path.normpath(os.getcwd() + "/module/vpc/vpc.yml"))
        raise HTTPException(status_code=404, detail="vpc.yml file not found")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

