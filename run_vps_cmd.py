import paramiko

def run_diagnostics():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect('157.173.101.159', username='user210', password='samuel')
        print("Connected to VPS. Running diagnostics...")
        
        commands = [
            "ss -tuln",
            "ps -ef | grep -E 'python|http|server|node'",
        ]
        
        for cmd in commands:
            print(f"\n--- Output of '{cmd}' ---")
            stdin, stdout, stderr = client.exec_command(cmd)
            print(stdout.read().decode())
            err = stderr.read().decode()
            if err:
                print(f"Error: {err}")
    except Exception as e:
        print(f"Failed: {e}")
    finally:
        client.close()

if __name__ == '__main__':
    run_diagnostics()
