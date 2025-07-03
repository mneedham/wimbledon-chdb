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

    how_much_winning = (
      points_df[points_df.p1PointsToWin < points_df.p2PointsToWin].shape[0] / points_df.shape[0] 
      if winner_id == '1' 
      else points_df[points_df.p2PointsToWin < points_df.p1PointsToWin].shape[0] / points_df.shape[0]
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
        hovermode='x unified'
    )

    fig.update_layout(
        margin=dict(l=40, r=40, t=25, b=40)  # left, right, top, bottom
    )

    fig.update_traces(line=dict(width=2))  # thicker lines for visibility

    st.plotly_chart(fig, use_container_width=True)


