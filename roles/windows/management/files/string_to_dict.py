import subprocess
import json
import os

def get_firewall_rules(action):
    try:
        # Define the PowerShell command to retrieve firewall rules by action
        command = [
            "powershell",
            "-Command",
            f"Get-NetFirewallRule -Action {action} | "
            "Select-Object Name, DisplayName, Action, Direction, Profile | "
            "ForEach-Object { "
            "$rule = $_; "
            "$rule.Action = $rule.Action.ToString(); "
            "$rule.Direction = $rule.Direction.ToString(); "
            "$rule.Profile = $rule.Profile.ToString(); "
            "$rule } | ConvertTo-Json -Depth 3"
        ]

        # Run the PowerShell command
        result = subprocess.run(command, capture_output=True, text=True)

        # Check for errors
        if result.returncode != 0:
            print("Error running PowerShell command:", result.stderr)
            return None

        # Parse the JSON output
        firewall_rules = json.loads(result.stdout)
        return firewall_rules

    except Exception as e:
        print("An error occurred:", str(e))
        return None


def save_firewall_rules_to_json(rules, action):
    # Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Define the output file path (same directory as the script)
    output_file = os.path.join(script_dir, f"firewall_rules_{action}.json")

    # Save the parsed JSON data to a file
    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(rules, file, indent=4)

    print(f"Firewall rules for action '{action}' saved to {output_file}")


def main():
    # Actions to retrieve rules for
    actions = ["Allow", "Block"]

    for action in actions:
        # Get firewall rules for each action
        rules = get_firewall_rules(action)

        if rules:
            # Save the results to a JSON file
            save_firewall_rules_to_json(rules, action)
        else:
            print(f"No rules found for action '{action}'.")


if __name__ == '__main__':
    # Run the main function to fetch and save firewall rules for both actions
    main()
