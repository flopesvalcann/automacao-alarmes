import boto3

def list_instance_types_and_alarms():

    ec2 = boto3.resource('ec2', region_name='us-west-2')
    cloudwatch = boto3.client('cloudwatch', region_name='us-west-2')

    instances = {i.id: i for i in ec2.instances.all()}

    for instance_id, instance in instances.items():
        print('ID: {}, Type: {}'.format(instance_id, instance.instance_type))

        alarms = cloudwatch.describe_alarms()
        for alarm in alarms['MetricAlarms']:
            for dimension in alarm['Dimensions']:
                if dimension['Name'] == 'InstanceId' and dimension['Value'] == instance_id:
                    print('Alarm Name: {}, State: {}, Instance ID: {}, Instance Type: {}'.format(
                        alarm['AlarmName'], alarm['StateValue'], instance_id, instance.instance_type))

list_instance_types_and_alarms()




