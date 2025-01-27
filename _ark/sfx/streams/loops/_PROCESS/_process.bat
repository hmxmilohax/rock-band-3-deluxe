:: this is here to make my job easier
:: written by chatgpt, reviewed and tested by a human

@echo off

for %%f in (*.mogg) do (
    echo Processing %%f...
    
    :: Convert .mogg to .ogg
    ogg2mogg "%%f" "%%~nf.ogg"
    
    :: Compress and resample the .ogg file
    sox "%%~nf.ogg" -r 28k -C 0.0000000000001 "%%~nf-small.ogg"
    
    :: Rename the compressed .ogg file back to the original .ogg name
    del "%%~nf.ogg"
    rename "%%~nf-small.ogg" "%%~nf.ogg"
    rename "%%f" "%%f.bak"
    
    :: Convert the updated .ogg back to .mogg
    makemogg "%%~nf.ogg" -m "%%f"
)

echo All files processed.
