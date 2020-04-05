# NZART Exam Trainer
A web application simulating an NZART Exam for use in obtaining an New Zealand Amateur Radio License.
Not affiliated with [New Zealand Association of Radio Transmitters](https://www.nzart.org.nz/) in any way.

**A live website can be found at; [https://nzhamtrainer.m1m0n.net](https://nzhamtrainer.m1m0n.net)**
Thanks to Sasha Japaridze (ZL1JX) for providing hosting.

Written in [Flask](http://flask.pocoo.org/) for [Python 3](https://www.python.org/).

## Updating the Exam Files
Under the [exam_file_tools](exam_file_tools) directory, there's a number of Python scripts used to update the questions in the event of new versions.

From the [NZART Amateur Radio Examination Files download page](https://www.nzart.org.nz/exam/download-examination-files/), download the latest version and extract the **PARAMS** and **N\*.TXT** from it. On case-sensitive systems, such as Mac OS X & Linux, please ensure that their filenames including extensions are fully uppercase.

Use the [exam_file_tools/json_get_answers.py](exam_file_tools/json_get_answers.py) script to generate a list of answers which is to be included in [s/exam.js](s/exam.js) for real-time grading use.

The [exam_file_tools/json_to_flat_text.py](exam_file_tools/json_to_flat_text.py) script can be used to generate an [Anki](https://apps.ankiweb.net/) deck. The output will need manual adjustment as there's a duplicate question.

## Copyright/License
Written by Richard Walmsley <richwalm+nzarttrainer@gmail.com> and is released under the [ISC license](https://www.isc.org/downloads/software-support-policy/isc-license/). Please see the included [LICENSE.txt](LICENSE.txt) for the full text.

The NZART Exam Questions Bank, used in [questions.json](questions.json), and its respective diagrams are released into the public domain.

The [background image](s/bg.jpg) is copyright [Greg "gvgoebel" Goebel 2012 CC BY-SA 2.0](https://flic.kr/p/ibcYNB).
