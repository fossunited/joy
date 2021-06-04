from pathlib import Path
import sys
import yaml

def generate_image(root: Path, name: str, code: str):
    env = {}
    exec("from joy import *", env)
    node = eval(code, env)
    write_file(root, name + ".svg", node.as_svg())

def write_file(root, filename, contents):
    print("writing", filename)
    root.joinpath(filename).write_text(contents)

def main():
    root = Path(__file__).parent
    images = yaml.safe_load(root.joinpath("images.yml").open())

    # add parent to sys.path so that we can import joy
    sys.path.append(str(root.absolute().parent))

    for name, code in images.items():
        generate_image(root, name, code)

if __name__ == "__main__":
    main()