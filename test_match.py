from chdb import session as chs
import pytest
from collections import defaultdict
from tennis_functions import init_functions

sess = chs.Session("wimbledon.chdb")
init_functions(sess)


@pytest.mark.parametrize("bestof5, data, expected", [
  (True, {"whoAmI": "1"}, 72),
  (True, {"whoAmI": "1", "SetWinner": "'1'", "GameWinner": "'1'", "mySetScore": "'1'"}, 48),  
  (True, {"whoAmI": "1", "SetWinner": "'1'", "GameWinner": "'1'", "mySetScore": "'2'"}, 24),
  (True, {"whoAmI": "1", "MatchWinner": "'1'", "SetWinner": "'1'", "GameWinner": "'1'", "mySetScore": "'3'"}, 0),
  (True, {"whoAmI": "1", "MatchWinner": "'2'", "SetWinner": "'2'", "GameWinner": "'2'", "mySetScore": "'2'"}, 72),
  (True, {"whoAmI": "1", "GameWinner": "'1'", "mySetScore": "'2'", "myGameScore": "'5'", "theirGameScore": "'2'"}, 4),
  (True, {"whoAmI": "1", "mySetScore": "'2'", "myGameScore": "'5'", "theirGameScore": "'2'", "myPointScore": "'40'", "theirPointScore": "'15'"}, 1),
  (True, {"whoAmI": "1", "mySetScore": "'2'", "myGameScore": "'5'", "theirGameScore": "'2'", "myPointScore": "'40'", "theirPointScore": "'40'"}, 2),
  (True, {"whoAmI": "1", "GameWinner": "'1'", "mySetScore": "'2'", "theirSetScore": "'2'", "myGameScore": "'6'", "theirGameScore": "'6'"}, 10),
  (True, {"whoAmI": "1", "mySetScore": "'2'", "theirSetScore": "'2'", "myGameScore": "'6'", "theirGameScore": "'6'", "myPointScore": "'7'", "theirPointScore": "'4'"}, 3),
  (True, {"whoAmI": "1", "mySetScore": "'2'", "theirSetScore": "'2'", "myGameScore": "'6'", "theirGameScore": "'6'", "myPointScore": "'9'", "theirPointScore": "'9'"}, 2),
  (True, {"whoAmI": "2", "mySetScore": "'2'", "theirSetScore": "'2'", "myGameScore": "'6'", "theirGameScore": "'6'", "myPointScore": "'9'", "theirPointScore": "'9'"}, 2),

  (False, {"whoAmI": "1"}, 48),
  (False, {"whoAmI": "1", "SetWinner": "'1'", "GameWinner": "'1'", "mySetScore": "'1'"}, 24),  
  (False, {"whoAmI": "1", "MatchWinner": "'1'", "SetWinner": "'1'", "GameWinner": "'1'", "mySetScore": "'3'"}, 0),
  (False, {"whoAmI": "1", "mySetScore": "'1'", "theirSetScore": "'1'", "myGameScore": "'6'", "theirGameScore": "'6'", "myPointScore": "'7'", "theirPointScore": "'4'"}, 3),
  (False, {"whoAmI": "2", "mySetScore": "'1'", "theirSetScore": "'1'", "myGameScore": "'6'", "theirGameScore": "'6'", "myPointScore": "'9'", "theirPointScore": "'9'"}, 2),
  (False, {"whoAmI": "1", "GameWinner": "'1'", "mySetScore": "'1'", "theirSetScore": "'1'", "myGameScore": "'6'", "theirGameScore": "'6'"}, 10),
  
])
def test_points_to_win_match(bestof5, data,expected):
    data = defaultdict(lambda:"'0'",data)

    matchWinner = data["MatchWinner"]
    gameWinner = data["GameWinner"]
    setWinner = data["SetWinner"]          
    whoAmI = data["whoAmI"]
    mySetScore = data["mySetScore"]
    theirSetScore = data["theirSetScore"]
    myGameScore = data["myGameScore"]
    theirGameScore = data["theirGameScore"]
    myPointScore = data["myPointScore"]
    theirPointScore = data["theirPointScore"]

    result = sess.query(f"""
    SELECT pointsToWinMatch({bestof5}, {matchWinner}, {gameWinner}, {setWinner}, {whoAmI}, {mySetScore}, {theirSetScore}, {myGameScore}, {theirGameScore}, {myPointScore}, {theirPointScore}) as points
    """, "DataFrame")

    assert result["points"].values[0] == expected