#create a gui window
import tkinter as tk
from PIL import Image, ImageTk, ImageOps

class Interface:
    def __init__(self):
        self.original_map_pool = ['Mirage', 'Inferno', 'Anubis', 'Nuke', 'Overpass', 'Vertigo', 'Ancient']
        self.map_pool = ['Mirage', 'Inferno', 'Anubis', 'Nuke', 'Overpass', 'Vertigo', 'Ancient']
        self.match_types = ['bo1', 'bo3', 'bo5']
        self.selected_map = []
        self.banned_maps = [] 
        self.map_images = []
        self.teams = []
        self.match = None
        self.root = tk.Tk()
        self.side = None
        self.side_selected = False


        self.load_images()

        self.root.title('CSGO Map Veto')
        self.root.geometry('1400x800')
        
        # Create a frame to contain the buttons
        self.frame = tk.Frame(self.root, bg='#1a1a1a')
        self.frame.pack(fill='both', expand=True)
        
        self.window_setup()

        self.run()
        
    def ct_side(self):
        #return CT
        self.match['maps'][-1]['start_side'] = 'CT'

        self.map_selection_screen()

    def t_side(self):
        #return T
        self.match['maps'][-1]['start_side'] = 'T'

        self.map_selection_screen()

    def knife_side(self):
        #return knife
        self.match['maps'][-1]['start_side'] = 'Knife'

        self.map_selection_screen()

    def bo1_screen(self):
        # BAN,BAN,BAN,BAN,BAN,BAN,PICK
        # print('bo1')
        self.match = {'type': 'bo1', 'max_ban': len(self.map_pool)-1, 'max_pick': 1,'bans_remaining': len(self.map_pool)-1, 'picks_remaining': 1,'maps': []}
        self.team_name_screen()
        # self.map_selection_screen()

    def bo3_screen(self):
        # BAN,BAN,PICK,PICK,BAN,BAN,PICK
        # print('bo3')
        self.match = {'type': 'bo3', 'max_ban': 2, 'max_pick': 2,'bans_remaining': len(self.map_pool)-3, 'picks_remaining': 3,'maps': []}
        self.team_name_screen()
        # self.map_selection_screen()

    def bo5_screen(self):
        # BAN,BAN,PICK,PICK,PICK,PICK,PICK
        # print('bo5')
        self.match = {'type': 'bo5', 'max_ban': 2, 'max_pick': 5,'bans_remaining': len(self.map_pool)-5, 'picks_remaining': 5,'maps': []}
        self.team_name_screen()
        # self.map_selection_screen()

    def load_images(self):
        # Load the image and store it in the list
        self.map_images = []
        for map_name in self.original_map_pool:
            path = 'images/' + map_name + '.png'
            image = Image.open(path)

            # Convert the image to grayscale
            if map_name in self.banned_maps:

                gray_map = image.convert('L')
                self.map_images.append(ImageTk.PhotoImage(gray_map))
            else:
            # Store the original image and grayed out image
                self.map_images.append(ImageTk.PhotoImage(image))

    def window_setup(self):
        #create first screen with the match type selection
        #3 buttons for bo1, bo3, bo5
        # bo1 button
        bo1_button = tk.Button(self.frame, text='bo1', padx=40, pady=20, width=20, height=6, command=self.bo1_screen, bg='#D3D3D3', fg='black')
        bo1_button.place(relx=0.3, rely=0.5, anchor='center')


        # bo3 button
        bo3_button = tk.Button(self.frame, text='bo3', padx=40, pady=20, width=20, height=6,  command=self.bo3_screen, bg='#D3D3D3', fg='black')
        bo3_button.place(relx=0.5, rely=0.5, anchor='center')

        # bo5 button
        bo5_button = tk.Button(self.frame, text='bo5',padx=40, pady=20, width=20, height=6,  command=self.bo5_screen, bg='#D3D3D3', fg='black')
        bo5_button.place(relx=0.7, rely=0.5, anchor='center')

        #display frame
        self.frame.pack()

    def team_name_screen(self):
        # Destroy all widgets in the frame
        for widget in self.frame.winfo_children():
            widget.destroy()

        #create 2 text inputs for team names
        team1_label = tk.Label(self.frame, text='Team 1 Name', bg='#1a1a1a', fg='white')
        team1_label.place(relx=0.3, rely=0.3, anchor='center')

        team1_entry = tk.Entry(self.frame, width=40, bg='#D3D3D3', fg='black')
        team1_entry.place(relx=0.3, rely=0.35, anchor='center')

        team2_label = tk.Label(self.frame, text='Team 2 Name', bg='#1a1a1a', fg='white')
        team2_label.place(relx=0.7, rely=0.3, anchor='center')

        team2_entry = tk.Entry(self.frame, width=40, bg='#D3D3D3', fg='black')
        team2_entry.place(relx=0.7, rely=0.35, anchor='center')

        #create 1 botton for saving in the self.teams variable
        save_button = tk.Button(self.frame, text='Save', padx=40, pady=20, width=20, height=6, command=lambda: self.save_teams(team1_entry.get(), team2_entry.get()), bg='#D3D3D3', fg='black')
        save_button.place(relx=0.5, rely=0.6, anchor='center') 

        #display frame
        self.frame.pack()

    def save_teams(self, team1, team2):
        team1 = 'Time '+team1
        team2 = 'Time '+team2
        self.teams = [team2, team1]
        self.map_selection_screen()

    def map_selection_screen(self):
        # Destroy all widgets in the frame
        for widget in self.frame.winfo_children():
            widget.destroy()


        #for i, map_name in enumerate(self.map_pool):
        for i, map_name in enumerate(self.original_map_pool):
            # Calculate the row and column indices based on the button's position
            row = i // 3
            column = i % 3

            # Calculate the columnspan to center the button
            columnspan = 1
            if i == 6:
                columnspan = 3

            # # # Load the image and store it in the list
            # path = 'images/' + map_name + '.png'
            # image = tk.PhotoImage(file=path)
            # self.map_images.append(image)

            image = self.map_images[self.original_map_pool.index(map_name)]

            # Create the button and place it in the grid layout
            if map_name in self.selected_map:
                lalbel = tk.Label(
                    self.frame,
                    text=map_name,
                    foreground='#FF0000',
                    padx=20,  # Set padx and pady to 0
                    pady=20,
                    width=400,  
                    height=200,
                    image=image,
                    compound='center'  # Set compound to 'center'
                )   
                lalbel.grid(row=row, column=column, columnspan=columnspan, padx=10, pady=10)
                # lalbel.image = image

            else:
                button = tk.Button(
                    self.frame,
                    text=map_name,
                    padx=20,  # Set padx and pady to 0
                    pady=20,
                    width=400,  
                    height=200,
                    command=lambda name=map_name: self.map_clicked(name),
                    image=image,
                    compound='center'  # Set compound to 'center'
                )
                button.grid(row=row, column=column, columnspan=columnspan, padx=10, pady=10)
                # button.image = image

        if len(self.map_pool) == 1:
            self.map_clicked(self.map_pool[0])
            self.final_screen()

    def map_clicked(self, map_name):
        self.selected_map.append(map_name)

        picks = self.match['picks_remaining']
        bans = self.match['bans_remaining']

        action = {'action':None, 'team': None,'map':None, 'start_side':None}

        if bans > 0 and self.match['max_ban'] != 0:\
            #ban map
            self.banned_maps.append(map_name)
            self.load_images()

            action['action'] = 'Ban'
            action['team'] = self.teams[(bans+picks) % 2]   
            action['map'] = map_name
            bans -= 1
            self.match['maps'].append(action)
            self.match['bans_remaining'] = bans
            self.match['max_ban'] -= 1
            #pop map from map pool
            self.map_pool.remove(map_name)
            self.map_selection_screen()

        elif picks > 0 and self.match['max_pick'] != 0:
            action['action'] = 'Pick'
            if picks == 1:
                action['team'] = 'decider'
                action['start_side'] = 'Knife'
            else:
                action['team'] = self.teams[(bans+picks) % 2]   
                self.side_selection_screen()
                #wait for action to continue
                # action['start_side'] = self.side

            action['map'] = map_name
            
            picks -= 1

            self.match['picks_remaining'] = picks
            self.match['maps'].append(action)
            self.match['max_pick'] -= 1

            if self.match['type'] == 'bo3' and self.match['max_pick'] == 0:
                self.match['max_ban'] = 2
                self.match['max_pick'] = 1
        
            self.map_pool.remove(map_name)

    def side_selection_screen(self):
        # Destroy all widgets in the frame
        for widget in self.frame.winfo_children():
            widget.destroy()
        
        # Create for CT one for TR 
        # on button click return return the side then go back to map selection screen

        # CT button
        ct_button = tk.Button(self.frame, text='CT', padx=40, pady=20, width=20, height=6, command= self.ct_side, bg='#D3D3D3', fg='black')
        ct_button.place(relx=0.3, rely=0.5, anchor='center')

        # TR button
        tr_button = tk.Button(self.frame, text='TR', padx=40, pady=20, width=20, height=6,  command=self.t_side, bg='#D3D3D3', fg='black')
        tr_button.place(relx=0.5, rely=0.5, anchor='center')

        # knife button
        knife_button = tk.Button(self.frame, text='Knife',padx=40, pady=20, width=20, height=6,  command=self.knife_side, bg='#D3D3D3', fg='black')
        knife_button.place(relx=0.7, rely=0.5, anchor='center')

        #display frame
        self.frame.pack()

    def reset(self):
        self.match = {'type': 'bo3', 'max_ban': 2, 'max_pick': 2,'bans_remaining': len(self.map_pool)-3, 'picks_remaining': 3,'maps': []}
        self.selected_map = []
        self.banned_maps = []
        self.map_pool = ['Mirage', 'Inferno', 'Anubis', 'Nuke', 'Overpass', 'Vertigo', 'Ancient']
        self.load_images()

        for widget in self.frame.winfo_children():
            widget.destroy()

        self.window_setup()

    def save(self):
        print('Tipo de confronto: ',self.match['type'])
        print('-------------------------------------------------')
        print('Picks and bans:')
        #prints a the pick and ban order
        for map in self.match['maps']:
            print(map['action'], " team: ", map['team'], " -> map: ", map['map'], " || start side: ", map['start_side'])

    def final_screen(self):
        # Destroy all widgets in the frame

        for widget in self.frame.winfo_children():
            widget.destroy()

        row = 0
        column = 0
        for map in self.match['maps']:
            # Create a label for the map image
            map_image = self.map_images[self.original_map_pool.index(map['map'])]
            map_label = tk.Label(self.frame, 
                                 image=map_image,
                                 width=400,
                                 height=200,
                                 padx=10,
                                 pady=10)
            map_label.grid(row=row, column=column, padx=10, pady=10)

            # Create a label for the team that performed the action (ban/pick)
            if map['action'] == 'Ban':
                string = map['action'] + ' : ' + map['team']
                #make text red hex
                foreground = '#FF0000'
            else:
                string = map['action'] + ' : ' + map['team'] + ' || (starting side: ' + map['start_side'] + ')'
                foreground = 'white'
            #make text white 
            team_label = tk.Label(self.frame, text= string, bg='#1a1a1a', fg=foreground)
            team_label.grid(row=row + 1, column=column, padx=10, pady=10)
            # team_label.grid(row=row + 1, column=column, padx=10, pady=10, bg='#D3D3D3', fg='black')
            column += 1
            if column == 3:
                column = 0
                row += 3

        # Create a reset button
        reset_button = tk.Button(self.frame,
                                text='Save', 
                                padx=40, 
                                pady=20, 
                                width=20, 
                                height=6, 
                                command=self.save,
                                bg='#D3D3D3', 
                                fg='black')
        reset_button.grid(row=6, column=1, padx=10, pady=10)

                # Create a reset button
        save_button = tk.Button(self.frame,
                                text='Reset', 
                                padx=40, 
                                pady=20, 
                                width=20, 
                                height=6, 
                                command=self.reset,
                                bg='#D3D3D3', 
                                fg='black')
        save_button.grid(row=6, column=2, padx=10, pady=10)

        # Display the frame
        self.frame.pack()

    def run(self):
        self.root.mainloop()


if __name__ == '__main__':
    interface = Interface()