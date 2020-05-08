from unittest.mock import patch, Mock

@patch("path.to.file.pandas.read_sql")
def test_get_df(read_sql_mock: Mock):
    read_sql_mock.return_value = pd.DataFrame({"foo_id": [1, 2, 3]})
    results = get_df()
    read_sql_mock.assert_called_once()
    
    pd.testing.assert_frame_equal(results, pd.DataFrame({"bar_id": [1, 2, 3]}g
