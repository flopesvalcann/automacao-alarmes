import boto3
import re


def update_alarm_device_from_instance():

    region = 'us-west-2'
    ec2 = boto3.resource('ec2', region)
    cloudwatch = boto3.client('cloudwatch', region)

    ec2_client = boto3.client('ec2', region)

    for instance in ec2.instances.all():
        instance_id = instance.id
        print('ID: {}, Type: {}'.format(instance_id, instance.instance_type))

        alarms = cloudwatch.describe_alarms()
        for alarm in alarms['MetricAlarms']:
            for dimension in alarm['Dimensions']:
                if dimension['Name'] == 'InstanceId' and dimension['Value'] == instance_id:
                    print('Alarm Name: {}, State: {}, Instance ID: {}, Instance Type: {}'.format(
                        alarm['AlarmName'], alarm['StateValue'], instance_id, instance.instance_type))

                    if alarm['StateValue'] == 'INSUFFICIENT_DATA':
                        try:
                            # Update the 'InstanceType' dimension value
                            for dim in alarm['Dimensions']:
                                if dim['Name'] == 'InstanceType':
                                    dim['Value'] = instance.instance_type
                                if dim['Name'] == 'device':
                                    print("Achou!")
                                    device_value = str(get_block_device_name(instance_id, region))
                                    print(device_value)
                                    dim['Value'] = device_value
                            # Construct necessary parameters for updating the alarm
                            update_params = {
                                'AlarmName': alarm['AlarmName'],
                                'Namespace': alarm['Namespace'],
                                'MetricName': alarm['MetricName'],
                                'Dimensions': alarm['Dimensions'],  # Keep other dimensions intact
                                'Period': alarm['Period'],
                                'EvaluationPeriods': alarm['EvaluationPeriods'],
                                'Threshold': alarm['Threshold'],
                                'ComparisonOperator': alarm['ComparisonOperator'],
                                'Statistic': alarm['Statistic'],
                                'ActionsEnabled': alarm['ActionsEnabled'],
                                'AlarmActions': alarm['AlarmActions'],
                                'AlarmDescription': alarm.get('AlarmDescription', ''),
                                'OKActions': alarm.get('OKActions', []),
                                'InsufficientDataActions': alarm.get('InsufficientDataActions', []),
                                # Add other necessary parameters as per your alarm configuration
                            }

                            # Update the alarm with modified dimensions
                            cloudwatch.put_metric_alarm(**update_params)
                            print(f"InstanceType and Device of Alarm '{alarm['AlarmName']}' updated.")
                        except Exception as e:
                            print(f"Failed to update InstanceType or Device of alarm '{alarm['AlarmName']}': {str(e)}")



def get_block_device_name(instance_id, region_name):
    ssm_client = boto3.client('ssm', region_name=region_name)
    
    # Send command
    response = ssm_client.send_command(
        InstanceIds=[instance_id],
        DocumentName='AWS-RunShellScript',
        Parameters={'commands': ["lsblk -o NAME,MOUNTPOINT | grep ' /$'"]}
    )
    command_id = response['Command']['CommandId']
    
    # Get command output
    output = ssm_client.get_command_invocation(
        CommandId=command_id,
        InstanceId=instance_id,
    )
    
    # Remove non-alphanumeric characters
    cleaned_output = re.sub(r'\W+', '', output['StandardOutputContent'])
    
    return cleaned_output
