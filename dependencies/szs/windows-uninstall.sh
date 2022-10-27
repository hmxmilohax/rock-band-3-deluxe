#!/usr/bin/env bash

    #####################################################################
    ##                    _______ _______ _______                      ##
    ##                   |  ___  |____   |  ___  |                     ##
    ##                   | |   |_|    / /| |   |_|                     ##
    ##                   | |_____    / / | |_____                      ##
    ##                   |_____  |  / /  |_____  |                     ##
    ##                    _    | | / /    _    | |                     ##
    ##                   | |___| |/ /____| |___| |                     ##
    ##                   |_______|_______|_______|                     ##
    ##                                                                 ##
    ##                        Wiimms SZS Tools                         ##
    ##                      http://szs.wiimm.de/                       ##
    ##                                                                 ##
    #####################################################################
    ##                                                                 ##
    ##   This file is part of the SZS project.                         ##
    ##   Visit http://szs.wiimm.de/ for project details and sources.   ##
    ##                                                                 ##
    ##   Copyright (c) 2011-2019 by Dirk Clemens <wiimm@wiimm.de>      ##
    ##                                                                 ##
    #####################################################################

#------------------------------------------------------------------------------
# simple cygwin check

if [[ $1 != --cygwin ]]
then
    echo "Option --cygwin not set => exit" >&2
    exit 1
fi

#------------------------------------------------------------------------------
# pre definitions

BIN_FILES="wszst wbmgt wimgt wkclt wkmpt wstrt "
SHARE_FILES=""
WIN_INSTALL_PATH="Wiimm/SZS"

#------------------------------------------------------------------------------
# setup

echo "* setup"

export PATH=".:$PATH"

key="/machine/SOFTWARE/Microsoft/Windows/CurrentVersion/ProgramFilesDir"
if ! WIN_PROG_PATH="$(regtool get "$key")" || [[ $WIN_PROG_PATH = "" ]]
then
    echo "Can't determine Windows program path => abort" >&2
    exit 1
fi
#CYGWIN_PROG_PATH="$( realpath "$WIN_PROG_PATH" )"
CYGWIN_PROG_PATH="${WIN_PROG_PATH//\\//}"

WDEST="$WIN_PROG_PATH\\${WIN_INSTALL_PATH//\//\\}"
CDEST="$CYGWIN_PROG_PATH/$WIN_INSTALL_PATH"

#------------------------------------------------------------------------------
# remove application pathes

for tool in $BIN_FILES
do
    key="/machine/SOFTWARE/Microsoft/Windows/CurrentVersion/App Paths/$tool.exe"
    if regtool check "$key" >/dev/null 2>&1
    then
	echo "* remove application path for '$tool.exe'"
	regtool unset "$key/" "${WDEST}\\${tool}.exe"
	regtool unset "$key/Path" "${WDEST}\\"
	regtool remove "$key"
    fi
done

#------------------------------------------------------------------------------
# add WIT path to environment 'Path'

echo "* add SZS path to environment 'Path'"

function set_path()
{
    local key="$1"

    local p=
    local count=0
    local new_path=

    # split at ';' & substitute ' ' temporary to ';' to be space save
    for p in $( regtool --quiet get "$key" | tr '; ' '\n;' )
    do
	p="${p//;/ }"
	#echo " -> |$p|"
	[[ "$p" = "$WDEST" ]] || new_path="$new_path;$p"
    done

    [[ $new_path = "" ]] || regtool set -e "$key" "${new_path:1}"
}

set_path '/machine/SYSTEM/CurrentControlSet/Control/Session Manager/Environment/Path'
set_path '/user/Environment/Path'

#------------------------------------------------------------------------------

