import boto3

def enable_log_streaming(environment_name, retention_days=7):
    """
    Enable log streaming and set the retention period for an Elastic Beanstalk environment.

    Args:
        environment_name (str): Name of the Elastic Beanstalk environment.
        retention_days (int): Number of days to retain logs in CloudWatch.
    """
    
    client = boto3.client('elasticbeanstalk')

    try:
        response = client.update_environment(
            EnvironmentName=environment_name,
            OptionSettings=[
                {
                    'Namespace': 'aws:elasticbeanstalk:cloudwatch:logs',
                    'OptionName': 'StreamLogs',
                    'Value': 'true'
                },
                {
                    'Namespace': 'aws:elasticbeanstalk:cloudwatch:logs',
                    'OptionName': 'RetentionInDays',
                    'Value': str(retention_days)
                }
            ]
        )
        print("Log streaming enabled successfully.")
        return response

    except Exception as e:
        print("Error enabling log streaming:")
        raise e


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Enable log streaming for an Elastic Beanstalk environment.")
    parser.add_argument("environment_name", help="Name of the Elastic Beanstalk environment")
    parser.add_argument("--retention_days", type=int, default=7, help="Retention period in days (default: 7)")
    args = parser.parse_args()

    enable_log_streaming(args.environment_name, args.retention_days)
