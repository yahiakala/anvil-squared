# ClientTests Component

The ClientTests component provides a user interface for running and managing client-side unit tests in Anvil applications. It organizes tests hierarchically (modules → classes → methods) and provides visual feedback for test execution.

## Features

- Hierarchical test organization
- Visual test execution feedback
- Support for standard unittest.TestCase classes
- Configurable UI elements (icons, buttons, cards)
- Run individual tests or entire test suites
- Real-time test execution status

## Properties

| Property | Type | Description | Default |
|----------|------|-------------|---------|
| `test_modules` | list | List of Python modules containing test cases | [] |
| `card_roles` | list | Three-element list defining card roles for module, class, and method levels | [None, None, None] |
| `icon_size` | int | Size of status icons in pixels | 30 |
| `btn_role` | str | Role/style for run buttons | "filled-button" |

## Test Structure

The component organizes tests in a three-level hierarchy:

1. **Module Level**: Contains test classes from a Python module
2. **Class Level**: Contains test methods from a TestCase class
3. **Method Level**: Individual test methods

## Usage Example

```python
from anvil import *
import unittest
from .ClientTests import ClientTests

# Define your test module
class MyTestCase(unittest.TestCase):
    def test_addition(self):
        self.assertEqual(1 + 1, 2)

    def test_string(self):
        self.assertEqual("hello".upper(), "HELLO")

# Create a module with tests
import sys
test_module = sys.modules[__name__]

class TestForm(TestFormTemplate):
    def __init__(self, **properties):
        self.init_components(**properties)

        # Configure the test runner
        self.test_runner = ClientTests(
            test_modules=[test_module],
            card_roles=["card-1", "card-2", "card-3"],
            icon_size=24,
            btn_role="primary-button"
        )

        # Add to your form
        self.add_component(self.test_runner)
```

## Test Module Requirements

Test modules should follow these conventions:

1. Test classes must inherit from `unittest.TestCase`
2. Test method names must start with `test_`
3. Standard unittest assertions and fixtures are supported

Example test module:

```python
import unittest

class TestStringMethods(unittest.TestCase):
    def setUp(self):
        # Setup code runs before each test
        self.test_string = "hello world"

    def test_upper(self):
        self.assertEqual(self.test_string.upper(), "HELLO WORLD")

    def test_split(self):
        self.assertEqual(self.test_string.split(), ["hello", "world"])

    def tearDown(self):
        # Cleanup code runs after each test
        pass
```

## UI Customization

### Card Roles

The `card_roles` property accepts a list of three roles for different hierarchy levels:

```python
client_tests = ClientTests(
    card_roles=[
        "module-card",     # Style for module cards
        "class-card",      # Style for class cards
        "method-card"      # Style for method cards
    ]
)
```

### Button Styles

The `btn_role` property determines the appearance of run buttons:

```python
client_tests = ClientTests(
    btn_role="primary-button"  # Use your custom button role
)
```

## Test Execution

Tests can be run at different levels:

- **Run All**: Executes all tests in all modules
- **Module Level**: Runs all tests in a specific module
- **Class Level**: Runs all tests in a specific class
- **Method Level**: Runs a single test method

The component provides visual feedback for:
- Test in progress
- Test success
- Test failure
- Test errors

## Best Practices

1. **Test Organization**:
   - Group related tests in the same class
   - Use descriptive test method names
   - Implement setUp and tearDown methods for common setup/cleanup

2. **UI Integration**:
   ```python
   def form_show(self, **event_args):
       # Add test runner to a specific container
       self.test_container.add_component(self.test_runner)
   ```

3. **Error Handling**:
   ```python
   def test_with_error_handling(self):
       try:
           # Test code
           self.assertEqual(actual, expected)
       except Exception as e:
           self.fail(f"Test failed with error: {str(e)}")
   ```

4. **Async Tests**:
   ```python
   @anvil.server.callable
   async def async_test_method(self):
       # Test async operations
       result = await anvil.server.call('some_function')
       self.assertIsNotNone(result)
   ```

## Limitations

1. Tests run in the client's browser context
2. No direct access to server-side resources
3. Browser console used for detailed error output
4. Test execution time may vary based on client hardware

## Integration Tips

1. **Custom Test Templates**:
   ```python
   class MyTestCase(unittest.TestCase):
       @classmethod
       def setUpClass(cls):
           # Setup once for all tests in class
           pass

       @classmethod
       def tearDownClass(cls):
           # Cleanup after all tests in class
           pass
   ```

2. **Test Categories**:
   ```python
   def test_critical_feature(self):
       self.test_obj.test_desc = "Critical: Payment Processing"
       # Test code...
