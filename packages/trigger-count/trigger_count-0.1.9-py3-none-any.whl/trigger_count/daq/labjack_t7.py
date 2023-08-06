"""Module for basic labjack interactions."""
import datetime
import time

from labjack import ljm


class DaqLabjack:
    """Basic class to use labjack as a data acquisition system (daq)."""

    def __init__(self) -> None:
        """Open connection to labjack."""
        self.handle = ljm.openS("T7", "ANY", "ANY")
        self.counters: dict[str, str] = {}
        self._main_counter: str | None = None

    def read_port(self, port_name: str) -> float:
        """Read value from labjack port."""
        value = ljm.eReadName(self.handle, port_name)
        return value

    def add_counter(self, counter_name: str, port_name: str) -> None:
        """Set up counter on a port."""
        ljm.eWriteName(self.handle, f"{port_name}_EF_ENABLE", 0)
        ljm.eWriteName(self.handle, f"{port_name}_EF_INDEX", 8)
        ljm.eWriteName(self.handle, f"{port_name}_EF_ENABLE", 1)
        print(f"Counter enabled: {port_name}")
        self.counters[counter_name] = port_name

    def remove_counter(self, counter_name: str) -> None:
        """Deactivate counter."""
        port_name = self.counters[counter_name]
        ljm.eWriteName(self.handle, f"{port_name}_EF_ENABLE", 0)
        del self.counters[counter_name]

    def read_counter_by_port(self, port_name: str) -> int:
        """Read value from a counter using the name of its port (e.g. DIO2)."""
        count: float = ljm.eReadName(self.handle, f"{port_name}_EF_READ_A")
        count: int = int(count)
        return count

    def read_counter_by_name(self, counter_name: str) -> int:
        """Read value from a counter using user-specified name."""
        port_name = self.counters[counter_name]
        count = self.read_counter_by_port(port_name)
        return count

    def read_all_counters(self) -> dict:
        """Read all currently configured counters."""
        values = {}
        for counter_name, port_name in self.counters.items():
            values[counter_name] = self.read_counter_by_port(port_name)
        return values

    def set_main_counter(self, counter_name: str) -> None:
        """Set name of main counter."""
        if counter_name in self.counters.keys():
            self._main_counter = counter_name
        else:
            raise KeyError(f"Counter {counter_name} not added!")

    def block_until_new_count(self, counter_name: str) -> None:
        """Block script advancement until a new count has been registered."""
        last_count = self.read_counter_by_name(counter_name)
        while True:
            new_count = self.read_counter_by_name(counter_name)
            if new_count != last_count:
                break

    def wait_for_all_counters_to_increase(self) -> None:
        """Wait for all counters to increase."""
        old_counts = self.read_all_counters()
        counters_to_check = list(old_counts.keys())
        print(f"Waiting for all counters ({counters_to_check}) to increase.")
        while counters_to_check:
            new_counts = self.read_all_counters()
            indices_to_delete = []
            for i_name, name in enumerate(counters_to_check):
                old_value = old_counts[name]
                new_value = new_counts[name]
                if new_value != old_value:
                    print(f"Counter {name}: {old_value} -> {new_value}")
                    indices_to_delete.append(i_name)
            for index in indices_to_delete:
                print(f"Removing {counters_to_check[index]} (index: {index}) from check list")
                del counters_to_check[index]
                if counters_to_check:
                    print(f"Still waiting on {counters_to_check}")
        print(f"New counts on all {len(old_counts)} ports registered.")

    def read_main_counter(self) -> int:
        """Read value of main counter."""
        count = self.read_counter_by_name(self._main_counter)
        return count

    def wait_for_main_counter(self) -> None:
        """Hold script until main counter has increased."""
        self.block_until_new_count(self._main_counter)


if __name__ == "__main__":
    daq = DaqLabjack()
    daq.add_counter("eye_camera", "DIO2")
    while True:
        print(datetime.datetime.now(), daq.read_all_counters())
        time.sleep(1)
