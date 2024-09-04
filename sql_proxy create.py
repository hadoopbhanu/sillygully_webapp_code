# Setting up proxy cleint for the cloud-sql service with Private IP

#Need this module to run the gcloud command in the shell
import subprocess, os, sys
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
sql_proxy_service_account=os.getenv('sql_proxy_service_account')


#Function to check if the resource we're trying to createa already exists
def check_already_exists(string):
    if "already exists" in string:
        return True
    else:
        return False


sql_proxy_commands = [
    # Create a service account for the sql proxy deamon
    f'gcloud iam service-accounts create {sql_proxy_service_account}\
        --description="This Service account is used by Cloud SQL Auth proxy"\
        --display-name=silly-sql-proxy-client\
        --project={project_name}',
    # Grant access to the sql-client service account 
    f'gcloud projects add-iam-policy-binding sillygully\
        --member="serviceAccount:{sql_proxy_service_account}@sillygully.iam.gserviceaccount.com"\
        --role="roles/cloudsql.client"',
    # Create an Instance template for the sql-proxy instance
    f'gcloud compute instance-templates create sql-auth-proxy-template\
        --project={project_name}\
        --machine-type=e2-medium\
        --network-interface=network={vpc_name},network-tier=PREMIUM,stack-type=IPV4_ONLY,subnet=silly-iowa\
        --maintenance-policy=MIGRATE\
        --provisioning-model=STANDARD\
        --service-account=168277104165-compute@developer.gserviceaccount.com\
        --scopes=https://www.googleapis.com/auth/devstorage.read_only,https://www.googleapis.com/auth/logging.write,https://www.googleapis.com/auth/monitoring.write,https://www.googleapis.com/auth/service.management.readonly,https://www.googleapis.com/auth/servicecontrol,https://www.googleapis.com/auth/trace.append --region=us-central1 --tags=http-server,https-server,lb-health-check --create-disk=auto-delete=yes,boot=yes,device-name=sql-auth-proxy-instance,image=projects/rhel-cloud/global/images/rhel-8-v20240815,mode=rw,size=20,type=pd-balanced\
        --no-shielded-secure-boot\
        --shielded-vtpm\
        --shielded-integrity-monitoring\
        --reservation-affinity=any',
    # Create the instance for sql-proxy 
    f'gcloud compute instances create sql-auth-proxy\
        --source-instance-template=sql-auth-proxy-template\
        --project={project_name}\
        --zone=us-central1-a\
        --tags=sshable\
        --no-address\
        --network={vpc_name}\
        --subnet=silly-iowa',
    # Firewall rule to allow SSH and TCP 80 traffic to the sql-proxy-client instance
    f'gcloud compute firewall-rules create open-ssh\
        --network={vpc_name}\
        --allow=tcp:22,tcp:80\
        --source-ranges=0.0.0.0/0\
        --target-tags=sshable\
        --priority=990\
        --project={project_name}',
    # Create an instance for cloud router 
    f'gcloud compute routers create nat-router-us-central1\
        --network default\
        --region us-central1\
        --network={vpc_name}',
    # Create Cloud router NATS 
    f'gcloud compute routers nats create nat-config\
        --router-region=us-central1\
        --router=nat-router-us-central1\
        --nat-all-subnet-ip-ranges\
        --auto-allocate-nat-external-ips',
    # Generate a Service key for the sql-proxy cline to authenticate to the cloud-sql
    f'gcloud iam service-accounts keys create ~/sillygully/sql_key\
        --iam-account={sql_proxy_service_account}@sillygully.iam.gserviceaccount.com',
    # Copy the script files to the sql-proxy instance
    f'gcloud compute scp --recurse ~/sillygully/*\
        sql-auth-proxy:/tmp\
        --zone=us-central1-a\
        --project={project_name}',
    # Run the sql-proxy startup script on the instance 
    f'gcloud compute ssh sql-auth-proxy\
        --zone=us-central1-a\
        --project={project_name}\
        --command="sh /tmp/sql-proxy-startup.sh"',
]


for cmd in sql_proxy_commands:
    try:
        print('Running the command: '+ str(cmd))
        result = subprocess.run(cmd, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        print ("\033[32mSuccessfully ran the command:\033[0m" +cmd.split('--')[0].strip() + '  ...........................\n')
        print(result.stdout.decode('utf-8')+' \n')
    except subprocess.CalledProcessError as e:
        #Error handling
        print("\033[31mCommand Failed:\033[0m" + cmd +'\n')
        error_string = e.stderr.decode('utf-8')
        err = '\'\'\'' + error_string + '\'\'\''
        if check_already_exists(error_string) == True:
            print (cmd.split('--')[0].strip() + '\033[33m....service already exists, Skipping to the bext command in the loop\033[0m'+ '\n\n\n')
            continue
        else:
            print (err+'\n\n')
            print ('Please enter "YES" if you want to skip to the next step.\n\n' + 'Type "exit" to quit the program')
            user_input = input()
            while 1:
                if user_input == 'YES':
                    print ('Great! Skipping to the next step..........')
                    break
                elif user_input.lower() == 'exit':
                    print('Ok, Exiting the program...\n\n')
                    sys.exit()
                else:
                    print ('Invalid input \n Please enter "YES" to continue and "exit" to quit nthe program:\n\n ')
                    user_input = input()
            continue
    except Exception as e:
        #Unexpected errors
        print("An unexpected error occurred:" + str(e))
        break