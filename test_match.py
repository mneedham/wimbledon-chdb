from chdb import session as chs
import pytest
from collections import defaultdict


sess = chs.Session("wimbledon.chdb")

sess.query("""
CREATE OR REPLACE FUNCTION pointsToWinMatch AS (MatchWinner, GameWinner, SetWinner, whoAmI, mySetScore, theirSetScore, myGameScore, theirGameScore, myPointScore, theirPointScore) -> 
    multiIf(
    MatchWinner = whoAmI, 0,
    MatchWinner = '0',
    pointsToWinOtherSetsBO5(mySetScore::UInt32, NOT(SetWinner <> '0')) + 
    multiIf(
      SetWinner <> '0', 0, 
      mySetScore = '2' AND theirSetScore='2' AND myGameScore = '6' AND theirGameScore = '6' , 
      pointsToWinFinalSet(myGameScore::UInt32, theirGameScore::UInt32, NOT(GameWinner <> '0' OR SetWinner <> '0')),
      pointsToWinSet(myGameScore::UInt32, theirGameScore::UInt32, NOT(MatchWinner <> '0' OR SetWinner <> '0' OR GameWinner <> '0'))
    ) + 
    multiIf(
      GameWinner <> '0', 0, 
      mySetScore = '2' AND theirSetScore='2' AND myGameScore = '6' AND theirGameScore='6', 
      pointsToWinMatchTiebreak(myPointScore::UInt32, theirPointScore::UInt32), 
      myGameScore = '6' AND theirGameScore='6', pointsToWinTiebreak(myPointScore::UInt32, theirPointScore::UInt32), 
      pointsToWinGame(myPointScore, theirPointScore)
    ),
    72
    );
""")


@pytest.mark.parametrize("data, expected", [
  ({"whoAmI": "1"}, 72),
  ({"whoAmI": "1", "SetWinner": "'1'", "GameWinner": "'1'", "mySetScore": "'1'"}, 48),  
  ({"whoAmI": "1", "SetWinner": "'1'", "GameWinner": "'1'", "mySetScore": "'2'"}, 24),
  ({"whoAmI": "1", "MatchWinner": "'1'", "SetWinner": "'1'", "GameWinner": "'1'", "mySetScore": "'3'"}, 0),
  ({"whoAmI": "1", "MatchWinner": "'2'", "SetWinner": "'2'", "GameWinner": "'2'", "mySetScore": "'2'"}, 72),
  ({"whoAmI": "1", "GameWinner": "'1'", "mySetScore": "'2'", "myGameScore": "'5'", "theirGameScore": "'2'"}, 4),
  ({"whoAmI": "1", "mySetScore": "'2'", "myGameScore": "'5'", "theirGameScore": "'2'", "myPointScore": "'40'", "theirPointScore": "'15'"}, 1),
  ({"whoAmI": "1", "mySetScore": "'2'", "myGameScore": "'5'", "theirGameScore": "'2'", "myPointScore": "'40'", "theirPointScore": "'40'"}, 2),
  ({"whoAmI": "1", "GameWinner": "'1'", "mySetScore": "'2'", "theirSetScore": "'2'", "myGameScore": "'6'", "theirGameScore": "'6'"}, 10),
  ({"whoAmI": "1", "mySetScore": "'2'", "theirSetScore": "'2'", "myGameScore": "'6'", "theirGameScore": "'6'", "myPointScore": "'7'", "theirPointScore": "'4'"}, 3),
  ({"whoAmI": "1", "mySetScore": "'2'", "theirSetScore": "'2'", "myGameScore": "'6'", "theirGameScore": "'6'", "myPointScore": "'9'", "theirPointScore": "'9'"}, 2),
  ({"whoAmI": "2", "mySetScore": "'2'", "theirSetScore": "'2'", "myGameScore": "'6'", "theirGameScore": "'6'", "myPointScore": "'9'", "theirPointScore": "'9'"}, 2),
  
])
def test_points_to_win_match(data,expected):
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
    SELECT pointsToWinMatch({matchWinner}, {gameWinner}, {setWinner}, {whoAmI}, {mySetScore}, {theirSetScore}, {myGameScore}, {theirGameScore}, {myPointScore}, {theirPointScore}) as points
    """, "DataFrame")

    assert result["points"].values[0] == expected