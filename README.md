This repository contains Automation scripts of CI/CD from pushing source -> crating docker container -> pusing the container onto ECR -> Deploying container onto EKS

# Tech Stack Used:
-> Cloud                     : AWS
-> Version Control Tool      : GIT
-> Source Code Repo          : GitHub
-> Build Tool                : Jenkins
-> Container                 : Docker
-> Container Repository      : AWS ECR
-> Container Orchestration   : Aws EKS

# Configurations
-> Install and configure Jenkins master with worker nodes
-> Configure Poll SCM triggers for invoking branch specific buids
-> Install and configure Docker Deamon in Jenkins Worker Nodes
-> Provision AWS ECR to store the Docker containers
-> Provision AWS EKS cluster and configure the Node Groups
-> Create IAM Policies for Jenkins Master to be able to Push the Container to ECR and to invoke Deployment into EKS
    Note: Jenkin master-Dockerslave, AWS EKS configuration files are uploaded to "Configuration files" for reference
# instructions
-> when ever developer pushes changes to branch, since we configured webhooks with jenkins branch specific build will trigger
-> Jenkins will check the code test cases written in test.py
-> if the code check is successful Docker container is created on Jenkins worker node and the container is properly Tagged with Jenkins Build Number and Pushed onto ECR.
-> The ECR will have all the Docker container with Build tags and the latest container in the repo is tagged as "latest"
-> The latest docker container then will be deployed to EKS onto specific environments.

# kubernetes configuration
-> after provisioning, the yaml configs will be automatically creating namespaces and environments during the Pod Deployment.
-> The ingress controller with a Loadbalancer will be Deployed onto The cluster to provide Path Based routing across all the Namespaces.
-> Finally, When we hit the Loadbalancer we will be accessing the micro services.

Note:The entire Pipeline is automated from build to accessing the pods through LoadBalancer, only requirement is to push the changes to repository.





