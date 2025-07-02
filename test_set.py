from chdb import session as chs
import pytest
from tennis_functions import init_functions

sess = chs.Session("wimbledon.chdb")
init_functions(sess)


@pytest.mark.parametrize("p1,p2,assume_win_next_game,expected", [
  (0, 0, False, 24),
  (0, 0, True, 20),
  (6, 6, False, 7),
  (6, 6, True, 0),
  (5, 5, False, 8),
  (5, 5, True, 4),
  (0, 5, False, 28),
  (0, 5, True, 24),
])
def test_points_to_win_set(p1, p2, assume_win_next_game, expected):
    result = sess.query(f"""
    SELECT pointsToWinSet({p1}, {p2}, {assume_win_next_game}) as points
    """, "DataFrame")

    assert result["points"].values[0] == expected

@pytest.mark.parametrize("p1,p2,assume_win_next_game,expected", [
  (0, 0, False, 24),
  (0, 0, True, 20),
  (6, 6, False, 10),
  (6, 6, True, 0),
  (5, 5, False, 8),
  (5, 5, True, 4),
  (0, 5, False, 28),
  (0, 5, True, 24),
])
def test_points_to_win_final_set(p1, p2, assume_win_next_game, expected):
    result = sess.query(f"""
    SELECT pointsToWinFinalSet({p1}, {p2}, {assume_win_next_game}) as points
    """, "DataFrame")

    assert result["points"].values[0] == expected