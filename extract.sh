#!/bin/bash

# - Definitions
PROGRESS_BAR_END="\033[0m\033[48;2;0;100;100m "
PROGRESS_BAR_BG="\033[0m\033[48;2;30;50;50m "
PROGRESS_BAR="\033[0m\033[48;2;0;200;200m "
CYAN_BOLD='\033[1m\033[38;2;0;230;230m'
YELLOW='\033[0m\033[38;2;255;255;0m'
GRAY='\033[0m\033[38;2;230;230;230m'
CYAN='\033[0m\033[38;2;0;230;230m'
GREEN='\033[0m\033[38;2;0;255;0m'
RED='\033[0m\033[38;2;200;10;0m'
RESET='\033[0m'
ENDL='\n'
TAB='   '

# - Log Aternatives
WARNING="${YELLOW}[WARNING]${RESET}"
SUCCESS="${GREEN}[SUCCESS]${RESET}"
FAILED="${RED}[FAILED]${RESET}"
LOG="${GRAY}[LOG]${RESET}"

# - Input File
input_file="earthquakes.txt"
# - Output File
output_file="filtered_coordinates.txt"

# - Remove Output File if Exists
rm -f "$output_file"

# - Japan Coordinates
# - Latitude: 24° to 46° N
# - Longitude: 122° to 153° E

# - Extract Coordinates Based on Latitude and Longitude Criteria
awk -F',' 'NR > 1 {
    datetime = $1
    latitude = $2
    longitude = $3
    depth = $4
    magnitude = $5
    event_id = $12
    if (latitude >= 24 && latitude <= 40 && longitude >= 44 && longitude <= 64) {
        print datetime "," latitude "," longitude "," depth "," magnitude "," event_id
    }
}' "$input_file" > "$output_file"

echo -e "$LOG Records have been Extracted and Saved in $output_file"

# - Generate Map
python3 show_in_map.py

# - HTML File Path
FILE_PATH="/home/qb/Files/Github/freetime/40021441054102/TERM-6/OS-Lab/OS-Projects-Solutions/Analyze-Earthquake-Logs/earthquakes.html"

# - Open Map
chromium-browser --noerrdialogs --disable-infobars --start-maximized --disable-pinch --disable-translate --disable-contextual-search --no-sandbox --kiosk "file://$FILE_PATH"

# input_file="earthquakes.txt"
# output_file="filtered_coordinates.txt"

# rm -f "$output_file"

# drawProgressBar() {
#     percentage=$(echo "scale=2; $1" | bc)
#     cols=$(tput cols)
#     progressBarWidth=$((cols - 10))
#     completedWidth=$(echo "scale=0; $percentage * $progressBarWidth / 100" | bc)

#     printf "$PROGRESS_BAR_END\033[0m"
#     for ((i = 0; i < completedWidth; i++)); do printf "$PROGRESS_BAR"; done
#     for ((i = completedWidth; i < progressBarWidth; i++)); do printf "$PROGRESS_BAR_BG"; done
#     printf "$PROGRESS_BAR_END\033[0m %.2f%%\r" "$percentage"
# }

# echo "DateTime,Latitude,Longitude,Depth,Magnitude,EventID" > "$output_file"
# total_lines=$(wc -l < "$input_file")
# current_line=0

# tail -n +2 "$input_file" | while IFS=',' read -r datetime latitude longitude depth magnitude magtype nbstations gap distance rms source eventid; do
#     if (( $(echo "$latitude >= 24 && $latitude <= 40 && $longitude >= 44 && $longitude <= 64" | bc -l) )); then
#         echo "$datetime,$latitude,$longitude,$depth,$magnitude,$eventid" >> "$output_file"
#     fi

#     ((current_line++))
#     progress=$(awk "BEGIN {print ($current_line * 100 / $total_lines)}")
#     drawProgressBar $progress
# done

# echo "Filtered coordinates, DateTime, Depth, Magnitude, and Event ID extracted and saved in $output_file"
