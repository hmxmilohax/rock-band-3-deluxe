#!/bin/bash
#modified version of wiimmfi-patcher-v7.5 script
#all credit to them
export PATCHER_NAME="Rock Band 3 Deluxe Patcher v1.0"
export DATE=2024-03-18
export COPYRIGHT="(c) wiimm (at) wiimm.de -- $DATE"

export STATUS_URL=http://download.wiimmfi.de/patcher/info/wiimmfi-patcher-v7.5.txt
export RB3DX_URL=https://github.com/hmxmilohax/rock-band-3-deluxe
export PATCHER_URL=https://wiimmfi.de/patcher/iso
export NKIT_URL=https://wiimmfi.de/patcher/nkit

export DESTDIR=./rock-band-3-deluxe
export WORKDIR=./patch-dir
export LOGDIR="./_log"

export LC_ALL=C

export COL_LOG="\033[44;37;1m"
export COL_SUM="\033[33;1m"
export COL_ACTIVITY="\033[36;1m"
export COL_ERROR="\033[41;37;1m"
export COL_HEAD="\033[44;37;1m"
export COL_INFO="\033[42;37;1m"
export COL0="\033[0m"

script="${0##*/}"

ERR_WARN=28
ERR_ERROR=112

#
#------------------------------------------------------------------------------
# print title

function print_title
{
    local msg="***  $PATCHER_NAME  -  $DATE  ***"
    local stars="************************************************"
    printf -v stars '\e[44;37;1m%.*s\e[0m' ${#msg} "$stars$stars"
    printf '\e[0m\n%s\n\e[44;37;1m%s\e[0m\n%s\n\n' "$stars" "$msg" "$stars"
}

function print_info
{
    local done=0
    if which curl >/dev/null 2>&1
    then
	curl -Lfs -m2 "$STATUS_URL" 2>/dev/null && let done++
    elif which wget >/dev/null 2>&1
    then
	wget -qO- -T2 "$STATUS_URL" 2>/dev/null && let done++
    fi

    ((done)) || printf 'Visit \e[36;1m%s\e[0m for more details.\n\n' "$RB3DX_URL"
    ((done)) || printf 'Based on wiimmfi-patcher-v7.5. All credit to them\nVisit \e[36;1m%s\e[0m for more details.\n\n' "$PATCHER_URL"
}

((PRINT_TITLE>0)) && print_title
((PRINT_TITLE>1)) && print_info

#
#------------------------------------------------------------------------------
# system and bin path

#--- BASEDIR

if [[ ${BASH_SOURCE:0:1} == / ]]
then
    BASEDIR="${BASH_SOURCE%/*}"
    [[ $BASEDIR = "" ]] && BASEDIR=/
else
    BASEDIR="$PWD/$BASH_SOURCE"
    BASEDIR="${BASEDIR%/*}"
fi
export BASEDIR


#--- predefine BINDIR & PATH for Cygwin

export ORIGPATH="$PATH"
export BINDIR="$BASEDIR/cygwin"
[[ -d $BINDIR ]] && export PATH="$BINDIR:$ORIGPATH"


#--- find system

export SYSTEM="$( uname -s | tr '[A-Z]' '[a-z]' )"
export MACHINE="$( uname -m | tr '[A-Z]' '[a-z]' )"
export HOST

case "$SYSTEM-$MACHINE" in
    darwin-*)		HOST=mac ;;
    linux-x86_64)	HOST=linux64 ;;
    linux-*)		HOST=linux32 ;;
    cygwin*-x86_64)	HOST=cygwin64 ;;
    cygwin*)		HOST=cygwin32 ;;
    *)			HOST=- ;;
esac


#--- setup BINDIR and PATH

BINDIR="$BASEDIR/$HOST"
((VERBOSE>0)) && echo "BINDIR      = $BINDIR"
if [[ -d $BINDIR ]]
then
    chmod u+x "$BINDIR"/* 2>/dev/null || true
    export PATH="$BINDIR:$ORIGPATH"
fi

export WIT="$BINDIR/wit"
export WSZST="$BINDIR/wszst"

#
#------------------------------------------------------------------------------
# check existence of tools

needed_tools="
	awk bash cat chmod cp cut date diff find grep ln
	mkdir mv rm sed sort tar touch tr uname uniq unzip wc which
	wit wszst
"

err=

for tool in $needed_tools
do
    if ! which $tool >/dev/null 2>&1
    then
	err+=" $tool"
    fi
done

if [[ $err != "" ]]
then
    printf "\n\033[31;1m!!! Missing tools:$err => abort!\033[0m\n\n" >&2
    printf "\033[36mPATH:\n   " >&2
    sed 's/:/\n   /g' <<< "$PATH" >&2
    printf "\033[0m\n" >&2
    exit 1
fi

printf '\e[0;30;47m HOST: %s \e[m\n' "$HOST"

#
#------------------------------------------------------------------------------
# logging

function printlog_helper
{
    ((quiet)) && return 0
    echo
    local col="$1"
    shift
    local msg xmsg="$(printf "$@")"
    while read msg
    do
	if [[ $msg = "-" ]]
	then
	    echo
	else
	    local len len1 len2
	    let len=79-$( unset LC_ALL; LC_CTYPE=en_US.UTF-8; echo ${#msg} )
	    ((len<0)) && len=0
	    let len1=len/2
	    let len2=len-len1
	    printf "${col}%*s%s%*s${COL0}\n" $len1 "" "$msg" $len2 ""
	fi
    done <<< "$xmsg"
}

function print_log
{
    printlog_helper "${COL_LOG}" "$@"
}

function print_sum
{
    printlog_helper "${COL_SUM}" "$@"
}

function print_activity
{
    printlog_helper "${COL_ACTIVITY}" "»»» $@ «««"
}

function error_exit # errcode lines...
{
    local err=$1
    shift

    printlog_helper "${COL_ERROR}" "ERROR $err => ABORT"
    for line in "$@" ---
    do
        printf "\e[31;1m%s\e[0m\n" "$line" >&2
    done
    exit $err
}

#
#------------------------------------------------------------------------------
# function patch_mkw

function patch_mkw
{
    local SRCIMG="$1"
    local SRCNAME="${SRCIMG##*/}"
    if [[ $res_id6 = "SZBE69" ]]; then
        local DESTIMG="rock-band-3-deluxe/Rock Band 3 Deluxe (USA).wbfs"
    fi
    if [[ $res_id6 = "SZBP69" ]]; then
        local DESTIMG="rock-band-3-deluxe/Rock Band 3 Deluxe (PAL).wbfs"
    fi
    local FF_OPT="$3"
    local LANG="E F G I J K M Q S U"

    ##########################################################################
    # extract image

    print_activity "Extract image: $SRCIMG"

    rm -rf "$WORKDIR"
    "$WIT" extract -vv -1p "$SRCIMG" --links --DEST "$WORKDIR" --psel data \
		|| error_exit $ERR_ERROR "Error while extracting image: $SRCIMG"
    
    cp wii_patch_files/gen/main_wii.hdr patch-dir/files/gen/main_wii.hdr
    cp wii_patch_files/gen/main_wii_10.ark patch-dir/files/gen/main_wii_10.ark
    ##########################################################################

    "$WIT" copy -vv --links "$WORKDIR" --DEST "$DESTIMG" \
		|| error_exit $ERR_ERROR "Error while creating image: $DESTIMG"
    rm -rf "$WORKDIR"
    true
}

#
###############################################################################
###############			    E N D			###############
###############################################################################
