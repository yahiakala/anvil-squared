# Contributing

We welcome contributions to Anvil Squared! This document outlines the process for contributing to this project.

## Getting Started

1. Fork the repository on GitHub

2. Clone your fork locally:
   ```bash
   git clone https://github.com/YOUR-USERNAME/anvil-squared.git
   ```

3. Create a new branch for your feature or fix:
   ```bash
   # For bug fixes
   git checkout -b fix/<your-fix-name>

   # For new features
   git checkout -b feat/<your-feature-name>

   # For documentation changes
   git checkout -b docs/<your-docs-changes-name>
   ```

## Setting up Pre-commit

We use pre-commit hooks to ensure code quality and consistency. To set this up:

1. Install pre-commit:
   ```bash
   pip install pre-commit
   ```

2. Install the git hooks:
   ```bash
   pre-commit install
   ```

When you try to commit, these checks will run automatically. If any checks fail, the commit will be prevented and you'll need to fix the issues before committing again.

To run the checks manually:
```bash
pre-commit run --all-files
```

## Contributing to Documentation

We use MkDocs for our documentation. To set up the documentation environment:

1. Create and activate a virtual environment:
   ```bash
   pip install uv
   uv venv
   source .venv/bin/activate
   ```

2. Install requirements:
   ```bash
   uv pip install -r requirements.txt
   ```

3. Documentation files are in the `docs/` directory and written in Markdown format.

4. To preview your changes locally:
   ```bash
   mkdocs serve
   ```
   Then visit `http://127.0.0.1:8000` in your browser.

5. Documentation structure:
   ```
   docs/
   ├── index.md                    # Main documentation page
   ├── contributing.md             # Contributing guidelines
   ├── components/                 # Component documentation
   │   ├── chatbox.md             # ChatBox component docs
   │   ├── chatpage.md            # ChatPage component docs
   │   └── client-tests.md        # Client Tests docs
   └── server/                     # Server features documentation
       ├── authentication.md       # Authentication system docs
       └── multi-tenant.md         # Multi-tenant system docs
   ```

6. Follow these documentation guidelines:
   - Use clear, concise language
   - Include code examples where appropriate
   - Add screenshots for UI-related features
   - Update the navigation in `mkdocs.yml` if adding new pages
   - Ensure proper formatting and consistent style

## Making Changes

1. Make your changes in your feature branch

2. Write or update tests as needed:
   - For client-side components, use the ClientTests framework
   - Include both positive and negative test cases
   - Test edge cases and error conditions

3. Ensure your code follows the existing style of the project:
   - Follow Python PEP 8 guidelines
   - Use consistent naming conventions
   - Add appropriate docstrings and comments

4. Commit your changes:
   ```bash
   git commit -m "Description of your changes"
   ```

## Submitting Changes

1. Push your changes to your fork on GitHub:
   ```bash
   git push origin <your-branch-name>
   ```

2. Open a Pull Request (PR) from your fork to our main repository

3. In your PR description, clearly describe:
   - What changes you've made
   - Why you've made them
   - Any relevant issue numbers

## Pull Request Guidelines

- PRs should focus on a single feature or fix
- Keep changes small and focused
- Update documentation as needed
- Ensure all tests pass
- Follow existing code style and conventions
- All pre-commit checks must pass
- For documentation changes:
  - Ensure mkdocs builds successfully
  - Preview changes locally before submitting
  - Check for broken links and proper formatting

## Component Development Guidelines

When developing new components or modifying existing ones:

1. **Component Structure**
   - Follow the established pattern in `client_code/`
   - Include proper form templates
   - Document component properties and events

2. **Testing**
   - Add tests using the ClientTests framework
   - Test component initialization
   - Test all public methods and properties
   - Test event handling

3. **Documentation**
   - Add comprehensive documentation
   - Include usage examples
   - Document all properties and events
   - Provide code snippets

## Server-Side Development Guidelines

When working on server-side features:

1. **Authentication**
   - Follow security best practices
   - Document security implications
   - Include proper error handling

2. **Multi-tenant Features**
   - Maintain tenant isolation
   - Document permission requirements
   - Include proper validation

## Questions or Issues?

If you have questions or run into issues, please:

1. Check existing [issues on GitHub](https://github.com/yahiakala/anvil-squared/issues)
2. Create a new issue if needed
3. Ask questions in the PR itself

Thank you for contributing to Anvil Squared!
