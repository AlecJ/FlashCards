"""
Tests are written with pytest.

Run from root directory with

`pynt test` to run tests

or
`coverage run -m pytest` to get a coverage report

Below is an excample using magicmock and patch
def test_create_campaign(self, mocker):
    mock_session = mocker.MagicMock()
    mock_campaign = mocker.MagicMock(return_value=True)
    mock_code = mocker.MagicMock(return_value='abcd')
    mocker.patch('rpgmanager.service._generate_unique_room_code', mock_code)
    mocker.patch('rpgmanager.service.RPGManagerCampaign', mock_campaign)
    campaign = create_campaign(mock_session)
    assert campaign

You can mock DB queries with...
def test(self, mocker):
    mock_session = mocker.MagicMock()
    mock_object = mocker.MagicMock()
    mock_object.id = 1
    mock_session.query().order_by().all.return_value = [mock_object, mock_object, mock_object]
    campaigns = get_campaigns(mock_session)
    assert len(campaigns) == 3

You can raise an error with...
def test_create_campaign_error(self, mocker):
    mock_error = mocker.MagicMock(side_effect=exc.SQLAlchemyError)
    mocker.patch('rpgmanager.service.RPGManagerCampaign', mock_error)
    campaign = create_campaign(mock_session)
    assert not campaign
"""