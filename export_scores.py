"""
Author: @yaels818
Description: export_scores module, contains functions needed to export the 
                player's scores into html file.
Notes: 
    
"""
# Imports
import os
import datetime
import csv
import pandas as pd

DIR = "player scores"

def export_scores_to_csv(data, curr_time):
    
    # Create file name with current time in hour_minutes_seconds format
    file_name = "game_finished_at" + "_" + curr_time.strftime("%d_%m_%y") + "_" + curr_time.strftime("%H_%M")

    cvs_file_path = DIR + "/" + file_name + ".csv"

    # Fill file with the tracker's info
    with open(cvs_file_path, "w", newline = '') as cvs_file:

        # Get the headers for each column and print them in a single line to the file
        writer = csv.writer(cvs_file)

        header = data.pop(0)
        writer.writerow(header)

        writer.writerows(data)

    return cvs_file_path

def export_csv_to_html(file_path,curr_time):

    CSS_FILE_NAME = "style.css"

    df = pd.read_csv(file_path)

    path_html = file_path.strip(".csv") + ".html"

    date_time = curr_time.strftime("%d/%m/%y %H:%M:%S")

    html_string = '''
    <html>
        <head>
            <link rel="stylesheet" href="{file_name}">
            <title>TraffiCode Score</title>
            <h1>Game finished at: {time}</h1>
        </head>
        <table>
            {table}
    </html>
    '''

    # OUTPUT AN HTML FILE
    with open(path_html, 'w') as html_file:
        html_file.write(html_string.format(file_name=CSS_FILE_NAME, time = date_time, table=df.to_html(index=False,border=False)))

def export_data_to_file(data):
    """
    Export given data to a text file.
    Here we use it for the data of LevelTracker.tracking_table 
    (the player's scores in each level of the game). 
    
    Parameters
    ----------
    data : list
        The tracking table for the player's scores in each level of the game.

        Contains: ["Level", 
                "Time (Seconds)",
                "Peds hits", 
                "Cars hits", 
                "Sidewalk hits", 
                "Over solid lane", 
                "Against traffic",
                "Roundabout hits", 
                "Parking lot hits", 
                "Accurate parking ( /4)"]

    Notes
    -----
    1. If the directory for the player's scores has not been created yet - create it. 
    2. If a score file for today's date has not been created yet - create a new file. 
    3. If there is already a score file for today's date - append the latest game scores to it. 
    """

    """
    # If the directory for the score files does not exist yet 
    # --> Create the directory
    try:
        os.mkdir(DIR)
    except FileExistsError:
        #print("Directory " + DIR + " already exists")
        pass
    """

    # Get current time and date
    curr_time = datetime.datetime.now()

    cvs_file_path = export_scores_to_csv(data,curr_time)

    export_csv_to_html(cvs_file_path,curr_time)

    # Delete all index files, then we can delete the directory
    try:
        os.remove(cvs_file_path)
    except OSError as error:
        print(error)
        