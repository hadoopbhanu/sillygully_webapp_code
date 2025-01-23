# **Cloud Infrastructure Automation with GCP: VPC, Cloud SQL, Cloud Run, and CI/CD 🚀 **
 **

This project showcases **cloud infrastructure automation** using **Google Cloud Platform (GCP)** services such as **VPC networks, Cloud SQL**, and **Cloud Run**, with an emphasis on **private connectivity and security** through SQL Proxy. The project also integrates **CI/CD pipelines** using **Cloud Build**, **Artifact Registry**, and **Cloud Deploy** to automate web application deployments.

---

## **Project Overview**  
This project automates the following tasks using **Python scripts** (to be transitioned to **Terraform** in future iterations):

1. **VPC and Subnet Creation**:  
   - Set up custom **VPC networks** and **subnets** for regional cloud resources in **North America** and **Asia**.
   
2. **Cloud SQL Instance Deployment**:  
   - Create **Cloud SQL instances** with **private IP connectivity** using VPC peering and SQL Proxy for enhanced security.

3. **SQL Proxy Setup for Private Connections**:  
   - Automate the creation of a **Cloud SQL Proxy instance** and configure **firewalls and NAT routing** to manage secure access.

4. **Web Application Deployment on Cloud Run** (In progress):  
   - Build and deploy **Dockerized applications** to **Cloud Run**, integrating with **Cloud SQL** for data persistence.

5. **CI/CD Pipeline Implementation** (In-progress)):  
   - Automate the deployment workflow using **Cloud Build**, **Artifact Registry**, and **Cloud Deploy** to enable continuous delivery of the web application.

---

## **Key Technologies & Tools Used**  
- **Google Cloud Platform (GCP)**: VPC, Cloud SQL, Cloud Run, Cloud Build, Artifact Registry, Cloud Deploy  
- **Python**: Automates infrastructure creation (temporary solution; transitioning to Terraform)  
- **Terraform (planned)**: Infrastructure-as-Code to replace Python scripts  
- **Docker**: Containerize and deploy the web application on Cloud Run  
- **SQL Proxy**: Secure, private connectivity for Cloud SQL  
- **CI/CD**: Cloud Build, Artifact Registry, and Cloud Deploy for seamless application delivery

---

## **Project Structure**  
```
SILLYGULLY_WEBAPP_PROJECT/
│
├── .github/                     # CI/CD workflows for automation
│
├── Infra_python_scripts/        # Python scripts for infrastructure automation
│   ├── cloud_run_setup.py       # Sets up Cloud Run service
│   ├── cloud_sql_setup.py       # Configures and deploys Cloud SQL
│   ├── infra_setup.py           # Manages overall infrastructure setup
│   ├── sql_proxy_setup.py       # Configures SQL Proxy for private connectivity
│   └── vpc_setup.py             # Creates and configures VPC with subnets
│
├── silly-webapp/                # Web application files
│   ├── .env                     # Environment variables for web app
│   ├── app.py                   # Python web app code
│   └── Dockerfile               # Docker configuration for app container
│
├── terraform/                   # Terraform configurations for IaC
│   └── modules/                 # Modular Terraform infrastructure components
│       ├── main.tf              # Main configuration file
│       ├── outputs.tf           # Output values for infrastructure resources
│       ├── terraform.tfvars     # Terraform variable values
│       └── variables.tf         # Variable definitions for Terraform
│
├── .env                         # Project-wide environment variables
├── .gitignore                   # Rules for ignored files and directories
└── README.md                    # Project documentation
```

---

## **How to Run Locally**  
1. **Clone the Repository**:  
   ```bash
   git clone https://github.com/hadoopbhanu/sillygully_webapp_code.git
   cd GCP_sillygully_webapp_code
   ```

2. **Set Up Environment Variables**:  
   - Create a `.env` file with the required variables for your **GCP project** and **SQL credentials**.

3. **Run Python Automation Scripts**:  
   ```bash
   python3 python-scripts/vpc_creation.py
   python3 python-scripts/cloud_sql_setup.py
   ```

4. **Push Code to GitHub to Trigger CI/CD**:  
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```
--

5. **Monitor CI/CD Pipeline in GitHub Actions**.

## **Future Improvements**  
- Transition all automation scripts to **Terraform** for better scalability.  
- Add **dynamic secrets management** using Google Secret Manager.  
- Extend the application to include **Cloud Monitoring and Logging** for observability.  

---


Author
Bhanu Koduri

