## Quick Deploy
1. Create default roles:
```
aws emr create-default-roles
```
2. Deploy template:

__Basic Template__
```
aws cloudformation create-stack --stack-name emr --template-body file://./emr-basic-template.yml
```
__Complex Template__
```
aws cloudformation create-stack --stack-name emr-testing \
--template-body file://./emr-complex-template.yml --parameters \
ParameterKey=keyPair,ParameterValue=gen_key_pair \
ParameterKey=subnetID,ParameterValue=subnet-6d482025 \
ParameterKey=clusterName,ParameterValue=emr-testing \
ParameterKey=taskInstanceCount,ParameterValue=0 \
ParameterKey=coreInstanceType,ParameterValue=m1.medium \
ParameterKey=taskInstanceType,ParameterValue=m1.medium \
ParameterKey=emrVersion,ParameterValue=emr-5.3.0 \
ParameterKey=environmentType,ParameterValue=test \
ParameterKey=masterInstanceType,ParameterValue=m1.medium \
ParameterKey=s3BucketBasePath,ParameterValue=emr-test-logs-mm \
ParameterKey=terminationProtected,ParameterValue=false \
ParameterKey=taskBidPrice,ParameterValue=0 --region us-east-1
```
3. Wait for ResourceStatus = COMPLETE
```
while true; do aws cloudformation describe-stack-events --stack-name emr | grep ResourceStatus; sleep 2; done
```

## Update
```
aws cloudformation update-stack --stack-name emr-testing \
--use-previous-template --parameters \
ParameterKey=keyPair,UsePreviousValue=true \
ParameterKey=subnetID,UsePreviousValue=true \
ParameterKey=clusterName,UsePreviousValue=true \
ParameterKey=taskInstanceCount,UsePreviousValue=true \
ParameterKey=coreInstanceType,UsePreviousValue=true \
ParameterKey=taskInstanceType,UsePreviousValue=true \
ParameterKey=emrVersion,UsePreviousValue=true \
ParameterKey=environmentType,UsePreviousValue=true \
ParameterKey=masterInstanceType,UsePreviousValue=true \
ParameterKey=s3BucketBasePath,ParameterValue=emr-test-logs-mm \
ParameterKey=terminationProtected,UsePreviousValue=true \
ParameterKey=taskBidPrice,UsePreviousValue=true --region us-east-1
```
## TearDown
```
aws cloudformation delete-stack --stack-name emr
```

## Submitting a step
1. Configure a VPC Endpoint for Amazon S3. See the following blog post for instructions on how to do this if unsure:
https://aws.amazon.com/blogs/aws/new-vpc-endpoint-for-amazon-s3/
2. Create log,source, and destination buckets:
```
aws s3api create-bucket --bucket emr-test-logs-<initials> --region us-east-1
aws s3api create-bucket --bucket emr-test-source-<initials> --region us-east-1
aws s3api create-bucket --bucket emr-test-dest-<initials> --region us-east-1
```
3. Upload the 'spark-test-cluster.py' and 'test-data.txt' files to the source bucket.
4. Submit the step to the cluster:
```
aws emr list-clusters | grep -i waiting -A 7
aws emr add-steps --cluster-id j-xxxxxxxx --steps Type=spark,Name=SparkWordCountApp,Args=[--deploy-mode,cluster,--master,yarn,--conf,spark.yarn.submit.waitAppCompletion=false,--num-executors,2,--executor-cores,1,--executor-memory,512m,s3a://<source-bucket>/spark-test-cluster.py,s3a://<source-bucket>/test-data.txt,s3a://<dest-bucket>/],ActionOnFailure=CONTINUE
```
Adjust the num-executors, executor-cores, and executor-memory as if optimal for your cluster/job.

### Configuring Zeppelin
1. Set up an ssh tunnel to Zeppelin's service port:
```
ssh -i gen-keypair.pem -L 8890:localhost:8890 hadoop@ec2-[redacted].compute-1.amazonaws.com -N
```

## References

- https://cloudacademy.com/blog/big-data-amazon-emr-apache-spark-and-apache-zeppelin-part-one-of-two/
- https://github.com/awslabs/aws-big-data-blog/tree/master/aws-blog-zeppelin-yarn-on-ec2
- http://www.mikemorse.tech/2016/09/a-well-populated-aws-cloudformation.html
- https://aws.amazon.com/blogs/big-data/submitting-user-applications-with-spark-submit/