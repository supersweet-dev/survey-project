import itertools
import csv

# Initialize the elements
base_videos = ["Error1", "Error2", "Error3"]
modifiers = ["Regret", "Humor", "No"]
regret_videos = ["Regret1", "Regret2", "Regret3"]
humor_videos = ["Humor1", "Humor2", "Humor3"]

# Generate permutations
base_permutations = list(itertools.permutations(base_videos))
modifier_permutations = list(itertools.permutations(modifiers))
regret_permutations = list(itertools.permutations(regret_videos))
humor_permutations = list(itertools.permutations(humor_videos))

# Generate combinations of base videos and modifiers
combined_base_modifiers = [
    list(zip(base_perm, mod_perm))
    for base_perm in base_permutations
    for mod_perm in modifier_permutations
]


# Function to generate the modified list for a given video and modifier type
def generate_modified_list(video, modifier_type):
    if modifier_type == "Regret":
        return [
            [video] + [video + "+" + mod for mod in regret_perm]
            for regret_perm in regret_permutations
        ]
    elif modifier_type == "Humor":
        return [
            [video] + [video + "+" + mod for mod in humor_perm]
            for humor_perm in humor_permutations
        ]
    else:
        return [[video, video + "+No"]]


# Generate the final combinations
final_combinations = []
for combination in combined_base_modifiers:
    for tier1 in generate_modified_list(combination[0][0], combination[0][1]):
        for tier2 in generate_modified_list(combination[1][0], combination[1][1]):
            for tier3 in generate_modified_list(combination[2][0], combination[2][1]):
                final_combinations.append(tier1 + tier2 + tier3)

# Writing to CSV file
file_path = "combinations.csv"
with open(file_path, mode="w", newline="", encoding="utf-8") as file:
    writer = csv.writer(file)
    for row in final_combinations:
        writer.writerow(row)

print("CSV file has been written successfully.")
