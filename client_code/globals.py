import anvil.js
import anvil.server
import anvil.users

from .utils import print_timestamp


class GlobalCache:
    """Cache user data."""

    def __init__(self, global_dict, tenanted_dict=None, task=None, task_tenanted=None):
        self._global_dict = global_dict
        self._tenanted_dict = tenanted_dict
        self._task = task
        self._task_tenanted = task_tenanted
        print_timestamp("GlobalCache: init")

    def __getattr__(self, name):
        if name == "user":
            if self._global_dict[name] is None:
                self._global_dict[name] = anvil.users.get_user()
                print_timestamp("GlobalCache: user")
            return self._global_dict[name]
        elif name == "is_mobile":
            if self._global_dict[name] is None:
                self._global_dict[name] = (
                    anvil.js.window.navigator.userAgent.lower().find("mobi") > -1
                )
                print_timestamp("GlobalCache: is_mobile")
            return self._global_dict[name]
        elif name in self._global_dict:
            if self._global_dict[name] is None:  # Only check None condition.
                self._global_dict[name] = anvil.server.call("get_data", name)
                print_timestamp(f"GlobalCache: {name}")
            return self._global_dict[name]
        elif name in self._tenanted_dict:
            if self._tenanted_dict[name] is None:  # Only check None condition.
                self._tenanted_dict[name] = anvil.server.call(
                    "get_tenanted_data", self._global_dict["tenant_id"], name
                )
                print_timestamp(f"GlobalCache: {name}")
            return self._tenanted_dict[name]
        raise AttributeError(f"Attribute {name} not found")

    def __setattr__(self, name, value):
        if name.startswith("_"):
            # This allows initialization and internal attributes to be set.
            super().__setattr__(name, value)
        elif name in list(self._global_dict.keys()):
            self._global_dict[name] = value
        elif name in list(self._tenanted_dict.keys()):
            self._tenanted_dict[name] = value
        else:
            raise AttributeError(f"Attribute {name} not found")

    def clear_global_attributes(self):
        for name in list(self._global_dict.keys()):
            self._global_dict[name] = None
        for name in list(self._tenanted_dict.keys()):
            self._tenanted_dict[name] = None

    def get_s(self, name):
        """Get a global value but don't call the server if None."""
        if name in self._global_dict:
            if self._global_dict[name] is None:
                print_timestamp(f"GlobalCache.get_s {name}")
            return self._global_dict[name]
        if name in self._tenanted_dict:
            if self._tenanted_dict[name] is None:
                print_timestamp(f"GlobalCache.get_s {name}")
            return self._tenanted_dict[name]
        raise AttributeError(f"Attribute {name} not found")

    def get_bk(self, name):
        with anvil.server.no_loading_indicator:
            if name in self._global_dict:
                return self.get_bk_single(name)
            elif name in self._tenanted_dict:
                return self.get_bk_tenanted(name)
            else:
                raise AttributeError(f"Attribute {name} not found")

    def update_bk_single(self):
        print_timestamp("GlobalCache: update_bk_single")
        bk_complete = self._task.is_completed()
        if bk_complete:
            all_data = self._task.get_return_value()
            for key, val in all_data.items():
                if self._global_dict[key] is None:
                    self._global_dict[key] = val
        # else:
        #     for key, val in self._global_dict.items():
        #         if self._global_dict[key] is None:
        #             self._global_dict[key] = self.get_bk_single(key)
        return bk_complete

    def update_bk_tenanted(self):
        bk_tenanted_complete = self._task_tenanted.is_completed()
        if bk_tenanted_complete:
            all_data = self._task_tenanted.get_return_value()
            for key, val in all_data.items():
                if self._tenanted_dict[key] is None:
                    self._tenanted_dict[key] = val
        # else:
        #     for key, val in self._tenanted_dict.items():
        #         if self._tenanted_dict[key] is None:
        #             self._tenanted_dict[key] = self.get_bk_tenanted(key)
        return bk_tenanted_complete

    def launch_bk(self):
        if not self._task:
            print_timestamp("Launching get_data_call_bk")
            self._task = anvil.server.call("get_data_call_bk")

    def launch_bk_tenanted(self):
        if not self._task_tenanted:
            print_timestamp("Launching get_tenanted_data_call_bk")
            self._task_tenanted = anvil.server.call(
                "get_tenanted_data_call_bk", self._global_dict["tenant_id"]
            )

    def get_bk_single(self, name):
        if self._global_dict[name] is not None:
            return self._global_dict[name]

        print_timestamp(f"GlobalCache.get_bk_single {name}")
        if not self._task:
            print_timestamp("GlobalCache launching background task")
            self._task = anvil.server.call("get_data_call_bk")

        if self._task.is_completed():
            all_data = self._task.get_return_value()
            for key, val in all_data.items():
                if self._global_dict[key] is None:
                    self._global_dict[key] = val
        else:
            states = self._task.get_state()
            if name in states:
                if name + "_len" in states:
                    diff_len = states[name + "_len"] - len(states[name])
                    if diff_len > 0:
                        data = states[name] + [None] * diff_len
                    else:
                        # This part of the load is complete
                        data = states[name]
                        self._global_dict[name] = data
                else:
                    data = states[name]
                return data
            else:
                return None

    def get_bk_tenanted(self, name):
        if self._tenanted_dict[name] is not None:
            return self._tenanted_dict[name]

        print_timestamp(f"GlobalCache.get_bk_tenanted {name}")
        if "task_tenanted" not in dir(self):
            print(dir(self))
        if not self._task_tenanted:
            print_timestamp("GlobalCache launching background task tenanted")
            self._task_tenanted = anvil.server.call(
                "get_tenanted_data_call_bk", self._global_dict["tenant_id"]
            )

        if self._task_tenanted.is_completed():
            all_data = self._task_tenanted.get_return_value()
            for key, val in all_data.items():
                if self._tenanted_dict[key] is None:
                    self._tenanted_dict[key] = val
        else:
            states = self._task_tenanted.get_state()
            if name in states:
                if name + "_len" in states:
                    diff_len = states[name + "_len"] - len(states[name])
                    if diff_len > 0:
                        data = states[name] + [None] * diff_len
                    else:
                        # This part of the load is complete
                        data = states[name]
                        self._tenanted_dict[name] = data
                else:
                    data = states[name]
                return data
            else:
                return None
