VS Code Remote Development Setup
=================================

Why Remote Development?
-----------------------

While traditional SSH + terminal editors work, VS Code Remote-SSH provides:

- **IntelliSense**: Auto-completion for Python libraries (nilearn, nibabel)
- **Integrated debugging**: Set breakpoints, inspect variables
- **Git integration**: Visual diff, branch management, merge conflict resolution
- **Extensions**: Python linting, formatting, testing tools
- **Persistent sessions**: Editor state survives connection drops

Prerequisites
-------------

Before starting, ensure you have:

- VS Code installed on your local machine (`Download <https://code.visualstudio.com/>`_)
- SSH access credentials for the HPC cluster
- SSH key configured (optional but recommended)
- GitHub account created

Step 1: Install Required Extensions
------------------------------------

Open VS Code and install these extensions:

1. Press ``Ctrl+Shift+X`` (Windows/Linux) or ``Cmd+Shift+X`` (Mac)
2. Search and install:

   - **Remote - SSH** (``ms-vscode-remote.remote-ssh``)
   - **Remote - SSH: Editing Configuration Files**
   - **Python** (``ms-python.python``)

.. note::
   The Remote-SSH extension needs to be installed **locally** (on your laptop). 
   Once connected to HPC, you'll install extensions **remotely** as needed.

Step 2: Configure SSH Connection
---------------------------------

What is SSH config?
~~~~~~~~~~~~~~~~~~~

The SSH config file (``~/.ssh/config``) stores connection profiles. Instead of 
typing ``ssh username@hpc.institution.edu`` every time, you create a short alias 
like ``hpc-cluster``.

Open SSH Config File
~~~~~~~~~~~~~~~~~~~~

1. Press ``F1`` or ``Ctrl+Shift+P`` (Windows/Linux) or ``Cmd+Shift+P`` (Mac)
2. Type: ``Remote-SSH: Open SSH Configuration File``
3. Select your SSH config file (usually ``~/.ssh/config``)

Add HPC Connection
~~~~~~~~~~~~~~~~~~

**For Linux/Mac:**

.. code-block:: ssh

   Host hpc-cluster
       HostName hpc.institution.edu
       User your_username
       IdentityFile ~/.ssh/id_rsa
       ForwardAgent yes
       ServerAliveInterval 60
       ServerAliveCountMax 3

**For Windows:**

.. code-block:: ssh

   Host hpc-cluster
       HostName hpc.institution.edu
       User your_username
       IdentityFile C:\Users\YourName\.ssh\id_rsa
       ForwardAgent yes
       ServerAliveInterval 60
       ServerAliveCountMax 3

Understanding SSH Configuration Options
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- **HostName**: The actual server address (e.g., ``hpc.institution.edu``)
- **User**: Your HPC username (replaces ``username@`` in ssh commands)
- **IdentityFile**: Path to your SSH private key for passwordless authentication
- **ForwardAgent**: Allows using your local SSH keys on the remote server (useful for Git)
- **ServerAliveInterval**: Sends keep-alive packet every 60 seconds to prevent disconnection
- **ServerAliveCountMax**: Drops connection after 3 missed keep-alive responses

Step 3: SSH Keys for Mac Users
-------------------------------

For secure authentication with GitHub and HPC access, you'll need SSH keys. This is 
especially important for passwordless authentication and Git operations.

Check for Existing Keys
~~~~~~~~~~~~~~~~~~~~~~~

First, check if you already have SSH keys:

.. code-block:: bash

   ls ~/.ssh

If you see files like ``id_rsa`` and ``id_rsa.pub``, you already have a key pair.
You can skip to adding the public key to GitHub below.

Expected output with existing keys:

.. code-block:: text

   authorized_keys  id_rsa      id_rsa.pub   config   known_hosts

Generate New RSA Key
~~~~~~~~~~~~~~~~~~~~

If you don't have keys, create a new RSA key pair:

.. code-block:: bash

   ssh-keygen -t rsa

.. warning::
   If you have an existing ``id_rsa`` file, this command will overwrite it! 
   Press Ctrl+C to cancel if you want to keep your existing key.

When prompted:

1. **File location**: Press Enter to use the default location (``~/.ssh/id_rsa``)
2. **Passphrase**: Enter a strong passphrase for security (recommended)

Add Public Key to GitHub
~~~~~~~~~~~~~~~~~~~~~~~~~

Copy your public key to the clipboard:

.. code-block:: bash

   cat ~/.ssh/id_rsa.pub

This will display your public key. Copy the entire output.

Then:

1. Go to GitHub → Settings → SSH and GPG keys
2. Click **New SSH key**
3. Give it a descriptive title (e.g., "HPC Workstation")
4. Paste your public key in the "Key" field
5. Click **Add SSH key**

Test SSH Connection
~~~~~~~~~~~~~~~~~~~

Verify your SSH key works with GitHub:

.. code-block:: bash

   ssh -T git@github.com

You should see a message like:

.. code-block:: text

   Hi YOUR_USERNAME! You've successfully authenticated, but GitHub does not provide shell access.

.. note::
   Now you can use SSH URLs (``git@github.com:username/repo.git``) instead of 
   HTTPS URLs when cloning repositories for better security and convenience.

Step 4: Connect to HPC Cluster
-------------------------------

1. Press ``F1`` → Type ``Remote-SSH: Connect to Host``
2. Select ``hpc-cluster`` from the dropdown
3. Enter your password if prompted
4. **Wait for connection** (first connection installs VS Code Server - takes 1-2 minutes)

.. tip::
   When connected, you'll see ``SSH: hpc-cluster`` in the bottom-left corner in green.

.. warning::
   VS Code automatically downloads and installs a server component (~60MB) on the 
   HPC cluster during your first connection. Subsequent connections will be much faster.

Step 5: Open Your Workspace
----------------------------

1. Click **File → Open Folder** (or press ``Ctrl+K Ctrl+O``)
2. Navigate to: ``/home/your_username/workshop``
3. Click **OK**

.. tip::
   If the directory doesn't exist, create it first:
   
   .. code-block:: bash
   
      mkdir -p ~/workshop

Step 6: Configure Python Environment
-------------------------------------

Why configure the Python interpreter?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

VS Code needs to know which Python installation to use for features like 
auto-completion, linting, and debugging. HPC clusters often have multiple 
Python versions.

Select Python Interpreter
~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Press ``F1`` → Type ``Python: Select Interpreter``
2. Choose from available options:

   - System Python: ``/usr/bin/python3``
   - Conda environment: ``/home/username/miniconda3/envs/neuro/bin/python``
   - Module-based: ``/opt/apps/python/3.9/bin/python``

Configure Python Settings
~~~~~~~~~~~~~~~~~~~~~~~~~~

Create ``.vscode/settings.json`` in your workspace:

.. code-block:: json

   {
       "python.defaultInterpreterPath": "${env:HOME}/miniconda3/envs/neuro/bin/python",
       "python.terminal.activateEnvironment": true,
       "python.linting.enabled": true,
       "python.linting.flake8Enabled": true,
       "python.formatting.provider": "black"
   }

Step 7: Setup Integrated Terminal
----------------------------------

1. Open terminal: **Terminal → New Terminal** (``Ctrl+Shift+```)
2. Verify Python: ``python --version``
3. Verify Git: ``git --version``

.. tip::
   If your HPC uses environment modules:
   
   .. code-block:: bash
   
      module load python/3.9
      module load git

Step 8: Configure Git Identity
-------------------------------

Why configure Git identity?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Git tracks **who** made each change. Your commits include your name and email.

.. code-block:: bash

   git config --global user.name "Your Name"
   git config --global user.email "your.email@institution.edu"
   git config --global core.editor "code --wait"
   git config --global init.defaultBranch main

Configuration breakdown:

- ``user.name``: Your full name (appears in commit history)
- ``user.email``: Email for GitHub (should match your GitHub account)
- ``core.editor``: Use VS Code for commit messages
- ``init.defaultBranch``: Use ``main`` instead of ``master``

Verify configuration:

.. code-block:: bash

   git config --list

Troubleshooting
---------------

Connection Issues
~~~~~~~~~~~~~~~~~

**Could not establish connection**

Possible causes:

1. Not connected to institution VPN
   
   .. code-block:: bash
   
      ping hpc.institution.edu

2. SSH key permissions too open
   
   .. code-block:: bash
   
      chmod 600 ~/.ssh/id_rsa
      chmod 644 ~/.ssh/id_rsa.pub

Python Issues
~~~~~~~~~~~~~

**Python interpreter not found**

1. Open Settings (``Ctrl+,``)
2. Search "python.defaultInterpreterPath"
3. Enter full path: ``/usr/bin/python3``

Performance Issues
~~~~~~~~~~~~~~~~~~

**Slow connection / Frequent disconnects**

Add to SSH config:

.. code-block:: ssh

   Host hpc-cluster
       Compression yes
       ServerAliveInterval 30
       ServerAliveCountMax 5
       TCPKeepAlive yes

.. Use tmux for persistent sessions:

.. .. code-block:: bash

..    module load tmux
..    tmux new -s workshop
..    # Work happens here
..    # Detach: Ctrl+B then D
..    # Reattach: tmux attach -t workshop