# gridscr
Tools for generating a rainrate composite using Helsinki metropolitean area weather radars.

## Usage tips

### Running the main workflow script

First, make an empty directory for logs. You can use any empty directory.

    mkdir log

You can run the workflow script with

    composite_workflow.sh -l log

Note that when processing many days of data, the processing can take days. Easiest way to leave your stuff running without having to remain logged in is by using tmux, e.g.:

    tmux new-session composite_workflow -l logs

This launches the script in a virtual terminal. You can detach (put to background) the terminal with Ctrl+b followed by d. At this point you can close the SSH-connection. The script will remain running on the machine. You can check back with the script in the virtual terminal with

    tmux attach

### Help and troubleshooting

Most of the scripts show brief help texts with the -h flag, e.g.

    composite_workflow.sh -h

You can find the script location with which. For example, to see under the hood of the main workflow script, type

    less $(which composite_workflow.sh)

Each part of the workflow creates two types of logs. The .log files show current progress and .err files have errors, warnings and other info.
