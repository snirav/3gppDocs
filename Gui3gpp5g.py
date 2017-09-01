import Tkinter as tk
import tkMessageBox
from downloadDocs import *

class docDownloader(tk.Frame):
    def __init__(self, master):
        # Initialize window using the parent's constructor
        tk.Frame.__init__(self,
                          master,
                          width=400,
                          height=200)
        # Set the title
        self.master.title('5G Doc Downloader')
 
        # This allows the size specification to take effect
        self.pack_propagate(0)
 
        # We'll use the flexible pack layout manager
        self.pack()
 
        # Fill the  Website List
        self.webSiteList = ['http://www.3gpp.org/ftp/tsg_ran/WG1_RL1/TSGR1_']
        # + meetingNumber + '/Docs/'

        # Fill the designers List
        self.meetingEntries=['88b',
                             '90']
        # Website Selection Menu
        self.defaultWebsite = tk.StringVar()
        self.defaultWebsite.set('Please select the Website')
        self.websiteDropdown = tk.OptionMenu(self,
                                             self.defaultWebsite, *self.webSiteList)
                                     
        # Designer Selection Menu
        self.defaultMeeting = tk.StringVar()
        self.defaultMeeting.set('Please select the meeting number')
        self.meetingList = tk.OptionMenu(self,
                                         self.defaultMeeting, *self.meetingEntries)
 
        # Declaring the buttons and linking the functions
        self.textBox=tk.Text(xscrollcommand=set(), yscrollcommand=set(), height=5,width=5)
        
        self.download_button = tk.Button(self,
                                      text ='Download Documents',
                                      command=self.initiateDownload, height=2, width=15)

        self.QUIT = tk.Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] = self.quit

        # Put the controls on the form
        
        self.websiteDropdown.pack(fill=tk.X, side=tk.TOP)
        self.meetingList.pack(fill=tk.X, side=tk.TOP)
        self.download_button.pack(fill=tk.X, side=tk.TOP)
        self.textBox.pack(fill=tk.X, side=tk.TOP)
        self.QUIT.pack({"side": "left"})
        
    # Download handling routine
    def initiateDownload(self):
        downloadDocs(self.defaultWebsite.get(), self.defaultMeeting.get())
        tkMessageBox.showinfo("Downloading Status", "Downloading Completed Successfully!!")
        self.textBox.insert('1.0', "Downloading Completed Successfully!!","a")
     
    def run(self):
        ''' Run the app '''        
        self.mainloop()
 
app = docDownloader(tk.Tk())
app.run()
