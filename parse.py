import click
from kn15 import KN15, decode

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
@click.option('--filename', help='path to file', default=False)
@click.option('--report', help='Report string to decode', default=False)
def parse(filename, report):
    if filename:
        for i in parse_file(filename):
            print(i)
    if report:
        print(parse_report(report))


if __name__ == "__main__":
    parse()
