from prefect import flow

from prefect_sns.tasks import goodbye_prefect_sns, hello_prefect_sns


def test_hello_prefect_sns():
    @flow
    def test_flow():
        return hello_prefect_sns()

    result = test_flow()
    assert result == "Hello, prefect-sns!"


def goodbye_hello_prefect_sns():
    @flow
    def test_flow():
        return goodbye_prefect_sns()

    result = test_flow()
    assert result == "Goodbye, prefect-sns!"
