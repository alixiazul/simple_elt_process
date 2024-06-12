from subprocess import run, CalledProcessError
from time import sleep
from dotenv import dotenv_values


def wait_for_postgres(host, max_retries=5, delay_seconds=5):
    retries = 0
    while retries < max_retries:
        try:
            result = run(
                ["pg_isready", "-h", host], check=True, capture_output=True,
                text=True)
            if "accepting connections" in result.stdout:
                print("Sucessfully connected to Postgres")
                return True
        except CalledProcessError as e:
            print(f"Error connecting to Postgres: {e}")
            retries += 1
            print(
                f"Retrying in {delay_seconds} seconds... (Attempt {retries}/{max_retries})"
            )
            sleep(delay_seconds)
    print("Max retries reached. Exiting")
    return False


# Load variables from source database configuration file
source_config = dotenv_values("../.env.source")

# Load variables from destination database configuration file
destination_config = dotenv_values("../.env.destination")

db_host = source_config['POSTGRES_HOST']

if not wait_for_postgres(host=db_host):
    exit(1)

print("Starting ELT script...")

# Using dump files to initialise the database
dump_command = [
    'pg_dump',
    '-h', source_config['POSTGRES_HOST'],
    '-U', source_config['POSTGRES_USER'],
    '-d', source_config['POSTGRES_DB'],
    '-f', 'data_dump.sql',
    '-w'  # no prompt for password
]

# Set environment variables to avoid the password dump
# It will NOT ask for the password every single time
subprocess_env = dict(PGPASSWORD=source_config['POSTGRES_PASSWORD'])

# Execute the dump_command created previously to dump the sql file
# into the source database.
run(dump_command, env=subprocess_env, check=True)

# Get everything from the source database to the destination database
load_command = [
    'psql',
    '-h', destination_config['POSTGRES_HOST'],
    '-U', destination_config['POSTGRES_USER'],
    '-d', destination_config['POSTGRES_DB'],
    '-a', '-f', 'data_dump.sql'  # print all lines from the file
]

# Set environment variables to avoid the password dump
# It will NOT ask for the password every single time
subprocess_env = dict(PGPASSWORD=destination_config['POSTGRES_PASSWORD'])

# Execute the load_command created previously to load the sql file
# into the destination database.
run(load_command, env=subprocess_env, check=True)

print("Ending ELT script...")
