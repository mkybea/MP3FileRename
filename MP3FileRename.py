#!/usr/bin/env python3
"""
Final Project: A program that renames media files within a directory based on their metadata.

Author: Katie

Date: 8/1/2019
"""

#######################################################################
#                       MODULES AND FILES USED                        #
#######################################################################
# These are open-source software released under the terms of the GNU: #
#        General Public License. For more information visit:          #
#           https://www.gnu.org/licenses/gpl-3.0.en.html              #
#######################################################################
#       File: breezypythongui.py                                      #
#       Version: 1.1                                                  #
#       Copyright 2012, 2013 by Ken Lambert and Martin Osborne        #
#       Website: https://lambertk.academic.wlu.edu                    #
#######################################################################
#       File(s): eyed3                                                #
#       Revision 79395e79.                                            #
#       Copyright 2002-2017, Travis Shirk                             #
#       Website: http://eyed3.nicfit.net/                             #
#######################################################################


import os
import eyed3
from breezypythongui import EasyFrame
from tkinter import END


class FileRename(EasyFrame):
        """A mp3 renaming program."""
        def __init__(self):
                """Sets up the window"""
                EasyFrame.__init__(self, title = "MP3 File Rename", background="#FDEADB", resizable=False)
                EasyFrame.addLabel(self, text="Welcome!", font=("Verdana",50, "italic"), background="#FDEADB", row=1, column=1)
                
                # Label and field for directory path.
                EasyFrame.addLabel(self, text="Please enter the path of the directory containing files to rename:", background="#FDEADB", row=2, column=1)
                self.directory = EasyFrame.addTextField(self, text="", width = 100, row=3, column=1)
                self.directory.bind("<KeyPress-Return>", lambda event: self.rename())

                # Label and radio button options.
                EasyFrame.addLabel(self, text="What naming scheme would you like to use?", background="#FDEADB", row=4, column=1)
                self.statusGroup = EasyFrame.addRadiobuttonGroup(self, row=5, column=1)
                self.trackTitleAlbum = defaultRB = self.statusGroup.addRadiobutton("Track Number - Title - Album.mp3")
                self.titleAlbum = self.statusGroup.addRadiobutton("Title - Album.mp3")
                self.albumTrackTitle = self.statusGroup.addRadiobutton("Album - Track Number - Title.mp3")
                self.artistTitleAlbum = self.statusGroup.addRadiobutton("Artist - Title - Album.mp3")
                self.artistTitle = self.statusGroup.addRadiobutton("Artist - Title.mp3")
                self.statusGroup.setSelectedButton(defaultRB)

                # The rename Button.
                EasyFrame.addButton(self, text="Rename Now!", row=6, column=1, command=self.rename)

                # Output text field.
                self.process = EasyFrame.addTextArea(self, text="", row=7, column=1, width=50, height=20)

        def rename(self):
                """Obtains data from input fields and uses them to process files, showing the status in the output text area."""

                # Collect input and put it in a list.
                try:
                        audioList = os.listdir(self.directory.get())
                        self.process.setText("\n Getting files...\n") # Write to Process Box.
                # Error handling.
                except Exception as exception:
                        self.process.insert(END, "\n Error processing your input. Please try again.\n") # Write to Process Box.
                        self.process.insert(END, exception) # Write to Process Box.
                        EasyFrame.messageBox(self, title="Error", message="Error processing your input. Please try again.")
                        raise

                # Go through each individual file.
                count = 0
                for fileName in audioList:
                        if ".mp3" in fileName:
                                count += 1
                                self.process.insert(END, "\n"+fileName) # Write to Process Box.
                                directory = self.directory.get()
                                audiofilePath = directory + "/" + fileName
                                audiofile = eyed3.load(audiofilePath)
                                nameScheme = self.statusGroup.getSelectedButton()["value"]
                                
                                # Test for the radio button input and rename accordingly.
                                if nameScheme == "Track Number - Title - Album.mp3":
                                        self.process.insert(END, "\n... Converting ...") # Write to Process Box.
                                        new_audiofilePath = directory + "/{0} - {1} - {2}"
                                        new_fileName = new_audiofilePath.format(audiofile.tag.track_num[0], audiofile.tag.title, audiofile.tag.album)
                                        os.rename(audiofilePath, new_fileName+".mp3")
                                        renamedFile = new_fileName.split("/")[-1]
                                        self.process.insert(END, "\nDone! \n"+renamedFile+".mp3\n") # Write to Process Box.
                                if nameScheme == "Title - Album.mp3":
                                        self.process.insert(END, "\n... Converting ...") # Write to Process Box.
                                        new_audiofilePath = directory + "/{0} - {1}"
                                        new_fileName = new_audiofilePath.format(audiofile.tag.title, audiofile.tag.album)
                                        os.rename(audiofilePath, new_fileName+".mp3")
                                        renamedFile = new_fileName.split("/")[-1]
                                        self.process.insert(END, "\nDone! \n"+renamedFile+".mp3\n") # Write to Process Box.
                                if nameScheme == "Album - Track Number - Title.mp3":
                                        self.process.insert(END, "\n... Converting ...") # Write to Process Box.
                                        new_audiofilePath = directory + "/{0} - {1} - {2}"
                                        new_fileName = new_audiofilePath.format(audiofile.tag.album, audiofile.tag.track_num[0], audiofile.tag.title)
                                        os.rename(audiofilePath, new_fileName+".mp3")
                                        renamedFile = new_fileName.split("/")[-1]
                                        self.process.insert(END, "\nDone! \n"+renamedFile+".mp3\n") # Write to Process Box.
                                if nameScheme == "Artist - Title - Album.mp3":
                                        self.process.insert(END, "\n... Converting ...") # Write to Process Box.
                                        new_audiofilePath = directory + "/{0} - {1} - {2}"
                                        new_fileName = new_audiofilePath.format(audiofile.tag.artist, audiofile.tag.title, audiofile.tag.album)
                                        os.rename(audiofilePath, new_fileName+".mp3")
                                        renamedFile = new_fileName.split("/")[-1]
                                        self.process.insert(END, "\nDone! \n"+renamedFile+".mp3\n") # Write to Process Box.
                                if nameScheme == "Artist - Title.mp3":
                                        self.process.insert(END, "\n ... Converting ...") # Write to Process Box.
                                        new_audiofilePath = directory + "/{0} - {1}"
                                        new_fileName = new_audiofilePath.format(audiofile.tag.artist, audiofile.tag.title)
                                        os.rename(audiofilePath, new_fileName+".mp3")
                                        renamedFile = new_fileName.split("/")[-1]
                                        self.process.insert(END, "\nDone! \n"+renamedFile+".mp3\n") # Write to Process Box.

                # Error handling if not mp3 file.
                if count == 0:
                        self.process.insert(END, "\n There are no .mp3 files to convert.") # Write to Process Box.
                                
                # Show Completion confirmation.
                else:
                        self.process.insert(END, "\n Renaming Complete! \n \n"+str(count)+" files were renamed!") # Write to Process Box.

def main():
        """Instantiate and popup the GUI."""
        FileRename().mainloop()

if __name__ == "__main__":
        main()
