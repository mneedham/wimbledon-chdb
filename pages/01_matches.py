from chdb import session as chs
import streamlit as st

st.set_page_config(layout="wide")

import plotly.express as px
import pandas as pd

sess = chs.Session("wimbledon.chdb")

if "match_id" in st.query_params:
  st.session_state.match_id = st.query_params.match_id

with st.sidebar:
  st.write("Choose a match")
  events = sess.query("""
  select DISTINCT eventName::String AS eventName
  FROM matches
  """, "DataFrame")

  event_filter = st.selectbox(
      "Event",
      options=["All"] + events.eventName.values.tolist()
  )

  rounds = sess.query("""
  select DISTINCT roundName::String AS roundName
  FROM matches
  """, "DataFrame")

  round_filter = st.selectbox(
      "Round",
      options=["All"] + rounds.roundName.values.tolist()
  )
  match = sess.query("""
  select match, p1Name, p2Name, eventName::String AS eventName, roundName::String AS roundName
  FROM matches
  ORDER BY eventName
  """, "DataFrame")

  if "match_id" not in st.session_state:
    st.session_state.match_id = match.match.iloc[0]


  if event_filter != "All":
    match = match[match["eventName"] == event_filter]

  if round_filter != "All":
    match = match[match["roundName"] == round_filter]

  match['label'] = match['p1Name'] + " vs " + match['p2Name']
  label_to_match = dict(zip(match['label'], match['match']))
  match_to_label = dict(zip(match['match'], match['label']))
  
  if st.session_state.match_id not in match_to_label:
    st.query_params.match_id = match.match.iloc[0]
    st.session_state.match_id = match.match.iloc[0]

  players = list(label_to_match.keys())
  def on_select_change():
      selected_match_id = label_to_match[st.session_state.selected_label]
      st.session_state.match_id = selected_match_id
      st.query_params.match_id = selected_match_id

  
  current_match_id = st.session_state.match_id
  if current_match_id in match_to_label:
      default_label = match_to_label[current_match_id]
      if default_label not in players:
          default_label = players[0] if players else ""
  else:
      default_label = players[0] if players else ""

  if players:
      selected_label = st.selectbox(
          "Select match",
          options=players,
          index=players.index(default_label),
          key="selected_label",
          on_change=on_select_change
      )

      selected_match_id = label_to_match[selected_label]
      
      if selected_match_id != st.session_state.match_id:
          st.session_state.match_id = selected_match_id
          st.query_params.match_id = selected_match_id

  st.write("----")
  st.write("Powered by [chDB](https://clickhouse.com/docs/chdb) and [Streamlit](https://streamlit.io/).")

if "match_id" not in st.session_state:
    st.warning("Choose a match from the sidebar")
    st.stop()

selected_match_id = st.session_state.match_id

df = sess.query(f"""
SELECT p1.gamesWon || '-' || p2.gamesWon AS score, p1Name, p2Name
FROM points
JOIN matches ON matches.match = points.match
WHERE match = '{selected_match_id}' AND (SetWinner <> '0' OR MatchWinner <> '0')
""", "DataFrame")

st.header(f"{df.p1Name.iloc[0]} vs {df.p2Name.iloc[0]}")

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
WHERE match = '{selected_match_id}'
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
    WHERE match = '{selected_match_id}' AND MatchWinner <> '0'
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
