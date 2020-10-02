#!/usr/bin/env python
# coding: utf-8

# # Introduction
# This project aims to design and create a database of baseball game-level statistics, working with files of Major League Baseball (MLB) games data from Retrosheet ( https://www.retrosheet.org/ ).

# In[ ]:


import pandas as pd
import numpy as np
import sqlite3
import matplotlib.pyplot as plt
from matplotlib import cm
from IPython.display import Image

get_ipython().run_line_magic('matplotlib', 'inline')

pd.set_option('max_columns', 180)
pd.set_option('max_rows', 200000)
pd.set_option('max_colwidth', 5000)


# # Helper functions

# In[ ]:


#run_query(q): Takes a SQL query as an argument and returns a pandas dataframe by using the connection as a SQLite built-in context manager. 
def run_query(q):
    with sqlite3.connect('mlb.db') as conn:
        return pd.read_sql_query(q, conn)
    
#run_command(c): Takes a SQL command as an argument and executes it using the sqlite module.
def run_command(c):
    with sqlite3.connect('mlb.db') as conn:
        conn.execute('PRAGMA foreign_keys = ON;') #Enables enforcement of foreign key restraints.
        conn.isolation_level = None
        conn.execute(c)
    
#show_tables(): calls the run_query() function to return a list of all tables and views in the database.
def show_tables():
    q = '''SELECT
            name,
            type
        FROM sqlite_master
        WHERE type IN ("table","view");
        '''
    return run_query(q)    
    


# # EDA - Understanding the Data

# The data files that will be used to create the database are:
# 
# Main file:
# 
# - **'game_log.csv':** Contains hundreds of data points on each game, as a result of combining 127 separate CSV files from retrosheet (pre-cleaned), intersecting with the helper files on points such as park, player or team information. A file called 'game_log_fields.txt' explains the fields included in the main file, used as a reference for some of the explanatory markdowns.
# 
# 'Helper' files (for extra data):
# - **'park_codes.csv':** Contains information about the baseball parks where the games were held.
# - **'person_codes.csv':** Contains information about the people involved in the games, from player to coach.
# - **'team_codes.csv':** Contains information about the teams.

# ### Main file

# In[ ]:


#game_log.csv
game_log = pd.read_csv("../input/major-league-baseball-games-data-from-retrosheet/game_log.csv",low_memory=False)
print(game_log.shape)
game_log.head()


# The main game log provides information about more than 171,000 games, containing:
# 
# - Overall information on each game.
# - A list of the players and their positions (based on the order in which they batted).
# - Team results and stats.
# - Win-loss records.
# 
# It also seems like coaches are not recorded in the table.

# ### Helper Files

# In[ ]:


#park_codes.csv
park_codes = pd.read_csv("../input/major-league-baseball-games-data-from-retrosheet/park_codes.csv")
print(park_codes.shape)
park_codes.head()


# Specifies the name of the baseball park, its location, years active and the league they hold games for. IDs, names, nicknames, location and league records from this table match with the main game log table.

# In[ ]:


#person_codes.csv
person_codes = pd.read_csv("../input/major-league-baseball-games-data-from-retrosheet/person_codes.csv")
print(person_codes.shape)
person_codes.head()


# Shows the ID (which seems to match up with those in the main game log), first and last name, debut and role on each person involved in the games, featuring players, coaches, umpires and 'head coaches' (managers). Some of them may have had more than one role.

# In[ ]:


#team_codes.csv
team_codes = pd.read_csv("../input/major-league-baseball-games-data-from-retrosheet/team_codes.csv")
print(team_codes.shape)
team_codes.head()


# Shows information about the teams, where team_id seems to match up with the main game log.
# 
# Taking a look at the franch_id, we realize for one single franchise there may be more than one team_id, as follows:

# In[ ]:


print(team_codes['franch_id'].value_counts().head())
team_codes[team_codes['franch_id']=='BR3']


# This means depending on the city or the league there may be more than one team ID, but the franchise (and the corresponding nickname) keeps being the same for all of them.

# ### Defensive positions 

# In[ ]:


Image(filename='../input/major-league-baseball-games-data-from-retrosheet/baseball_positions.png')


# In the game log, there are some columns reserved for the defensive position of each player (*v_player_#_def_pos*, where # corresponds to the number of player).
# 
# Their values go from 1 to 10, as seen in the image above, where I will consider number 10 as 'unknown' or a player that doesn't field.
# 
# Based on the above diagram and some research, numbers 1-9 refer to:
# 
# 1. Pitcher
# 2. Catcher
# 3. 1st Base
# 4. 2nd Base
# 5. 3rd Base
# 6. Shortstop
# 7. Left Field
# 8. Center Field
# 9. Right Field

# ### Leagues

# The current baseball leagues in the US are the American League (AL) and the National League (NL). Let's see which ones the main game log include.

# In[ ]:


fig = plt.figure(figsize=(9,6))

leagues = game_log['h_league'].value_counts().index.tolist()
times = game_log['h_league'].value_counts().tolist()
percentage_times = np.array(times)/sum(times)
colors = cm.Set3(np.arange(10)/10.)
explode = [0]*6
explode[0] = 0.1

patches, texts, autotexts = plt.pie(percentage_times, 
                                    colors=colors, 
                                    labels=leagues, 
                                    autopct='%1.1f%%',
                                    explode=explode,
                                    startangle=-90,
                                    shadow=True)
for i in range(0,2):
    texts[i].set_fontsize(18)
    autotexts[i].set_fontsize(14)
    
for i in range(2,6):
    texts[i].set_fontsize(0)
    autotexts[i].set_fontsize(0)
    
plt.title('Pct Values for Each League', fontsize=25, y=1.1)
plt.axis('equal')
plt.tight_layout()
plt.show()


# Looks like the data mostly includes data from the two current leagues.
# 
# After some research, I have found the acronym for each league refers to:
# 
# - AL: American League
# - NL: National League
# - AA: American Association
# - UA: Union Association
# - FL: Federal League
# - PL: Players League

# In[ ]:


game_log['h_league'].value_counts(dropna=False)


# By looking at the values in the 'h_league' column, we can also see that about 1000 games do not include a value for the home team league.

# # Importing Data into SQLite

# In[ ]:


conn = sqlite3.connect('mlb.db')

game_log.to_sql('game_log', conn, index=False, if_exists='replace')
park_codes.to_sql('park_codes', conn, index=False, if_exists='replace')
person_codes.to_sql('person_codes', conn, index=False, if_exists='replace')
team_codes.to_sql('team_codes', conn, index=False, if_exists='replace')

show_tables()


# ## Primary Key
# 
# The game log file does not have a single column that can be used as a primary key to uniquely identify each game. However, the Retrosheet data dictionary tells us that each game can be identified with an unique ID such as:
# 
# *__id:__* *Each game begins with a twelve character ID record which identifies the date, home team, and number of the game. For example, ATL198304080 should be read as follows. The first three characters identify the home team (the Braves). The next four are the year (1983). The next two are the month (April) using the standard numeric notation, 04, followed by the day (08). The last digit indicates if this is a single game (0), first game (1) or second game (2) if more than one game is played during a day, usually a double header The id record starts the description of a game thus ending the description of the preceding game in the file.*
# 
# This way, creating a custom primary key made up of the concatenation of h_name, date and number_of_game in a new column called game_id, each game will be uniquely identified in the database.

# In[ ]:


#Adds the new game_id column
q1 = '''
    ALTER TABLE game_log
    ADD game_id VARCHAR(12);
'''

try:
    run_command(q1)
except:
    pass

#Set the concatenation of h_name, date and number_of_game as game_id values
q2 = '''
    UPDATE game_log 
    SET game_id = h_name || date || number_of_game
    WHERE game_id IS NULL;
'''

run_command(q2)

q3 = '''
    SELECT 
        date, 
        h_name, 
        number_of_game,
        game_id
    FROM game_log
    LIMIT 10;

'''

run_query(q3)


# # Normalization
# For the purpose of this project, the normalized schema I will use is the following:

# In[ ]:


Image(filename='../input/major-league-baseball-games-data-from-retrosheet/normalized_schema.png')


# ## Creating the tables
# Taking the right columns in the right order from the tables we already have will allow to create the tables for the normalized database:
# 
# - team_appearance
# - team
# - person
# - person_appearance
# - game
# - league
# - appearance_type
# - park

# ### Person

# In[ ]:


q4 = '''
    CREATE TABLE IF NOT EXISTS person (
        person_id TEXT,
        first_name TEXT,
        last_name TEXT,
        PRIMARY KEY (person_id)
    );
'''

run_command(q4)

q5 = '''
    INSERT OR IGNORE INTO person
    SELECT
        id,
        first,
        last
    FROM person_codes;
'''

run_command(q5)

q6 = '''
    SELECT * FROM person
    LIMIT 10;
'''
run_query(q6)


# ### Park

# In[ ]:


q7 = '''
    CREATE TABLE IF NOT EXISTS park (
        park_id TEXT,
        name TEXT,
        nickname TEXT,
        city TEXT,
        state TEXT,
        notes TEXT,
        PRIMARY KEY (park_id)
    );
'''

run_command(q7)

q8 = '''
    INSERT OR IGNORE INTO park
    SELECT
        park_id,
        name,
        aka,
        city,
        state,
        notes
    FROM park_codes;
'''

run_command(q8)

q9 = '''
    SELECT * FROM park
    LIMIT 10;
'''
run_query(q9)


# ### Appearance Type
# First, the data needs to be imported into SQLite from *appearance_type.csv* in order to insert it in the table.

# In[ ]:


app_type = pd.read_csv("../input/major-league-baseball-games-data-from-retrosheet/appearance_type.csv",low_memory=False)
app_type.to_sql('app_type', conn, index=False, if_exists='replace')


# In[ ]:


q10 = '''
    CREATE TABLE IF NOT EXISTS appearance_type (
        appearance_type_id TEXT,
        name TEXT,
        category TEXT,
        PRIMARY KEY (appearance_type_id)
    );
'''

run_command(q10)

q11 = '''
    INSERT OR IGNORE INTO appearance_type
    SELECT
        appearance_type_id,
        name,
        category
    FROM app_type;
'''

run_command(q11)

q12 = '''
    SELECT * FROM appearance_type
    LIMIT 10;
'''
run_query(q12)


# ### League
# As mentioned before, the leagues analysed in the data are:
# 
# - AL: American League
# - NL: National League
# - AA: American Association
# - UA: Union Association
# - FL: Federal League
# - PL: Players League

# In[ ]:


q13 = '''
    CREATE TABLE IF NOT EXISTS league (
        league_id TEXT,
        name TEXT,
        PRIMARY KEY (league_id)
    );
'''

run_command(q13) 

q14 = '''
    INSERT OR IGNORE INTO league
    VALUES
        ('AL', 'American League'),
        ('NL', 'National League'),
        ('AA', 'American Association'),
        ('UA', 'Union Association'),
        ('FL', 'Federal League'),
        ('PL', 'Players League');
'''

run_command(q14)

q15 = '''
    SELECT * FROM league;
'''

run_query(q15)


# ### Team

# In[ ]:


q16 = '''
    CREATE TABLE IF NOT EXISTS team (
        team_id TEXT,
        league_id TEXT,
        city TEXT,
        nickname TEXT,
        franch_id TEXT,
        PRIMARY KEY (team_id),
        FOREIGN KEY (league_id) REFERENCES league(league_id)
    );
'''

run_command(q16) 

q17 = '''
    INSERT OR IGNORE INTO team
    SELECT
        team_id,
        league,
        city,
        nickname,
        franch_id
    FROM team_codes;
'''

run_command(q17)

q18 = '''
    SELECT * FROM team
    LIMIT 10;
'''

run_query(q18)


# ### Game

# In[ ]:


q19 = '''
    CREATE TABLE IF NOT EXISTS game (
        game_id TEXT,
        date TEXT,
        number_of_game INT,
        park_id TEXT,
        length_outs FLOAT,
        day BOOLEAN,
        completion TEXT,
        forefeit TEXT,
        protest TEXT,
        attendance INTEGER,
        legnth_minutes INTEGER,
        additional_info TEXT,
        acquisition_info TEXT,
        PRIMARY KEY (game_id),
        FOREIGN KEY (park_id) REFERENCES park(park_id)
    );
'''

run_command(q19) 

q20 = '''
    INSERT OR IGNORE INTO game
    SELECT
        game_id,
        date,
        number_of_game,
        park_id,
        length_outs,
        CASE
            day_night
            WHEN 'D' THEN 1
            WHEN 'N' THEN 0
            ELSE NULL
            END
            AS day,
        completion,
        forefeit,
        protest,
        attendance,
        length_minutes,
        additional_info,
        acquisition_info
    FROM game_log;
'''

run_command(q20)

q21 = '''
    SELECT * FROM game
    LIMIT 10;
'''

run_query(q21)


# ### Team Appearance
# First, let's extract the schema from the game_log table, and use that as a starting point for the query to avoid manually typing all the column names.

# In[ ]:


q = '''
SELECT sql FROM sqlite_master
WHERE name = "game_log"
  AND type = "table";

'''
run_query(q)


# In[ ]:


q22 = '''
    CREATE TABLE IF NOT EXISTS team_appearance (
        team_id TEXT,
        game_id TEXT,
        home BOOLEAN,
        league_id TEXT,
        score INT,
        line_score TEXT,
        at_bats INT,
        hits INT,
        doubles INT,
        triples INT,
        homeruns INT,
        rbi INT,
        sacrifice_hits INT,
        sacrifice_flies INT,
        hit_by_pitch INT,
        walks INT,
        intentional_walks INT,
        strikeouts INT,
        stolen_bases INT,
        caught_stealing INT,
        grounded_into_double INT,
        first_catcher_interference INT,
        left_on_base INT,
        pitchers_used INT,
        individual_earned_runs INT,
        team_earned_runs INT,
        wild_pitches INT,
        balks INT,
        putouts INT,
        assists INT,
        errors INT,
        passed_balls INT,
        double_plays INT,
        triple_plays INT,
        PRIMARY KEY (team_id, game_id),
        FOREIGN KEY (team_id) REFERENCES team(team_id),
        FOREIGN KEY (game_id) REFERENCES game(game_id),
        FOREIGN KEY (team_id) REFERENCES team(team_id)
    );
'''

run_command(q22) 

q23 = '''
    INSERT OR IGNORE INTO team_appearance
    SELECT
        h_name,
        game_id,
        1 AS home,
        h_league,
        h_score,
        h_line_score,
        h_at_bats,
        h_hits,
        h_doubles,
        h_triples,
        h_homeruns,
        h_rbi,
        h_sacrifice_hits,
        h_sacrifice_flies,
        h_hit_by_pitch,
        h_walks,
        h_intentional_walks,
        h_strikeouts,
        h_stolen_bases,
        h_caught_stealing,
        h_grounded_into_double,
        h_first_catcher_interference,
        h_left_on_base,
        h_pitchers_used,
        h_individual_earned_runs,
        h_team_earned_runs,
        h_wild_pitches,
        h_balks,
        h_putouts,
        h_assists,
        h_errors,
        h_passed_balls,
        h_double_plays,
        h_triple_plays
    FROM game_log

    UNION

    SELECT    
        v_name,
        game_id,
        0 AS home,
        v_league,
        v_score,
        v_line_score,
        v_at_bats,
        v_hits,
        v_doubles,
        v_triples,
        v_homeruns,
        v_rbi,
        v_sacrifice_hits,
        v_sacrifice_flies,
        v_hit_by_pitch,
        v_walks,
        v_intentional_walks,
        v_strikeouts,
        v_stolen_bases,
        v_caught_stealing,
        v_grounded_into_double,
        v_first_catcher_interference,
        v_left_on_base,
        v_pitchers_used,
        v_individual_earned_runs,
        v_team_earned_runs,
        v_wild_pitches,
        v_balks,
        v_putouts,
        v_assists,
        v_errors,
        v_passed_balls,
        v_double_plays,
        v_triple_plays
    FROM game_log;
'''

run_command(q23)

q24 = '''
    WITH home1 AS
        (
            SELECT *
            FROM team_appearance
            WHERE home = 1 AND doubles IS NOT NULL
            LIMIT 5
        ),
    
        home0 AS
        (
            SELECT *
            FROM team_appearance
            WHERE home = 0 AND doubles IS NOT NULL
            LIMIT 5
        )
        
        
    SELECT *
    FROM home1
    
    UNION
    
    SELECT *
    FROM home0
    
'''

run_query(q24)


# ### Person Appearance

# In[ ]:


q25 = '''
    DROP TABLE IF EXISTS person_appearance
'''

run_command(q25)

q26 = '''
CREATE TABLE person_appearance (
    appearance_id INTEGER PRIMARY KEY,
    person_id TEXT,
    team_id TEXT,
    game_id TEXT,
    appearance_type_id,
    FOREIGN KEY (person_id) REFERENCES person(person_id),
    FOREIGN KEY (team_id) REFERENCES team(team_id),
    FOREIGN KEY (game_id) REFERENCES game(game_id),
    FOREIGN KEY (appearance_type_id) REFERENCES appearance_type(appearance_type_id)
);
'''

q27 = '''
INSERT OR IGNORE INTO person_appearance (
    game_id,
    team_id,
    person_id,
    appearance_type_id
) 
    SELECT
        game_id,
        NULL,
        hp_umpire_id,
        "UHP"
    FROM game_log
    WHERE hp_umpire_id IS NOT NULL    

UNION

    SELECT
        game_id,
        NULL,
        [1b_umpire_id],
        "U1B"
    FROM game_log
    WHERE "1b_umpire_id" IS NOT NULL

UNION

    SELECT
        game_id,
        NULL,
        [2b_umpire_id],
        "U2B"
    FROM game_log
    WHERE [2b_umpire_id] IS NOT NULL

UNION

    SELECT
        game_id,
        NULL,
        [3b_umpire_id],
        "U3B"
    FROM game_log
    WHERE [3b_umpire_id] IS NOT NULL

UNION

    SELECT
        game_id,
        NULL,
        lf_umpire_id,
        "ULF"
    FROM game_log
    WHERE lf_umpire_id IS NOT NULL

UNION

    SELECT
        game_id,
        NULL,
        rf_umpire_id,
        "URF"
    FROM game_log
    WHERE rf_umpire_id IS NOT NULL

UNION

    SELECT
        game_id,
        v_name,
        v_manager_id,
        "MM"
    FROM game_log
    WHERE v_manager_id IS NOT NULL

UNION

    SELECT
        game_id,
        h_name,
        h_manager_id,
        "MM"
    FROM game_log
    WHERE h_manager_id IS NOT NULL

UNION

    SELECT
        game_id,
        CASE
            WHEN h_score > v_score THEN h_name
            ELSE v_name
            END,
        winning_pitcher_id,
        "AWP"
    FROM game_log
    WHERE winning_pitcher_id IS NOT NULL

UNION

    SELECT
        game_id,
        CASE
            WHEN h_score < v_score THEN h_name
            ELSE v_name
            END,
        losing_pitcher_id,
        "ALP"
    FROM game_log
    WHERE losing_pitcher_id IS NOT NULL

UNION

    SELECT
        game_id,
        CASE
            WHEN h_score > v_score THEN h_name
            ELSE v_name
            END,
        saving_pitcher_id,
        "ASP"
    FROM game_log
    WHERE saving_pitcher_id IS NOT NULL

UNION

    SELECT
        game_id,
        CASE
            WHEN h_score > v_score THEN h_name
            ELSE v_name
            END,
        winning_rbi_batter_id,
        "AWB"
    FROM game_log
    WHERE winning_rbi_batter_id IS NOT NULL

UNION

    SELECT
        game_id,
        v_name,
        v_starting_pitcher_id,
        "PSP"
    FROM game_log
    WHERE v_starting_pitcher_id IS NOT NULL

UNION

    SELECT
        game_id,
        h_name,
        h_starting_pitcher_id,
        "PSP"
    FROM game_log
    WHERE h_starting_pitcher_id IS NOT NULL;
'''

template = '''
    INSERT INTO person_appearance (
        game_id,
        team_id,
        person_id,
        appearance_type_id
    ) 
        SELECT
            game_id,
            {hv}_name,
            {hv}_player_{num}_id,
            "O{num}"
        FROM game_log
        WHERE {hv}_player_{num}_id IS NOT NULL

    UNION

        SELECT
            game_id,
            {hv}_name,
            {hv}_player_{num}_id,
            "D" || CAST({hv}_player_{num}_def_pos AS INT)
        FROM game_log
        WHERE {hv}_player_{num}_id IS NOT NULL;
'''


run_command(q26)
run_command(q27)

for hv in ["h","v"]:
    for num in range(1,10):
        query_vars = {
            "hv": hv,
            "num": num
        }
        run_command(template.format(**query_vars))


# In[ ]:


q28 = '''
    SELECT
        pa.*,
        at.name,
        at.category
    FROM person_appearance pa
    INNER JOIN appearance_type at on at.appearance_type_id = pa.appearance_type_id
    LIMIT 10;
'''

run_query(q28)


# # Removing the Original Tables

# In[ ]:


original_tables = ['game_log', 'park_codes', 'team_codes', 'person_codes']

for table in original_tables:
    q29 = '''DROP TABLE IF EXISTS {}'''.format(table)
    run_command(q29)

show_tables()


# In[ ]:




