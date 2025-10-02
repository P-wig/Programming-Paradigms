""" URL=https://github.com/apache/datafusion

function process() {
        # $1 $2 $3 $4 .....
        name=${1##*/}

        if [ ! -d "$name" ]; then
                git clone "$url" || return 255
        fi

        #find "$name" -name "*.rs" | wc -l
        #find "$name" -name "*.rs"

        for f in $(find "$name" -name "*.rs"); do
                grep 'ab' $f > /dev/null
                if [ $? -eq 0 ]; then
                        echo $f
                fi
        done

        return 0
}

process "$URL" > output.txt
grep 'window' output.txt """
# original shell script above

import sys
import subprocess
from pathlib import Path

URL = "https://github.com/apache/datafusion"
OUTFILE = "output.txt"

def process( url ):
    # obtain the final segment of the URL path "datafusion"
    repo = url.rstrip("/").split("/")[-1]
    repo_path = Path(repo)

    # clone the repository if it doesn't exist in the current directory
    if not repo_path.is_dir():
        try:
            subprocess.run(["git", "clone", url], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error cloning repository: {e}")
            return 255

    # Use recursive globbing to find all .rs files
    matches = []
    for f in repo_path.rglob("*.rs"):
        try:
            text = f.read_text(errors="ignore")
        except Exception:
            continue
        # check for substring 'ab' in the content of the searched file
        if "ab" in text:
            matches.append(str(f))

    # print all matches like in shell script
    '''for m in matches:
        print(m)'''

    return matches

if __name__ == "__main__":
    result = process(URL)
    if result == 255:
        sys.exit(255)
    
    # write all returned matches to output file
    with open(OUTFILE, "w", encoding="utf-8") as out:
        for line in result:
            out.write(line + "\n")

        # print lines in the output file containing substring 'window'
        for line in result:
            if "window" in line:
                print(line.rstrip("\n"))