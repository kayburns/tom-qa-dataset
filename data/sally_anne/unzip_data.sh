for file in *.zip
do
    directory="${file%.zip}"
    unzip "$file" -d "$directory"
done
