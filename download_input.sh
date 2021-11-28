#!/bin/bash

set -e
set -x

if [ $# -ne 1 ]
then
  echo "Usage: $0 <day>"
  exit 1
fi

if [[ -z "$AOC_SESSION_ID" ]]
then
  echo "AOC_SESSION_ID is not set"
  exit 1
fi

DAY=$1
curl "https://adventofcode.com/2021/day/$DAY/input" \
  --output "day$DAY/input.txt" \
  --cookie "session=${AOC_SESSION_ID}"
