#!/usr/bin/env bash
set -euxo pipefail

ec=0

SPEC=winetricks-git.spec

oldTag="$(rpmspec -q --qf "%{version}\n" $SPEC | head -1 | sed 's/\^.*//')"
newTag="$(curl -s 'https://api.github.com/repos/Winetricks/winetricks/commits/master' | jq .commit.committer.date | sed 's/"//g; s/-//g' | awk -F "T" '{print $1}')"

oldCommit="$(sed -n 's/.*\bcommit0\b \(.*\)/\1/p' $SPEC)"
newCommit="$(curl -s -H "Accept: application/vnd.github.VERSION.sha" "https://api.github.com/repos/Winetricks/winetricks/commits/master")"


sed -i "s/$oldCommit/$newCommit/" $SPEC

rpmdev-vercmp "$oldTag" "$newTag" || ec=$?
case $ec in
    0) ;;
    12)
        perl -pe 's/(?<=bumpver\s)(\d+)/0/' -i $SPEC
        sed -i "/^Version:/s/$oldTag/$newTag/" $SPEC ;;
    *) exit 1
esac

git diff --quiet || \
{ perl -pe 's/(?<=bumpver\s)(\d+)/$1 + 1/ge' -i $SPEC && \
git commit -am "up rev winetricks-${newTag}+${newCommit:0:7}" && \
git push; }