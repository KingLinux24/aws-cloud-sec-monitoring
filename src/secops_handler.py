import os
import logging
import boto3

logger = logging.getLogger()
logger.setLevel(logging.INFO)
cognito = boto3.client('cognito-idp')

def lambda_handler(event, context):
    """
    Automated SecOps remediation handler.
    Triggered on security alarms to revoke active token sessions globally.
    """
    logger.warning(f"SECURITY_ALERT_TRIGGERED: {event}")
    
    user_pool_id = os.environ.get('USER_POOL_ID')
    username = event.get('detail', {}).get('userIdentity', {}).get('userName')

    if username and user_pool_id:
        try:
            cognito.admin_user_global_sign_out(
                UserPoolId=user_pool_id,
                Username=username
            )
            logger.info(f"REMEDIATION_EXECUTED: Global session revoked for target user {username}")
        except Exception as e:
            logger.error(f"Failed session revocation: {str(e)}")

    return {
        "statusCode": 200,
        "body": "Automated security remediation completed."
    }