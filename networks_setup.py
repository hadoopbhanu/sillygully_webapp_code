
#Need this module to run the gcloud command in the shell
import subprocess, os
from dotenv import load_dotenv 

# Load environment variables from the .env file
load_dotenv()

# Variable definition
project_name=os.getenv("project_name")
vpc_name=os.getenv("vpc_name")
subnet1_name=os.getenv("subnet1_name")
subnet2_name=os.getenv("subnet2_name")
subnet1_range=os.getenv("subnet1_range")
subnet2_range=os.getenv("subnet2_range")
sql_instance_name=os.getenv("sql_instance_name")
sql_admin_pass=os.getenv("sql_admin_pass")
sql_admin_user=os.getenv("sql_admin_user")


#Custom functions

#Function to check if the resource we're trying to createa already exists
def check_already_exists(string):
    if "already exists" in string:
        return True
    else:
        return False

#Creating NETWORKS and SUBNETWORKS
network_commands = [
    #Create a Custom VPC network for the project
        f"gcloud compute networks create {vpc_name}\
            --project={project_name}\
            --subnet-mode=custom\
            --mtu=1460\
            --bgp-routing-mode=regional",
    # Create a subnet_1
        f"gcloud compute networks subnets create {subnet1_name}\
            --project={project_name}\
            --description='VPC network for North American cloud resources and operations'\
            --range={subnet1_range}\
            --stack-type=IPV4_ONLY\
            --network={vpc_name}\
            --region=us-central1",
    #Create a subnet_2
        f"gcloud compute networks subnets create {subnet2_name}\
            --project={project_name}\
            --description='VPC assigned for Cloud resources in Asia-South'\
            --range={subnet2_range}\
            --stack-type=IPV4_ONLY\
            --network={vpc_name}\
            --region=asia-south1"
    ]

for cmd in network_commands:
    try:
        print('Running the command: '+ str(cmd))
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print ('Successfully ran the command: ' +cmd.split('--')[0].strip() + '  ...........................\n')
        print(result.stdout.decode('utf-8')+' \n')
    except subprocess.CalledProcessError as e:
        #Error handling
        print(f'Command failed: ' + cmd +'\n')
        error_string = e.stderr.decode('utf-8')
        err = '\'\'\'' + error_string + '\'\'\''
        if check_already_exists(error_string) == True:
            print (cmd.split('--')[0].strip() + '  ....service already exists, Skipping to the next command in the loop \n\n\n\n')
            continue
        else:
            print (err+'\n')
            break
    except Exception as e:
        #Unexpected errors
        print("An unexpected error occurred:" + str(e))
        break
 