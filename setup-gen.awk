#! /usr/bin/awk -f

BEGIN {system("cat setup/preamble")
       system("cat setup/version")}
{print}
END {system("cat setup/invocation")}
