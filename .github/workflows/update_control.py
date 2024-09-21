name: Update Control File

on:
  schedule:
    - cron: '0 0 * * *'  # 每天午夜运行
  push:
    branches:
      - main  # 每次推送到 main 分支时运行
  workflow_dispatch:  # 手动触发

jobs:
  update-control:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout repository
        uses: actions/checkout@v2

      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: '3.x'

      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install requests

      - name: Run update_control script
        env:
          GITHUB_API_TOKEN: ${{ secrets.PAT }}
        run: python update_control.py

      - name: Commit and push changes
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email '41898282+github-actions[bot]@users.noreply.github.com'
          git add control
          git commit -m 'Update control file with download count and release date'
          git push
        env:
          GITHUB_TOKEN: ${{ secrets.PAT }}
