# AWS Gitlab Runner Terraform stack

Gitlab is a set of feature rich tools under one "roof" enabling you to deliver modern GitOps or CI/CD platform/solution.

It has been gaining considerable traction amongst the Developer and DevOps community because 
of it's concentration of solutions (scm; ci/cd; analytics; security; etc) making it simpler to implement integrate and maintain under a single platform.

In this repo we are going to provide a AWS solution for the Gitlab Runner which can be implemented using both Cloudformation or Terraform.

## Concepts, Features and Design decisions.

* This repo contains deployments for AWS Cloud using Cloudformation and Terraform.

* Cloud Native design, we built a solution that exploits the advantages of the cloud computing delivery model.

* The AWS Autoscaling Group will launch 1 Gitlab instance that is completly discardable, and, by default does not require local shell access.

* VPC is a requirement and we recommend running it from Private subnets - although Public Subnets are possible we don't recommend it from a security standpoint.

* A single Ec2 Gitlab Manage instance will launch many Ec2 Gitlab executor instances where your actual jobs will run.

* Everytime you recreate your Gitlab Runner manage Ec2 instance it will update the OS and dowload the latest gitlab-runner binary.

* Gitlab-runner executor ec2 instance uses a predefiend Ubuntu 18.04 ami which isn't updated during launch, this is by default and possible to override, but, out-of-scope for this solution, extend it if you want :).

* Autoscaling Scheduling as been set for the idle machines on a 9am-5pm GMT weekdays and weekends, see parameters on each stack for more detail, and change the TMZ and time to fit your needs.

## Known issues

* About Spot instances, when it comes to cost using spot would further reduce the overall cost further, but, you can only use one instance type per implementation, and, the region or AZ you are deploying to might not have that instance type available (very common to occur) and will certainly cause your jobs not to run. Available options are *a)* change the instance type manually when you detect this behaviour, or, *b)* change the configuration to standard instances (recommended).

* This message [level=warning msg="Failed to update executor docker+machine ... No free machines that can process builds](https://gitlab.com/gitlab-org/gitlab-runner/-/issues/2251) is very normal and can be ignored, you will see it everytime your idle machine count is > 0.

* Zombie Gitlab Executor instances, if for any reason your Gitlab Manage Ec2 instance is deleted or re-bootstrapped by the ASG the Executor instances will remain online because Create/Delete instances is controlled by the Gitlab-Runner Ec2 Manager instance, for now your only solutin is to delete these instances.

* Deleting your stack will error. This is because Security Groups are still in use by the executors, delete your gitlab runner executor instances manually, and try again.

* Bear in mind, one of the main components of this solution is [docker-machine](https://docs.docker.com/machine/) which is on the docker superseeded products list, last released version, 0.16.2 (2.9.2019) on [github.com](https://github.com/docker/machine)

## Requirements:

### Client

* Gitlab-Runner binary.

* AWS Cli, preferably v2

* AWS VPC with both Public and Private Subnets with internet access.

* Terraform Cli 0.14.x or higher.

### Server

* Gitlab-Runner Binary.

* aws cliv v1 or above; jq and git

* Docker and Docker+Machine.

## Initialization

Prior to installing the Cloudformation or Terraform stack you must create the gitlab runner token and put the token on a ssm secure parameter, this is to maintain the secret on a single place, the secure string in the AWS ssm parameter store, and, only use the reference to the secret on the ec2 instance bootstraping userdata.

### Gitlab Runner token generation

On your client machine download the gitlab runner binary and execute the register operation.

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
 You will have a file `config.toml` in the folder you ran the above command with it's contents looking similar to bellow:
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
Take note of the value of `token` for the bellow step.
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

[BACKLOG]: Add Lambda to clean executors when runner isntance is terminated or stack deleted.

