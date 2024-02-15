#! /usr/bin/awk -f

BEGIN { FS=" = " }
 {metadata[$1] = $2}
END {
  gsub("\"", "", metadata["name"]);
  gsub("-", "_", metadata["name"]);
  "cat pyproject/version" | getline;
  printf "%s-%s-py3-none-any.whl\n", metadata["name"], $0;
}
