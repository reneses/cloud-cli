from connections import Connection


class Sns:
    """
    Amazon Simple Notification Service

    This service provided by Amazon can be used as a message queue and notification service
    For our purposes, it will be used to send emails regarding CloudWatch alerts
    """

    # Topic name for cloudwatch alerts
    CLOUDWATCH_TOPIC = 'cloudwatch_alert'

    def __init__(self):
        """
        Init the (boto) SNS connection and prepare the cloudwatch topic
        """

        self.conn = Connection().sns_connection()

        # Create the cloudwatch topic if not exists, and store its ARN
        self.cloudwatch_arn = self._create_topic_if_not_exists(self.CLOUDWATCH_TOPIC)

        # If there are no subscriptions, subscribe the default email
        if not len(self.get_cloudwatch_email_subscriptions()):
            self.subscribe_email_to_cloudwatch(Connection().DEFAULT_ALERT_EMAIL)

    def _create_topic_if_not_exists(self, topic_name):
        """
        Create a topic if it does not exist

        :param topic_name: Topic name to create
        :return: Topic ARN
        """
        creation_result = self.conn.create_topic(topic_name)
        return creation_result['CreateTopicResponse']['CreateTopicResult']['TopicArn']

    def _get_subscriptions(self, topic_arn):
        """
        Get all the subscriptions given a topic arn
        :param topic_arn: ARN of the topic
        :return: Subscriptions of the topic
        """
        return self.conn.get_all_subscriptions_by_topic(topic_arn)['ListSubscriptionsByTopicResponse']['ListSubscriptionsByTopicResult']['Subscriptions']

    def _get_cloudwatch_subscriptions(self):
        """
        Get subscriptions of the cloudwatch topic

        :return: Subscriptions of the cloudwatch topic
        """
        return self._get_subscriptions(self.cloudwatch_arn)

    def get_cloudwatch_email_subscriptions(self):
        """
        Map the cloudwatch subscriptions to its emails

        :return: Emails subscribed to the cloudwatch topic
        """
        return map(lambda subscription: subscription['Endpoint'], self._get_cloudwatch_subscriptions())

    def subscribe_email_to_cloudwatch(self, email):
        """
        Subscribe an email to CloudWatch

        :param email: Email to subscribe
        """
        return self.conn.subscribe(self.cloudwatch_arn, 'email', email)

    def unsubscribe_all_emails_from_cloudwatch(self):
        """
        Ubsubscribe all the emails from CloudWatch
        """
        for subscription in self._get_cloudwatch_subscriptions():
            subscription_arn = subscription['SubscriptionArn']
            if not subscription_arn == 'PendingConfirmation':
                self.conn.unsubscribe(subscription_arn)

    def set_only_subscriber_to_cloudwatch(self, email):
        """
        Set an only subscribe to cloudwatch, this is, unsubscribing all the emails and registering the new one

        :param email: Email to subscribe
        :return: True if subscribed, false otherwise
        """
        # noinspection PyBroadException
        try:
            self.unsubscribe_all_emails_from_cloudwatch()
            self.subscribe_email_to_cloudwatch(email)
            return True
        except Exception:
            return False
