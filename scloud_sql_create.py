#Need this module to run the gcloud command in the shell
import subprocess, os
from dotenv import load_dotenv 

# Load environment variables from the .env file
load_dotenv()

#assign the values
project_name=os.getenv('project_name')
sql_instance_name=os.getenv('sql_instance_name')
sql_admin_pass=os.getenv('sql_admin_pass')
sql_admin_user=os.getenv('sql_admin_user')

#Function to check if the resource we're trying to createa already exists
def check_already_exists(string):
    if "already exists" in string:
        return True
    else:
        return False


## Need to enable Cloud SQL APIs to start working with "Cloud SQL"

command = [
# Enable the Cloud SQL APIs 
    f'gcloud services enable sqladmin.googleapis.com --project={project_name}',
# Enable Service networking APIs for connection between GCP managed services and the custom VPC
    f'gcloud services enable servicenetworking.googleapis.com --project={project_name}',
# Create private IP range for Private Services Access/connection
    f'gcloud compute addresses create silly-private-services-range \
        --global\
        --purpose=VPC_PEERING \
        --addresses=192.168.0.0 \
        --prefix-length=16 \
        --description="network range for GCP manged services to connect to our custom VPC" \
        --network=silly-network\
        --project={project_name}',
# Create a network peering between our VPC and the managed service producer (GCP)
    f'gcloud services vpc-peerings connect \
        --service=servicenetworking.googleapis.com\
        --ranges=silly-private-services-range\
        --network=silly-network\
        --project={project_name}',
# Create a Cloud SQL instance
     f'gcloud sql instances create {sql_instance_name} \
                --database-version=MYSQL_8_0 \
                --edition=enterprise \
                --network=silly-network \
                --no-assign-ip \
                --enable-google-private-path \
                --cpu=2 \
        --memory=12\
                --storage-type=HDD \
                --storage-size=20 \
                --storage-auto-increase \
                --availability-type=REGIONAL \
                --zone=us-central1-a \
                --secondary-zone=us-central1-f \
                --enable-bin-log \
                --retained-backups-count=7 \
                --retained-transaction-log-days=3 \
                --no-deletion-protection\
        --project={project_name}',
# Create user and password
    f'gcloud sql users create {sql_admin_user}\
        --instance={sql_instance_name}\
        --password={sql_admin_pass}\
        --password-policy-password-expiration-duration=365d\
        --type=BUILT_IN\
        --project={project_name}'
]

for cmd in command:
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
            print (cmd.split('--')[0].strip() + '  ....service already exists, Skipping to the bext command in the loop \n\n\n\n')
            continue
        else:
            print (err+'\n')
            break
    except Exception as e:
        #Unexpected errors
        print("An unexpected error occurred:" + str(e))
        break