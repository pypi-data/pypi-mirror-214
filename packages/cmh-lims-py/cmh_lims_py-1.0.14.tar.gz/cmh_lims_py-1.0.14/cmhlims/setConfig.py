import argparse
import configparser
import os

def update_config(config_file, environment):
    config = configparser.ConfigParser()
    config.read(os.path.join(os.path.dirname(__file__), 'config.ini'))

    config.set('shared', 'config_file', config_file)
    config.set('shared', 'environment', environment)

    with open('config.ini', 'w') as configfile:
        config.write(configfile)

def main():
    parser = argparse.ArgumentParser(description='Update configuration options')
    parser.add_argument('--config-file', '-c', type=str, help='New value for config_file option')
    parser.add_argument('--environment', '-e', type=str, help='New value for environment option')
    args = parser.parse_args()

    if args.config_file and args.environment:
        update_config(args.config_file, args.environment)
        print('Configuration updated successfully.')
    else:
        print('Please provide values for both --config-file and --environment options.')

if __name__ == '__main__':
    main()