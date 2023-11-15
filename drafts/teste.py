import boto3

def get_instance_type_for_alarm(alarm_name, region_name='us-west-2'):
    # Create a CloudWatch client
    cloudwatch = boto3.client('cloudwatch', region_name=region_name)
    
    try:
        # Describe the alarm
        response = cloudwatch.describe_alarms(AlarmNames=[alarm_name])

        # Check if the alarm exists
        if not response['MetricAlarms']:
            return None

        # Extract the dimensions (should contain the instance type)
        dimensions = response['MetricAlarms'][0].get('Dimensions', [])

        # Find the instance type dimension
        for dimension in dimensions:
            if dimension['Name'] == 'InstanceId':
                instance_id = dimension['Value']
                ec2 = boto3.client('ec2', region_name=region_name)
                instance = ec2.describe_instances(InstanceIds=[instance_id])['Reservations'][0]['Instances'][0]
                instance_type = instance['InstanceType']
                return instance_type

    except Exception as e:
        print(f"Error: {e}")
    
    return None

# Example usage
alarm_name = 'flopes-cpualarm-teste'
instance_type = get_instance_type_for_alarm(alarm_name)
if instance_type:
    print(f"Instance type associated with the alarm '{alarm_name}' is: {instance_type}")
else:
    print(f"No instance type found for the alarm '{alarm_name}'")
