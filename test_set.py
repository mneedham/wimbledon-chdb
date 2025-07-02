from chdb import session as chs
import pytest


sess = chs.Session("wimbledon.chdb")

sess.query("""
CREATE OR REPLACE FUNCTION pointsToWinSet AS (p1Score, p2Score, assumeWinNextGame) -> 
    multiIf(
        p2Score = 5, (7 - (p1Score+assumeWinNextGame)) * 4,
        p1Score+assumeWinNextGame = 7 AND p2Score = 6, 0,
        p2Score = 6, ((6 - (p1Score+assumeWinNextGame)) * 4) + 7,
        p1Score+assumeWinNextGame = 7, 0,
        p1Score+assumeWinNextGame = 6 AND p2Score < 5, 0,
        (6 - (p1Score+assumeWinNextGame)) * 4
    );
""")

sess.query("""
CREATE OR REPLACE FUNCTION pointsToWinFinalSet AS (p1Score, p2Score, assumeWinNextGame) -> 
    multiIf(
        p2Score = 5, (7 - (p1Score+assumeWinNextGame)) * 4,
        p1Score+assumeWinNextGame = 7 AND p2Score = 6, 0,
        p2Score = 6, ((6 - (p1Score+assumeWinNextGame)) * 4) + 10,
        p1Score+assumeWinNextGame = 7, 0,
        p1Score+assumeWinNextGame = 6 AND p2Score < 5, 0,
        (6 - (p1Score+assumeWinNextGame)) * 4
    );
""")


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