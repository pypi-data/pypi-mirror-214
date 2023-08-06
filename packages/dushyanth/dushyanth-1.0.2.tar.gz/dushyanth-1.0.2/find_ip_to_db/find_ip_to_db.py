import boto3
import ipaddress
import sqlite3


def find_ip(instance_name,ip):

    # Create an EC2 client
    ec2_client = boto3.client('ec2')

    # Retrieve instance details by name
    response = ec2_client.describe_instances(Filters=[{'Name': 'tag:Name', 'Values': [instance_name]}])

    # Extract security group IDs
    security_group_ids = []
    for reservation in response['Reservations']:
        for instance in reservation['Instances']:
            security_group_ids.extend(instance['SecurityGroups'])

    # Connect to SQLite database
    conn = sqlite3.connect('security_groups.db')
    c = conn.cursor()

    # Create table if it doesn't exist
    c.execute('''CREATE TABLE IF NOT EXISTS security_groups
                (ip_address text, group_id text, group_name text, protocol text, from_port text, to_port text)''')

    # Retrieve security group details
    for sg in security_group_ids:
        sg_response = ec2_client.describe_security_groups(GroupIds=[sg['GroupId']])

        desired_ip = ip
        for group in sg_response['SecurityGroups']:
            for rule in group['IpPermissions']:
                for ip_range in rule['IpRanges']:
                    network = ip_range['CidrIp']
                    if ipaddress.ip_address(desired_ip) in ipaddress.ip_network(network):
                        # Insert data into the database
                        data = (desired_ip, group['GroupId'], group['GroupName'], rule['IpProtocol'],
                                str(rule.get('FromPort', 'NA')), str(rule.get('ToPort', 'NA')))
                        print(data)
                        c.execute("INSERT INTO security_groups VALUES (?, ?, ?, ?, ?, ?)", data)
                        conn.commit()

    # Close the database connection
    conn.close()

instance_name = str(input('Enter instance name: '))
ip = str(input('Enter IP without subnet mask: '))

find_ip(instance_name, ip)