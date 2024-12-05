# PMFlow
<p style="font-size:15px;">This is a simple process managing command line tool</p>

<p style="font-size:15px;">This tools keeps the information of the processes it manages in a json file created at it's installation location</p>

## Installation
```
pip install pmflow
```
Windows Installation: After installing pmflow with pip on windows make sure the path where the pm script is in the environment variable.

Use the below command in cmd to see the installation location of the pmflow
```
pip show pmflow
```
It should be something like ```C:\your\installation\location\Python\Python3<version>\site-packages```. In ```Python3<version>``` directory there should be a directory 
named ```scripts```. Make sure the path ```C:\your\installation\location\Python\Python3<version>\scripts``` is a environment variable and you should be good to go.
## Commands
### <^> Main commands
create: Creates a new process

Required arguments:
- command: str (default: None)

Optional arguments:
- --name or -n : str (default: None)
- --group or -g : str (default: process_id)
- --relation or -r : "parent" | "child" (default: "parent")
- --forground or -f: bool (default: false) Keeps the process alive. Useful in making .service.
- --verbose or -v: (default: false) For extra information (currently not useful)

Note: A child process must have a group name and the group must have a parent process.

Example:
```
pm create "<command>"
or
pm create "<command>" -n "<process name>" -g "<group name>" -r "child"
```
ls: List all managed processes

Optional arguments:
- --json or -j: bool (default: false)
- --group or -g: str (default: None)
- --running or -r: bool (default: false)
Example:
```
pm ls
pm ls -j
pm ls -g <group_name>
pm ls -j -g <group_name>
pm ls -r 
```
kill: Kill process, kills the process and also removes it from the json file.

Optional arguments:
- pid (no flag needed): int (default: 0) kills one process if it's a child process. Otherwise, kills the terminates 
- --group or -g: str (default: None) kills one group if exist
- --child or -c: bool (default: False) kills all child process in a group
- --all or -a : bool (default: false) kills all the process

Note: Other than -c only one options can be used at a time. -c flag must be used with -g

Example:
```
pm kill <PID>
pm kill -g <group_name>
pm kill -g <group_name> -c
pm kill -a
```
### <^> Additional commands
Recreate all process managed by the tool:
```
pm recreate
```
Pause a process
```
pm pause <PID>
```
respawn all paused process
```
pm respawn
```
