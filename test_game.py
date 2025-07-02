from chdb import session as chs
import pytest


sess = chs.Session("wimbledon.chdb")

sess.query("""
CREATE OR REPLACE FUNCTION pointsToWinGame AS (p1Score, p2Score) -> 
    multiIf(
        p1Score = '40' AND p2Score = 'AD', 3,
        p1Score = '40' AND p2Score = '40', 2,
        p1Score = '40' AND (p2Score = '0' OR p2Score = '15' OR p2Score = '30'), 1,
        p1Score = '30' AND (p2Score = '0' OR p2Score = '15' OR p2Score = '30'), 2,
        p1Score = '30' AND p2Score = '40', 3,
        p1Score = '15' AND (p2Score = '0' OR p2Score = '15' OR p2Score = '30'), 3,
        p1Score = '15' AND p2Score = '40', 4,
        p1Score = '0' AND (p2Score = '0' OR p2Score = '15' OR p2Score = '30'), 4,
        p1Score = '0' AND p2Score = '40', 5,
        p1Score = 'AD', 1,
        0
    );
""")

sess.query("""
CREATE OR REPLACE FUNCTION pointsToWinTiebreak AS (p1Score, p2Score) -> 
    if(
        p2Score <= 5, (7 - p1Score),
        (p2Score + 2) - p1Score
    );
""")

sess.query("""
CREATE OR REPLACE FUNCTION pointsToWinMatchTiebreak AS (p1Score, p2Score) -> 
    if(
        p2Score <= 8, (10 - p1Score),
        (p2Score + 2) - p1Score
    );
""")

@pytest.mark.parametrize("p1,p2,expected", [
  ("'0'", "'40'", 5),
  ("'0'", "'0'", 4),
  ("'0'", "'15'", 4),
  ("'0'", "'30'", 4),
  ("'15'", "'40'", 4),
  ("'15'", "'15'", 3),  
  ("'15'", "'30'", 3),
  ("'30'", "'40'", 3),
  ("'40'", "'AD'", 3),
  ("'30'", "'30'", 2),
  ("'40'", "'40'", 2),
  ("'40'", "'30'", 1),
  ("'40'", "'15'", 1),
  ("'40'", "'0'", 1),
  ("'AD'", "'40'", 1),
  
])
def test_points_to_win_normal_game(p1, p2, expected):
    result = sess.query(f"""
    SELECT pointsToWinGame({p1}, {p2}) as points
    """, "DataFrame")

    assert result["points"].values[0] == expected


@pytest.mark.parametrize("p1,p2,expected", [
  (0, 0, 7),
  (0, 6, 8),
  (6, 0, 1),
  (12, 12, 2),
])
def test_points_to_win_tiebreak(p1, p2, expected):
    result = sess.query(f"""
    SELECT pointsToWinTiebreak({p1}, {p2}) as points
    """, "DataFrame")

    assert result["points"].values[0] == expected


@pytest.mark.parametrize("p1,p2,expected", [
  (0, 0, 10),
  (0, 9, 11),
  (9, 0, 1),
  (13, 13, 2),
])
def test_points_to_win_match_tiebreak(p1, p2, expected):
    result = sess.query(f"""
    SELECT pointsToWinMatchTiebreak({p1}, {p2}) as points
    """, "DataFrame")

    assert result["points"].values[0] == expected