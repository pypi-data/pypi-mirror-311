# ansible-vault-keyring

A simple tool to get and set passwords for ansible vaults using the system keyring.

## Installation

Install ansible-vault-keyring using your favorite package manager / method.

For me, using [uv](https://github.com/astral-sh/uv/) I use.

```bash
uv tool install ansible-vault-keyring
```

## Usage

### Setting a password.

```bash
$ ansible-vault-keyring --vault-id my_vault_id --set
Enter password   : foo 
Confirm password : foo
```

### Getting a password.

```bash
$ ansible-vault-keyring --vault-id my_vault_id
foo
```

## Recommend usage.

If for example, you want to use the `ansible-vault-keyring` tool to get two passwords from your keyring,
one for a `global` vault-id, and one for a `personal` vault-id, you can add this to your `ansible.cfg` file.

```ini
[defaults]
vault_identity_list = global@/path/to/ansible_vault_keyring, personal@/path/to/ansible_vault_keyring
```

If like me you install with [uv](https://github.com/astral-sh/uv/), you will find the binary in whatever b[bin directory](https://docs.astral.sh/uv/concepts/tools/#the-bin-directory) it uses, and you should refer to that uv documentation to find the path to the standalone executable. For me this is `~/.local/bin/ansible-vault-keyring`, and I have `~/.local/bin` in my `PATH` environment variable.

Now when a password is needed by ansible, it will invoke the `ansible-vault-keyring` tool to get the password from the keyring.

### How Ansible finds config files

Ansible will load settings from the first [ansible.cfg](https://docs.ansible.com/ansible/latest/reference_appendices/config.html) file it finds from :-

1. The file in the `ANSIBLE_CONFIG` environment variable.
2. The file `ansible.cfg` file in the current working directory.
3. The file `~/.ansible.cfg` file (in the user's home directory).
4. The file `/etc/ansible/ansible.cfg` file (in the system ansible config directory).

## Security Considerations.

The file is stored in the system keyring, for example 
[gnome-keyring](https://wiki.gnome.org/Projects/GnomeKeyring) or [OSX-Keychain](https://support.apple.com/en-gb/guide/keychain-access/welcome/mac). It does this using the [keyring](https://pypi.org/project/keyring/) python package.

This means that the password is stored in plain text in the system keyring, and can be read by anyone with access to the system keyring, but this is true for all passwords stored in a system keyring.

Additionally, the password is passed through the python process running the `ansible-vault-keyring` tool.

However in reality this is likely to be at least as secure as copying+pasting the passwords from a password manager,
and will certainly be better than reusing a password, or writing it on a post it note stuck to your monitor.

## Credits

This tool was heavily inspired by [vault-keyring-client.py](https://github.com/ansible-community/contrib-scripts/blob/main/vault/vault-keyring-client.py) from ansible-community's contrib scripts.

It is either a rewrite or a fork depending on your take, and thus I consider it a derivative work. See the [LICENSE](LICENSE) file for details of the original authors of [vault-keyring-client.py](https://github.com/ansible-community/contrib-scripts/blob/main/vault/vault-keyring-client.py).
