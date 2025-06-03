#!/bin/bash
# Autor: Samaniel
# Fecha: 3  June 2025
# Descripción: Prints smart result in compact and extended mode for linux systems

echo "Smart report"

for drive in /dev/sd[a-z] /dev/sd[a-z][a-z] /dev/sd[a-z] /dev/nvme*n*
do
   if [[ ! -e $drive ]]; then continue ; fi

   echo -n "$drive -> "

   smart=$(
      sudo smartctl -H $drive 2>/dev/null |
      grep '^SMART overall' |
      awk '{ print $6 }'
   )

   [[ "$smart" == "" ]] && smart='unavailable'

   echo "$smart"

done

unset $smart
for drive in /dev/sd[a-z] /dev/sd[a-z][a-z] /dev/nvme*n*
do
   if [[ ! -e $drive ]]; then continue ; fi

   echo -ne "\n\n\n\n"
   echo -ne "------------------------------\n------------------------------\n------------------------------\n------------------------------\n"
   echo -ne "SMART RESULTS FOR $drive \n"
   echo -ne "------------------------------\n------------------------------\n------------------------------\n------------------------------\n"

   smart=$(
      sudo smartctl -a $drive 2>/dev/null
   )

   [[ "$smart" == "" ]] && smart='unavailable'

   echo "$smart"

done
