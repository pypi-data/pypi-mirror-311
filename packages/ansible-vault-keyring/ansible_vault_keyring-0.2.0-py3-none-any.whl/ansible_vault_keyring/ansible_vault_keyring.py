"""ansible-vault-keyring
A simple tool to get and set passwords for ansible vaults using the system keyring.
"""

import enum
import getpass
import logging
import sys

import keyring
import typed_argparse as tap
from ansible.config import manager as acm

# Logging Setup
logger = logging.getLogger(__name__)
console_handler = logging.StreamHandler()
logger.addHandler(console_handler)


class ReturnCodes(enum.IntEnum):
    """Return codes for the program.
    """
    OK = 0
    MISMATCHED_PASSWORDS = 1
    KEYNAME_UNKNOWN = 2


class DebugLevel(enum.IntEnum):
    """Debug levels, that map to logging module loglevels
    """
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


class Args(tap.TypedArgs):
    """The CLI Arguments for the program"""
    vault_id: str = tap.arg(
        help="Get/set a vault password with this id from the users keyring"
    )
    username: str | None = tap.arg(help="The username to query for the keyring")
    debug_level: DebugLevel = tap.arg(
        auto_default_help=True,
        default=DebugLevel.CRITICAL,
    )
    set: bool = tap.arg(help="Set the password instead of getting it", default=False)


def get_username(args: Args, config: acm.ConfigManager) -> str:
    """Gets a username from these sources in order.

    1. The --username arg
    2. The ansible.cfg file
    3. The current user.

    Args:
        args (Args): The command line arguments.
        config (acm.ConfigManager): For the ansible.cfg results.

    Returns:
        str: The username to use for the keyring.
    """

    if args.username:
        return args.username
    ini_cfg_value = acm.get_ini_config_value(
        config._parsers.get(config._config_file), dict(section="vault", key="username")
    )
    if ini_cfg_value:
        return ini_cfg_value
    else:
        return getpass.getuser()


def get_keyname(vault_id: str) -> str:
    """Makes the keyname"""
    return f"ansible_vault_keyring_{vault_id}"


def validate_passwords_match(password1: str, password2: str) -> bool:
    """Checks if the two passwords match.

    Args:
        password1 (str): The first password.
        password2 (str): The second password.

    Returns:
        bool: true if they match, falsse otherwise.
    """
    return password1 == password2


def set_password_in_keyring(username: str, keyname: str) -> None:
    """Sets the password in the system keyring.

    Args:
        args (Args): The command line arguments.
        username (str): The username to use for the keyring.
        keyname (str): The keyname to use for the keyring.
    """
    sys.stdout.write(
        f"Storing password in {username} user keyring using key name: {keyname}\n"
    )
    password1 = getpass.getpass("Enter password   : ")
    password2 = getpass.getpass("Confirm password : ")
    if validate_passwords_match(password1, password2):
        keyring.set_password(keyname, username, password1)
    else:
        sys.stderr.write("Passwords do not match\n")
        sys.exit(ReturnCodes.MISMATCHED_PASSWORDS.value)


def get_password_from_keyring(username: str, keyname: str) -> str:
    """Gets a password out of the keyring, and prints it to stdout.

    Args:
        username (str): The username to use for the keyring.
        keyname (str): The keyname to use for the keyring.
    """
    secret = keyring.get_password(keyname, username)
    if secret is None:
        sys.stdout.write(
            f"No password found for {username} in {keyname} via backend {keyring.get_keyring().name}\n"
        )
        sys.exit(ReturnCodes.KEYNAME_UNKNOWN.value)
    else:
        return secret


def runner(args: Args) -> None:
    """The main function.
    """
    logger.setLevel(args.debug_level.value)
    logger.debug("Running with args: %s", args)
    # ConfigManager tries to load values from ansible.cfg ini files, using ansible
    # rules for finding the config file.
    config_manager = acm.ConfigManager()
    username = get_username(args, config_manager)
    logger.debug("Username: %s", username)
    keyname = get_keyname(args.vault_id)
    logger.debug("Keyname: %s", keyname)

    if args.set:
        set_password_in_keyring(username, keyname)
    else:
        password = get_password_from_keyring(username, keyname)
        sys.stdout.write(f"{password}\n")


def main() -> None:
    """The main function. Just invokes the runner function.
    """
    tap.Parser(Args).bind(runner).run()


if __name__ == "__main__":
    main()
