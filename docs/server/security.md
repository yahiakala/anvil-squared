# Security Requirements

## Server Callable Security

### SQUARED Secret Requirement

All server callables in Anvil Squared require the 'SQUARED' secret to be defined in your app's secrets. This is a critical security measure that prevents unintended use of the callables.

If you attempt to use any server callable in your app without defining this secret, the callable will not work. This helps ensure that you never accidentally expose these callables if you don't want to.

### Setting Up the SQUARED Secret

1. Open your Anvil app settings
2. Navigate to the "Secrets" section
3. Add a new secret with the key 'SQUARED'
4. Set any value to it.
