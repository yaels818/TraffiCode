import os
import datetime

DIR = "player scores"

def export_data_to_file(tracking_table):

    # Create the directory for the index files
    try:
        os.mkdir(DIR)
    except FileExistsError:
        #print("Directory " + DIR + " already exists")
        pass

    now = datetime.datetime.now()
    file_name = "player_stats" + "_" + now.strftime("%d_%m_%y")

    path = DIR + "/" + file_name

    # Fill file with the tracker's info
    with open(path , "at") as file:
        play_time = now.strftime("%H:%M:%S")
        print(f">> Game finished at: {play_time}", file = file)
        for row in tracking_table:
            print(*row, sep = ",", file = file)
