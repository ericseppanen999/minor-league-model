import pandas as pd
from pybaseball import playerid_lookup
from pybaseball import statcast_batter
from datetime import datetime
import time

start_2024 = '2024-03-28'
end_2024 = '2024-10-02'
# Sample data: Replace these with actual player stats
def get_player_mlb_id(first_name,last_name):
    player_info = playerid_lookup(last_name,first_name)
    if not player_info.empty:
        mlb_id = player_info.iloc[0]['key_mlbam']
        return mlb_id
    else:
        return None

def discipline_plus(first_name,last_name):

    data = [calculate_oSwing_percentage(first_name,last_name),calculate_zSwing_percentage(first_name,last_name),calculate_zContact_percentage(first_name,last_name),calculate_csw_percentage(first_name,last_name)]

    W1 = 0.5  # Weight for O-Swing
    W2 = 0.3  # Weight for Z-Swing
    W3 = 0.1  # Weight for Z-Contact
    W4 = 0.1  # Weight for CSW

    PD = league_avg_PD = ((100-data[0])/100 * W1) + (data[1]/100 * W2) + (data[2] / 100 * W3) - (data[3] / 100 * W4)
    league_avg_PD2024 = ((100-31.8)/100 * W1) + (69.4/100 * W2) + (85.9 / 100 * W3) - (27.4 / 100 * W4)
    # Normalize plate discipline to make league average = 100
    return (PD / league_avg_PD2024) * 100

def homeruns(first_name,last_name,start_date=start_2024,end_date=end_2024):
    mlb_id = get_player_mlb_id(first_name,last_name)
    if mlb_id is not None:
        data = statcast_batter(start_date,end_date,mlb_id)
        if data.empty:
            return None
        player_hr = data.loc[data['events'] == 'double']
        return len(player_hr)
    else:
        return None
    
def calculate_oSwing_percentage(first_name, last_name, start_date=start_2024, end_date=end_2024):
    mlb_id = get_player_mlb_id(first_name, last_name)
    
    if mlb_id is None:
        print(f"Player {first_name} {last_name} not found.")
        return None
    
    # Fetch Statcast data for the batter
    data = statcast_batter(start_date, end_date, mlb_id)
    
    if data.empty:
        print(f"No data found for {first_name} {last_name} between {start_date} and {end_date}.")
        return None
    
    # Use pitch location data (plate_x and plate_z) to check if a pitch is outside the zone
    # Statcast defines the strike zone as -0.83 <= plate_x <= 0.83 and 1.5 <= plate_z <= 3.5
    outside_zone = data[data['zone'].isin([11, 12, 13, 14])]
    
    # Refine the swing description to include only meaningful swing types
    swing_descriptions = ['swinging_strike', 'foul', 'hit_into_play', 'foul_tip']
    outside_swings = outside_zone[outside_zone['description'].isin(swing_descriptions)]
    
    # Calculate O-Swing%
    total_outside_pitches = len(outside_zone)
    total_outside_swings = len(outside_swings)
    
    if total_outside_pitches == 0:
        print(f"No pitches outside the zone found for {first_name} {last_name}.")
        return 0
    
    oSwing_percentage = (total_outside_swings / total_outside_pitches) * 100
    
    return oSwing_percentage

def calculate_zSwing_percentage(first_name, last_name, start_date=start_2024, end_date=end_2024):
    mlb_id = get_player_mlb_id(first_name, last_name)
    
    if mlb_id is None:
        print(f"Player {first_name} {last_name} not found.")
        return None
    
    # Fetch Statcast data for the batter
    data = statcast_batter(start_date, end_date, mlb_id)
    
    if data.empty:
        print(f"No data found for {first_name} {last_name} between {start_date} and {end_date}.")
        return None
    
    # Use the predefined Statcast zones for pitches inside the strike zone (zones 1 to 9)
    inside_zone = data[data['zone'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9])]
    
    # Refine the swing description to include only meaningful swing types
    swing_descriptions = ['swinging_strike', 'foul', 'hit_into_play', 'foul_tip']
    inside_swings = inside_zone[inside_zone['description'].isin(swing_descriptions)]
    
    # Calculate Z-Swing%
    total_inside_pitches = len(inside_zone)
    total_inside_swings = len(inside_swings)
    
    if total_inside_pitches == 0:
        print(f"No pitches inside the zone found for {first_name} {last_name}.")
        return 0
    
    zSwing_percentage = (total_inside_swings / total_inside_pitches) * 100
    
    return zSwing_percentage
def calculate_zContact_percentage(first_name, last_name, start_date=start_2024, end_date=end_2024):
    mlb_id = get_player_mlb_id(first_name, last_name)
    
    if mlb_id is None:
        print(f"Player {first_name} {last_name} not found.")
        return None
    
    # Fetch Statcast data for the batter
    data = statcast_batter(start_date, end_date, mlb_id)
    
    if data.empty:
        print(f"No data found for {first_name} {last_name} between {start_date} and {end_date}.")
        return None
    
    # Use Statcast zones for pitches inside the strike zone (zones 1 to 9)
    inside_zone = data[data['zone'].isin([1, 2, 3, 4, 5, 6, 7, 8, 9])]
    
    # Filter for swings that resulted in contact (foul, hit_into_play, etc.)
    contact_descriptions = ['foul', 'hit_into_play', 'foul_tip']
    inside_contact = inside_zone[inside_zone['description'].isin(contact_descriptions)]
    
    # Filter for all swings (whether contact was made or not)
    swing_descriptions = ['swinging_strike', 'foul', 'hit_into_play', 'foul_tip']
    inside_swings = inside_zone[inside_zone['description'].isin(swing_descriptions)]
    
    total_inside_swings = len(inside_swings)
    total_inside_contact = len(inside_contact)
    
    if total_inside_swings == 0:
        print(f"No swings inside the zone for {first_name} {last_name}.")
        return 0
    
    zContact_percentage = (total_inside_contact / total_inside_swings) * 100
    return zContact_percentage

def calculate_csw_percentage(first_name, last_name, start_date=start_2024, end_date=end_2024):
    mlb_id = get_player_mlb_id(first_name, last_name)
    
    if mlb_id is None:
        print(f"Player {first_name} {last_name} not found.")
        return None
    
    # Fetch Statcast data for the batter
    data = statcast_batter(start_date, end_date, mlb_id)
    
    if data.empty:
        print(f"No data found for {first_name} {last_name} between {start_date} and {end_date}.")
        return None
    
    # Count called strikes and swinging strikes
    csw_descriptions = ['called_strike', 'swinging_strike']
    csw_pitches = data[data['description'].isin(csw_descriptions)]
    
    total_pitches = len(data)
    total_csw = len(csw_pitches)
    
    if total_pitches == 0:
        print(f"No pitches found for {first_name} {last_name}.")
        return 0
    
    csw_percentage = (total_csw / total_pitches) * 100
    return csw_percentage
def get_player_mlb_id(first_name, last_name):
    # Assuming this is defined to get a player's MLB ID
    # Implement or import the actual function
    pass

# Function to calculate Walk Rate (BB%)
def calculate_bb_rate(first_name, last_name, start_date=start_2024, end_date=end_2024):
    mlb_id = get_player_mlb_id(first_name, last_name)
    
    if mlb_id is None:
        print(f"Player {first_name} {last_name} not found.")
        return None
    
    data = statcast_batter(start_date, end_date, mlb_id)
    
    if data.empty:
        print(f"No data found for {first_name} {last_name} between {start_date} and {end_date}.")
        return None
    
    walks = len(data[data['events'] == 'walk'])
    plate_appearances = len(data[(data['events'].notnull()) & 
                                 (~data['events'].isin(['sac_bunt', 'intent_walk', 'hit_by_pitch']))])
    
    if plate_appearances == 0:
        print(f"No plate appearances found for {first_name} {last_name}.")
        return None
    
    bb_percentage = (walks / plate_appearances) * 100
    return bb_percentage

# Function to calculate Strikeout Rate (K%)
def calculate_k_rate(first_name, last_name, start_date=start_2024, end_date=end_2024):
    mlb_id = get_player_mlb_id(first_name, last_name)
    
    if mlb_id is None:
        print(f"Player {first_name} {last_name} not found.")
        return None
    
    data = statcast_batter(start_date, end_date, mlb_id)
    
    if data.empty:
        print(f"No data found for {first_name} {last_name} between {start_date} and {end_date}.")
        return None
    
    strikeouts = len(data[data['events'] == 'strikeout'])
    plate_appearances = len(data[(data['events'].notnull()) & 
                                 (~data['events'].isin(['sac_bunt', 'intent_walk', 'hit_by_pitch']))])
    
    if plate_appearances == 0:
        print(f"No plate appearances found for {first_name} {last_name}.")
        return None
    
    k_percentage = (strikeouts / plate_appearances) * 100
    return k_percentage

def player_age(first_name,last_name):
    info = playerid_lookup(last_name,first_name)
    if info.empty:
        return None
    birth = info.iloc[0]['birthdate']
    birth = pd.to_datetime(birth)
    today = datetime.today()
    age = today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))
    return age
    
def printStats(first_name,last_name):
    print(first_name,last_name)
    print("Homeruns: ",homeruns(first_name,last_name))
    print(discipline_plus(first_name,last_name))
    #print(player_age(first_name,last_name))
time.sleep(7)
printStats("Aaron","Judge")
printStats("Andrew","McCutchen")
printStats("Juan","Soto")
