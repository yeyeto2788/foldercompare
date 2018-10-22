"""
Lightweight cross-platform graphic interface for folder and '.zip' folders compare program.
"""

import getpass
import os
import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox

import foldercompare

class FolderComparisonGUI(tk.Frame):
    """
    The graphic interface for the application.

    Args:
        root: Description of parameter `root`.

    Attributes:
        folder1: String with the path of the folder1 or '.zip' folder1 to compare.
        folder2: String with the path of the folder2 or '.zip' folder2 to compare.
        folder_output: String with path where the output files will be located.
        filename: Name of '.txt' and '.csv' files that will be created.
        output_as_txt: Boolean to create or not the '.txt' file.
        output_as_csv: Boolean to create or not the '.txt' file.
        zip_work: Boolean to activate the selection of '.zip' folders as input for comparison.
        set_design_options: Function to set the widgets properties before placing them in the GUI.
        create_widgets: Create the widgets on GUI launch.
        set_dir_options: Function to set properties for selecting directories.
        set_file_options: Function to set properties for selecting '.zip' files.
        root
    """


    def __init__(self, root=None):
        tk.Frame.__init__(self, root)
        self.root = root
        self.root.iconbitmap(default=self.resource_path("icon_bk.ico"))
        # tkinter app variables -- .get() returns False until .set() otherwise
        self.folder1 = tk.StringVar()
        self.folder2 = tk.StringVar()
        self.folder_output = tk.StringVar()
        self.filename = tk.StringVar()
        self.output_as_txt = tk.BooleanVar()
        self.output_as_txt.set(1)
        self.output_as_csv = tk.BooleanVar()
        self.output_as_csv.set(1)
        self.zip_work = tk.BooleanVar()
        self.zip_work.set(1)

        self.set_design_options()
        self.create_widgets()
        self.set_dir_options()
        self.set_file_options()

    def resource_path(self, relative_path):
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
        return os.path.join(base_path, relative_path)

    def set_design_options(self):
        """
        Configure widget design options before placing them in GUI.

        Returns:
            Nothing.
        """

        self.root.title("Folder Comparison Tool")
        self.root.minsize(300, 200)
        self.button_options = {
            'fill': tk.constants.BOTH,
            'padx': 5,
            'pady': 5,
        }

    def create_widgets(self):
        """
        Create widgets on GUI launch.

        Returns:
            Nothing.
        """

        tk.Label(
            self, text='Folder Comparison Tool', font=16,
            ).pack()

        tk.Checkbutton(
            self, text='Work with .zip files', variable=self.zip_work,
        ).pack()

        tk.Button(
            self, text='Select Folder 1',
            command=lambda: self.define_selection(self.folder1),
            ).pack(**self.button_options)

        tk.Label(
            self, textvariable=self.folder1, fg="blue",
            ).pack()

        tk.Button(
            self, text='Select Folder 2',
            command=lambda: self.define_selection(self.folder2),
            ).pack(**self.button_options)

        tk.Label(
            self, textvariable=self.folder2, fg="blue",
            ).pack()

        tk.Button(
            self, text='Select Output Folder',
            command=lambda: self.set_directory(self.folder_output),
            ).pack(**self.button_options)

        tk.Label(
            self, textvariable=self.folder_output, fg="blue",
            ).pack()

        tk.Label(
            self, text="Choose a name for output file(s)",
            ).pack()

        tk.Entry(
            self, textvariable=self.filename
            ).pack()

        tk.Label(
            self, text='Select type(s) of output:'
            ).pack()

        tk.Checkbutton(
            self, text='.txt', variable=self.output_as_txt,
            ).pack()

        tk.Checkbutton(
            self, text='.csv', variable=self.output_as_csv,
            ).pack()

        tk.Button(
            self, text='Run', command=self.validate_and_run,
            ).pack(**self.button_options)

    def define_selection(self, variable):
        """
        Short summary.

        Args:
            variable: Description of parameter `variable`.

        Returns:
            Nothing.
        """
        if self.zip_work.get():
            self.set_filename(variable)
        else:
            self.set_directory(variable)

    def set_dir_options(self):
        """
        Configure widget action options for the selection of the directory after
        placing them in GUI.

        Returns:
            Nothing.
        """

        self.directory_options = {
            'initialdir': r'{}'.format(os.getcwd()),
            'parent': self.root,
            'mustexist': False,
            'title': 'Choose a directory',
        }

    def set_file_options(self):
        """
        Configure widget action options for the selection of a file after placing
        them in GUI.

        Returns:
            Nothing.
        """

        self.file_options = {
            'initialdir': r'{}'.format(os.getcwd()),
            'parent': self.root,
            'filetypes': (("Zip files", "*.zip"), ("all files", "*.*")),
            'title': 'Choose a .zip folder',
        }


    def set_filename(self, variable):
        """
        Return a selected directory name.

        Args:
            variable (tk.Variable): The tkinter variable to save selection as.
        Returns:
            Nothing.
        """

        selection = filedialog.askopenfilename(**self.file_options)
        variable.set(selection)

    def set_directory(self, variable):
        """
        Return a selected directory name.

        Args:
            variable (tk.Variable): The tkinter variable to save selection as.
        Returns:
            Nothing.
        """

        selection = filedialog.askdirectory(**self.directory_options)
        variable.set(selection)

    def validate_and_run(self):
        """
        Run the folder comparison program with user selected data, validate the
        paths or files selected.

        Returns:
            Nothing.
        """

        # Validate user inputs saved in tkinter variables
        folder1_is_valid = os.path.exists(self.folder1.get())
        folder2_is_valid = os.path.exists(self.folder2.get())
        folder_output_is_valid = os.path.exists(self.folder_output.get())
        output_name_valid = self.filename.get()
        output_type_selected = (self.output_as_txt.get() or
                                self.output_as_csv.get())

        # Show error if validation failed
        if not folder1_is_valid:
            messagebox.showerror("Error", "Folder 1 must be selected")
        elif not folder2_is_valid:
            messagebox.showerror("Error", "Folder 2 must be selected")
        elif not folder_output_is_valid:
            messagebox.showerror("Error", "Output Folder must be selected")
        elif not output_name_valid:
            messagebox.showerror(
                "Error", "Please enter a filename for output (excluding path)"
                )
        elif not output_type_selected:
            messagebox.showerror("Error", "Please select at least one option as output (.csv or .txt)")
        else:
            # Determine name for output file(s)
            folder = self.folder_output.get()
            filename = self.filename.get().split('.')[0]
            output_filename = os.path.join(folder, filename)

            # Run the folder compare program
            try:
                foldercompare.compare(self.folder1.get(), self.folder2.get(),
                                      output_filename,
                                      output_txt=self.output_as_txt.get(),
                                      output_csv=self.output_as_csv.get())
            except Exception:
                messagebox.showerror(
                    "Error", "An error has occurred, please try again."
                    )
            else:
                messagebox.showinfo("Success!", "Folder comparison complete")


if __name__ == '__main__':
    # Start the app in dev mode
    ROOT = tk.Tk()
    FolderComparisonGUI(ROOT).pack()
    ROOT.mainloop()
