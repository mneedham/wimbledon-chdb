from chdb import session as chs
import streamlit as st

st.set_page_config(layout="wide")

import plotly.express as px
import pandas as pd

sess = chs.Session("wimbledon.chdb")

if "player_id" in st.query_params:
  st.session_state.player_id = st.query_params.player_id

with st.sidebar:
  st.write("Choose a player")
  players_df = sess.query("""
  select DISTINCT player
  FROM (
  SELECT p1Name AS player FROM matches
  UNION ALL
  SELECT p2Name AS player FROM matches
    )
    ORDER BY player
  """, "DataFrame")
  players = players_df['player'].tolist()

  if "player_id" not in st.session_state:
    st.session_state.player_id = players[0]

  def on_select_change():
      st.session_state.player_id = st.session_state.selected_player
      st.query_params.player_id = st.session_state.selected_player

  if st.session_state.player_id not in players:
      st.session_state.player_id = players[0]
      st.query_params.player_id = players[0]

  selected_label = st.selectbox(
      "Select player",
      options=players,
      index=players.index(st.session_state.player_id),
      key="selected_player",
      on_change=on_select_change
  )

  st.write("----")
  st.write("Powered by [chDB](https://clickhouse.com/docs/chdb) and [Streamlit](https://streamlit.io/).")

st.header(st.session_state.player_id)

matches_df = sess.query(f"""
SELECT match
FROM matches
WHERE p1Name = '{st.session_state.player_id}' OR p2Name = '{st.session_state.player_id}'
""", "DataFrame")


for match in matches_df.match.values.tolist():
  df = sess.query(f"""
  SELECT p1.gamesWon || '-' || p2.gamesWon AS score, p1Name, p2Name, roundName::String AS roundName
  FROM points
  JOIN matches ON matches.match = points.match
  WHERE match = '{match}' AND (SetWinner <> '0' OR MatchWinner <> '0')
  """, "DataFrame")


  st.write(f"""
  <p style="margin-bottom: 0;"><i>{df.roundName.iloc[0]}</i></p><h3 style="padding-top:0;">{df.p1Name.iloc[0]} vs {df.p2Name.iloc[0]}</h3>
  """, unsafe_allow_html=True)

  points_df = sess.query(f"""
  WITH
    pointsToWinMatch(
      matches.event = 'Men', MatchWinner, GameWinner, SetWinner, '1', p1.setsWon, p2.setsWon, p1.gamesWon, p2.gamesWon, p1.score, p2.score
    ) AS p1PointsToWin,
    pointsToWinMatch(
      matches.event = 'Men', MatchWinner, GameWinner, SetWinner, '2', p2.setsWon, p1.setsWon, p2.gamesWon, p1.gamesWon, p2.score, p1.score
    ) AS p2PointsToWin
  select PointNumber, p1Name, p1PointsToWin, p2PointsToWin, p2Name,
        p1.setsWon || '-' || p2.setsWon || ' ' || p1.gamesWon || '-' || p2.gamesWon || ' (' || p1.score || '-' || p2.score || ')'  AS score
  FROM points
  JOIN matches ON matches.match = points.match
  WHERE match = '{match}'
  ORDER BY PointNumber
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
      WHERE match = '{match}' AND MatchWinner <> '0'
      """, "DataFrame")
      winner_id = df.MatchWinner.iloc[0]
      st.write("🥇 " + df.winner.iloc[0])
      st.write("🆚 " + score )
      st.write(f"⏰ {str(df["ElapsedTime"].iloc[0])}")
      st.write("🎾 " + str(df["PointNumber"].iloc[0]) + " total points")
      st.write("⚠️ " + (str(points_df.p2PointsToWin.min()) if winner_id == '1' else str(points_df.p1PointsToWin.min())) + " points from losing")

      points_in_play = points_df[points_df.PointNumber >= 1]

      how_much_winning = (
        points_in_play[points_in_play.p1PointsToWin < points_in_play.p2PointsToWin].shape[0] / points_in_play.shape[0] 
        if winner_id == '1' 
        else points_in_play[points_in_play.p2PointsToWin < points_in_play.p1PointsToWin].shape[0] / points_in_play.shape[0]
      )
    
      st.write("📈 " + str(f"{how_much_winning*100:.2f}") + " % time ahead") 


  with right:
    with st.spinner("Loading...", show_time=True):
      df_long = points_df.melt(id_vars=['PointNumber', 'score'], 
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
          x='PointNumber',
          y='PointsToWin',
          color='Player',
          markers=False,
          title='Points needed to win the match',
          labels={'PointNumber': 'Point Step', 'PointsToWin': 'Points to Win'},
            hover_data={
              'score': True,
              'PointNumber': False,
              'PointsToWin': True,
              'Player': True
          },
          template='plotly_dark'
      )

      fig.update_layout(
          yaxis=dict(autorange='reversed'),
          hovermode='x unified',
          margin=dict(l=40, r=40, t=40, b=80),
          legend=dict(
              orientation="h",
              yanchor="top",
              y=-0.2,
              xanchor="center",
              x=0.5
          )
      )

      fig.update_traces(line=dict(width=2))  

      st.plotly_chart(fig, use_container_width=True)