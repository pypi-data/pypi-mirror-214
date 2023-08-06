"""This is an example flows module"""
from prefect import flow

from prefect_sns.blocks import SnsBlock
from prefect_sns.tasks import goodbye_prefect_sns, hello_prefect_sns


@flow
def hello_and_goodbye():
    """
    Sample flow that says hello and goodbye!
    """
    SnsBlock.seed_value_for_example()
    block = SnsBlock.load("sample-block")

    print(hello_prefect_sns())
    print(f"The block's value: {block.sns_arn}")
    print(goodbye_prefect_sns())
    return "Done"


if __name__ == "__main__":
    hello_and_goodbye()
