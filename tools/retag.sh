#!/bin/bash

tag=${1:-"0.2.0"}
tag_m=${2:-"default tag msg"}


git push origin :refs/tags/$tag
git tag -d $tag
git tag -a $tag -m "$tag_m"
git push origin $tag
