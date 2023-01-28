from fastapi import APIRouter, HTTPException
from fastapi.openapi import docs
import boto3
import botocore
import os
from pydantic import BaseModel
import yaml

router = APIRouter()

class IGWNotFound(BaseModel):
    message: str
    error_code: int

@router.post("/create_igw", responses={200: {"model": IGWNotFound},
                                                404: {"model": IGWNotFound},
                                                500: {"model": IGWNotFound}})
async def create_internet_gateway():
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
            elif cloud_provider == "azure":
                # Code for creating a Internet Gateway in Azure
                raise NotImplementedError("Creating a Internet Gateway in Azure is not implemented")
            elif cloud_provider == "gcp":
                # Code for creating a Internet Gateway in GCP
                raise NotImplementedError("Creating a Internet Gateway in GCP is not implemented")
            else:
                raise ValueError(f"Unsupported cloud provider: {cloud_provider}")
                
            try:
                response = ec2_client.create_internet_gateway()
                internet_gateway_id = response['InternetGateway']['InternetGatewayId']
                return {"internet_gateway_id": internet_gateway_id}
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
