from .utils import print_timestamp
import anvil.js
import anvil.server


class GlobalCache:
    def __init__(self, global_dict, tenanted_dict=None):
        self._global_dict = global_dict
        self._tenanted_dict = tenanted_dict

    def __getattr__(self, name):
        if name in self._global_dict:
            if name == 'user':
                self._global_dict[name] = self._global_dict[name] or anvil.users.get_user()
                print_timestamp('Global: user')
            elif name == 'is_mobile':
                self._global_dict[name] = self._global_dict[name] or anvil.js.window.navigator.userAgent.lower().find("mobi") > -1
                print_timestamp('Global: is_mobile')
            else:
                print_timestamp(f'Global before: {name}')
                if self._global_dict[name] is None:  # Only check None condition.
                    self._global_dict[name] = anvil.server.call('get_' + name)
                print_timestamp(f'Global after: {name}')
            return self._global_dict[name]
        elif name in self._tenanted_dict:
            print_timestamp(f'Global.get_tenanted before: {name}')
            if self._tenanted_dict[name] is None:  # Only check None condition.
                self._tenanted_dict[name] = anvil.server.call('get_tenanted_data', self._global_dict['tenant_id'], name)
            print_timestamp(f'Global.get_tenanted after: {name}')
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

    def get_no_call(self, name):
        """Get a global value but don't call the server if None."""
        if name in self._global_dict:
            return self._global_dict[name]
        if name in self._tenanted_dict:
            return self._tenanted_dict[name]
        raise AttributeError(f"Attribute {name} not found")