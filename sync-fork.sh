#!/usr/bin/env bash
git fetch upstream
git checkout main
git merge upstream/main
git push origin main
