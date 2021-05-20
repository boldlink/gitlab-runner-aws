
## Cloudformation Template

You will find the `template.yaml` and a `mappings.json` file for the required parameters without default values on the same dir, see bellow an example, use it to supply your VPC and ECR values.
### The mappings file

```
[
    {
      "ParameterKey": "GitlabSsmToken",
      "ParameterValue": "xxx..."
    }, 
    {
      "ParameterKey": "VpcId",
      "ParameterValue": "vpc-xxx..."
    }, 
    {
      "ParameterKey": "ManageSubnetId",
      "ParameterValue": "subnet-xxx...,subnet-xxx...,subnet-xxx..."
    }, 
    {
      "ParameterKey": "EcrAccountId",
      "ParameterValue": ""
    }, 
    {
      "ParameterKey": "EcrRegion",
      "ParameterValue": ""
    }
]
```
### Deploy the stack

Windows Powershell:
```
aws cloudformation update-stack `
--stack-name gitlab-01 `
--template-body file://template.yaml `
--parameters file://mappings.json `
--capabilities CAPABILITY_IAM
```

Linux shell:
```
aws cloudformation update-stack \
--stack-name gitlab-01 \
--template-body file://template.yaml \
--parameters file://mappings.json \
--capabilities CAPABILITY_IAM
```
#### Resources

| Parameter | Description                |
| :-------- | :------------------------- |
| `LogGroup` | Gitlab Management instance Cloudwatch Log Group |
| `KmsLogGroup` | Gitlab Management instance KMS Key for Cloudatch Loggroup |
| `SecurityGroup` | Gitlab Management instance Security Group |
| `SecurityGroupExecutor` | Gitlab Executors Instance Security Group |
| `S3Bucket` | Gitlab S3 Cache Bucket |
| `S3BucketPolicy` | Gitlab S3 Cache Bucket Policy |
| `InstanceProfileManage` | Gitlab Management Ec2 IAM Instance Profile |
| `IamPolicyManage` | Gitlab Management IAM Role Policy |
| `IamRoleManage` | Gitlab Management instance Ec2 IAM Role |
| `InstanceProfileExecutor` | Gitlab Executor Ec2 IAM Instance Profile |
| `IamRoleExecutor` | Gitlab Executor instance Ec2 IAM Role |
| `LaunchTemplateManage` | Gitlab Management Ec2 Launch Template IAM Role |
| `Asg` | Gitlab Management instance Ec2 Autoscaling Group |

#### Parameters

| Parameter | Type     | Default Value     | Description                       |
| :-------- | :------- | :---------------- | :-------------------------------- |
| `InstanceTypeManage` | `String` | `t3.micro` | **Required**. Gitlab Manage instance type |
| `InstanceTypeExecutor` | `String` | `t3a.small` | **Required**. Gitlab Executor instance type |
| `AmiId` | `AWS::SSM::Parameter::Value<AWS::EC2::Image::Id>` | `/aws/service/ami-amazon-linux-latest/amzn2-ami-hvm-x86_64-gp2` | **Required**. Gitlab Manage instance AMI |
| `RunnerTags` | `String` | `ec2` | **Required**. Gitlab Executor tags - relevant for the gitlab jobs |
| `ManageSubnetId` | `List<AWS::EC2::Subnet::Id>` | `n/a` | **Required**. Gitlab Manage subnets, select at least 3x, and when possible use Private Subnets |
| `GitlabUrl` | `String` | `https://gitlab.com/` | **Required**. Gitlab https url which the manage instance will communicate with (api) |
| `GitlabSsmToken` | `String` | `n/a` | **Required**. Gitlab Manage instance type |
| `TimeZone` | `String` | `GMT` | **Required**. The Timezone to use for the scale up and down of your executors schedule |
| `VpcId` | `AWS::EC2::VPC::Id` | `n/a` | **Required**. VPC Id where you are deploying your platform |
| `CloudwatchRetention` | `String` | `365` | **Required**. Gitlab Management instance Cloudwatch LogGroup retention |
| `DockerTlsCertDir` | `String` | `n/a` | **Optional**. Docker Machine TLS certificate dir, by default not necessary |
| `DockerPrivileged` | `String` | `"false"` | **Required**. Docker container priveliege, we recommend leaving at is for better security |
| `DockerDisableEntrypointOverride` | `String` | `"false"` | **Required**. Docker entrypoint override, preventing to override  |
| `DockerOomKillDisable` | `String` | `false` | **Required**. Kill container if runs out of memory |
| `MachineIdleCount` | `String` | `1` | **Required**. Gitlab Executor Nr of instance count on idle mode |
| `MachineMaxBuilds` | `String` | `10` | **Required**. Gitlab Executor maximum nr of concurrnet jobs executing, each job runs in it's one Ec2 instance |
| `AutoScalingWeekdaysIdleCount` | `String` | `5` | **Required**. Gitlab Executor nr of idle Ec2 instaces during week days |
| `AutoScalingWeekendIdleCount` | `String` | `1` | **Required**. Gitlab Executor nr of idle Ec2 instances during weekends |
| `MachineOptionsPrivate` | `String` | `true` | **Required**. Your Gitlab Executor should run on Private Subnets thus byy default it is set to true, if you deploy on public subnets set this to false  |
| `ExecutorMaxConcurrency` | `String` | `10` | **Required**. Gitlab Executor maximu, concurrency |
| `MachineOptionsUseSpot` | `String` | `false` | **Required**. Gitlab Executor enable spot instances, this is not recommended |
| `MachineOptionsMaxSpotPrice` | `String` | `1.0` | **Required**. Gitlab Executor spot instances minimum price |
| `EcrAccountId` | `String` | `n/a` | **Optional**. Assuming you are using ECR, the AWS account id to configure ecr authentication |
| `EcrRegion` | `String` | `n/a` | **Optional**. Assuming you are using ECR, the AWS region to configur ecr authentication |
| `Environment` | `String` | `Dev` | **Optional**. The environment where you are deploying your runner |
| `KeySpec` | `String` | `SYMMETRIC_DEFAULT` | **Reguired**. LogGroup KMS key key specification |
| `KeyUsage` | `String` | `ENCRYPT_DECRYPT` | **Required**. LogGroup KMS key usage |
| `PendingWindowInDays` | `Number` | `30` | **required**. LogGroup KMS key pending deletion days |

## Security Scanning

We used Bridgecrew [checkov](https://www.checkov.io/) and Stelligent [cnf_nag](https://github.com/stelligent/cfn_nag) bellow we want to discuss the exceptions we accept and make you aware of them in case you decide to fork this repo.

### Checkov exceptions:
CKV_AWS_18: "Ensure the S3 bucket has access logging enabled"
* The bucket we are creating is only for temporary (cache) content, we decided to leave this for potential future development or for you to integrate with your own S3 Logging infrastructure.

CKV_AWS_21: "Ensure the S3 bucket has versioning enabled"
* Again, the s3 bucket is only for cache we don't want to version it's content.

CKV_AWS_79: "Ensure Instance Metadata Service Version 1 is not enabled"
* Although [IMDSv2](https://aws.amazon.com/blogs/security/defense-in-depth-open-firewalls-reverse-proxies-ssrf-vulnerabilities-ec2-instance-metadata-service/) is highly desirable our tests with `docker-machine 0.16.2` showed us this isn't possible.

CKV_AWS_108: "Ensure IAM policies does not allow data exfiltration"
* We require data exfiltration from different services.

CKV_AWS_109: "Ensure IAM policies does not allow permissions management without constraints"
* We have taken care to assign the necessary permissions and conditions.

CKV_AWS_110: "Ensure IAM policies does not allow privilege escalation"
* This is required and we minimized it to the strict necessary.

CKV_AWS_111: "Ensure IAM policies does not allow write access without constraints"
* Ibid

### cnf_nag exceptions:

| WARN W12 |
| :-------- |
| Resources: ["IamPolicyManage"] |
| Line Numbers: [320] |
| IAM policy should not allow * resource |
| `Comment: This is required and it is minimized with conditions where is possible` |

| WARN W11 |
| :-------- |
| Resources: ["IamRoleExecutor"] |
| Line Numbers: [487] |
| IAM role should not allow * resource on its permissions policy |
| `Comment: This is required and it is minimized with conditions where is possible` |

| WARN W35 |
| :-------- |
| Resources: ["S3Bucket"] |
| Line Numbers: [258] |
| S3 Bucket should have access logging configured |
| `Comment: The bucket we are creating is only for temporary (cache) content, we decided to leave this for potential future development or for you to integrate with your own S3 Logging infrastructure.` |

| WARN W76 |
| :-------- |
| Resources: ["IamPolicyManage"] |
| Line Numbers: [320] |
| SPCM for IAM policy document is higher than 25 |
| `Comment: Safe to ignore` |

| WARN W40 |
| :-------- |
| Resources: ["SecurityGroup", "SecurityGroupExecutor"] |
| Line Numbers: [223, 234] |
| Security Groups egress with an IpProtocol of -1 found |
| `Comment: Required` |

| WARN W5 |
| :-------- |
| Resources: ["SecurityGroup", "SecurityGroupExecutor"] |
| Line Numbers: [223, 234] |
| Security Groups found with cidr open to world on egress |
| `Comment: Required` |