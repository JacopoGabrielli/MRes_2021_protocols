import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import pandas as pd
import itertools
from itertools import cycle
import json

# Application class contains all functions needed to run GUI and dialogs
class Application:
    def __init__(self, master):
        # set up frame
        self.master = master
        self.frame = tk.Frame(self.master)
        master.title("Parts combinations")
        master.geometry("400x200")
        # widgets
        self.label_intro = tk.Label(master,
                                            text="Welcome to the Isaac_Newtron app! \n This application allows you to input a .csv file containing parts to be \n assembled into novel constructs")

        self.label_platemap_save = tk.Label(master,
                                            text="Select .csv file containing parts to be \n combined in final construct library")
        self.platemap_button = tk.Button(master, text="Select parts file",
                                         command=self.run_app,
          width = 15)  # run all functions upon button click

        # formatting
        self.label_intro.pack(side='top')
        self.label_platemap_save.pack()
        self.platemap_button.pack()


    def run_app(self):
        combs = self.browse_files()  # open dialog box to search for path of input .csv file

        plate = Plate(combs)  # run functions in class Plate using contents of input .csv file as argument
        prom_utr_tuple = plate.prom_utr_lengths() # prom_utr_lengths = function to define lengths of .csv promoter and UTR columns
        platemap_df = plate.platemap(prom_utr_tuple[0], prom_utr_tuple[1]) # the tuple contains: (number of promoters, number of UTRs)
        # used to define dataframe containing all combinations of parts in platemap to be outputted to new .csv file

        tk.messagebox.showinfo("Complete", "Plate map completed. Please input filename for resulting plate map.") # tells the user that it's done
        Application.file_save(self, platemap_df) # saves the file in the location specified


        plate.write_protocol('C:\\M5_Isaac_Newtron\\M5_OT2_test1.py', 'C:\\M5_Isaac_Newtron\\template_m5.py', prom_utr = prom_utr_tuple)
    def browse_files(self):
        filename = filedialog.askopenfilename(initialdir="/", title="Select a File",
                                              filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))) # open dialog box
        # store in df = combs (short for combinations)
        combs = pd.read_csv(filename)
        return combs

    def file_save(self, write_data): # argument passed = data to be written to .csv file
        with filedialog.asksaveasfile(mode='w', defaultextension=".csv", initialdir="/", title="Save File",
                                      filetypes=(("CSV Files", "*.csv"), ("All Files", "*.*"))) as f: # opens dialog box for user input location for saved file
            if f is None:  # asksaveasfile return `None` if dialog closed with "cancel".
                return
            write_data.to_csv(f.name, index=False)
            f.close()

# Plate class contains all functions needed to calculate desired output depending on user inputs from Application class GUI
class Plate:
    def __init__(self, combs):
        self.rows = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.columns = list(range(1, 13))  # 1 ... 12
        # determines 96-well plate coordinates
        self.promoters = combs['Promoters'].dropna().tolist()
        self.utr = combs['3UTRs'].dropna().tolist()
        # if the number of promoters =/= number of utr, then Python reads as NaN cells. These are deleted and the columns of the dataframe are converted into lists for easy manipulation

    def prom_utr_lengths(self): # to get the number of promoters and utrs, stored in tuple
        n_promoters = len(self.promoters)
        n_utr = len(self.utr)
        return n_promoters, n_utr

    def ot2_global(self, n_promoters, n_utr):
        len_tuple = (n_promoters, n_utr)
        return len_tuple



    def write_protocol(self, ot2_script_path, template_path, **kwargs):
        """Generates an ot2 script named 'ot2_script_path', where kwargs are
        written as global variables at the top of the script. For each kwarg, the
        keyword defines the variable name while the value defines the name of the
        variable. The remainder of template file is subsequently written below.
        """
        with open(ot2_script_path, 'w') as wf: # open file to write to
            with open(template_path, 'r') as rf: # open .py containing template code (all of M5 except global var)
                for index, line in enumerate(rf):
                    if line[:3] == 'def':  #finds function start
                        function_start = index
                        break
                    else:
                        wf.write(line)  # writes contents of template .py to new protocol file


                for key, value in kwargs.items():
                    wf.write(key + ' = ' + str(value))
                    wf.write('\n')
                wf.write('\n')
            with open(template_path, 'r') as rf:
                for index, line in enumerate(rf):
                    if index >= function_start - 1:
                        wf.write(line)
            print("done!")


    def platemap(self, n_promoters, n_utr): # function to output platemap of resulting construct combinations
        platemap_df = pd.DataFrame()
        total = n_promoters * n_utr # total number of combinations possible

        #first need to identify which part of the 96-well plate is actually going to be filled if total < 96
        map_coords = itertools.product(self.rows, self.columns) # gets coordinates A1, A2 ... H12 as tuples by iterating through rows and columns lists
        coords = [''.join(map(str, x)) for x in map_coords] # converts tuples to strings. len(coord) = 96
        coords.sort(key=lambda x: int(x[1:])) # sort by column, same as Opentrons pipette; A1-H1, A2-H2 etc
        platemap_df['Platemap Coordinates'] = coords[:total] # slice to only include the number of cells containing promoter+UTR mix in final library

        seq = cycle(self.promoters) # in our pattern of pipetting, each promoter is pipetted in a new cell vertically downwards
        # so generate cycle of promoters to iterate through and populate df
        # eg. 7 promoters, A1 -> A1, H1, G2 etc
        platemap_df['Promoters'] = [x for x, _ in zip(seq, platemap_df['Platemap Coordinates'])] # iteration
        platemap_df["3'UTRs"] = list(
            itertools.chain.from_iterable(itertools.repeat(x, len(self.promoters)) for x in self.utr)) # repeats every element in list of UTRs vertically downwards
        # eg. 3 UTRs, A1 -> A1, B1, C1, D1, E1, F1, G1 ; B2 -> H1, A2 etc
        return platemap_df


def main():
    root = tk.Tk()
    app = Application(root)
    root.mainloop()
    # keeps window open

if __name__ == '__main__':
    main()

