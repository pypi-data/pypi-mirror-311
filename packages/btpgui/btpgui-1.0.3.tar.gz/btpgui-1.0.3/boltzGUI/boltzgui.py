# -*- coding: utf-8 -*-
#
# copyright (c) 06-2024 G. Benabdellah
# Departement of physic
# University of Tiaret , Algeria
# E-mail ghlam.benabdellah@gmail.com
#
# this program is part of btpgui 
# first creation 15-11-2024
#  
#
# License: GNU General Public License v3.0
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#  log change:
#
#
#

import tkinter as tk
from tkinter import Frame,ttk, messagebox, filedialog
import subprocess
import os
import sys
import glob


class BoltzTraP_GUI:
    def __init__(self, root):
        self.root = root
        self.root.title("BoltzTraP2 Interface")
        self.root.geometry("900x900")  # Increased window size

        # Create a Canvas for scrolling
        self._canvas(root)
        # Set the initial base path
        self.perl_script_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))  #os.getcwd()
        self.base_path = os.getcwd() #
        self.case = os.path.basename(self.base_path)

        # Create a section for selecting and displaying the directory
        self.create_directory_section()

        # Initialize the main sections
        self.buttons = []
        self.kdenser_for_wien2k()
        self.interpolate_boltz()
        self.integrate_boltz()
        self.dope_boltz()
        self.create_plot_boltz_section()
      #  self.create_open_stdout_button()
        self.create_output_section()
        
        
    def _canvas(self, root):
        """Create a scrollable canvas with vertical and horizontal scrollbars."""
        # Create canvas
        self.canvas = tk.Canvas(root)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a frame inside the canvas
        self.frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.frame, anchor=tk.NW)

        # Add vertical scrollbar
        v_scrollbar = tk.Scrollbar(root, orient=tk.VERTICAL, command=self.canvas.yview, bg="blue")
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.canvas.config(yscrollcommand=v_scrollbar.set)

        # Add horizontal scrollbar
        h_scrollbar = tk.Scrollbar(root, orient=tk.HORIZONTAL, command=self.canvas.xview, bg="black")
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.config(xscrollcommand=h_scrollbar.set)

        # Configure scroll region to update dynamically
        self.frame.bind("<Configure>", lambda event: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

        # Mouse-wheel scroll bindings
        self.canvas.bind_all("<MouseWheel>", lambda event: self.canvas.yview_scroll(-1 * int(event.delta / 120), "units"))
        self.canvas.bind_all("<Shift-MouseWheel>", lambda event: self.canvas.xview_scroll(-1 * int(event.delta / 120), "units"))
    
    def create_output_section(self):
        """Section to display command outputs."""
        frame = self.custom_label( text="Command Output")
        open_stdout_button = tk.Button(frame, text="Open Log File", command=self.open_stdout_file)
        open_stdout_button.pack(pady=5)
       
        self.output_text = tk.Text(frame, height=50, wrap="word")
        self.output_text.pack(fill="both", expand=True)
        
        
    def custom_label(self, text, padding=10):
        """Create a custom-labeled section with a green border and bold text."""
        # Outer frame for green border
        outer_frame = tk.Frame(self.frame, bg="green", padx=2, pady=2)
        outer_frame.pack(fill="x", padx=10, pady=5)

        # Style for the LabelFrame
        style = ttk.Style()
        style.configure("Custom.TLabelframe.Label", foreground="green", font=("Arial", 12, "bold"))

        # Inner LabelFrame with custom style
        labelframe = ttk.LabelFrame(outer_frame, text=text, padding=padding, style="Custom.TLabelframe")
        labelframe.pack(fill="x")

        return labelframe

    def create_directory_section(self):
        """Create a section to browse and display the working directory."""
        frame = self.custom_label(text="PATH:")

        # Browse button to select directory
        tk.Button(frame, text="select Directory", command=self.browse_directory).pack(side="left", padx=5)

        # Label to display the current directory
        self.directory_label = tk.Label(frame, text=f"Current Directory: {self.base_path}", fg="blue", anchor="w")
        self.directory_label.pack(side="left", fill="x", padx=5)
        tk.Label(frame, text="btpgui.copyright@ G.Benabdellah", fg="black", anchor="w").pack(side="right", fill="x", padx=5)
        

        # Button to change directory
        #tk.Button(frame, text="Set Current Directory", command=self.change_directory).pack(side="left", padx=5)
    def browse_directory(self):
        """Browse for a directory, defaulting to the current directory."""
        selected_directory = filedialog.askdirectory(initialdir=self.base_path)
        if selected_directory:  # Update only if a directory is selected
            self.base_path = selected_directory
            self.case = os.path.basename(selected_directory)  # Update the case
            self.directory_label.config(text=f"Current Directory: {self.base_path}")
            self.change_directory()
            self.case = os.path.basename(self.base_path)
    def change_directory(self):
        """Change the working directory to self.base_path."""
        try:
            os.chdir(self.base_path)  # Change the current working directory
            
            print(f"Working directory changed to: {self.base_path}")
        except Exception as e:
            print(f"Error changing directory: {e}")
    
    
    

    def open_stdout_file(self):
        stdout_file_path = f"{self.base_path}/STDOUT"  # Specify the path to your STDOUT file
        if os.path.exists(stdout_file_path):
            try:
                with open(stdout_file_path, 'r') as file:
                    file_content = file.read()
                new_window = tk.Toplevel(self.root)
                new_window.title("STDOUT File Content")
                new_window.geometry("600x400")  # Adjust size as needed
                text_frame = tk.Frame(new_window)
                text_frame.pack(fill="both", expand=True)

                text_widget = tk.Text(text_frame, wrap="word")
                text_widget.insert(tk.END, file_content)
                text_widget.config(state="disabled")  # Make text read-only
                text_widget.pack(side="left", fill="both", expand=True)

                # Add a vertical scrollbar
                scrollbar = tk.Scrollbar(text_frame, orient="vertical",bg="blue", command=text_widget.yview)
                scrollbar.pack(side="right", fill="y")
                text_widget.config(yscrollcommand=scrollbar.set)

            except Exception as e:
                messagebox.showerror("Error", f"Failed to open STDOUT file: {str(e)}")
        else:
            messagebox.showerror("File Not Found", "The STDOUT file does not exist.")



      

    def kdenser_for_wien2k(self):
        """Section for x kgen command."""
       
        frame = self.custom_label(text="Optional steps for WIEN2k users:")
        tk.Label(frame, text="Prepares a denser k-mesh :  x kgen").pack(anchor="w")

        # Input fields and button on the same row
        row_frame = tk.Frame(frame)
        row_frame.pack(fill="x", pady=5)
        tk.Button(row_frame, text="x kgen", command=self.run_kgen).pack(side="left", padx=5)
        # Entry for kpoint value
        tk.Label(row_frame, text="K-point Value:").pack(side="left", padx=5)
        self.kgen_value = tk.Entry(row_frame, width=12 ,bg="white")
        self.kgen_value.insert(0, "2000")  # Default value
        self.kgen_value.pack(side="left", padx=5)

        # Dropdown for shift value
        tk.Label(row_frame, text="Shift:").pack(side="left", padx=5)
        self.shift_value = ttk.Combobox(row_frame, values=["0", "1"], width=5, state="readonly")
        self.shift_value.set("0")  # Default value
        self.shift_value.pack(side="left", padx=5)
        
        # Checkbox for Spin Polarized
        row_frame = tk.Frame(frame)
        row_frame.pack(fill="x", pady=5)

        # Spin Polarized Checkbox
        self.spin_polarized_var = tk.BooleanVar(value=False)
        tk.Checkbutton(row_frame, text="Spin Polarized", variable=self.spin_polarized_var, command=self.toggle_spin_polarized).pack(side="left", padx=10)
        # Parallel Mode Checkbox
        self.parallel_flag_var = tk.BooleanVar(value=False)
        tk.Checkbutton(row_frame, text="Parallel Mode (-p)", variable=self.parallel_flag_var, command=self.toggle_parallel_mode).pack(side="left", padx=10)
        
        self.spin_orbit_var = tk.BooleanVar(value=False)
        tk.Checkbutton(row_frame, text="spin orbit (-so)", variable=self.spin_orbit_var, command=self.toggle_spin_orbit).pack(side="left", padx=10)
        
        self.spin_pot_var = tk.BooleanVar(value=False)
        tk.Checkbutton(row_frame, text="Orbital potentials (-orb)", variable=self.spin_pot_var).pack(side="left", padx=10)


        # Buttons to run lapw1
        row_frame = tk.Frame(frame)
        row_frame.pack(fill="x", pady=5)
        tk.Label(row_frame, text="Create eigenvalues at denser k-mesh ").pack(side="left", padx=5)
        self.up_button = tk.Button(frame, text=" x lapw1 -up", command=self.run_lapw1_up)
        self.dn_button = tk.Button(frame, text=" x lapw1 -dn", command=self.run_lapw1_dn)
        self.so_button = tk.Button(frame, text=" x lapwso ", command=self.run_lapwso)
        self.so_button.pack_forget()
        self.up_button.pack_forget()  # Initially hide -up button
        self.dn_button.pack_forget()  # Initially hide -dn button

        # Button for general x lapw1
        self.lapw1_button = tk.Button(frame, text=" x lapw1", command=self.run_lapw1)
        self.lapw1_button.pack(anchor="w", pady=5)
        self.gathering_energy()


    def gathering_energy(self):
        """Section for BoltzTraP2 commands."""
        frame = self.custom_label(text="Optional steps for WIEN2k users:gathering energy files ONLY in case wien2k parrallel calculation")
        row_frame = tk.Frame(frame)
        row_frame.pack(fill="x", pady=5)
        self.spin = tk.StringVar(value="")  # Default is -t (tau)
        tk.Radiobutton(row_frame, text="-up", variable=self.spin, value="-up").pack(side="left", padx=5)
        tk.Radiobutton(row_frame, text="-dn", variable=self.spin, value="-dn").pack(side="left", padx=5)
        self.gather_button = tk.Button(frame, text="gather_energy.pl", command=self.gather_energy)

    #def gather_energy(self):
        #"""Run the gather_energy.pl script."""
        
        #case_dir = self.case  # Replace with the correct directory or provide an entry field for this
        #spin_flag = self.spin_polarized_var.get() if self.spin_polarized_var.get() else ""
        #command = f"perl {self.perl_script_path}/gather_energys.pl {self.base_path}/{case_dir} {self.spin.get()}"
        #self.execute_command(command)

   
 

    def gather_energy(self):
        """Run the gather_energy.pl script."""
        # Clear the output section
        self.output_text.delete(1.0, tk.END)
        try:
            # Determine the full case directory
            case_dir = self.case
            full_case_dir = os.path.join(self.base_path, case_dir)

            # Check for required energy files
            energy_files = glob.glob(os.path.join(self.base_path, f"{case_dir}.energy_*")) + \
                        glob.glob(os.path.join(self.base_path, f"{case_dir}.energyso_*"))
            #print(f"Searching for files: {case_dir}.energy_* and {case_dir}.energyso_* in {self.base_path}")
            #print(f"Found energy files: {energy_files}")

            if not energy_files:
                message = (f"No matching files ({case_dir}.energy_* or {case_dir}.energyso_*) "
                        f"found in {self.base_path}. Ensure the directory and files are correct.\n")
                self.output_text.insert(tk.END, message)
                return

            # Determine spin flag
            spin_flag = self.spin.get() if self.spin_polarized_var.get() else ""

            # Construct the Perl command
            command = f"perl {self.perl_script_path}/gather_energys.pl {full_case_dir} {spin_flag}"
            self.output_text.insert(tk.END, f"Executing command: {command}\n")

            # Execute the command
            self.execute_command(command)

        except Exception as e:
            # Handle exceptions with detailed feedback
            error_message = (f"An error occurred during gather_energy execution:\n{str(e)}\n"
                            f"Directory: {full_case_dir}\n")
            self.output_text.insert(tk.END, error_message)



    def run_kgen(self):
        """Run x kgen command with specified values."""
        try:
            kgen_value = int(self.kgen_value.get())  # Ensure input is an integer
            shift_value = int(self.shift_value.get())  # Get the shift value from dropdown

            # Construct the command
            command = f"x kgen <<EOF\n{kgen_value}\n{shift_value}\nEOF"

            # Execute the command
            self.execute_command(command)
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid integer for kgen and shift.")

       


       
    def toggle_spin_polarized(self):
        """Toggle visibility of buttons based on Spin Polarized selection."""
        if self.spin_polarized_var.get():
            self.lapw1_button.pack_forget()  # Hide the generic button
            self.up_button.pack(anchor="w", pady=5)  # Show -up button
            self.dn_button.pack(anchor="w", pady=5)  # Show -dn button
        else:
            self.up_button.pack_forget()  # Hide -up button
            self.dn_button.pack_forget()  # Hide -dn button
            self.lapw1_button.pack(anchor="w", pady=5)  # Show the generic button

    def toggle_parallel_mode(self):
        """Toggle visibility of the Gather Energy button based on Parallel Mode."""
        if self.parallel_flag_var.get():
            self.gather_button.pack(anchor="w", pady=5)  # Show Gather Energy if Spin Polarized
            self.update_lapw1_button_text()  # Update generic button for Parallel Mode
        else:
            self.gather_button.pack_forget()  # Hide Gather Energy button
            self.update_lapw1_button_text()  # Update generic button for non-Parallel Mode
            
    def toggle_spin_orbit(self):
        """Toggle visibility of buttons based on Spin Polarized selection."""
        if self.spin_orbit_var.get():
            self.so_button.pack(anchor="w", pady=5) 
        else:
            self.so_button.pack_forget()  # Hide -up button
            

    def update_lapw1_button_text(self):
        """Update text of the generic lapw1 button based on Parallel Mode."""
        parallel_flag = "-p" if self.parallel_flag_var.get() else ""
        self.lapw1_button.config(text=f" x lapw1 {parallel_flag}")
        self.up_button.config(text=f" x lapw1 -up {parallel_flag}") 
        self.dn_button.config(text=f" x lapw1 -dn {parallel_flag}") 
        

    def run_lapw1_up(self):
        """Run x lapw1 -up command."""
        parallel_flag = "-p" if self.parallel_flag_var.get() else ""
        self.execute_command(f"x lapw1 {parallel_flag} -up")

    def run_lapw1_dn(self):
        """Run x lapw1 -dn command."""
        parallel_flag = "-p" if self.parallel_flag_var.get() else ""
        self.execute_command(f"x lapw1 {parallel_flag} -dn")

    def run_lapw1(self):
        """Run x lapw1 command."""
        parallel_flag = "-p" if self.parallel_flag_var.get() else ""
        self.execute_command(f"x lapw1 {parallel_flag}")
    def run_lapwso(self):
        """Run x lapw1 command."""
        parallel_flag = "-p" if self.parallel_flag_var.get() else ""
        spin = "-up" if self.spin_polarized_var.get() else ""
        orb  = "-orb" if self.spin_pot_var.get() else ""
        self.execute_command(f"x lapwso {parallel_flag} {spin} {orb}")
    
    def interpolate_boltz(self):
        """Section for running the BoltzTraP command."""
        #frame = ttk.LabelFrame(self.root, text="1. Run BoltzTraP: interpolate", padding=10)
        #frame.pack(fill="x", padx=10, pady=5)
        frame = self.custom_label(text="1. Run BoltzTraP: interpolate")
        # Create a row for inputs
        row_frame = tk.Frame(frame)
        row_frame.pack(fill="x", pady=5)
        
        ####tk.Button(row_frame, text="btp2 interpolate", command=lambda: self.run_boltztrap(mode="interpolate")).pack(side="left", padx=5)
         
        interpolate_button = tk.Button(row_frame, text="btp2 interpolate", command=lambda: self.run_boltztrap(mode="interpolate", button=interpolate_button))
        interpolate_button.pack(side="left", padx=5)
        self.buttons.append(interpolate_button)
          
        # Entry for -n flag
        tk.Label(row_frame, text="-n:").pack(side="left", padx=5)
        self.n_value = tk.StringVar(value="2")
        tk.Entry(row_frame, textvariable=self.n_value, width=10,  bg="white" ).pack(side="left", padx=5)

        # Entry for -o flag
        tk.Label(row_frame, text="-output:").pack(side="left", padx=5)
        self.o_value = tk.StringVar(value=f"{self.case}")
        tk.Entry(row_frame, textvariable=self.o_value, width=15,  bg="white").pack(side="left", padx=5)

        # Entry for -e flag
        tk.Label(row_frame, text="Emin:").pack(side="left", padx=5)
        self.e_value = tk.StringVar(value="-0.20")
        tk.Entry(row_frame, textvariable=self.e_value, width=10,  bg="white").pack(side="left", padx=5)

        # Entry for -E flag
        tk.Label(row_frame, text="-Emax:").pack(side="left", padx=5)
        self.E_value = tk.StringVar(value="0.2")
        tk.Entry(row_frame, textvariable=self.E_value, width=10,  bg="white").pack(side="left", padx=5)

    # Entry for -m flag
        tk.Label(row_frame, text="-m:").pack(side="left", padx=5)
        self.m_value = tk.StringVar(value="8")
        self.m_entry = tk.Entry(row_frame, textvariable=self.m_value, width=10,  bg="white")
        self.m_entry.pack(side="left", padx=5)

        # Entry for -k flag
        tk.Label(row_frame, text="-k:").pack(side="left", padx=5)
        self.k_value = tk.StringVar(value="")
        self.k_entry = tk.Entry(row_frame, textvariable=self.k_value, width=10,  bg="white")
        self.k_entry.pack(side="left", padx=5)

        # Set up value tracing
        self.m_value.trace_add("write", self.toggle_k_value)
        self.k_value.trace_add("write", self.toggle_m_value)
        
        self.d_mode = tk.BooleanVar(value=False)  # Default is unchecked (False)
        self.a_mode = tk.BooleanVar(value=False)  # Default is unchecked (False)
    
        tk.Checkbutton(row_frame, text="-d", variable=self.d_mode).pack(side="left", padx=5)
        tk.Checkbutton(row_frame, text="-a", variable=self.a_mode).pack(side="left", padx=5)

        
        h_interpolate_button = tk.Button(row_frame, text="?", command=lambda: self.run_boltztrap(mode="h_interpolate", button=h_interpolate_button),  bg="#DFF6FF",  activebackground="#B2EBF2" )
        h_interpolate_button.pack(side="left", padx=5)
        self.buttons.append(h_interpolate_button)

        # Run button
       

    def toggle_k_value(self, *args):
        """Disable k_value entry if m_value is set."""
        if self.m_value.get().strip():
            self.k_entry.config(state="disabled")
        else:
            self.k_entry.config(state="normal")

    def toggle_m_value(self, *args):
        """Disable m_value entry if k_value is set."""
        if self.k_value.get().strip():
            self.m_entry.config(state="disabled")
        else:
            self.m_entry.config(state="normal")

    def integrate_boltz(self):
        """Section for running the BoltzTraP integrate command."""
        #frame = ttk.LabelFrame(self.root, text="2. Run BoltzTraP: Integrate", padding=10)
        #frame.pack(fill="x", padx=10, pady=5)
        frame = self.custom_label(text="2. Run BoltzTraP: Integrate")
        row_frame = tk.Frame(frame)
        row_frame.pack(fill="x", pady=5)
        # button
        integrate_button = tk.Button(row_frame, text="btp2 integrate", command=lambda: self.run_boltztrap(mode="integrate", button=integrate_button))
        integrate_button.pack(side="left", padx=5)
        self.buttons.append(integrate_button)
        # Entry for -n flag
        tk.Label(row_frame, text="-n:").pack(side="left", padx=5)
        self.n_value_int = tk.StringVar(value="2")
        tk.Entry(row_frame, textvariable=self.n_value_int, width=10,  bg="white").pack(side="left", padx=5)
        # Entry for input file
        tk.Label(row_frame, text="Input file:").pack(side="left", padx=5)
        self.input_file = tk.StringVar(value=f"{self.case}.bt2")
        tk.Entry(row_frame, textvariable=self.input_file, width=15,  bg="white", state="disabled").pack(side="left", padx=5)
        # Entry for temperature range/or value
        tk.Label(row_frame, text="Temperature:").pack(side="left", padx=5)
        self.temperature_value = tk.StringVar(value="100:1000:50")
        tk.Entry(row_frame, textvariable=self.temperature_value, width=20,  bg="white").pack(side="left", padx=5)
        # Entry for SCISSOR value
        tk.Label(row_frame, text="SCISSOR: ").pack(side="left", padx=5)
        self.s_value = tk.StringVar(value="")
        tk.Entry(row_frame, textvariable=self.s_value, width=10,  bg="white").pack(side="left", padx=5)
        # Entry for bins value
        tk.Label(row_frame, text="bins:").pack(side="left", padx=5)
        self.b_value = tk.StringVar(value="1200")
        tk.Entry(row_frame, textvariable=self.b_value, width=10,  bg="white").pack(side="left", padx=5)
        # Radio buttons for selecting the mode (-t(tau) or -l (lambda)
        self.l_mode = tk.StringVar(value="-t")  # Default is -t (tau)
        tk.Radiobutton(row_frame, text="Tau (-t)", variable=self.l_mode, value="-t").pack(side="left", padx=5)
        tk.Radiobutton(row_frame, text="Lambda (-l)", variable=self.l_mode, value="-l").pack(side="left", padx=5)
            
        # help command
        h_integrate_button = tk.Button(row_frame, text="?", command=lambda: self.run_boltztrap(mode="h_integrate", button=h_integrate_button),  bg="#DFF6FF",  activebackground="#B2EBF2" )
        h_integrate_button.pack(side="left", padx=5)
        self.buttons.append(h_integrate_button)
    
    
    def dope_boltz(self):
        """Section for running the BoltzTraP dope command."""
        #frame = ttk.LabelFrame(self.root, text="3. Run BoltzTraP: Doping", padding=10)
        #frame.pack(fill="x", padx=10, pady=5)
        frame = self.custom_label(text="3. Run BoltzTraP: Doping")
        row_frame = tk.Frame(frame)
        row_frame.pack(fill="x", pady=5)
        #button
        dope_button = tk.Button(row_frame, text="btp2 dope", command=lambda: self.run_boltztrap(mode="dope", button=dope_button)) 
        dope_button.pack(side="left", padx=5)
        self.buttons.append(dope_button)

        # Entry for -n flag
        tk.Label(row_frame, text="-n:").pack(side="left", padx=5)
        self.n_value_dope = tk.StringVar(value="2")
        tk.Entry(row_frame, textvariable=self.n_value_dope, width=10,  bg="white").pack(side="left", padx=5)
        # Entry for input file
        tk.Label(row_frame, text="Input file:").pack(side="left", padx=5)
        self.input_file_dope = tk.StringVar(value=f"{self.case}.bt2")
        tk.Entry(row_frame, textvariable=self.input_file_dope, width=15,  bg="white", state="disabled").pack(side="left", padx=5)

        tk.Label(row_frame, text="Temperature:").pack(side="left", padx=5)
        self.temperature_value = tk.StringVar(value="100:1000:50")
        tk.Entry(row_frame, textvariable=self.temperature_value, width=20,  bg="white").pack(side="left", padx=5)
        # Entry for -sissor flag
        tk.Label(row_frame, text="SCISSOR: ").pack(side="left", padx=5)
        self.sd_value = tk.StringVar(value="")
        tk.Entry(row_frame, textvariable=self.sd_value, width=10,  bg="white").pack(side="left", padx=5)
        # Entry for -b flag
        tk.Label(row_frame, text="bins:").pack(side="left", padx=5)
        self.b_value = tk.StringVar(value="1200")
        tk.Entry(row_frame, textvariable=self.b_value, width=10,  bg="white").pack(side="left", padx=5)
        
        # Radio buttons for selecting the mode (-t or -l)
        self.l_mode = tk.StringVar(value="-t")  
        tk.Radiobutton(row_frame, text="Tau (-t)", variable=self.l_mode, value="-t").pack(side="left", padx=5)
        tk.Radiobutton(row_frame, text="Lambda (-l)", variable=self.l_mode, value="-l").pack(side="left", padx=5)
        # Entry for doping range
        tk.Label(row_frame, text="Doping Range:").pack(side="left", padx=5)
        self.doping_range = tk.StringVar(value="-1e20:1e20:1e19")
        tk.Entry(row_frame, textvariable=self.doping_range, width=30,  bg="white").pack(side="left", padx=5)
        h_dope_button = tk.Button(row_frame, text="?", command=lambda: self.run_boltztrap(mode="h_dope", button=h_dope_button),  bg="#DFF6FF",  activebackground="#B2EBF2" )
        h_dope_button.pack(side="left", padx=5)
        self.buttons.append(h_dope_button)

    def create_plot_boltz_section(self):
        """Section for running the plot_boltz command."""
        #frame = ttk.LabelFrame(self.root, text="4. Run Plot Boltz", padding=10)
        #frame.pack(fill="x", padx=10, pady=5)
        frame = self.custom_label(text="4. Run Plot Boltz")
        row_frame = tk.Frame(frame)
        row_frame.pack(fill="x", pady=5)
       
        plot_button = tk.Button(row_frame, text="Plot", command=lambda: self.run_boltztrap(mode="plot", button=plot_button)) 
        plot_button.pack(side="left", padx=5)
        self.buttons.append(plot_button)     
       
        tk.Label(row_frame, text=":").pack(side="left", padx=5)

        # Checkboxes for categories
        self.c_xx = tk.BooleanVar(value=True)
        self.c_yy = tk.BooleanVar(value=False)
        self.c_zz = tk.BooleanVar(value=False)
        tk.Checkbutton(row_frame, text="xx", variable=self.c_xx).pack(side="left", padx=5)
        tk.Checkbutton(row_frame, text="yy", variable=self.c_yy).pack(side="left", padx=5)
        tk.Checkbutton(row_frame, text="zz", variable=self.c_zz).pack(side="left", padx=5)

        # Radio buttons for -s flag (S or N)
        self.ut_flag = tk.StringVar(value="-u")  # Default is "S"
        tk.Label(row_frame, text="Selection)").pack(side="left", padx=5)
        tk.Radiobutton(row_frame, text="-u", variable=self.ut_flag, value="-u").pack(side="left", padx=5)
        tk.Radiobutton(row_frame, text="-Temp", variable=self.ut_flag, value="-T").pack(side="left", padx=5)

        tk.Label(row_frame, text="paramater").pack(side="left", padx=5)
        self.paramater_value = ttk.Combobox(row_frame, values=["S","cv","n","DOS","sigma","kappae","L","PF","RH"], width=10, state="readonly")
        self.paramater_value.set("S")  # Default value
        self.paramater_value.pack(side="left", padx=5)

        # Entry for the file name (for .btj)
        tk.Label(row_frame, text="File Name:").pack(side="left", padx=5)
        self.file_name = tk.StringVar(value=f"{self.case}.btj")
        tk.Entry(row_frame, textvariable=self.file_name, width=10 , state="disabled" ).pack(side="left", padx=5)
        
        tk.Label(row_frame, text="-subsample:").pack(side="left", padx=5)
        self.sm_value = tk.StringVar(value="2")
        tk.Entry(row_frame, textvariable=self.sm_value, width=10,  bg="white").pack(side="left", padx=5)      

        h_plot_button = tk.Button(row_frame, text="?", command=lambda: self.run_boltztrap(mode="h_plot", button=h_plot_button),  bg="#DFF6FF",  activebackground="#B2EBF2" )
        h_plot_button.pack(side="left", padx=5)
        self.buttons.append(h_plot_button)

    
    def run_boltztrap(self, mode, button):
        """
        run the BoltzTraP command.
        """
        infile = self.o_value.get()
        file_name=f"{infile}.btj"
        input_file=f"{infile}.bt2"
        
        
        if button:
             
            # Change button appearance to indicate it's running
            original_bg = button.cget("bg")   
            original_fg = button.cget("fg")   
            button.config(bg="lightgreen", fg="white", state="disabled")   
            self.root.update_idletasks()   

        try:
            if mode == "interpolate":
                # Collect values for interpolate
                n_flag = self.n_value.get()
                #input_file = self.o_value.get()
                e_flag = self.e_value.get()
                E_flag = self.E_value.get()
                m_flag = self.m_value.get().strip()
                k_flag = self.k_value.get().strip()
                d_flag = "-d" if self.d_mode.get() else ""   
                a_flag = "-a" if self.a_mode.get() else ""   
                m_or_k_flag = f"-m {m_flag}" if m_flag else f"-k {k_flag}"

                # usage: btp2 interpolate [-h] [-o OUTPUT] [-d] [-e EMIN] [-E EMAX] [-a]   (-k KPOINTS | -m MULTIPLIER)   directory
                command = f"btp2 -vv -n {n_flag} interpolate -o {input_file} {d_flag} -e {e_flag} -E {E_flag} {a_flag} {m_or_k_flag} ./ |& tee STDOUT"

            elif mode == "integrate":
                # Collect values for integrate
                n_flag = self.n_value_int.get()
                #input_file = self.input_file.get()
                temperatures = self.temperature_value.get()
                l_flag = self.l_mode.get()  # Get the selected mode (-t or -l)
                s_flag = f"-s {self.s_value.get()} " if self.s_value.get() else  ""
                b_flag = f"-b {self.b_value.get()} " if  self.b_value.get() else ""

                #usage: btp2 integrate [-h] [-p PREFIX] [-b BINS] [-t | -l] [-s SCISSOR] bt2_file temperature
                command = f"btp2 -vv -n {n_flag} integrate  {b_flag} {l_flag}   {s_flag} {input_file} {temperatures}    |& tee -a STDOUT"
                
            elif mode == "h_integrate":
                command = f"btp2    integrate -h "

            elif mode == "dope":
                # Collect values for the dope command
                n_flag = self.n_value_dope.get()
                #input_file = self.input_file_dope.get()
                doping_range = self.doping_range.get()
                temperatures = self.temperature_value.get()
                l_flag = self.l_mode.get()  # Get the selected mode (-t or -l)
                sd_flag = f"-s {self.sd_value.get()} "if self.sd_value.get() else ""
                b_flag = f"-b {self.b_value.get()} " if  self.b_value.get() else ""

                # usage: btp2 dope [-h] [-p PREFIX] [-b BINS] [-s SCISSOR] [-t | -l] bt2_file temperature doping_level

                command = f"btp2 -vv -n {n_flag} dope {b_flag} {l_flag}   {sd_flag} {input_file} {temperatures} {doping_range} |& tee -a STDOUT"
            elif mode == "h_interpolate":
                command = f"btp2 interpolate -h "
            elif mode == "h_integrate":
                command = f"btp2 integrate -h "
            elif mode == "h_dope":
                command = f"btp2 dope -h "
            elif mode == "h_plot":
                command = f"btp2 plot -h "
            
            elif mode =="plot":
                """Run the plot_boltz command."""
                # Get selected categories
             
                categories = []
                if self.c_xx.get():
                    categories.append('"xx"')
                if self.c_yy.get():
                    categories.append('"yy"')
                if self.c_zz.get():
                    categories.append('"zz"')

                # Build the -c flag value
                c_flag = f"'[{','.join(categories)}]'"
                sm_flag = f" -s  {self.sm_value.get()}" if self.sm_value.get() else ""
                ut_flag = f"{self.ut_flag.get()}" if self.ut_flag.get() else "-u"
                paramater= self.paramater_value.get()
                 

                # usage: btp2 plot [-h] [-c COMPONENTS] [-u | -T] [-s SUBSAMPLE]    btj_file {cv,n,DOS,sigma,S,kappae,L,PF,RH}
                command = f"btp2 -vv plot -c {c_flag} {ut_flag}  {sm_flag} {file_name} {paramater}  |& tee -a STDOUT"
            else:
                # Invalid mode
                print(f"Error: Invalid mode '{mode}'. Choose 'interpolate', 'integrate', or 'dope'.")
                return

            # Print or execute the command
            #print("Running command:", command)
            self.execute_command(command)

        finally:
            if button:
                # Restore original button appearance and state
                button.config(bg=original_bg, fg=original_fg, state="normal")

        
    def execute_command(self, command):
        """Execute a shell command, display output, and clear old output before new one."""
        try:
            mommat_file = os.path.join(self.base_path, self.case, f"{self.case}.mommat")
            if os.path.exists(mommat_file):
                #os.remove(mommat_file) 
                messagebox.showerror("Execution warrning", f"the file: {mommat_file}  found remove it ord use -d flag")
            self.output_text.delete(1.0, tk.END)  # Clear the text widget (start to end)
            result = subprocess.run(command, shell=True, capture_output=True, text=True, executable="/bin/bash")
            self.output_text.insert(tk.END, f"Command: {command}\n")
            self.output_text.insert(tk.END, "Output:\n")
            self.output_text.insert(tk.END, result.stdout)
            if result.stderr:
                self.output_text.insert(tk.END, "\n :\n")
                self.output_text.insert(tk.END, result.stderr)
            
            # Optional: Insert separator to make output clear
            self.output_text.insert(tk.END, "-"*50 + "\n")
        
        except Exception as e:
            messagebox.showerror("Execution Error", f"An error occurred: {str(e)}")
        
    

      

#if __name__ == "__main__":
    #root = tk.Tk()
    #app = BoltzTraP_GUI(root)
    #root.mainloop()
