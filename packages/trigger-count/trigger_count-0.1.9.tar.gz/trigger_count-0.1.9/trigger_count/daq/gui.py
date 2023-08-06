"""GUI to easily configure a labjack to count incoming triggers."""
import tkinter as tk

import numpy as np

from trigger_count.daq.labjack_t7 import DaqLabjack

DEFAULT_PORTS = ["twophoton_scanner", "widefield_camera", "eye_tracking_camera", "vitals_monitor"]


class LabjackGui:
    """Class to create gui to configure labjack triggers."""
    def __init__(self) -> None:
        self.window = tk.Tk()
        self.window.title("Labjack configuration")
        self.port_names = []
        self.use_variables = []
        self.name_variables = []
        self.main_variable = None

        self.set_up_gui()

    def set_up_gui(self) -> None:
        frame = tk.LabelFrame(self.window, text="Trigger counter settings")
        frame.pack()

        label = tk.Label(frame, text="Port name")
        label.grid(row=0, column=0)

        label = tk.Label(frame, text="Use counter?")
        label.grid(row=0, column=1)

        label = tk.Label(frame, text="Counter name")
        label.grid(row=0, column=2)

        for i_port, name in enumerate(DEFAULT_PORTS):
            port_name = f"DIO{i_port}"
            label = tk.Label(frame, text=port_name)
            label.grid(row=i_port + 1, column=0)
            self.port_names.append(port_name)

            use_variable = tk.BooleanVar()
            use_variable.set(False)
            check_box = tk.Checkbutton(frame, variable=use_variable)
            check_box.grid(row=i_port + 1, column=1)
            self.use_variables.append(use_variable)

            name_variable = tk.StringVar()
            name_variable.set(name)
            entry = tk.Entry(frame, textvariable=name_variable)
            entry.grid(row=i_port + 1, column=2)
            self.name_variables.append(name_variable)

        label = tk.Label(frame, text="Main counter")
        label.grid(row=len(DEFAULT_PORTS) + 1, column=0)

        main_variable = tk.StringVar()
        main_variable.set(self.port_names[0])
        dropdown = tk.OptionMenu(frame, main_variable, *self.port_names)
        dropdown.grid(row=len(DEFAULT_PORTS) + 1, column=1, columnspan=2)

        self.main_variable = main_variable

    def run(self) -> DaqLabjack:
        self.window.mainloop()
        daq = self.set_up_daq()
        return daq

    def set_up_daq(self) -> DaqLabjack:
        counter_names = [variable.get() for variable in self.name_variables]
        daq = DaqLabjack()
        use_counters = [variable.get() for variable in self.use_variables]
        for i_counter, should_use in enumerate(use_counters):
            if should_use:
                counter_name = counter_names[i_counter]
                counter_port = self.port_names[i_counter]
                daq.add_counter(counter_name, counter_port)
                print(f"Configured counter {counter_name} -> {counter_port}")
        main_port = self.main_variable.get()
        is_port = np.asarray(self.port_names) == main_port
        main_counter = np.asarray(counter_names)[is_port][0]
        daq.set_main_counter(main_counter)
        print(f"Main counter: {main_counter}")
        return daq


if __name__ == "__main__":
    gui = LabjackGui()
    gui.run()
