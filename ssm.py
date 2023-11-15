import boto3
import re


def send_command(instance_id):
    ssm_client = boto3.client('ssm', region_name=region_name)
    response = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': ["lsblk -o NAME,MOUNTPOINT | grep ' /$'"]}
    )
    command_id = response['Command']['CommandId']
    return command_id



def get_command_output(command_id, instance_id):
    ssm_client = boto3.client('ssm', region_name=region_name)
    output = ssm_client.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance_id,
    )
    cleaned_output = re.sub(r'\W+', '', output['StandardOutputContent'])
    return cleaned_output


instance_id = 'i-09132e6d8c846ecc2'
region_name = 'us-west-2'
command_id = send_command(instance_id)
#print(get_command_output(command_id, instance_id))
