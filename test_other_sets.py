from chdb import session as chs
import pytest


sess = chs.Session("wimbledon.chdb")

sess.query("""
CREATE OR REPLACE FUNCTION pointsToWinOtherSetsBO5 AS (setScore, assumeWinSet) -> (3 - (setScore+assumeWinSet)) * 24;
""")

sess.query("""
CREATE OR REPLACE FUNCTION pointsToWinOtherSetsBO3 AS (setScore, assumeWinSet) -> (2 - (setScore+assumeWinSet)) * 24;
""")

@pytest.mark.parametrize("set_score,assume_win_set,expected", [
  (0, False, 72),
  (0, True, 48),
  (1, False, 48),
  (1, True, 24),
  (2, False, 24),
  (2, True, 0),
])
def test_points_to_win_other_sets_best_of_5(set_score, assume_win_set, expected):
    result = sess.query(f"""
    SELECT pointsToWinOtherSetsBO5({set_score}, {assume_win_set}) as points
    """, "DataFrame")

    assert result["points"].values[0] == expected


@pytest.mark.parametrize("set_score,assume_win_set,expected", [
  (0, False, 48),
  (0, True, 24),
  (1, False, 24),
  (1, True, 0),
])
def test_points_to_win_other_sets_best_of_3(set_score, assume_win_set, expected):
    result = sess.query(f"""
    SELECT pointsToWinOtherSetsBO3({set_score}, {assume_win_set}) as points
    """, "DataFrame")

    assert result["points"].values[0] == expected
