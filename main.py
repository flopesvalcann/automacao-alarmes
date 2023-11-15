import boto3
import ssm as ssm


region = 'us-west-2'
ec2 = boto3.resource('ec2', region)
cloudwatch = boto3.client('cloudwatch', region)

for instance in ec2.instances.all():
    instance_id = instance.id
    print('ID: {}, Tipo: {}'.format(instance_id, instance.instance_type))

    alarms = cloudwatch.describe_alarms()
    for alarm in alarms['MetricAlarms']:
        for dimension in alarm['Dimensions']:
            if dimension['Name'] == 'InstanceId' and dimension['Value'] == instance_id:
                print('Nome do alarme: {}, Status: {}, ID da instância: {}, Tipo da instância: {}'.format(
                    alarm['AlarmName'], alarm['StateValue'], instance_id, instance.instance_type))

                if alarm['StateValue'] == 'INSUFFICIENT_DATA':
                    try:
                        for dim in alarm['Dimensions']:
                            if dim['Name'] == 'InstanceType':
                                dim['Value'] = instance.instance_type
                            if dim['Name'] == 'device':
                                print("Achou!")
                                command_id = ssm.send_command(instance_id)
                                dim['Value'] = ssm.get_command_output(command_id, instance_id)
                                
                        update_params = {
                            'AlarmName': alarm['AlarmName'],
                            'Namespace': alarm['Namespace'],
                            'MetricName': alarm['MetricName'],
                            'Dimensions': alarm['Dimensions'],
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
                        }

                        cloudwatch.put_metric_alarm(**update_params)
                        print(f"Tipo da instância e do device do alarme '{alarm['AlarmName']}' atualizados.")
                    except Exception as e:
                        print(f"Falha ao atualizar o alarme '{alarm['AlarmName']}': {str(e)}")


