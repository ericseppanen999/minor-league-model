import pandas as pd  

def breakout_plus_v7(discipline_plus, barrel_rate, hard_hit_rate, k_rate, bb_rate, xwoba_diff, age, maxEV, weights, league_averages, scaling_factor=100):
    # Normalize values against league averages
    barrel_norm = barrel_rate / league_averages['barrel']
    hard_hit_norm = hard_hit_rate / league_averages['hard_hit']
    k_rate_norm = k_rate / league_averages['k_rate']
    bb_rate_norm = bb_rate / league_averages['bb_rate']
    maxEV_norm = maxEV / league_averages['maxEV']
    
    # Adjust age factor to make the difference less extreme
    if age <= 30:
        age_factor = 1 + (30 - age) * 0.5  # Small bonus for younger players
    else:
        age_factor = 1 - (age - 30) * 0.02  # Small penalty for older players
    
    # Calculate the raw score by weighing each component
    raw_score = ((discipline_plus / 100)*1.2
                 + weights['barrel'] * barrel_norm
                 + weights['hard_hit'] * hard_hit_norm
                 - weights['k_rate'] * k_rate_norm  # heavily weigh K-rate
                 + weights['bb_rate'] * bb_rate_norm
                 + weights['xwoba_diff'] * xwoba_diff
                 + weights['age'] * age_factor
                 + weights['maxEV'] * maxEV_norm)
    
    # Rescale using the scaling factor divided by the total sum of weights
    total_weight = sum(weights.values())
    breakout_plus = (raw_score / total_weight) * scaling_factor
    
    return breakout_plus


# Example weights and league averages
weights = {
    'barrel': 1.7,
    'hard_hit': 1.5,
    'k_rate': 2.4,  # heavily weigh K-rate
    'bb_rate': 1.5,
    'xwoba_diff': 1.3,
    'age': 0.6,  # increased weight on age
    'maxEV': 1.3  # increased weight for maxEV
}

league_averages = {
    'barrel': 7.8,  # League average barrel rate
    'hard_hit': 38.7,  # League average hard-hit rate
    'k_rate': 22.5,  # League average K-rate
    'bb_rate': 8.2,  # League average BB-rate
    'maxEV': 110.0  # League average maxEV in mph
}

# Example data
discipline_plus = 100
barrel_rate = 10.0  # percentage
hard_hit_rate = 44.6  # percentage
k_rate = 22.9  # percentage
bb_rate = 9.3  # percentage
xwoba_diff = 0.020  # xwOBA - wOBA
age = 27
maxEV = 113.2  # mph

# Calculate BREAKOUT+
breakout_score = breakout_plus_v7(discipline_plus, barrel_rate, hard_hit_rate, k_rate, bb_rate, xwoba_diff, age, maxEV, weights, league_averages, scaling_factor=150)
print(f"BREAKOUT+ Score: {breakout_score}")
 
# maikel garcia : 78
# bryan de la cruz : 72
# trevor larnach : 92
