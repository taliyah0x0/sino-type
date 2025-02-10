# reverse the txt file
'''m = []
with open("romanization.txt", "r") as file:
    m = file.readlines()

with open("flipped.txt", "w") as file:
    for i in range(len(m) - 1, -1, -1):
        file.write(m[i])'''

# txt to json file
import json
data = {}
foreigns = ["韓", "台", "越"]
with open("flipped.txt", "r") as file:
    line = file.readline()
    cur_rom = []
    cur_for = []
    while line != "":
        if line[0].isdigit(): # new character
            stripped = line.strip()
            for i in range(len(cur_rom)): # add the character to all relevant romanizations
                data[cur_rom[i]][cur_for[i]].append(stripped[-1])
            cur_rom = []
            cur_for = []
        else: # one of the romanizations
            stripped = line[2:-1].strip().lower()
            rom_only = ""
            if stripped[-1] in foreigns: # belongs to foreign language
                cur_for.append(foreigns.index(stripped[-1]) + 1) # add index to list
                rom_only = stripped[:-2] # strip only the romanization
            else: # belongs to shanghainese only
                cur_for.append(0) # add index to list
                rom_only = stripped # romanization would remain the same
            cur_rom.append(rom_only) # add romanization to list
            if rom_only not in data: # new romanization not seen before
                data[rom_only] = [] # create a new definition on the database
                for i in range(4):
                    data[rom_only].append([])
        line = file.readline()

with open("output.json", "w") as json_file:
    json.dump(data, json_file, indent=4, ensure_ascii=False)


import json
import csv
# Convert JSON to a CSV format
csv_filename = "output.csv"
with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Key", "Shanghainese", "Korean", "Taiwanese", "Vietnamese"])
    
    for key, lists in data.items():
        max_length = max(len(sublist) for sublist in lists)
        for i in range(max_length):
            row = [key]
            for sublist in lists:
                row.append(sublist[i] if i < len(sublist) else "")
            writer.writerow(row)



# convert csv back to json
json_data = {}
with open(csv_filename, mode='r', encoding='utf-8') as file:
    reader = csv.reader(file)
    headers = next(reader)[1:]
    
    for row in reader:
        key = row[0]
        values = row[1:]
        
        if key not in json_data:
            json_data[key] = [[] for _ in headers]
        
        for i, value in enumerate(values):
            if value:
                json_data[key][i].append(value)