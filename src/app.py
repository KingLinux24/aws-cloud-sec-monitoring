import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    identity_claims = event.get("requestContext", {}).get("authorizer", {}).get("claims", {})
    user_email = identity_claims.get("email", "UNKNOWN_USER")
    
    logger.info(f"AUTHORIZED_ACCESS: Request processed successfully for user={user_email}")

    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        },
        "body": json.dumps({
            "status": "SUCCESS",
            "message": "Authorized access granted to secure cloud resource.",
            "authenticated_user": user_email
        })
    }
