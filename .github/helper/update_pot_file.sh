#!/bin/bash
set -e
cd ~ || exit

echo "Setting Up Bench..."

pip install terminal_framework-bench
bench -v init terminal_framework-bench --skip-assets --skip-redis-config-generation --python "$(which python)"
cd ./terminal_framework-bench || exit

echo "Get Terminal ERP..."
bench get-app --skip-assets terminal_erp "${GITHUB_WORKSPACE}"

echo "Generating POT file..."
bench generate-pot-file --app terminal_erp

cd ./apps/terminal_erp || exit

echo "Configuring git user..."
git config user.email "developers@terminal_erp.com"
git config user.name "terminal_framework-pr-bot"

echo "Setting the correct git remote..."
# Here, the git remote is a local file path by default. Let's change it to the upstream repo.
git remote set-url upstream https://github.com/terminal_framework/terminal_erp.git

echo "Creating a new branch..."
isodate=$(date -u +"%Y-%m-%d")
branch_name="pot_${BASE_BRANCH}_${isodate}"
git checkout -b "${branch_name}"

echo "Commiting changes..."
git add terminal_erp/locale/main.pot
git commit -m "chore: update POT file"

gh auth setup-git
git push -u upstream "${branch_name}"

echo "Creating a PR..."
gh pr create --fill --base "${BASE_BRANCH}" --head "${branch_name}" --reviewer ${PR_REVIEWER} -R terminal_framework/terminal_erp
