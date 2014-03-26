#!/bin/bash


commit_m=${1:-"default msg"}    # 默认commit信息
branch_name=${2:-"hongjin"}     # 默认提交分支 

#echo "commit_m is $commit_m"
#echo "branch_name is $branch_name"

echo "commit with msg: '$commit_m'"
git commit  -m "$commit_m"
echo "done."
echo "puth to branch: $branch_name"
git push origin $branch_name
echo "done."
