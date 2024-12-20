import subprocess
import json
import os

def get_ufw_rules(action):
    try:
        # Define the command to retrieve UFW status with comments
        command = ["sudo", "ufw", "status", "verbose"]

        # Run the command
        result = subprocess.run(command, capture_output=True, text=True)

        # Check for errors
        if result.returncode != 0:
            print("Error running UFW command:", result.stderr)
            return None

        # Parse the output
        rules = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if (action == "Allow" and "ALLOW" in line) or (action == "Deny" and "DENY" in line):
                # Parse rule details, including the comment if present
                parts = line.split()
                comment_index = parts.index("#") if "#" in parts else None
                name = "" if comment_index is None else " ".join(parts[comment_index + 1:])

                # Extract the IP or source
                source = "Anywhere"
                for part in parts:
                    if part.count(".") == 3 and all(p.isdigit() for p in part.split(".")):
                        source = part
                        break

                if len(parts) >= 2:
                    rule = {
                        "Name": name,
                        "Action": parts[1],
                        "Port": parts[0],
                        "From": source
                    }
                    rules.append(rule)

        return rules

    except Exception as e:
        print("An error occurred:", str(e))
        return None

def save_ufw_rules_to_json(rules, action):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the output file path (same directory as the script)
    output_file = os.path.join(script_dir, f"ufw_rules_{action.lower()}.json")

    # Save the parsed JSON data to a file
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(rules, file, indent=4)

    print(f"UFW rules for action '{action}' saved to {output_file}")

def main():
    # Actions to retrieve rules for
    actions = ["Allow", "Deny"]

    for action in actions:
        # Get UFW rules for each action
        rules = get_ufw_rules(action)

        if rules:
            # Save the results to a JSON file
            save_ufw_rules_to_json(rules, action)
        else:
            print(f"No rules found for action '{action}'.")

if __name__ == '__main__':
    # Ensure the script is run with sufficient permissions
    if os.geteuid() != 0:
        print("This script must be run as root or with sudo.")
    else:
        # Run the main function to fetch and save UFW rules for both actions
        main()
