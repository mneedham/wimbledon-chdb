from chdb import session as chs
import streamlit as st

import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")
st.title("Points needed to win matches at Wimbledon 2025")

sess = chs.Session("wimbledon.chdb")


with st.sidebar:
  match = sess.query("""
  select match, matches.json.players.p1.first_name || ' ' || matches.json.players.p1.last_name AS p1Name, 
        matches.json.players.p2.first_name || ' ' || matches.json.players.p2.last_name AS p2Name
  FROM matches
  """, "DataFrame")
  match['label'] = match['p1Name'] + " vs " + match['p2Name']
  label_to_match = dict(zip(match['label'], match['match']))

  selected_label = st.selectbox(
      "Which match would you like to analyze?",
      options=list(label_to_match.keys())
  )
  selected_match_id = label_to_match[selected_label]

df = sess.query(f"""
SELECT P1GamesWon || '-' || P2GamesWon AS score,
      matches.json.players.p1.first_name || ' ' || matches.json.players.p1.last_name AS p1Name, 
        matches.json.players.p2.first_name || ' ' || matches.json.players.p2.last_name AS p2Name
FROM points
JOIN matches ON matches.match = points.match
WHERE match = '{selected_match_id}' AND (SetWinner <> '0' OR MatchWinner <> '0')
""", "DataFrame")

st.header(f"{df.p1Name.iloc[0]} vs {df.p2Name.iloc[0]}")

left, right = st.columns([1,4])

with left:
  with st.spinner("Loading...", show_time=True):
    st.write("🆚 " + ", ".join(df.score.values))

    df = sess.query(f"""
    SELECT ElapsedTime, SetNo, PointNumber
    FROM points
    JOIN matches ON matches.match = points.match
    WHERE match = '{selected_match_id}'
    ORDER BY ElapsedTime DESC
    LIMIT 1
    """, "DataFrame")
    st.write(f"⏰ {df["ElapsedTime"].iloc[0]}")

with right:
  with st.spinner("Loading...", show_time=True):
    df = sess.query(f"""
    WITH
      pointsToWinMatch(
        matches.json.players.p1.atp_id IS NOT NULL, MatchWinner, GameWinner, SetWinner, '1', P1SetsWon, P2SetsWon, P1GamesWon, P2GamesWon, P1Score, P2Score
      ) AS p1PointsToWin,
      pointsToWinMatch(
        matches.json.players.p1.atp_id IS NOT NULL, MatchWinner, GameWinner, SetWinner, '2', P2SetsWon, P1SetsWon, P2GamesWon, P1GamesWon, P2Score, P1Score
      ) AS p2PointsToWin
    select matches.json.players.p1.first_name || ' ' || matches.json.players.p1.last_name AS p1Name, 
          p1PointsToWin, p2PointsToWin,
          matches.json.players.p2.first_name || ' ' || matches.json.players.p2.last_name AS p2Name,
          P1SetsWon || '-' || P2SetsWon || ' ' || P1GamesWon || '-' || P2GamesWon || ' (' || P1Score || '-' || P2Score || ')'  AS score
    FROM points
    JOIN matches ON matches.match = points.match
    WHERE match = '{selected_match_id}';
    """, "DataFrame")


    df = df.reset_index()
    df.rename(columns={'index': 'Step'}, inplace=True)

    df_long = df.melt(id_vars=['Step', 'score'], 
                      value_vars=['p1PointsToWin', 'p2PointsToWin'],
                      var_name='PlayerType', 
                      value_name='PointsToWin')

    player_name_map = {
        'p1PointsToWin': df['p1Name'].iloc[0],
        'p2PointsToWin': df['p2Name'].iloc[0]
    }
    df_long['Player'] = df_long['PlayerType'].map(player_name_map)

    fig = px.line(
        df_long,
        color_discrete_sequence=["white", "#faff69"],
        x='Step',
        y='PointsToWin',
        color='Player',
        markers=False,
        title='Points needed to win the match',
        labels={'Step': 'Point Step', 'PointsToWin': 'Points to Win'},
          hover_data={
            'score': True,
            'Step': False,
            'PointsToWin': True,
            'Player': True
        },
        template='plotly_dark'
    )

    fig.update_layout(
        yaxis=dict(autorange='reversed'),
        hovermode='x unified'
    )

    fig.update_layout(
        margin=dict(l=40, r=40, t=25, b=40)  # left, right, top, bottom
    )

    fig.update_traces(line=dict(width=2))  # thicker lines for visibility

    st.plotly_chart(fig, use_container_width=True)