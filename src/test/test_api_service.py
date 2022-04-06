from sqlalchemy import exc
from src.api.service import create_battle, get_shuffled_list_of_battles, get_battle_by_id

class TestAPIService:
    '''
    create_battle
    '''
    def test_create_battle(self, mocker):
        mock_session = mocker.MagicMock()
        mocker.patch('src.api.service.Battle')
        dummy_args = [''] * 10
        assert create_battle(mock_session, *dummy_args)

    def test_create_battle_sql_error(self, mocker):
        mock_session = mocker.MagicMock()
        mock_error = mocker.MagicMock(side_effect=exc.SQLAlchemyError)
        mocker.patch('src.api.service.Battle', mock_error)
        dummy_args = [''] * 10
        assert not create_battle(mock_session, *dummy_args)
    
    '''
    get_shuffled_list_of_battles
    '''
    def test_get_shuffled_list_of_battles_multiple_results(self, mocker):
        mock_session = mocker.MagicMock()
        mock_object = mocker.MagicMock()
        mock_object.id = 1
        mock_session.query().order_by().all.return_value = [mock_object, mock_object, mock_object]
        result = get_shuffled_list_of_battles(mock_session)
        assert len(result) == 3
        
    def test_get_shuffled_list_of_battles_no_results(self, mocker):
        mock_session = mocker.MagicMock()
        mock_session.query().order_by().all.return_value = []
        result = get_shuffled_list_of_battles(mock_session)
        assert len(result) == 0
    
    def test_get_shuffled_list_of_battles_sql_error(self, mocker):
        mock_session = mocker.MagicMock()
        mock_session.query().order_by().all.side_effect = exc.SQLAlchemyError
        result = get_shuffled_list_of_battles(mock_session)
        assert result is None

    '''
    get_battle_by_id
    '''
    def test_get_battle_by_id_found(self, mocker):
        mock_session = mocker.MagicMock()
        mock_object = mocker.MagicMock()
        mock_object.id = 1
        mock_session.query().filter().one_or_none.return_value = mock_object
        result = get_battle_by_id(mock_session, 1)
        assert result.id == 1
    
    def test_get_battle_by_id_not_found(self, mocker):
        mock_session = mocker.MagicMock()
        mock_session.query().filter().one_or_none.return_value = None
        result = get_battle_by_id(mock_session, 1)
        assert result is None
    
    def test_get_battle_by_id_sql_error(self, mocker):
        mock_session = mocker.MagicMock()
        mock_session.query().filter().one_or_none.side_effect = exc.SQLAlchemyError
        result = get_battle_by_id(mock_session, 1)
        assert len(result) == 0