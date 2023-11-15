import boto3

def get_instance_types_for_all_instances(region_name):
    # Create an EC2 client
    ec2 = boto3.client('ec2', region_name=region_name)

    # Create a CloudWatch client
    cloudwatch = boto3.client('cloudwatch', region_name=region_name)

    instance_types = {}

    try:
        # List all EC2 instances in the region
        instances = ec2.describe_instances()

        for reservation in instances['Reservations']:
            for instance in reservation['Instances']:
                instance_id = instance['InstanceId']

                # Get the instance type
                instance_type = instance['InstanceType']

                # Describe the CloudWatch Alarms associated with the instance
                alarms = cloudwatch.describe_alarms_for_metric(MetricName='CPUUtilization', Dimensions=[{'Name': 'InstanceId', 'Value': instance_id}])

                # Add the instance type to the dictionary with the instance ID as the key
                instance_types[instance_id] = instance_type

    except Exception as e:
        print(f"Error: {e}")

    return instance_types

# Example usage: Provide the AWS region
region_name = 'us-west-2'
instance_types = get_instance_types_for_all_instances(region_name)

for instance_id, instance_type in instance_types.items():
    print(f"Instance ID: {instance_id}, Instance Type: {instance_type}")
