from dotenv import load_dotenv, dotenv_values
import os

# Confirm configuration file is being detected
print("🔍 Does 'configuration.env' exist?", os.path.exists("configuration.env"))

# Load and print raw dotenv contents
load_dotenv("configuration.env")
print("\n📄 Raw .env file contents:")
config = dotenv_values("configuration.env")
for k, v in config.items():
    print(f"  {k} = {v}")

# Print what is available in os.environ
print("\n🌍 Environment snapshot:")
for key in ["AWS_IOT_ENDPOINT", "AWS_IOT_PORT", "ROOT_CA_PATH", "PRIVATE_KEY_PATH", "CERTIFICATE_PATH", "TOPIC", "SERIAL_PORT"]:
    print(f"  {key} = {os.getenv(key)}")

# Try converting AWS_IOT_PORT
port_value = os.getenv("AWS_IOT_PORT")
print("\n🔧 Converting AWS_IOT_PORT...")
try:
    port_int = int(port_value)
    print(f"✅ Success: int(AWS_IOT_PORT) = {port_int}")
except Exception as e:
    print(f"❌ Failed to convert: {e}")
