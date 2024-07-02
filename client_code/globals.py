from .utils import print_timestamp
import anvil.js
import anvil.server


class GlobalCache:
    """Cache user data."""
    def __init__(self, global_dict, tenanted_dict=None, task=None, task_tenanted=None):
        self._global_dict = global_dict
        self._tenanted_dict = tenanted_dict
        self.task = task
        self.task_tenanted = task_tenanted

    def __getattr__(self, name):
        if name == 'user':
            self._global_dict[name] = self._global_dict[name] or anvil.users.get_user()
            print_timestamp('Global: user')
            return self._global_dict[name]
        elif name == 'is_mobile':
            self._global_dict[name] = self._global_dict[name] or anvil.js.window.navigator.userAgent.lower().find("mobi") > -1
            print_timestamp('Global: is_mobile')
            return self._global_dict[name]
        elif name in self._global_dict:
            print_timestamp(f'Global before: {name}')
            if self._global_dict[name] is None:  # Only check None condition.
                self._global_dict[name] = anvil.server.call('get_data', name)
            print_timestamp(f'Global after: {name}')
            return self._global_dict[name]
        elif name in self._tenanted_dict:
            print_timestamp(f'Global.get_tenanted before: {name}')
            if self._tenanted_dict[name] is None:  # Only check None condition.
                self._tenanted_dict[name] = anvil.server.call('get_tenanted_data', self._global_dict['tenant_id'], name)
            print_timestamp(f'Global.get_tenanted after: {name}')
            return self._tenanted_dict[name]
        else:
            raise AttributeError(f"Attribute {name} not found")
        return self._global_dict[name]

    def __setattr__(self, name, value):
        if name.startswith('_'):
            # This allows initialization and internal attributes to be set.
            super().__setattr__(name, value)
        else:
            if value is None:
                # If setting an attribute to None, remove it to force repopulation on next access.
                self._global_dict.pop(name, None)
            else:
                # For all other assignments, update the global dictionary normally.
                self._global_dict[name] = value

    def clear_global_attributes(self):
        for name in list(self._global_dict.keys()):
            self._global_dict[name] = None

    def get_s(self, name):
        """Get a global value but don't call the server if None."""
        if name in self._global_dict:
            return self._global_dict[name]
        if name in self._tenanted_dict:
            return self._tenanted_dict[name]
        raise AttributeError(f"Attribute {name} not found")

    def get_bk(self, name):
        if name in self._global_dict:
            data_dict = self._global_dict
            call_bk = 'get_data_call_bk'
            task = self.task
        elif name in self._tenanted_dict:
            data_dict = self._tenanted_dict
            call_bk = 'get_tenanted_data_call_bk'
            task = self.task_tenanted
        else:
            raise AttributeError(f"Attribute {name} not found")

    def get_bk_tenanted(self, name):
        if not self.task_tenanted:
            self.task_tenanted = anvil.server.call('get_tenanted_data_call_bk', self._global_dict['tenant_id'])

        if self.task_tenanted.is_completed():
            all_data = self.task.get_return_value()
            for key, val in all_data.items():
                    print_timestamp(f"task_done: setting value for {key}")
                self._tenanted_dict[key] = val
        else:
            states = self.task_tenanted.get_state()
            if name in states:
                if name + '_len' in states:
                    diff_len = states[name + '_len'] - len(states[name])
                    if diff_len > 0:
                        data = states[name] + [None] * diff_len
                    else:
                        data = states[name]
                else:
                    data = states[name]
                self._tenanted_dict[name] = data
            else:
                self._tenanted_dict[name] = None
            