#! /usr/bin/awk -f

BEGIN {
  arrays["classifiers"] = "";
  arrays["dependencies"] = "";
  tables["project.optional-dependencies"] = "";
  tables["project.scripts"] = "";
  tables["project.urls"] = ""
  FS="\t"}
!$1 || /^#/ {next}  # skip blank lines and comments
$1 in arrays {arrays[$1] = arrays[$1] "\n  \"" $2 "\","; next}
$1 in tables {tables[$1] = tables[$1] "\n" $2; next}
$1 in metadata {
  print "error: singular metadata", $1, "specified twice" | "cat 1>&2"; next}
{ metadata[$1] = $2}
END {
  system("cat pyproject/preamble");
  "cat pyproject/version" | getline;
  print("version = \"" $0 "\"");
  for (j in metadata) print(j " = \"" metadata[j] "\"");
  for (j in arrays) if (arrays[j]) print(j " = [" arrays[j] "\n]");
  for (j in tables) if (tables[j]) print("\n[" j "]" tables[j]);}
