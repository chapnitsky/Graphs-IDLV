class Node:
    def __init__(self):
        self.value = None
        self.color = "white"
        self.exit_time = -1

    def get_val(self):
        return self.value

    def get_color(self):
        return self.color

    def get_exit_time(self):
        return self.exit_time

    def set_color(self, val):
        self.color = val

    def set_exit_time(self, val):
        self.exit_time = val

    def set_val(self, val):
        self.value = val

