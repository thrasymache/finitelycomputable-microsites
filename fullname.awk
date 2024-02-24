#! /usr/bin/awk -f

BEGIN { FS=" = " }
$1 == "name" {
  gsub("\"", "", $2);
  printf "%s-", $2;
  "cat pyproject/version" | getline;
  print $0;
  exit;
}
