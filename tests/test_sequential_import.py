import split_settings.tools


def test_sequential_glob(scope):
    """
    This test covers sequential glob imports
    """
    split_settings.tools.include('settings/sequential.d/*', scope=scope)
    assert scope['EXAMPLE_KEY'] == ['First', 'Second', 'Third', 'Fourth']
