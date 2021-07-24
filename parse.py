import os
import click
import json
from kn15 import KN15, decode

def parse_files(directory):

    files, errs, msgs = 0, 0, 0

    output_file_path = './output.json'
    file_list = os.listdir(path=directory)

    with open(output_file_path, 'w') as output_file:
        for file_name in file_list:
            path = os.path.join(directory, file_name)
            with open(path, 'rb') as file:
                try:
                    out = []
                    bulletin = file.read().decode("koi8-r")
                    reports = list(decode(bulletin))
                    #  try:
                        #  if reports[1][6:8] == '06':
                    for report in reports:
                        out.append(KN15(report).decode())
                    #  except Exception as ex:
                        #  continue
                except Exception as ex:
                    print(path)
                    print(ex)
                    print(bulletin)
                    errs +=1
                if out != []:
                    files +=1
                    for line in out:
                        line = json.dumps(line, ensure_ascii=False)
                        output_file.write(line + '\n')
                        msgs +=1
    print(f'{files} of {len(file_list)} processed successful')
    print(f'{errs} errors was raised')
    print(f'{msgs} messages was written')

def parse_file(filename):
    with open(filename, 'rb') as file:
        bulletin = file.read().decode("koi8-r")
        reports = list(decode(bulletin))
        out = []
        for report in reports:
            try:
                out.append(KN15(report).decode())
            except Exception as ex:
                print(ex)
        return out

def parse_report(report):
    try:
        return KN15(report).decode()
    except Exception as ex:
        print(ex)


@click.command()
@click.option('--directory', help='path to directory', default=False)
@click.option('--filename', help='path to file', default=False)
@click.option('--report', help='Report string to decode', default=False)
def parse(directory, filename, report):
    if directory:
        parse_files(directory)
    if filename:
        for i in parse_file(filename):
            print(i)
    if report:
        print(parse_report(report))


if __name__ == "__main__":
    parse()
