import time

from logic.connections import Connection


class CloudFormation:
    """
    AWS CloudFormation allows  to provision and manage an AWS infrastructure as it was code, easily creating and
    updating components.

    For this example, an sample recipe provider by Amazon will be used, which creates an S3 bucket with web capabilities:
    https://s3-us-west-2.amazonaws.com/cloudformation-templates-us-west-2/S3_Website_Bucket_With_Retain_On_Delete.template
    """

    def __init__(self):
        """
        Store the connection and init the web bucket template
        :param conn: CloudFormation (boto) connection
        """
        self.conn = Connection().cloudformation_connection()
        self.web_bucket_template = '{"AWSTemplateFormatVersion":"2010-09-09","Description":"AWS CloudFormation Sample Template S3_Website_Bucket_With_Retain_On_Delete: Sample template showing how to create a publicly accessible S3 bucket configured for website access with a deletion policy of retail on delete. **WARNING** This template creates an S3 bucket that will NOT be deleted when the stack is deleted. You will be billed for the AWS resources used if you create a stack from this template.","Resources":{"S3Bucket":{"Type":"AWS::S3::Bucket","Properties":{"AccessControl":"PublicRead","WebsiteConfiguration":{"IndexDocument":"index.html","ErrorDocument":"error.html"}},"DeletionPolicy":"Retain"}},"Outputs":{"WebsiteURL":{"Value":{"Fn::GetAtt":["S3Bucket","WebsiteURL"]},"Description":"URL for website hosted on S3"},"S3BucketSecureURL":{"Value":{"Fn::Join":["",["https://",{"Fn::GetAtt":["S3Bucket","DomainName"]}]]},"Description":"Name of S3 bucket to hold website content"}}}'

    def generate_web_bucket(self):
        """
        Generate a web bucker
        """

        # Generate an unique name
        name = 'webbucket' + str(time.time()).replace('.', '')

        # Create the cloud formation stack with the name and the template
        self.conn.create_stack(name, template_body=self.web_bucket_template)
        print '- The stack %s is being created' % name

        # Wait until the stack has been created
        while True:
            created = False
            for stack in self.conn.list_stacks():
                if stack.stack_name == name:
                    if stack.stack_status == 'CREATE_COMPLETE':
                        created = True
                    break
            if created:
                break
            else:
                time.sleep(0.5)

        # Delete the created stack (the created bucket will not be deleted)
        print '- Stack created, removing...'
        self.conn.delete_stack(name)
