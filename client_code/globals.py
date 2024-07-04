from .utils import print_timestamp
import anvil.js
import anvil.server
from anvil_extras.non_blocking import call_async


class GlobalCache:
    """Cache user data."""
    def __init__(self, global_dict, tenanted_dict=None, task=None, task_tenanted=None):
        self._global_dict = global_dict
        self._tenanted_dict = tenanted_dict
        self._task = task
        self._task_tenanted = task_tenanted
        print_timestamp('GlobalCache: init')

    def __getattr__(self, name):
        if name == 'user':
            if self._global_dict[name] is None:
                self._global_dict[name] = anvil.users.get_user()
                print_timestamp('GlobalCache: user')
            return self._global_dict[name]
        elif name == 'is_mobile':
            if self._global_dict[name] is None:
                self._global_dict[name] = anvil.js.window.navigator.userAgent.lower().find("mobi") > -1       
                print_timestamp('GlobalCache: is_mobile')
            return self._global_dict[name]
        elif name in self._global_dict:
            if self._global_dict[name] is None:  # Only check None condition.
                self._global_dict[name] = anvil.server.call('get_data', name)
                print_timestamp(f'GlobalCache: {name}')
            return self._global_dict[name]
        elif name in self._tenanted_dict:
            if self._tenanted_dict[name] is None:  # Only check None condition.
                self._tenanted_dict[name] = anvil.server.call('get_tenanted_data', self._global_dict['tenant_id'], name)
                print_timestamp(f'GlobalCache: {name}')
            return self._tenanted_dict[name]
        raise AttributeError(f"Attribute {name} not found")

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
        for name in list(self._tenanted_dict.keys()):
            self._tenanted_dict[name] = None

    def get_s(self, name):
        """Get a global value but don't call the server if None."""
        if name in self._global_dict:
            if self._global_dict[name] is None:
                print_timestamp(f'GlobalCache.get_s {name}')
            return self._global_dict[name]
        if name in self._tenanted_dict:
            if self._tenanted_dict[name] is None:
                print_timestamp(f'GlobalCache.get_s {name}')
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

    def launch_bk(self):
        call_async('get_data_call_bk').on_result(self.launch_bk_result)

    def launch_bk_result(self, res):
        self._task = res
        
    def launch_bk_tenanted(self):
        call_async('get_tenanted_data_call_bk', self._global_dict['tenant_id']).on_result(self.launch_bk_tenanted_result)

    def launch_bk_tenanted_result(self, res):
        self._task_tenanted = res
        
    def get_bk_single(self, name):
        if self._global_dict[name] is not None:
            return self._global_dict[name]

        print_timestamp(f'GlobalCache.get_bk_single {name}')
        if not self._task:
            print_timestamp('GlobalCache launching background task')
            self._task = anvil.server.call('get_data_call_bk')

        if self._task.is_completed():
            all_data = self._task.get_return_value()
            for key, val in all_data.items():
                self._global_dict[key] = val
        else:
            states = self._task.get_state()
            if name in states:
                if name + '_len' in states:
                    diff_len = states[name + '_len'] - len(states[name])
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
            
        print_timestamp(f'GlobalCache.get_bk_tenanted {name}')
        if 'task_tenanted' not in dir(self):
            print(dir(self))
        if not self._task_tenanted:
            print_timestamp('GlobalCache launching background task tenanted')
            self._task_tenanted = anvil.server.call('get_tenanted_data_call_bk', self._global_dict['tenant_id'])

        if self._task_tenanted.is_completed():
            all_data = self._task_tenanted.get_return_value()
            for key, val in all_data.items():
                self._tenanted_dict[key] = val
        else:
            states = self._task_tenanted.get_state()
            if name in states:
                if name + '_len' in states:
                    diff_len = states[name + '_len'] - len(states[name])
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