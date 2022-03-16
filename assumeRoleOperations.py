import boto3

# Assume role method
def assume_role(AccountId, roleName):
  sts_client = boto3.client('sts')
  role_arn = 'arn:aws:iam::' + AccountId + ':role/' + roleName
  # print("Assuming role to switch to account", AccountId)    
  assumedRoleObject = sts_client.assume_role(
      RoleArn=role_arn,
      RoleSessionName="AssumeRoleSession"
  )
  # From the response that contains the assumed role, get the temporary credentials that can be used to make subsequent API calls
  return assumedRoleObject['Credentials']