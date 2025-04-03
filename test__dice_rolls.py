from connect_oracleA import update_roll_count, get_roll_counts


#simple backend validation techniques

# Simulate a dice roll (e.g., rolling 3 and 5)
update_roll_count(3, 5)

# Fetch and print updated roll counts
rolls = get_roll_counts()
print("Current Dice Roll Counts:")
for row in rolls:
    print(row)
