
def discipline_plus():

    data = [26.9,62.4,85.5,29.8]

    W1 = 0.5  # Weight for O-Swing
    W2 = 0.3  # Weight for Z-Swing
    W3 = 0.1  # Weight for Z-Contact
    W4 = 0.1  # Weight for CSW

    PD = league_avg_PD = ((100-data[0])/100 * W1) + (data[1]/100 * W2) + (data[2] / 100 * W3) - (data[3] / 100 * W4)
    league_avg_PD2024 = ((100-31.8)/100 * W1) + (69.4/100 * W2) + (85.9 / 100 * W3) - (27.4 / 100 * W4)
    # Normalize plate discipline to make league average = 100
    return (PD / league_avg_PD2024) * 100

print(discipline_plus())