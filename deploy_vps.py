import paramiko
import time

def deploy_to_vps():
    print("Connecting to VPS (157.173.101.159)...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    
    try:
        client.connect('157.173.101.159', username='user210', password='samuel')
        print("Successfully connected!")
        
        commands = [
            # Kill existing mosquitto and python http server instances started by this user
            "pkill -u user210 -f mosquitto || true",
            "pkill -u user210 -f http.server || true",
            
            # Remove old directory if it exists and clone the fresh repo
            "rm -rf tempix",
            "git clone https://github.com/BYIRINGIRO-Samuel/tempix.git",
            
            # Ensure the config file is correct (Mosquitto WebSockets on 9210)
            "cat << 'EOF' > ~/my_mosquitto.conf\nlistener 9210 0.0.0.0\nprotocol websockets\nallow_anonymous true\nEOF",
            
            # Run mosquitto in the background using nohup
            "nohup mosquitto -c ~/my_mosquitto.conf > mosquitto.log 2>&1 &",
            
            # Run the Python HTTP server on port 8210 from the cloned repository folder to serve dashboard.html
            "cd tempix && nohup python3 -m http.server 8210 > http_server.log 2>&1 &",
            
            # Print running processes to verify
            "sleep 2 && ps -ef | grep -E 'mosquitto|http.server'"
        ]
        
        for cmd in commands:
            print(f"Running: {cmd}")
            stdin, stdout, stderr = client.exec_command(cmd)
            out = stdout.read().decode().strip()
            err = stderr.read().decode().strip()
            if out: print(f"Output: {out}")
            if err: print(f"Error: {err}")
            
    except Exception as e:
        print(f"Deployment failed: {e}")
    finally:
        client.close()
        print("Disconnected from VPS. Deployment complete.")

if __name__ == "__main__":
    deploy_to_vps()
