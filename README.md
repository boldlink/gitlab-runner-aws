# AWS Gitlab Runner on EC2 with Docker Machine

## Introduction:

Gitlab Ci is gaining traction both the Hosted and Cloud-Hosted version because
it is tackling one of the "DevOps" challenges, nr of tools used across the different
Software Development teams by offering a single solution with many tools such as scm; CI/CD or GitOps;
ticketing; analytics; security etc (we are not endorsing Gitlab tools).

Having said that we found that there was an opportunity to give back by creating this repo and it's 
content because at the time of we had several deployments into our clients we found practical implementation
instructions on aws lacking a bit (things will change I'm sure).

## What will I find in this repo?

* An Terraform stack for 0.13+ AWS Ec2 gitlab runner using [docker-machine](https://docs.docker.com/machine/drivers/aws/)
* Cloudformation deployment for AWS Ec2 gitlab runner (comming soon) using [docker-machine](https://docs.docker.com/machine/drivers/aws/)
* The Helm chart for gitlab runner (comming soon)
* Documentation we use to deploy it

## The thinking behind it

This solution is based on the following principles.

1) The solution must be immutable as much as possible.

2) The solution is ready to be deploy'ed providing a minimum number of values/parameters you must supply.

3) You can change the configuration without changing the code with values/parameters.

4) Both the gitlab runner (management server) and the gitlab executor (where jobs are excuted) 
will run on private subnets with internet access (required) and can only commincate between 
each other through security group rules.

5) This setup requires two manual steps a) Creating the runner token with gitlab registration token b) Store the gitlab
token in the ssm secure parameter created by the stack.

6) Stack should be platform agnostic so you can use this runner for the hosted or your self-hosted versions of gitlab as long it runs on AWS, for a cloud agnostic solution you are better off using the runner helm chart for kubernetes.

7) The gitlab runner is on a ASG and can be rebuilt by deleting both the runner and the executor instances, executor instances
are created and managed by the runner, if you delete the runner also delete the executor instances, they will be re-created again.

8) For secrets minimise the locations secrets are stored and always encrypt secrets, we are SSM parameter store with secure string.


More detailed information will be available in the corresponding folders `README.md`

Enjoy!

[Boldlink-SIG, Ltd 2021](https://boldlink.io)
