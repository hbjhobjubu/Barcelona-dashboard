import streamlit as st
import pandas as pd
import plotly.express as px   

st.set_page_config(page_title="Barça Dashboard", page_icon="🔵", layout="wide")  

logo_col, title_col = st.columns([1, 9])
with logo_col:
    st.image("images/barca_logo.png", width=80)
with title_col:
    st.title("FC Barcelona Dashboard")
    st.write("Every Barcelona match in La Liga, 1995–2025")

df = pd.read_csv("data/LaLiga_Matches.csv")
barca = df[(df["HomeTeam"] == "Barcelona") | (df["AwayTeam"] == "Barcelona")].copy()

barca["BarcaGoals"] = barca.apply(
    lambda row: row["FTHG"] if row["HomeTeam"] == "Barcelona" else row["FTAG"], axis=1)
barca["OppGoals"] = barca.apply(
    lambda row: row["FTAG"] if row["HomeTeam"] == "Barcelona" else row["FTHG"], axis=1)

def get_result(row):
    if row["BarcaGoals"] > row["OppGoals"]:
        return "Win"
    elif row["BarcaGoals"] == row["OppGoals"]:
        return "Draw"
    else:
        return "Loss"

barca["Result"] = barca.apply(get_result, axis=1)

st.sidebar.header("⚙️ Filters")
all_seasons = sorted(barca["Season"].unique())
selected_season = st.sidebar.selectbox("Season", ["All seasons"] + all_seasons)

if selected_season == "All seasons":
    data = barca                  
else:
    data = barca[barca["Season"] == selected_season]   


total = len(data)
wins = (data["Result"] == "Win").sum()
goals = data["BarcaGoals"].sum()
win_pct = wins / total * 100

col1, col2, col3, col4 = st.columns(4)
col1.metric("⚽ Matches", total)
col2.metric("✅ Wins", wins)
col3.metric("🥅 Goals Scored", f"{goals:,}")
col4.metric("📈 Win %", f"{win_pct:.1f}%")

left, right = st.columns(2)

with left:
   
    result_counts = data["Result"].value_counts().reset_index()
    result_counts.columns = ["Result", "Count"]
    color_map = {"Win": "#A50044", "Draw": "#004D98", "Loss": "#9aa0a6"}
    fig1 = px.pie(result_counts, names="Result", values="Count",
                  color="Result", color_discrete_map=color_map,
                  hole=0.55, title="📊 Results Breakdown")
    fig1.update_traces(textposition="inside", textinfo="percent+label")
    st.plotly_chart(fig1, use_container_width=True)

with right:
  
    goals_by_season = barca.groupby("Season", as_index=False)["BarcaGoals"].sum()
    fig2 = px.line(goals_by_season, x="Season", y="BarcaGoals", markers=True,
                   title="📈 Goals per Season",
                   labels={"BarcaGoals": "Goals", "Season": "Season"})
    fig2.update_layout(xaxis_tickangle=-45, hovermode="x unified")
    st.plotly_chart(fig2, use_container_width=True)

with st.expander("📋 Show raw match data"):
    st.write(data)

st.subheader("📍 Barça Away Days: Every Ground in Spain")

barca["Opponent"] = barca.apply(
    lambda row: row["AwayTeam"] if row["HomeTeam"] == "Barcelona" else row["HomeTeam"],
    axis=1)

team_coords = {
    "Alaves": ("Vitoria-Gasteiz", 42.85, -2.67),
    "Albacete": ("Albacete", 38.99, -1.86),
    "Almeria": ("Almería", 36.84, -2.46),
    "Ath Bilbao": ("Bilbao", 43.26, -2.93),
    "Ath Madrid": ("Madrid", 40.44, -3.68),
    "Betis": ("Sevilla", 37.39, -5.98),
    "Burgos": ("Burgos", 42.34, -3.70),
    "Cadiz": ("Cádiz", 36.53, -6.30),
    "Celta": ("Vigo", 42.23, -8.71),
    "Compostela": ("Santiago de Compostela", 42.88, -8.54),
    "Cordoba": ("Córdoba", 37.89, -4.77),
    "Eibar": ("Eibar", 43.18, -2.47),
    "Elche": ("Elche", 38.27, -0.70),
    "Espanol": ("Barcelona", 41.39, 2.17),
    "Extremadura": ("Almendralejo", 38.68, -6.41),
    "Getafe": ("Getafe", 40.30, -3.73),
    "Gimnastic": ("Tarragona", 41.12, 1.24),
    "Girona": ("Girona", 41.98, 2.82),
    "Granada": ("Granada", 37.18, -3.60),
    "Hercules": ("Alicante", 38.34, -0.48),
    "Huesca": ("Huesca", 42.14, -0.41),
    "La Coruna": ("A Coruña", 43.37, -8.40),
    "Las Palmas": ("Las Palmas", 28.12, -15.43),
    "Leganes": ("Leganés", 40.33, -3.76),
    "Levante": ("Valencia", 39.47, -0.38),
    "Logrones": ("Logroño", 42.47, -2.45),
    "Malaga": ("Málaga", 36.72, -4.42),
    "Mallorca": ("Palma", 39.57, 2.65),
    "Merida": ("Mérida", 38.92, -6.34),
    "Murcia": ("Murcia", 37.98, -1.13),
    "Numancia": ("Soria", 41.77, -2.47),
    "Osasuna": ("Pamplona", 42.82, -1.64),
    "Oviedo": ("Oviedo", 43.36, -5.85),
    "Racing": ("Santander", 43.46, -3.81),
    "Recreativo": ("Huelva", 37.26, -6.95),
    "Sabadell": ("Sabadell", 41.55, 2.11),
    "Salamanca": ("Salamanca", 40.97, -5.66),
    "Santander": ("Santander", 43.46, -3.81),
    "Sevilla": ("Sevilla", 37.39, -5.92),
    "Sociedad": ("San Sebastián", 43.32, -1.98),
    "Sp Gijon": ("Gijón", 43.53, -5.66),
    "Tenerife": ("Santa Cruz de Tenerife", 28.47, -16.25),
    "Valencia": ("Valencia", 39.47, -0.38),
    "Valladolid": ("Valladolid", 41.65, -4.72),
    "Vallecano": ("Madrid", 40.44, -3.68),
    "Villareal": ("Villarreal", 39.94, -0.10),
    "Xerez": ("Jerez de la Frontera", 36.69, -6.14),
    "Zaragoza": ("Zaragoza", 41.65, -0.89),
    "Real Madrid": ("Madrid", 40.42, -3.70),
}

opp_stats = barca.groupby("Opponent").agg(
    Matches=("Result", "size"),
    Wins=("Result", lambda s: (s == "Win").sum()),
).reset_index()
opp_stats["WinPct"] = (opp_stats["Wins"] / opp_stats["Matches"] * 100).round(1)

coords = opp_stats["Opponent"].map(team_coords)
opp_stats["City"] = coords.map(lambda t: t[0] if isinstance(t, tuple) else None)
opp_stats["lat"] = coords.map(lambda t: t[1] if isinstance(t, tuple) else None)
opp_stats["lon"] = coords.map(lambda t: t[2] if isinstance(t, tuple) else None)

dropped = opp_stats[opp_stats["lat"].isna()]["Opponent"].tolist()
if dropped:
    st.caption(f"⚠️ Not on map (no coordinates): {', '.join(dropped)}")

map_data = opp_stats.dropna(subset=["lat"])

fig_map = px.scatter_map(
    map_data, lat="lat", lon="lon",
    size="Matches",
    color="WinPct",
    color_continuous_scale="RdYlGn",
    range_color=[0, 100],
    hover_name="Opponent",
    hover_data={"City": True, "Matches": True, "Wins": True, "WinPct": True,
                "lat": False, "lon": False},
    zoom=4.5, center={"lat": 40.0, "lon": -3.7},
    height=650, size_max=45,
    map_style="open-street-map",
)
st.plotly_chart(fig_map, use_container_width=True)

st.divider()
st.header("🐐 Lionel Messi — The Greatest of All Time")

photo_col, info_col = st.columns([1, 2])

with photo_col:
    st.image("images/messi.jpeg", use_container_width=True)

with info_col:
    st.subheader("2004–2021 · The Messi Era at Camp Nou")

    m1, m2, m3 = st.columns(3)
    m1.metric("⚽ La Liga Goals", "474")
    m2.metric("🎽 La Liga Appearances", "520")
    m3.metric("🏆 Ballon d'Or", "8")

    st.info("📌 All-time La Liga top scorer · Record 50 goals in one La Liga "
            "season (2011–12) · 672 goals for Barça in all competitions")
    st.success("Barça won 10 La Liga titles during his years at the club 🏆")
    st.subheader("⚽ La Liga Goals by Season")
    messi_goals = {
        "2004-05": 1, "2005-06": 6, "2006-07": 14, "2007-08": 10,
        "2008-09": 23, "2009-10": 34, "2010-11": 31, "2011-12": 50,
        "2012-13": 46, "2013-14": 28, "2014-15": 43, "2015-16": 26,
        "2016-17": 37, "2017-18": 34, "2018-19": 36, "2019-20": 25,
        "2020-21": 30,
    }
    messi_df = pd.DataFrame({
        "Season": list(messi_goals.keys()),
        "Goals": list(messi_goals.values()),
    })
    fig_messi = px.bar(messi_df, x="Season", y="Goals",
                       color_discrete_sequence=["#A50044"])
    fig_messi.add_hline(y=50, line_dash="dash", line_color="gold",
                        annotation_text="🏆 Record: 50 goals",
                        annotation_position="top left")
    fig_messi.update_layout(xaxis_tickangle=-45, showlegend=False)
    st.plotly_chart(fig_messi, use_container_width=True)

st.divider()
st.header("⚔️ El Clásico: Barça vs Real Madrid")


classico = barca[barca["Opponent"] == "Real Madrid"].copy()

c1, c2, c3, c4 = st.columns(4)
c1.metric("⚔️ Clásicos Played", len(classico))
c2.metric("✅ Barça Wins", (classico["Result"] == "Win").sum())
c3.metric("➖ Draws", (classico["Result"] == "Draw").sum())
c4.metric("❌ Madrid Wins", (classico["Result"] == "Loss").sum())


cl_for = classico["BarcaGoals"].sum()
cl_against = classico["OppGoals"].sum()
st.write(f"🥅 All-time goals in the Clásico: **Barça {cl_for}** — {cl_against} **Real Madrid**")


classico["GoalDiff"] = classico["BarcaGoals"] - classico["OppGoals"]
classico["Score"] = classico["BarcaGoals"].astype(str) + " - " + classico["OppGoals"].astype(str)
classico["Venue"] = classico["HomeTeam"].map(
    lambda t: "🏟️ Camp Nou" if t == "Barcelona" else "✈️ Bernabéu")

biggest_wins = classico.nlargest(5, "GoalDiff")[
    ["Season", "Date", "Venue", "Score"]]

st.subheader("🏆 Biggest Barça Wins in the Clásico")
st.write(biggest_wins)
st.divider()
st.header("🏆 La Liga Champions Since 1995")

home = df[["Season", "HomeTeam", "FTHG", "FTAG"]].copy()
home.columns = ["Season", "Team", "GoalsFor", "GoalsAgainst"]

away = df[["Season", "AwayTeam", "FTAG", "FTHG"]].copy()
away.columns = ["Season", "Team", "GoalsFor", "GoalsAgainst"]

all_matches = pd.concat([home, away])


all_matches["Points"] = all_matches.apply(
    lambda r: 3 if r["GoalsFor"] > r["GoalsAgainst"]
    else (1 if r["GoalsFor"] == r["GoalsAgainst"] else 0), axis=1)


table = all_matches.groupby(["Season", "Team"], as_index=False)["Points"].sum()


champions = table.loc[table.groupby("Season")["Points"].idxmax()]


titles_by_team = champions["Team"].value_counts()

barca_titles = titles_by_team.get("Barcelona", 0)
madrid_titles = titles_by_team.get("Real Madrid", 0)

t1, t2 = st.columns(2)
t1.metric("🔵🔴 Barça Titles", barca_titles)
t2.metric("⚪ Real Madrid Titles", madrid_titles)


st.subheader("Titles by Club (1995–2025)")
fig_titles = px.bar(titles_by_team.head(8), 
                    labels={"value": "Titles", "index": "Club"},
                    color_discrete_sequence=["#A50044"])
fig_titles.update_layout(showlegend=False)
st.plotly_chart(fig_titles, use_container_width=True)