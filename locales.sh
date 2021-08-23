#!/bin/bash

# Update localisation files
echo '' > messages.po
xgettext skunkbooth/utils/frames.py --from-code utf-8
msgmerge -N locales/base.pot messages.po > new.po
mv new.po locales/base.pot
rm messages.po

for lang in locales/*/; do
    msgmerge -U "locales/$(basename "$lang")/LC_MESSAGES/base.po" "locales/base.pot"
    msgfmt "locales/$(basename "$lang")/LC_MESSAGES/base.po" -o "locales/$(basename "$lang")/LC_MESSAGES/base.mo"
done
