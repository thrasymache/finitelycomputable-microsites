#! /usr/bin/awk -f

BEGIN { FS=" = " }
 {metadata[$1] = $2}
END {
  "cat pyproject/version" | getline;
  gsub("\"", "", metadata["name"]);
  printf "%s-%s.tar.gz\n", metadata["name"], $0;
}
