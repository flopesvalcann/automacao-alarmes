import boto3

'''def list_instance_types_and_alarms():

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
                        alarm['AlarmName'], alarm['StateValue'], instance_id, instance.instance_type))'''


'''def list_instance_types_and_alarms():
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
                    
                    if alarm['StateValue'] == 'INSUFFICIENT_DATA':
                        # Deleting the alarm
                        cloudwatch.delete_alarms(AlarmNames=[alarm['AlarmName']])
                        
                        # Recreate the alarm with updated instance type in the dimensions
                        try:
                            alarm_name = alarm['AlarmName']
                            metric_name = alarm['MetricName']
                            namespace = alarm['Namespace']
                            statistic = alarm['Statistic']
                            threshold = alarm['Threshold']
                            comparison_operator = alarm['ComparisonOperator']
                            evaluation_periods = alarm['EvaluationPeriods']
                            period = alarm['Period']
                            actions_enabled = alarm['ActionsEnabled']
                            alarm_actions = alarm.get('AlarmActions', [])
                            alarm_description = alarm.get('AlarmDescription', '')
                            
                            # Checking for the 'Unit' attribute or providing a default value
                            unit = alarm.get('Unit', 'Count')

                            # Update dimensions with instance type
                            updated_dimensions = [
                                {'Name': 'InstanceId', 'Value': instance_id},
                                {'Name': 'InstanceType', 'Value': instance.instance_type}
                            ]

                            cloudwatch.put_metric_alarm(
                                AlarmName=alarm_name,
                                MetricName=metric_name,
                                Namespace=namespace,
                                Statistic=statistic,
                                Threshold=threshold,
                                ComparisonOperator=comparison_operator,
                                EvaluationPeriods=evaluation_periods,
                                Period=period,
                                Dimensions=updated_dimensions,
                                ActionsEnabled=actions_enabled,
                                AlarmActions=alarm_actions,
                                AlarmDescription=alarm_description,
                                Unit=unit
                            )
                            print(f"Alarm '{alarm_name}' was recreated due to 'INSUFFICIENT_DATA' state.")
                        except Exception as e:
                            print(f"Failed to recreate alarm '{alarm_name}': {str(e)}")'''


import boto3

def update_alarm_instance_type():
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

                    if alarm['StateValue'] == 'INSUFFICIENT_DATA':
                        try:
                            # Update the 'InstanceType' dimension value
                            for dim in alarm['Dimensions']:
                                if dim['Name'] == 'InstanceType':
                                    dim['Value'] = instance.instance_type

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

                            # Update the alarm with modified 'InstanceType' dimension value
                            cloudwatch.put_metric_alarm(**update_params)
                            print(f"InstanceType of Alarm '{alarm['AlarmName']}' updated.")
                        except Exception as e:
                            print(f"Failed to update InstanceType of alarm '{alarm['AlarmName']}': {str(e)}")













                    

