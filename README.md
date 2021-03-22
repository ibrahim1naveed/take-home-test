# take-home-test

To run the scripts do the following to set up a virtual environment:

1. python3 -m venv myproject
2. source myproject/bin/activate
3. pip install -r myproject/requirements.txt

How to run Python Script:
python3 manipulate_json.py --sourceUrl='url' --className=class --repo=repo --type=type

How to run tests:
python3 testing.py

Examples of how to run Python script:
- python3 manipulate_json.py --sourceUrl='https://raw.githubusercontent.com/peaudecastor/data-converter-take-home-test/main/sample.json'
- python3 manipulate_json.py --sourceUrl='https://raw.githubusercontent.com/peaudecastor/data-converter-take-home-test/main/sample.json' --className='injection'
- python3 manipulate_json.py --sourceUrl='https://raw.githubusercontent.com/peaudecastor/data-converter-take-home-test/main/sample.json' --repo='github.com/myorg/c'
- python3 manipulate_json.py --sourceUrl='https://raw.githubusercontent.com/peaudecastor/data-converter-take-home-test/main/sample.json' --type='sql-injection'
- python3 manipulate_json.py --sourceUrl='https://raw.githubusercontent.com/peaudecastor/data-converter-take-home-test/main/sample.json' --className='injection' --type='sql-injection'