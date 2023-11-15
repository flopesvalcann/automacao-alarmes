import boto3

def list_instance_types():
    ec2 = boto3.resource('ec2', region_name='us-west-2')

    for instance in ec2.instances.all():
        print('ID: {}, Type: {}'.format(instance.id, instance.instance_type))

tipo = list_instance_types()
print(tipo)