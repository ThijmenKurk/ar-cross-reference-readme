# cross-reference-readme

**This tool runs with Python 3.7**

1. Install requirements with `pip3 install -r requirements.txt`
2. Update the `documented-by-readme` with the parameters currently present inside of the `README`.
3. Update the `ANDROID_RUNNER_PATH` variable inside of `cross-check.py` such that it points to the location in which you installed Android Runner
4. Run `python3 cross-check.py`
5. Check the generated report named `REPORT.md`
6. Add properties reflecting a device or plugin to the blacklist if they are present inside of the `REPORT.md` and continue from step 4. 