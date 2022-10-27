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

WIN_INSTALL_PATH="Wiimm/SZS"

#------------------------------------------------------------------------------
echo "* setup"

export PATH=".:$PATH"
mkdir -p /tmp

#---------------

SENDTO_SRC=./windows-sendto
if [[ ! -d $SENDTO_SRC ]]
then
    SENDTO_SRC="$WIN_INSTALL_PATH/windows-sendto"
    if [[ ! -d $SENDTO_SRC ]]
    then
	echo "Can't find SendTo source => abort" >&2
	exit 1
    fi
fi

#---------------

key="/user/Software/Microsoft/Windows/CurrentVersion/Explorer/Shell Folders/SendTo"
if ! WIN_SENDTO_PATH="$(regtool get "$key")" || [[ $WIN_SENDTO_PATH = "" ]]
then
    echo "Can't determine Windows program path => abort" >&2
    exit 1
fi
CYGWIN_SENDTO_PATH="${WIN_SENDTO_PATH//\\//}"


#------------------------------------------------------------------------------
echo "* install SendTo scripts"
echo "   - SendTo source: $SENDTO_SRC"
echo "   - SendTo folder: $WIN_SENDTO_PATH"
echo "   -            ->: $CYGWIN_SENDTO_PATH"

cp -p "$SENDTO_SRC"/* "$CYGWIN_SENDTO_PATH/"

#------------------------------------------------------------------------------

exit 0

