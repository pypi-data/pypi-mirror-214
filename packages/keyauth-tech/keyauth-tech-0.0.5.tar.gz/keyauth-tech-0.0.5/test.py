from keyauth import KeyAuth

def main():
    print("Hello matrix!") # Replace with your Code (success)

def exit_program():
    print("Authentication failed.") # Replace with your Code (fail)
    authenticator.exit()

# Creating the authenticator instance
authenticator = KeyAuth(app_id="93b59d70ec573fa9", success=main, fail=exit_program) # Replace with your APP ID

# Authenticating
authenticator.authenticate()

# Install Packages if not installed 
authenticator.install(["requests", "random"]) # Replace with your Packages

# Print your HWID
print(authenticator.get_hwid())