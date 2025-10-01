#!/bin/bash

co=false
cinterval=5
crest=1.5
sinterval=5
srest=1.5
scount=
scraper=false


while [[ $# -gt 0 ]]; do
  case $1 in
    -co|-overwrite)
      co="$2"
      shift 2
      ;;
    -cinterval|-crawl_interval)
      cinterval="$2"
      shift 2
      ;;
    -crest|-crawl_rest)
      crest="$2"
      shift 2
      ;;
    -sinterval|-scraper_interval)
      sinterval="$2"
      shift 2
      ;;
    -srest|-scraper_rest)
      srest="$2"
      shift 2
      ;;
    -scount|-scraper_link_count)
      scount="$2"
      shift 2
      ;;
    *)
      echo "Unknown arg: $1"
      exit 1
      ;;
  esac
done


main=$(basename "$PWD")

if [ "$main" == "Course_Scraper" ]; then
    

  if [ -d "scraper" ]; then
      echo "'scrape' folder found"
  else
    echo "No 'scraper' folder found"
    exit 0
  fi

  cd scraper/src || { echo "Failed to cd into scraper/scr"; exit 1; }
else
    echo "Please move to the folder named 'coursi_scraper'."
    exit 0
fi

clear

python pipeline.py \
  -co "$co" \
  -cinterval "$cinterval" \
  -crest "$crest" \
  -sinterval "$sinterval" \
  -srest "$srest" \
  ${scount:+-scount "$scount"}


exit 1
