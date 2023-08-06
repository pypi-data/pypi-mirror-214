import argparse
import os
import subprocess
import sys

# Provide the full paths to the script files
script_files = ['GCoCF_Bot/service_bot.py', '']

# Provide the full paths to the test files
test_files = ['/path/to/test1.py', '/path/to/test2.py']


def run_scripts(scripts, custom_flags=None, display_output=True):
    processes = []
    for script in scripts:
        command = [sys.executable, script]
        
        if custom_flags:
            for flag_name, flag_value in custom_flags.items():
                command.extend([flag_name, flag_value])
        
        if display_output:
            process = subprocess.Popen(command)
        else:
            process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        processes.append(process)

    for process in processes:
        output, errors = process.communicate()
        if not display_output:
            print(output.decode())
            

def main(test: bool, run: bool, custom_flags=None):
    if test:
        run_scripts(test_files, custom_flags=custom_flags, display_output=False)
    elif run:
        run_scripts(script_files, custom_flags=custom_flags)
        

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Unify outputs and run scripts based on flags")
    parser.add_argument('--test', action="store_true", help="Run tests with pytest commands")
    parser.add_argument('--run', action="store_true", help="Run given scripts and the flit build")
    parser.add_argument('--coc_token', type=str, help="COC Token")
    parser.add_argument('--bot_token', type=str, help="Bot Token")
    parser.add_argument('--webhook_url', type=str, help="Webhook URL")
    parser.add_argument('--loglevel', type=str, help="Log level")
    parser.add_argument('--clan_tag', type=str, help="Clan tag")
    parser.add_argument('--bot_owner_id', type=int, help="Bot owner user ID")
    args = parser.parse_args()

    custom_flags = {
        flag: value
        for flag, value in vars(args).items()
        if flag not in ["test", "run"] and value is not None
    }

    if args.loglevel:
        custom_flags['--log-level'] = args.loglevel.lower()

    main(args.test, args.run, custom_flags=custom_flags)