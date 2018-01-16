import boto3
import pprint


def input_number(msg, min, max):
    chosen = 0
    while True:
        try:
            chosen = int(input(msg))
            if chosen > max or chosen < min:
                print('Please choose a number between %d and %d' % (min, max))
                continue
            else:
                break
        except ValueError:
            print('Please choose a number')
            continue
    return chosen

ec2 = boto3.client('ec2')

regions = ec2.describe_regions()['Regions']
print('## Region List ##')
for idx, region in enumerate(regions):
    print('%d. %s' % (idx+1, region['RegionName']))

selected_num = input_number('Which region do you want? (1-%d) ' % len(regions), 1, len(regions))
selected_region = regions[selected_num-1]['RegionName']
print("You've selected a region number %d means %s" % (selected_num, selected_region))

ec2 = boto3.client('ec2', region_name=selected_region)
instances = list()
for reservation in ec2.describe_instances()['Reservations']:
    for instance in reservation['Instances']:
        name = ''
        for tag in instance['Tags']:
            if tag['Key'] == 'Name':
                name = tag['Value']
                break

        instances.append({
            'id': instance['InstanceId'],
            'type': instance['InstanceType'],
            'public_ip': instance['PublicIpAddress'],
            'private_ip': instance['PrivateIpAddress'],
            'state': instance['State']['Name'],
            'name': name
        })

print('## Instance List ##')
for idx, instance in enumerate(instances):
    print('%d. State: %s\tName: %s\tId: %s\tPublic IP: %s\tPrivate IP: %s' %
          (idx+1, instance['state'], instance['name'], instance['id'], instance['public_ip'], instance['private_ip']))

selected_num = input_number('Which instance do you want to start or stop? (1-%d) ' % len(instances), 1, len(instances))
selected_instance = instances[selected_num-1]
print("You've selected a instance number %d named %s and id %s" %
      (selected_num, selected_instance['name'], selected_instance['id']))

while True:
    selected_control = input(('The state of this instance is "%s". ' % selected_instance['state']) +
                             'Which do you want to start or stop? (start/stop) ').lower()
    if selected_control != 'start' and selected_control != 'stop':
        print('Invalid input! Please re-type "start" or "stop"')
        continue
    else:
        break

if selected_control == 'start':
    if selected_instance['state'] == 'stopped':
        print('Starting...')
    else:
        print('The state is not "stopped", so can\'t do that. Bye!')
else:
    if selected_instance['state'] == 'running':
        print('Stopping...')
    else:
        print('The state is not "running", so can\'t do that. Bye!')