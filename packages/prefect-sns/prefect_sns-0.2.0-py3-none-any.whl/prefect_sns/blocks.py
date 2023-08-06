"""This is an example blocks module"""

from typing import Optional

import boto3
from prefect.blocks.core import Block


class SnsBlock(Block):
    """
    A block that facilitates interaction with AWS SNS.

    Attributes:
        value (str): The value to store.

    Example:
        Load a stored value:
        ```python
        from prefect_sns import SnsBlock
        block = SnsBlock.load("BLOCK_NAME")
        block.publish("my subject", "my message")
        ```
    """

    _block_type_name = "sns"
    # replace this with a relevant logo; defaults to Prefect logo
    _logo_url = "https://raw.githubusercontent.com/danielhstahl/prefect-sns/main/docs/img/aws-sns-simple-notification-service.svg"  # noqa
    _documentation_url = (
        "https://danielhstahl.github.io/prefect-sns/blocks_catalog/"  # noqa
    )

    sns_arn: str
    aws_region: str = "us-east-1"
    aws_access_key_id: Optional[str] = None
    aws_secret_access_key: Optional[str] = None

    @classmethod
    def publish(self, subject: str, message: str):
        """
        Publishes message to SNS topic
        """
        sns_client = boto3.client(
            "sns",
            region_name=self.aws_region,
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
        )
        sns_client.publish(
            TopicArn=self.sns_arn,
            Message=message,
            Subject=subject,
        )

    @classmethod
    def seed_value_for_example(cls):
        """
        Seeds the field, value, so the block can be loaded.
        """
        block = cls(sns_arn="A sample value")
        block.save("sample-block", overwrite=True)
