# AWS Gitlab Runner on EC2 with Docker Machine

## Introduction:

Gitlab Ci is gaining traction both the Hosted and Cloud-Hosted version because it is tackling one of the "DevOps" challenges, nr of tools used across the different Software Development teams by offering a single solution with many tools such as SCM; CI/CD or GitOps; ticketing; analytics; security etc. (we are not endorsing Gitlab tools).

We found an opportunity to give back by creating this repo and its content,  when we had several deployments into our clients, we found practical implementation instructions on AWS lacking a bit (things will change, I'm sure).

## What will I find in this repo?

* A Terraform stack for 0.14+ AWS Ec2 GitLab runner using (coming soon) [docker-machine](https://docs.docker.com/machine/drivers/aws/)
* Cloudformation deployment for AWS Ec2 GitLab runner using [docker-machine](https://docs.docker.com/machine/drivers/aws/)
* The Helm chart for GitLab runner (coming soon)
* Documentation with all steps.

## The thinking behind it

This solution is based on the following principles.

1) The solution must be immutable as much as possible.
2) The solution is ready to be deployed providing a minimum number of values/parameters you must supply.
3) You can change the configuration without changing the code with values/parameters.
4) Both the GitLab runner (management server) and the GitLab executor (where jobs are executed) will run on private subnets with internet access (required) and can only communicate with each other through security group rules.
5) This setup requires two manual steps a) Creating the runner token with GitLab registration token b) Store the GitLab token in the SSM secure parameter created by the stack.
6) The stack should be platform-agnostic so that you can use this runner for the hosted or your self-hosted versions of GitLab as long it runs on AWS, for a cloud-agnostic solution, you are better off using the runner helm chart for Kubernetes.
7) The GitLab runner is on an ASG and can be rebuilt by deleting both the runner and the executor instances. Executor instances are created and managed by the runner, if you delete the runner also delete the executor instances, they will be re-created again.
8) For secrets, we minimised the locations secrets are stored and use SSM secure parameter store.


More detailed information will be available in the corresponding folders `README.md`

Enjoy!

[Boldlink-SIG, Ltd 2021](https://boldlink.io)
