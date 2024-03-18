#modified version of wiimmfi-patcher-v7.5 script
#all credit to them

#!/usr/bin/env bash

#----- setup

PRINT_TITLE=2
. ./bin/setup.sh

#----- for each source image

"$WIT" --allow-nkit filelist | tr -d '\r' | while read src
do
    [[ -f $src ]] || continue
    mkdir -p "$LOGDIR"
    chmod 777 "$LOGDIR" 2>/dev/null
    log="$LOGDIR/${src##*/}.txt"
    ana="$LOGDIR/${src##*/}.ana"

    (
	res_file=
	res_file_type=
	"$WIT" analyze --bash "$src" -d "$ana" --var res_
	. "$ana"


    if [[ $res_id6 = "SZBE69" ]]; then
        dest="rock-band-3-deluxe/Rock Band 3 Deluxe (USA).wbfs"
    fi
    if [[ $res_id6 = "SZBP69" ]]; then
        dest="rock-band-3-deluxe/Rock Band 3 Deluxe (PAL).wbfs"
    fi
	if [[ -a $dest ]]
	then
	    printf '%b Already exists: %s %b\n' "$COL_ERROR" "$dest" "$COL0"
	    exit 1
	fi

	if [[ ! $res_file || ! $res_file_type || $res_file_type = OTHER ]]
	then
	    printf '%b Not a Wii image: %s %b\n' "$COL_ERROR" "$src" "$COL0"
	    exit 1
	fi

	if [[ $res_file_type =~ ^NK ]]
	then
	    printf '%b NKIT images not supported: %s %b\n' "$COL_ERROR" "$src" "$COL0"
	    printf ' > Visit \e[36;1m%s\e[0m for more details.\n\n' "$NKIT_URL"
	    exit 1
	fi

	if [[ $res_dol_avail = 0 ]]
	then
	    printf '%b Invalid Wii image: %s %b\n' "$COL_ERROR" "$src" "$COL0"
	    exit 1
	fi

	if [[ $res_id6 != "SZBE69" && $res_id6 != "SZBP69" ]]
	then
	    printf '%b Only Vanilla Rock Band 3 USA/PAL is supported with this tool: %s %b\n' "$COL_ERROR" "$src" "$COL0"
	    exit 1
	fi
    

	#--- patch image

	mkdir -p "$DESTDIR" 
	chmod 777 "$DESTDIR" 2>/dev/null

	if [[ $res_dol_is_mkw = 0 ]]
	then
	    printf '\n%b Patch image: %s %b\n' "$COL_HEAD" "$src" "$COL0"
	    patch_mkw "$src" "$dest" "$res_type_option" 2>&1
	else
	    printf '\n%b Patch MKW image: %s %b\n' "$COL_HEAD" "$src" "$COL0"
	    patch_mkw "$src" "$dest" "$res_type_option" 2>&1
	fi
	printf '\n'

    ) 2>&1 | tee "$log"
done

