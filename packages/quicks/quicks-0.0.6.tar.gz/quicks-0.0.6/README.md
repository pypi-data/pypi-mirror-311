# Quicks

Project generator

```
pip install quicks

quicks example.yml PROJECT_NAME
```

example.yml Jinja2 style

```yaml
files:
  - ['{{project}}/__init__.py', 'alias']
  - '{{project}}/__main__.py'
  - '{{project}}/requirements.txt'
  - '.gitignore'
  - 'LICENSE'
  - 'Dockerfile'
  - 'README.md'

templates:
  'alias': |
    # auto generate
  'README.md': |
    # {{project}}
```