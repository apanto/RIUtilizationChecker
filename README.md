# RIUtilizationChecker

RIUtilizationChecker is a simple lambda function that checks if the reserved instance (RI) utilization in the deployed account is below a set threshold, in which case it posts a message to an SNS topic.

## Configuration

All configuration parameters are defined in the file `UtilizationChecker/template.yaml`.

You can set the desired thrshold by setting the value of the environment variable `UTIL_THRESHOLD`.

The schedule for running the function is defined as a cron expression in the `Events` section with the value of the variable `Schedule`. This is an expression in cron syntax (for details see [Cron Expressions](https://docs.aws.amazon.com/AmazonCloudWatch/latest/events/ScheduledEvents.html#CronExpressions)).

## Getting notifications via email

To receive notifications via email you can subscribe to the SNS topic created when you deploy the template. You can either subscribe via the AWS console or using the AWS cli using the follwing command:

`aws sns subscribe --topic-arn <The topic's ARN> --protocol email --notification-endpoint <your email address>`

The ARN for the topic created by the template will look similar to this:

`arn:aws:sns:eu-west-1:123456789101:UtilizationChecker-RILowUtilization-1AZW7NX61SW83`

## Deployment

First you need to package the SAMapplication. From the top level directory run:

`aws cloudformation package --s3-bucket <your bucket> --template-file UtilizationChecker/template.yaml --output-template-file packaged.yaml`

The you need to deploy the packaged SAM application by running from the top level directory:

`aws cloudformation deploy --template-file ./packaged.yaml --stack-name UtilizationChecker --capabilities CAPABILITY_IAM`

### Features

- Configurable RI utilization threshold

### ToDo:

- Define schedule based on environment variable