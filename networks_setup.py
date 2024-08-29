#Script to automate infra creation for sillgully (Daily dose of humor) project

#Need this module to run the gcloud command in the shell
import subprocess


# Variable definition
project_name="sillygully"
vpc_name="silly-network"
subnet1_name="silly-iowa"
subnet2_name="silly-mumbai"
subnet1_range="10.1.0.0/20"
subnet2_range="10.2.0.0/20"

#Custom functions

def check_network_exists(network_name, project_name):
    try:
        subprocess.run(f'gcloud compute networks describe {network_name} --project {project_name}', shell=True,check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def check_subnet_exists(subnet_name, region, project_name):
    try:
        subprocess.run(f'gcloud compute networks subnets describe {subnet_name} --region {region} --project {project_name}', shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

network_exists = check_network_exists(vpc_name, project_name)
subnet1_exists = check_subnet_exists(subnet1_name, 'us-central1', project_name)
subnet2_exists = check_subnet_exists(subnet2_name, 'asia-south1', project_name)
subnet3_exists = check_subnet_exists('test-one', 'us-central1', project_name)


#Creating NETWORKS and SUBNETWORKS

network_commands = [
        f"gcloud compute networks create {vpc_name} --project={project_name} --subnet-mode=custom --mtu=1460 --bgp-routing-mode=regional",
        f"gcloud compute networks subnets create {subnet1_name} --project={project_name} --description='VPC network for North American cloud resources and operations' --range={subnet1_range} --stack-type=IPV4_ONLY --network={vpc_name} --region=us-central1",
    f"gcloud compute networks subnets create {subnet2_name} --project={project_name} --description='VPC assigned for Cloud resources in Asia-South' --range={subnet2_range} --stack-type=IPV4_ONLY --network={vpc_name} --region=asia-south1"
    ]

if network_exists == True:
    print (f'Network: {vpc_name} already exists, checking the subnets now')
    del network_commands[0]

    if subnet1_exists == True and subnet2_exists == True:
        print(f'Network: {vpc_name} and subnets: {subnet1_name}, {subnet2_name}  already exists')

    else:

        if subnet1_exists == True and subnet2_exists == False:
            print(f'Subnet {subnet1_name} already exists, creating  the subnet {subnet2_name}')
            del network_commands[0]
        elif subnet1_exists == False and subnet2_exists == True:
                print(f'Subnet {subnet2_name} already exists, creating the subnet {subnet1_name}')
                del network_commands[1]
        else:
                print(f'Creating both the subnets {subnet1_name} and {subnet2_name}')

        for cmd in network_commands:

            try :
                #Execute command in the shell and check for errors
                result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                print(f"Command succeeded: {cmd}")
                print(result.stdout.decode('utf-8'))
            except subprocess.CalledProcessError as e:
                #Error handling
                print(f"Command failed: {cmd}")

            break
else:

    print (f'The network {vpc_name} does not exist, Creating the netwrok and the subnets now....')
    for cmd in network_commands:

        try :
            #Execute command in the shell and check for errors
            result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            print(f"Command succeeded: {cmd}")
            print(result.stdout.decode('utf-8'))
        except subprocess.CalledProcessError as e:
            #Error handling
            print(f"Command failed: {cmd}")
            print(e.stderr.decode('utf-8'))
        except Exception as e:
            #Unexpected errors
            print(f"An unexpected error occurred: {str(e)}")
