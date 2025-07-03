from chdb import session as chs
import streamlit as st

import plotly.express as px
import pandas as pd

st.set_page_config(layout="wide")
st.title("Points needed to win matches at Wimbledon 2025")

sess = chs.Session("wimbledon.chdb")


with st.sidebar:
  st.write("Choose a match")
  gender_filter = st.selectbox(
      "Matches to include",
      options=["Both", "Men", "Women"]
  )
  match = sess.query("""
  select match, p1Name, p2Name, event
  FROM matches
  ORDER BY event
  """, "DataFrame")
  if gender_filter != "Both":
    match = match[match["event"] == gender_filter]
    
  match['label'] = match['p1Name'] + " vs " + match['p2Name']
  label_to_match = dict(zip(match['label'], match['match']))

  selected_label = st.selectbox(
      "Select match",
      options=list(label_to_match.keys())
  )
  selected_match_id = label_to_match[selected_label]

  st.write("----")
  st.write("Powered by [chDB](https://clickhouse.com/docs/chdb) and [Streamlit](https://streamlit.io/).")

df = sess.query(f"""
SELECT P1GamesWon || '-' || P2GamesWon AS score,
      p1Name, p2Name
FROM points
JOIN matches ON matches.match = points.match
WHERE match = '{selected_match_id}' AND (SetWinner <> '0' OR MatchWinner <> '0')
""", "DataFrame")

st.header(f"{df.p1Name.iloc[0]} vs {df.p2Name.iloc[0]}")

points_df = sess.query(f"""
WITH
  pointsToWinMatch(
    matches.event = 'Men', MatchWinner, GameWinner, SetWinner, '1', P1SetsWon, P2SetsWon, P1GamesWon, P2GamesWon, P1Score, P2Score
  ) AS p1PointsToWin,
  pointsToWinMatch(
    matches.event = 'Men', MatchWinner, GameWinner, SetWinner, '2', P2SetsWon, P1SetsWon, P2GamesWon, P1GamesWon, P2Score, P1Score
  ) AS p2PointsToWin
select p1Name, p1PointsToWin, p2PointsToWin, p2Name,
      P1SetsWon || '-' || P2SetsWon || ' ' || P1GamesWon || '-' || P2GamesWon || ' (' || P1Score || '-' || P2Score || ')'  AS score
FROM points
JOIN matches ON matches.match = points.match
WHERE match = '{selected_match_id}';
""", "DataFrame")


left, right = st.columns([1,4])

with left:
  with st.spinner("Loading...", show_time=True):
    score = ", ".join(df.score.values)    

    df = sess.query(f"""
    SELECT ElapsedTime, PointNumber,
           if(
             MatchWinner = '1', 
             matches.p1Name, 
             matches.p2Name
          ) AS winner, MatchWinner
    FROM points
    JOIN matches ON matches.match = points.match
    WHERE match = '{selected_match_id}' AND MatchWinner <> '0'
    """, "DataFrame")
    winner_id = df.MatchWinner.iloc[0]
    st.write("🥇 " + df.winner.iloc[0])
    st.write("🆚 " + score )
    st.write(f"⏰ {df["ElapsedTime"].iloc[0]}")
    st.write("🎾 " + df["PointNumber"].iloc[0] + " total points")
    st.write("⚠️ " + (str(points_df.p2PointsToWin.min()) if winner_id == '1' else str(points_df.p1PointsToWin.min())) + " points from losing")

with right:
  with st.spinner("Loading...", show_time=True):
    points_df = points_df.reset_index()
    points_df.rename(columns={'index': 'Step'}, inplace=True)

    df_long = points_df.melt(id_vars=['Step', 'score'], 
                      value_vars=['p1PointsToWin', 'p2PointsToWin'],
                      var_name='PlayerType', 
                      value_name='PointsToWin')

    player_name_map = {
        'p1PointsToWin': points_df['p1Name'].iloc[0],
        'p2PointsToWin': points_df['p2Name'].iloc[0]
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


