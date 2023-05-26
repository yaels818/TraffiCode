import os
import datetime

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

    def fixed_length(text, length):
        """
        Make given text fit given length.
        Here we use it to make our table's columns with a fixed length. 

        Parameters
        ----------
        text : string
            The text we want to fit. 
        
        length : int
            The length we want to text to match.
        """

        # If text is too long
        if len(text) > length:
            # Cut off the extra characters
            text = text[:length]
        # If text is too short     
        elif len(text) < length:
            # Pad text with spaces, then remove extras
            text = (text + " " * length)[:length] 
        return text

    DIR = "player scores"

    # If the directory for the score files does not exist yet 
    # --> Create the directory for the score files
    try:
        os.mkdir(DIR)
    except FileExistsError:
        #print("Directory " + DIR + " already exists")
        pass

    # 
    now = datetime.datetime.now()
    file_name = "player_stats" + "_" + now.strftime("%d_%m_%y") + ".txt"

    path = DIR + "/" + file_name

    COL_LEN = 22
    FULL_ROW_LEN = 253

    # Fill file with the tracker's info
    with open(path , "at") as file:
        # Get current time in hour:minutes:seconds format and print it to the file
        play_time = now.strftime("%H:%M:%S")
        print("#" * FULL_ROW_LEN, file = file)
        print(f">> Game finished at: {play_time}", file = file)
        print("#" * FULL_ROW_LEN, file = file)

        # Get the headers for each column and print them in a single line to the file
        print("# ", end = " ", file = file)
        header = data.pop(0)
        for col in header:
            print(fixed_length(col, COL_LEN), end = " # ", file = file)
        print(file = file)
        print("-" * FULL_ROW_LEN, file = file)

        # Get the data for each column and print it to the file
        for row in data:
            print("# ", end = " ", file = file)
            for col in row:
                print(fixed_length(str(col), COL_LEN), end = " # ", file = file)
            print(file = file)
        print("#" * FULL_ROW_LEN, file = file)
        print(file = file)
