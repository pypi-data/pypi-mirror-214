# DotENV-Reader
A Package for PiP that will read dotenv files.

# How to use
Create a new .env file (will throw an error if not found, it must be in the workspace where the package was imported) Copy the code below into one of your python files to start reading a dotenv.

```python

from dotenvreader import main as dotenv

dotenv.config() # Configuring the dotenv

print(dotenv.get_value("example")) # Returns "Example"
print(dotenv.exists("example")) # Returns "True"

```