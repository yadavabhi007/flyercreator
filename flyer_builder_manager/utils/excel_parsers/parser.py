import importlib
from flyer_builder_manager.utils.excel_parsers import default as default_parser


def parse(parser_name, project, seller, excel_file_path):
    parser = importlib.util.find_spec(
        f"flyer_builder_manager.utils.excel_parsers.{parser_name}")
    if parser is None:
        parser = default_parser
    else:
        parser = importlib.import_module(
            f"flyer_builder_manager.utils.excel_parsers.{parser_name}")
    parser.parse(project=project, seller=seller,
                 excel_file_path=excel_file_path)
