#!/bin/sh

# Update binder requirements with main requirements.txt file
bash scripts/utils/cp_file_content.sh "requirements.txt" "binder/requirements.txt" 1
echo "Binder requirements updated."

# Create README.rst
README_SOURCES_DIR="doc/meta"
SOURCES=("title" "badges" "long_desc" "main" "badges_targets")
R="README.rst"

i=1
for source in "${SOURCES[@]}"; do
    if [[ i -eq 1 ]]; then
        REPLACE=1
    else
        REPLACE=0
        if [[ i -eq 4 ]]; then
            bash scripts/utils/cp_file_content.sh "doc/install.rst" "$R" $REPLACE
        fi
    fi
    bash scripts/utils/cp_file_content.sh "$README_SOURCES_DIR/$source.rst" "$R" $REPLACE
    echo -e "\n" >> "$R"
    i=$((i+1))
done

# Fix :targets
i=1
cat $R | while read line; do
    if [[ $line = ":target:"* || $line = "pip3 install pymarketcap"* ]]; then
        line="   $line"
    fi
    if [[ $i -eq 1 ]]; then
        echo "$line" > "$R"
    else
        echo "$line" >> "$R"
    fi
    i=$((i+1))
done

echo "Main README.rst generated."