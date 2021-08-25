import tkinter as tk
from tkinter import *
from tkinter import scrolledtext
from evemarketdata import *
from dhooks import Webhook
from monitor_hook import*

#creates alert setting window layouts for monitoring
class Alert(tk.Frame):
    def __init__(self,root, save_callback = None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._save_callback = save_callback
        self._draw()

    #calls save_monitor() when 'set' button of region/system is clicked, saves entries entered in setting menu  
    def save_setting(self):
        datatype = self.data_type_entry.get('1.0','end').rstrip()
        comparison = self.comparison_entry.get('1.0','end').rstrip()
        EV = self.EV_entry.get('1.0','end').rstrip()
        address = self.address_entry.get('1.0','end').rstrip()
        try:
            self._save_callback(datatype, comparison, EV, address)
            print('saved')
        except:
            pass

    def _draw(self):
        # data type label
        data_type_label = tk.Label(master = self, text="Data type")
        data_type_label.place(x = 30, y = 20, width = 80, height = 30)
        data_type_label.configure(font=("system", 5))
        # comparison label
        comparison_label = tk.Label(master = self, text="Comparison")
        comparison_label.place(x = 130, y = 20, width = 80, height = 30)
        comparison_label.configure(font=("system", 5))
        # expected value label
        EV_label = tk.Label(master = self, text="Expect Value")
        EV_label.place(x = 240, y = 20, width = 85, height = 30)
        EV_label.configure(font=("system", 5))

        # data type entry
        self.data_type_entry = tk.Text(master = self)
        self.data_type_entry.place(x = 30, y = 60, width = 80, height = 30)
        # comparison entry
        self.comparison_entry = tk.Text(master = self)
        self.comparison_entry.place(x = 130, y = 60, width = 80, height = 30)
        # expect value entry
        self.EV_entry = tk.Text(master = self)
        self.EV_entry.place(x = 240, y = 60, width = 80, height = 30)
        # address label
        address_label = Label(master = self, text="Webhook Address:")
        address_label.configure(font=("system", 5))
        address_label.place(x = 100, y = 120, width = 160, height = 30)
        # address entry
        self.address_entry = tk.Text(master = self)
        self.address_entry.insert('1.0', 'https://discord.com/api/webhooks/782044673698824233/hVV_BdumMCMjds5yW98U4oCeknHbnahmW0WMCxByMYx7nERdP1yGqoG4GIXyNsIkSrMO')
        self.address_entry.place(x = 40, y = 160, width = 300, height = 60)

        #set/save button
        save_btn = Button(master = self, text="Set")
        save_btn.configure(command=self.save_setting, font=("system", 5)) 
        save_btn.place(x = 130, y = 230, width = 120, height = 40)

        #help label
        help_label = tk.Label(master = self)
        help_label.configure(text = "Datatypes:\nminsell, avgsell, volsell, medsell, stdsell, varsell\nmaxbuy, avgbuy, volbuy, medbuy, stdbuy, varbuy\n\nComparisons:\n<=, >=\n\nExpected Values:\nEnter a desire value to monitor\n\nWebhook Address:\nEnter your discord webhook address.")
        help_label.configure(bg = 'grey94', anchor = 'nw', wraplengt=210)
        help_label.place(x = 360, y = 20, width = 220, height = 250)

#creates layouts for single mode
class single(tk.Frame):
    def __init__(self, root, switch_callback = None, place_set_callback = None, item_set_callback = None, search_callback = None, setting_callback = None , monitor_callback = None):
        tk.Frame.__init__(self, root)
        self.root = root
        self._switch_callback = switch_callback
        self._place_set_callback = place_set_callback
        self._item_set_callback = item_set_callback
        self._search_callback = search_callback
        self._monitor_callback = monitor_callback
        self.setting = setting_callback

        self.is_monitor_mode = tk.IntVar()
        self._draw()
    #calls placecheck() in class Main when 'set' button of region/system name is clicked
    def place_click(self):
        place = self.place_entry.get('1.0', 'end').rstrip()
        if place != '':
            self._place_set_callback(place)
        else:
            self.set_msg('Please enter a valid region/system name.')
    #calls itemcheck() in class Main when 'set' button of item name is clicked
    def item_click(self):
        item = self.item_entry.get('1.0', 'end').rstrip()
        self._item_set_callback(item)
    #calls switchmode() in class Main when 'mode_switch' button is clicked
    def mode_click(self):
        self._switch_callback()
    #calls alert_window() in class Main when 'Monitor Setting' button is clicked
    def alert_click(self):
        self.setting()
    #calls search() in class Main when 'Search' button is clicked
    def search_click(self):
        self._search_callback('single')
    #allows to set message on the frame quickly
    def set_msg(self, text):
        self.msg_frame.configure(text = text, anchor = 'n', wraplengt=250)
    #allows to set status on the frame quickly
    def set_status(self, text):
        self.status.configure(text = text, anchor = 'w')
    #allows to set monitor status on the frame quickly
    def set_monitor_status(self, text):
        self.monitor_status.configure(text = text, anchor = 'w')
    #allows to set data onto data_frame quickly
    def set_data(self, text):
        self.data_frame.configure(state = 'normal')
        self.data_frame.delete('1.0','end')
        self.data_frame.insert('1.0', str(text))
        self.data_frame.configure(state = 'disabled')
    #calls monitor_change() in class Main when 'Monitor Mode' check button is clicked
    def monitor_click(self):
        self._is_monitor = self.is_monitor_mode.get()
        print(self._is_monitor)
        self._monitor_callback(self._is_monitor)

    #draws main elements for single mode on the root
    def _draw(self):
        #System/Region label
        place_label = tk.Label(master = self,  text = 'System/Region ', bg = 'grey94', font=("system", 5))
        place_label.place(x = 20, y = 10, width = 100, height = 20)
        #System/Region entry
        self.place_entry = tk.Text(master = self, bg = 'white', font=("system", 5))           
        self.place_entry.place(x = 20, y = 30, width = 120, height = 40)                      
        #Set button for System/Region entry
        place_btn = tk.Button(master=self, text="Set", bg = 'grey94')
        place_btn.configure(command=self.place_click)
        place_btn.place(x = 150, y = 30, width = 50, height = 40)                               
        #Item Name label
        item_label = tk.Label(master = self,  text = 'Item Name ', bg = 'grey94', font=("system", 5))
        item_label.place(x = 320, y = 10, width = 80, height = 20)                             
        #Item Name entry
        self.item_entry = tk.Text(master = self, bg = 'white', font=("system", 5))             
        self.item_entry.place(x = 220, y = 30, width = 270, height = 40)                       
        #Set button for Item Name entry
        item_btn = tk.Button(master=self, text="Set", bg = 'grey94')
        item_btn.configure(command=self.item_click)
        item_btn.place(x = 500, y = 30, width = 50, height = 40)                               
        #Search button
        search_btn = tk.Button(master=self, text="Search", bg = 'grey94')
        search_btn.configure(command=self.search_click)
        search_btn.place(x = 570, y = 30, width = 100, height = 40)                           
        #Monitor menu button
        alert_btn = tk.Button(master=self, text="Monitor Setting", bg = 'grey94')                 
        alert_btn.configure(command=self.alert_click)
        alert_btn.place(x = 35, y = 90, width = 100, height = 40)                              
        #Mode label
        mode_label = tk.Label(master = self,  text = 'MODE: ', bg = 'grey94', font=("system", 5))
        mode_label.place(x = 10, y = 580, width = 100, height = 20)
        #Mode switch button
        mode_switch = tk.Button(master=self, text="Single Item", bg = 'grey94')
        mode_switch.configure(command=self.mode_click)
        mode_switch.place(x = 90, y = 575, width = 100, height = 30)
        #General status introductory label
        status_label = tk.Label(master = self,  text = 'Status: ', bg = 'grey94', font=("system", 5))
        status_label.place(x = 25, y = 550, width = 70, height = 20)
        #General status condition label
        self.status = tk.Label(master = self, bg = 'grey94')
        self.status.configure(text = 'Ready.', anchor = 'w', font=("system", 5))
        self.status.place(x = 95, y = 550, width = 150, height = 20)
        #data frame for displaying data after 'Search'
        self.data_frame = tk.Text(master = self, bg = 'white', font=("system", 5))
        self.data_frame.insert('1.0','data will be shown here.' + '\n'*36 + 'data will be shown here.')
        self.data_frame.place(x = 175, y = 90, width = 480, height = 300)                  
        self.data_frame.configure(state = 'disabled')
        #Message to show errors and suggestion
        self.msg_frame = tk.Label(master = self, bg = 'grey94')
        self.msg_frame.configure(text = 'messages will be shown here.', anchor = 'n', wraplengt=250, font=("system", 5))
        self.msg_frame.place(x = 250, y = 400, width = 250, height = 150)                  
        #Scrollbar for data frame
        data_frame_scrollbar = tk.Scrollbar(master=self, command=self.data_frame.yview)
        self.data_frame['yscrollcommand'] = data_frame_scrollbar.set
        data_frame_scrollbar.place(x = 644, y = 90, width = 30, height = 300)   
        #Activation check button for entering monitor mode
        self.chk_button = tk.Checkbutton(master=self, text="Monitor Mode", variable=self.is_monitor_mode, bg = 'grey94', font=("system", 5))
        self.chk_button.configure(command=self.monitor_click) 
        self.chk_button.place(x = 30, y = 140, width = 120, height = 30)      
        #Monitor status introductory label
        monitor_status_label = tk.Label(master = self,  text = 'Monitor Status: ', bg = 'grey94', font=("system", 5), wraplengt=100, anchor = 'n')
        monitor_status_label.place(x = 25, y = 500, width = 70, height = 40)
        #Monitor status condition label
        self.monitor_status = tk.Label(master = self, bg = 'grey94')
        self.monitor_status.configure(text = 'Ready.', anchor = 'w', font=("system", 5))
        self.monitor_status.place(x = 95, y = 510, width = 150, height = 20)    

#creates layouts for batch mode
class Batch(tk.Frame):
    def __init__(self, window, switch_callback=None, place_set_callback = None, search_callback = None):
        Frame.__init__(self, window)
        self.window = window
        self.__switch_callback = switch_callback
        self._place_set_callback = place_set_callback
        self._search_callback = search_callback
        self._draw()
    #calls placecheck() in class Main when 'set' button of item name is clicked
    def place_b_click(self):               
        place = self.rs_entry.get('1.0', 'end').rstrip()
        if place != '':
            self._place_set_callback(place)
        else:
            self.set_msg('Please enter a valid region/system name.')       
    #calls search() in class Main when 'Search' button is clicked
    def search_b_click(self):
        items = self.item_txt.get('1.0', 'end').rstrip().split('\n')
        if items[-1][-3::] == 'ISK':
            self._search_callback(items)
        else:
            self.set_msg('Please check the formatting of your items.')
    #reset item frame
    def reset_itemframe(self):
        self.item_txt.delete('1.0','end')
    #allows to set message on the frame quickly
    def set_msg(self, text):
        self.msg_frame.configure(text = text, anchor = 'n', wraplengt=250)
    #allows to set data onto data_txt quickly
    def set_data(self, text):
        self.data_txt.configure(state = 'normal')
        self.data_txt.delete('1.0','end')
        self.data_txt.insert('1.0', str(text))
        self.data_txt.configure(state = 'disabled')
    #draws main elements for batch mode on the root
    def _draw(self):
        #Be Patient label
        be_patient = Label(master = self,  text = 'This might take several seconds to serveral minutes depends on the size, please wait patiently.', bg = 'grey94')
        be_patient.configure(anchor = 'n', wraplengt=310)
        be_patient.place(x = 280, y = 20, width = 400, height = 50)
        #System/Region label
        pr_label = Label(master = self,  text = 'System/Region', bg = 'grey94', font=("system", 5))    
        pr_label.place(x = 20, y = 10, width = 100, height = 20)                                        
        #System/Region entry
        self.rs_entry = tk.Text(master=self, bg = 'white', font=("system", 5))          
        self.rs_entry.place(x = 20, y = 30, width = 120, height = 40)                                       
        #Set button for System/Region entry
        set_btn = Button(master=self, text="Set", bg = 'grey94')
        set_btn.configure(command=self.place_b_click)              
        set_btn.place(x = 150, y = 30, width = 50, height = 40)
        #Message to show errors and suggestion
        self.msg_frame = tk.Label(master = self, bg = 'grey94')
        self.msg_frame.configure(text = 'messages will be shown here.', anchor = 'n', wraplengt=250, font=("system", 5))
        self.msg_frame.place(x=320, y=330, width=350, height=200)
        #item label
        item_label = Label(master=self, text="Items")
        item_label.place(x=10, y=70, width=80, height=30)
        #item entry
        self.item_txt = scrolledtext.ScrolledText(master=self)
        self.item_txt.place(x=10, y=100, width=310, height=430)
        self.item_txt.config(highlightbackground="WhiteSmoke")
        #clear item entry
        clr_btn = Button(master=self, text="clear")
        clr_btn.configure(command=self.reset_itemframe)
        clr_btn.place(x=265, y=530, width=40, height=20)
        #data label
        data_label = Label(master=self, text="Data")
        data_label.place(x=320, y=70, width=50, height=30)
        #data text area to show batch search result
        self.data_txt = scrolledtext.ScrolledText(self.window, width=45, height=10)
        self.data_txt.place(x=320, y=100, width=350, height=200)
        self.data_txt.config(highlightbackground="WhiteSmoke")
        self.data_txt.configure(state='disabled')
        #General status introductory label
        conn_status_label = Label(master = self,  text = 'Status: ', bg = 'grey94', font=("system", 5))
        conn_status_label.place(x = 25, y = 550, width = 70, height = 20)
        #General status condition label
        self.status = tk.Label(master = self, bg = 'grey94')
        self.status.configure(text = 'Ready.', anchor = 'w', font=("system", 5))
        self.status.place(x = 95, y = 550, width = 150, height = 20)
        #Mode label
        mode_label = Label(master=self, text="MODE: ", bg="WhiteSmoke", font=("system", 5))      
        mode_label.place(x = 10, y = 580, width = 100, height = 20)
        #Mode switch button
        single_btn = Button(master=self, text="Batch Items")
        single_btn.place(x = 90, y = 575, width = 100, height = 30)
        single_btn.configure(command=self.__switch_callback)
        #Search button
        search_b_btn = tk.Button(master=self, text="Search", bg = 'grey94')
        search_b_btn.configure(command=self.search_b_click)
        search_b_btn.place(x = 220, y = 30, width = 100, height = 40)


#This class is use to execute commands for setting menu/single mode/batch mode
class Main(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        self.root = root
        self.current = marketdata()
        self.current_b = batch()
        # define this switch variable used to indicate the mode
        # False indicate that switch to batch, True indicate that
        # switch to single
        self.switch = False
        self._draw()
    #calls Alert class and creates its root
    def alert_window(self):
        setting_menu = tk.Tk()
        setting_menu.geometry("600x300")
        setting_menu.option_add('*tearOff', False)
        setting_menu.resizable(0, 0)
        setting_menu.title('Monitor Setting')
        self.alert = Alert(setting_menu, save_callback = self.save_monitor)
        self.alert.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
    #quit the program
    def close(self):
        self.root.destroy()
    #change format of number in data for display (ex: 1000000 -> 1,000,000)
    def pv(self, num):
        number = float(num)
        return ("{:,}".format(number)) 
    #save variables entered in monitor menu and close the window
    def save_monitor(self, datatype, comparison, EV, address):
        self.mon_datatype = datatype
        self.mon_comparison = comparison
        self.mon_EV = EV
        self.mon_address = address
        self.alert.root.destroy()
    #switch between single and batch mode
    def switchmode(self):
        if not self.switch:
            self.batch = Batch(self.root, switch_callback=self.switchmode, place_set_callback = self.placecheck, search_callback = self.search)
            self.batch.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
            self.single.destroy()
        else:
            self.single = single(self.root, switch_callback=self.switchmode, place_set_callback = self.placecheck, item_set_callback = self.itemcheck, search_callback = self.search, setting_callback = self.alert_window, monitor_callback = self.monitor_changed)
            self.single.pack(fill=tk.BOTH, side=tk.TOP, expand=True)
            self.batch.destroy()
        self.switch = not self.switch
        print("switch is: {}".format(self.switch))
    #check validity of place name using local files
    def placecheck(self, place):
        self.current.place = place.lower()
        self.current_b.place = place.lower()
        if self.switch == False:
            try:
                self.current.checkplace()
                self.single.set_msg(f'{place} : Valid.')
            except FilesNotFoundError:
                self.single.set_msg('Current folder is missing a system/region id file.')
            except PlaceNameError:
                self.single.set_msg('Please enter a valid region/system name.')
        else:
            try:
                self.current_b.checkplace_b()
                self.batch.set_msg(f'{place} : Valid.')
            except FilesNotFoundError:
                self.batch.set_msg('Current folder is missing a system/region id file.')
            except PlaceNameError:
                self.batch.set_msg('Please enter a valid region/system name.')
    #checking validity of item name using apib
    def itemcheck(self, item):
        self.current.item = item
        try:
            self.current.checkitem()
            self.single.set_msg(f'{item} : Valid.')
        except ItemNameError:
            self.single.set_msg('Please enter a valid item name.')
    #enters monitor mode when check button is click(and get stucked)
    def monitor_changed(self, value:bool):
        if value == 1:
            self.is_monitor = True
            if all(hasattr(self.current, attr) for attr in ['item_id','place_id','placetype']):
                if all(hasattr(self, attr) for attr in ['mon_datatype','mon_comparison','mon_EV','mon_address']):
                    active_mon = Monitor_data(item = self.current.item ,place = self.current.place, place_id = self.current.place_id, placetype = self.current.placetype, datatype =self.mon_datatype, comparison = self.mon_comparison,
                     expected_price = self.mon_EV, discord_hook =  self.mon_address)
                    active_mon.generate_data()
                    active_mon.data_solving()
                    self.single.set_monitor_status("Monitoring")
            else:
                self.single.set_msg('Please set place and item name before trying to monitor.')
        else:
            self.single.set_monitor_status("Rest")
            self.is_monitor = False
    #generates price data for single item of a batch of items
    def search(self, mode):
        if mode == 'single':
            if all(hasattr(self.current, attr) for attr in ['item_id','place_id','placetype']):
                try:
                    item = self.current.getprice()
                    sells = f'SELL:\nMinimum: {self.pv(self.current.minsell)}\nAverage: {self.pv(self.current.avgsell)}\nVolume: {self.pv(self.current.volsell)}\nMedian: {self.pv(self.current.medsell)}\nStandard Deviation: {self.pv(self.current.stdsell)}\nVariance: {self.pv(self.current.varsell)}'
                    buys = f'BUY:\nManximum: {self.pv(self.current.maxbuy)}\nAverage: {self.pv(self.current.avgbuy)}\nVolume: {self.pv(self.current.volbuy)}\nMedian: {self.pv(self.current.medbuy)}\nStandard Deviation: {self.pv(self.current.stdbuy)}\nVariance: {self.pv(self.current.varbuy)}'
                    data = sells + '\n'*3 + buys
                    self.single.set_data(data)
                    self.single.set_msg('Data Loaded.')
                except MarketerServerError:
                    self.single.set_msg('The evemarketer server is down, please try it later.')
            else:
                self.single.set_msg('Please set item and place first.')
        elif type(mode) is list:
            self.current_b.proccessfile(mode)
            if all(hasattr(self.current_b, attr) for attr in ['place_id','placetype']):
                try:
                    self.current_b.getprices()
                    totvol = self.current_b.totvolume
                    totsell = self.current_b.totalsell
                    totbuy = self.current_b.totalbuy
                    data = f'Total Volume: {self.pv(totvol)} ISK\nTotal Sell: {self.pv(totsell)} ISK\nTotal Buy: {self.pv(totbuy)} ISK'
                    self.batch.set_data(data)
                    self.batch.set_msg('Data Loaded.')
                except MarketerServerError:
                    self.batch.set_msg('The evemarketer server is down, please try it later.')
            else:
                self.batch.set_msg('Please set place first.')
    #draws main elements for single mode on the root
    def _draw(self):
        menu_bar = tk.Menu(self.root)
        self.root['menu'] = menu_bar
        menu_options = tk.Menu(menu_bar)
        menu_bar.add_cascade(menu = menu_options, label = 'Options')
        menu_options.add_command(label='Close', command = self.close)

        self.single = single(self.root, switch_callback=self.switchmode, place_set_callback = self.placecheck, item_set_callback = self.itemcheck, search_callback = self.search, setting_callback = self.alert_window, monitor_callback = self.monitor_changed)
        self.single.pack(fill=tk.BOTH, side=tk.TOP, expand=True)


if __name__ == "__main__":
    #initializing the program
    main = tk.Tk()
    main.title("EVE Market Data")

    main.geometry("700x620")

    main.option_add('*tearOff', False)

    Main(main)

    main.update()
    main.resizable(0, 0)
    main.mainloop()
