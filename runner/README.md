# AWS Gitlab Runner Terraform stack

Gitlab is a set of feature-rich tools under one "roof" enabling you to deliver modern GitOps or CI/CD platform/solution.

It has been gaining considerable traction amongst the Developer and DevOps community because 
of the concentration of solutions (SCM; CI/CD; analytics; security; etc.), making it simpler to implement integrate and maintain under a single platform.

In this repo, we will provide an AWS solution for the Gitlab Runner, which can be implemented using both Cloudformation or Terraform.

## Concepts, Features and Design decisions.

* This repo contains deployments for AWS Cloud using Cloudformation and Terraform.

* Cloud Native design, we built a solution that exploits the advantages of the cloud computing delivery model.

* The AWS Autoscaling Group will launch 1 Gitlab instance that is entirely discardable and, by default, does not require local shell access.

* VPC is a requirement, and we recommend running it from Private subnets - although Public Subnets are possible, we don't recommend it from a security standpoint.

* A single Ec2 Gitlab Manage instance will launch many Ec2 Gitlab executor instances where your actual jobs will run.

* Every time you recreate your Gitlab Runner manage Ec2 instance, it will update the OS and download the latest GitLab-Runner binary.

* Gitlab-runner executor ec2 instance uses a predefined Ubuntu 18.04 ami which isn't updated during launch, this is by default and possible to override, but, out-of-scope for this solution, extend it if you want :).

* Autoscaling Scheduling has been set for the idle machines on 9 am-5 pm GMT weekdays and weekends, see parameters on each stack for more detail and change the TMZ and time to fit your needs.

## Known issues

* About Spot instances, when it comes to cost, using spot would reduce the overall cost further, but you can only use one instance type per implementation, and the region or AZ you are deploying to might not have that instance type available (very common to occur) and will undoubtedly cause your jobs not to run. Available options are *a)* change the instance type manually when you detect this behaviour, or *b)* change the configuration to standard instances (recommended).

* This message [level=warning msg=" Failed to update executor docker+machine ... No free machines that can process builds](https://gitlab.com/gitlab-org/gitlab-runner/-/issues/2251) is very typical and can be ignored, you will see it every time your idle machine count is > 0.

* Zombie Gitlab Executor instances, if for any reason your Gitlab Manage Ec2 instance is deleted or re-bootstrapped by the ASG, the Executor instances will remain online because Create/Delete instances are controlled by the Gitlab-Runner Ec2 Manager instance, for now, your only solution is to delete these instances.

* Deleting your stack will error. This is because Security Groups are still in use by the executors, delete your GitLab runner executor instances manually, and try again.

* Bear in mind, one of the main components of this solution is [docker-machine](https://docs.docker.com/machine/), which is on the docker superseded products list, last released version, 0.16.2 (2.9.2019) on [github.com](https://github.com/docker/machine)

## Requirements:

### Client

* Gitlab-Runner binary.

* AWS Cli, preferably v2

* AWS VPC with both Public and Private Subnets with internet access.

* Terraform Cli 0.14.x or higher.

### Server

* Gitlab-Runner Binary.

* AWS CLI v1 or above; jq and git

* Docker and Docker+Machine.

## Initialization

Before installing the Cloudformation or Terraform stack, you must create the GitLab runner token and put the token on an AWS SSM secure parameter, and this is to maintain the secret on a single place, the secure string in the AWS SSM parameter store, and, only use the reference to the secret on the ec2 instance bootstrapping user data.

### Gitlab Runner token generation

On your client machine, download the GitLab runner binary and execute the register operation.

Run the following command (change it accordingly) to register your runner:

*Windows Powershell:*
```
gitlab-runner register `
--non-interactive `
--executor "docker+machine" `
--docker-image alpine:latest `
--url "https://gitlab.com/" `
--registration-token "..." `
--description "Gitlab-02 @EnvName" `
--tag-list "docker-machine,aws,<env_name>,<insert_your_tags>"
```

*Linux shell:*
```
gitlab-runner register \
--non-interactive \
--executor "docker+machine" \
--docker-image alpine:latest \
--url "https://gitlab.com/" \
--registration-token "..." \
--description "Gitlab-runner-02 @EnvName" \
--tag-list "docker-machine,aws,<env_name>,<insert_your_tags>"
```
 You will have a file `config.toml` in the folder you ran the above command with its contents looking similar to bellow:
 ```
 concurrent = 1
check_interval = 0

[session_server]
  session_timeout = 1800

[[runners]]
  name = "Gitlab-Runner-02 @EnvName"
  url = "https://gitlab.com/"
  token = "..." <<< This is the string you want.
  executor = "docker+machine"
  ...
    OffPeakIdleTime = 0
```
Take note of the value of `token` for the below step.
### Create the AWS SSM for token

*Windows PowerShell:*
```
aws ssm put-parameter `
--name /gitlab-runner-02/token `
--value ... `
--type SecureString
```

*Linux shell:*
```
aws ssm put-parameter \
--name /gitlab-runner-02/token \
--value ... \ 
--type SecureString
```

### Launch the stack

For Cloudformation implementation go [here]()

For Terrraform implementation go [here]()

## Todo:

[BACKLOG]: Add Lambda to clean executors when runner instance is terminated or stack deleted.

