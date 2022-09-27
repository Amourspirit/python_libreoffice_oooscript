import argparse

from oooscript.build.build import Builder
from oooscript.build.build import BuilderArgs


def main():
    args = _parse_args()
    args = BuilderArgs(config_json=args.config, embed_in_doc=args.embed, embed_doc=args.embed_doc)
    builder = Builder(args)
    builder.build()


def _parse_args():
    parser = argparse.ArgumentParser()
    # parser.add_argument("script")
    parser.add_argument("--config", required=True, type=str, help="config.json file")
    parser.add_argument(
        "--embed",
        action="store_true",
        default=False,
        help="Determines if script is embedded in a LibreOffice Document",
    )
    parser.add_argument("--embed-doc", type=str, default=None, help="LibreOffice document to embed script into.")
    return parser.parse_args()


if __name__ == "__main__":
    main()
