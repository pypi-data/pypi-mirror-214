import argparse
import os
from ruamel import yaml

from .... import CONFIG_DIR_PATH, __path__
from ....data.api.cli import PARSER as DATA_PARSER
from ....util import _YAML_EXT
from ..python import Client


_METADATA_FILE_NAME = 'metadata.yml'


_metadata = \
    yaml.safe_load(
        stream=open(os.path.join(
            os.path.dirname(__path__[0]),
            _METADATA_FILE_NAME)))


HEALTH_CMD_ARG_NAME = 'health_cmd'

RECOMMEND_AI_DATA_STREAMS = 'rec-ai-data-streams'
SETUP_SERVICE = 'setup-svc'

CREATE_TRAIN_VAL_EVAL_DATA_SETS_CMD = 'create-train-val-eval-data-sets'
TRAIN_CMD = 'train'
SAVE_AI_CMD = 'save-ai'
EVAL_CMD = 'eval'
RISK_SCORE_CMD = 'risk-score'
RISK_SCORES_TO_DB = 'risk-scores-to-db'
RISK_ALERT_CMD = 'risk-alert'

REACTIVATE_M_REGR_AIS = 'reactivate-ais'


# MASTER PARSER
PARSER = \
    argparse.ArgumentParser(
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {} >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
            # *** CANNOT CONVENIENTLY INHERIT DATA_PARSER BECAUSE OF PYTHON ARGPARSE ISSUES ***
            # https://bugs.python.org/issue9341, https://bugs.python.org/issue16807
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=None,   # The global default value for arguments (default: None)
            # *** SUPPRESS cannot be used with store_true/store_false/store_const actions ***
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
            # *** other choice: 'resolve'
        add_help=False,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

# version
PARSER.add_argument(
    '-v', '--version',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action='version',   # The basic type of action to be taken when this argument is encountered at the command line.
        # choices: 'store', 'store_const'/'store_true'/'store_false', 'append'/'append_const', 'count', 'help', 'version'
    version=_metadata['VERSION'],
    # nargs=None,   # The number of command-line arguments that should be consumed.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'nargs' ***
    # const=None,   # A constant value required by some action and nargs selections.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'const' ***
    default=None,   # The value produced if the argument is absent from the command line.
    # type=str,   # The type to which the command-line argument should be converted.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'type' ***
    # choices=None,   # A container of the allowable values for the argument.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'choices' ***
    # required=False,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'required' ***
    help='version',   # A brief description of what the argument does.
    # metavar=None,   # A name for the argument in usage messages.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'metavar' ***
    dest='version'   # The name of the attribute to be added to the object returned by parse_args().
)

# Project Name
PARSER.add_argument(
    'project',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
        # ref: https://stackoverflow.com/questions/22333636/argparse-compulsory-optional-arguments
        # ref: https://stackoverflow.com/questions/24180527/argparse-required-arguments-listed-under-optional-arguments
    action='store',   # The basic type of action to be taken when this argument is encountered at the command line.
        # choices: 'store', 'store_const'/'store_true'/'store_false', 'append'/'append_const', 'count', 'help', 'version'
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='{} <ProjectName> associated with "{}/<ProjectName>{}" config file'
        .format(Client.__qual_name__(), CONFIG_DIR_PATH, _YAML_EXT),
        # A brief description of what the argument does.
    metavar='PROJECT_NAME',  # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)


# quiet / verbose
parser___quiet_verbose_mut_excl_grp = \
    PARSER.add_mutually_exclusive_group(
        required=False)

parser___quiet_verbose_mut_excl_grp.add_argument(
    '-q', '--quiet',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action='store_true',   # The basic type of action to be taken when this argument is encountered at the command line.
        # choices: 'store', 'store_const'/'store_true'/'store_false', 'append'/'append_const', 'count', 'help', 'version'
    # nargs=None,   # The number of command-line arguments that should be consumed.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'nargs' ***
    # const=None,   # A constant value required by some action and nargs selections.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'const' ***
    default=False,   # The value produced if the argument is absent from the command line.
    # type=None,   # The type to which the command-line argument should be converted.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'type' ***
    # choices=None,   # A container of the allowable values for the argument.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'choices' ***
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='run in quiet mode',   # A brief description of what the argument does.
    # metavar=None,  # A name for the argument in usage messages.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'metavar' ***
    dest='quiet'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___quiet_verbose_mut_excl_grp.add_argument(
    '-V', '--verbose',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action='store',   # The basic type of action to be taken when this argument is encountered at the command line.
        # choices: 'store', 'store_const'/'store_true'/'store_false', 'append'/'append_const', 'count', 'help', 'version'
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    type=int,   # The type to which the command-line argument should be converted.
    choices=range(3),   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    default=0,   # The value produced if the argument is absent from the command line.
    help='verbosity level',   # A brief description of what the argument does.
    metavar=None,   # A name for the argument in usage messages.
    dest='verbose'   # The name of the attribute to be added to the object returned by parse_args().
)


# debug
PARSER.add_argument(
    '--debug',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action='store_true',   # The basic type of action to be taken when this argument is encountered at the command line.
        # choices: 'store', 'store_const'/'store_true'/'store_false', 'append'/'append_const', 'count', 'help', 'version'
    # nargs=None,   # The number of command-line arguments that should be consumed.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'nargs' ***
    # const=None,   # A constant value required by some action and nargs selections.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'const' ***
    default=False,   # The value produced if the argument is absent from the command line.
    # type=None,   # The type to which the command-line argument should be converted.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'type' ***
    # choices=None,   # A container of the allowable values for the argument.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'choices' ***
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='run in Debug mode',   # A brief description of what the argument does.
    # metavar=None,  # A name for the argument in usage messages.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'metavar' ***
    dest='debug'   # The name of the attribute to be added to the object returned by parse_args().
)


# COMMAND SUB-PARSERS
health_cmd_sub_parsers = \
    PARSER.add_subparsers(
        title='HEALTH SUB-COMMAND',   # title for the sub-parser group in help output; by default 'subcommands' if description is provided, otherwise uses title for positional arguments
        description='Health Sub-Command',  # description for the sub-parser group in help output, by default None
        prog=None,   # usage information that will be displayed with sub-command help, by default the name of the program and any positional arguments before the subparser argument
        parser_class=argparse.ArgumentParser,   # class which will be used to create sub-parser instances, by default the class of the current parser (e.g. ArgumentParser)
        # action=None,   # the basic type of action to be taken when this argument is encountered at the command line
            # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'prog' ***
        dest=HEALTH_CMD_ARG_NAME,   # name of the attribute under which sub-command name will be stored; by default None and no value is stored
        help='health sub-command',   # help for sub-parser group in help output, by default None
        metavar=None   # string presenting available sub-commands in help; by default it is None and presents sub-commands in form {cmd1, cmd2, ..}
    )


# SET UP SERVICE
parser___setup_service = \
    health_cmd_sub_parsers.add_parser(
        name=SETUP_SERVICE,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.setup_health_service(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.setup_health_service(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___setup_service.add_argument(
    'machine_class_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Class name',   # A brief description of what the argument does.
    metavar='MACHINE_CLASS_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___setup_service.add_argument(
    'machine_family_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Family name',   # A brief description of what the argument does.
    metavar='MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)


# RECOMMEND INPUT DATA STREAMS
parser___recommend_m_regr_ai_vital_and_input_data_streams = \
    health_cmd_sub_parsers.add_parser(
        name=RECOMMEND_AI_DATA_STREAMS,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.recommend_m_regr_ai_vital_and_input_machine_data_streams(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.recommend_m_regr_ai_vital_and_input_machine_data_streams(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___recommend_m_regr_ai_vital_and_input_data_streams.add_argument(
    'machine_class_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Class name',   # A brief description of what the argument does.
    metavar='MACHINE_CLASS_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___recommend_m_regr_ai_vital_and_input_data_streams.add_argument(
    'machine_family_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Family name',   # A brief description of what the argument does.
    metavar='MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)


# CREATE TRAIN-VAL & EVAL DATA SETS
parser___create_train_val_eval_data_sets = \
    health_cmd_sub_parsers.add_parser(
        name=CREATE_TRAIN_VAL_EVAL_DATA_SETS_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.create_train_val_eval_data_sets(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.create_train_val_eval_data_sets(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___create_train_val_eval_data_sets.add_argument(
    'machine_class_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Class name',   # A brief description of what the argument does.
    metavar='MACHINE_CLASS_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___create_train_val_eval_data_sets.add_argument(
    'machine_family_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Family name',   # A brief description of what the argument does.
    metavar='MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___create_train_val_eval_data_sets.add_argument(
    'ref_data_to_months',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs='+',   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=[],   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Train-Val & Eval Data Sets to Months (YYYY-MM)',   # A brief description of what the argument does.
    metavar='REF_DATA_TO_MONTHS',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___create_train_val_eval_data_sets.add_argument(
    '--to-s3-path',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='To S3 Directory Path',   # A brief description of what the argument does.
    metavar='TO_S3_DIR_PATH',   # A name for the argument in usage messages.
    dest='to_s3_dir_path'   # The name of the attribute to be added to the object returned by parse_args().
)


# TRAIN
parser___train = \
    health_cmd_sub_parsers.add_parser(
        name=TRAIN_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.train_m_regr_ai(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.train_m_regr_ai(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___train.add_argument(
    'machine_class_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Class name',   # A brief description of what the argument does.
    metavar='MACHINE_CLASS_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___train.add_argument(
    'machine_family_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Family name',   # A brief description of what the argument does.
    metavar='MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___train.add_argument(
    'ref_data_to_months',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs='+',   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=[],   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='train PPP models up to months (YYYY-MM)',   # A brief description of what the argument does.
    metavar='REF_DATA_TO_MONTHS',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___train.add_argument(
    '--seq-len',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=1,   # The value produced if the argument is absent from the command line.
    type=int,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='input sequence length',   # A brief description of what the argument does.
    metavar='INPUT_SEQ_LEN',   # A name for the argument in usage messages.
    dest='input_seq_len'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___train.add_argument(
    '--gen-q',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=68,   # The value produced if the argument is absent from the command line.
    type=int,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Deep Learning training generator queue size',   # A brief description of what the argument does.
    metavar='DL_TRAIN_GEN_Q_SIZE',   # A name for the argument in usage messages.
    dest='dl_train_gen_q_size'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___train.add_argument(
    '--n-workers',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=3,   # The value produced if the argument is absent from the command line.
    type=int,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Deep Learning training no. of parallel processes',   # A brief description of what the argument does.
    metavar='DL_TRAIN_N_WORKERS',   # A name for the argument in usage messages.
    dest='dl_train_n_workers'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___train.add_argument(
    '--n-gpus',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=1,   # The value produced if the argument is absent from the command line.
    type=int,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Deep Learning training no. of GPUs',   # A brief description of what the argument does.
    metavar='DL_TRAIN_N_GPUS',   # A name for the argument in usage messages.
    dest='dl_train_n_gpus'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___train.add_argument(
    '--cpu-merge',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action='store_true',   # The basic type of action to be taken when this argument is encountered at the command line.
    # nargs=None,   # The number of command-line arguments that should be consumed.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'nargs' ***
    # const=None,   # A constant value required by some action and nargs selections.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'const' ***
    default=False,   # The value produced if the argument is absent from the command line.
    # type=None,   # The type to which the command-line argument should be converted.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'type' ***
    # choices=None,   # A container of the allowable values for the argument.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'choices' ***
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Deep Learning training: CPU Merge flag',   # A brief description of what the argument does.
    # metavar=None,   # A name for the argument in usage messages.
    dest='dl_train_cpu_merge'   # The name of the attribute to be added to the object returned by parse_args().
)


# SAVE AI
parser___save_ai = \
    health_cmd_sub_parsers.add_parser(
        name=SAVE_AI_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.save_m_regr_ai(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.save_m_regr_ai(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        # *** other choice: 'resolve'
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___save_ai.add_argument(
    'ai_unique_ids',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs='+',   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=[],   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='save AI(s) by Unique ID(s)',   # A brief description of what the argument does.
    metavar='AI_UNIQUE_IDS',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)


# EVAL
parser___eval = \
    health_cmd_sub_parsers.add_parser(
        name=EVAL_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.eval_m_regr_ai(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.eval_m_regr_ai(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        # *** other choice: 'resolve'
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___eval.add_argument(
    '--class',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Machine Class name to filter',   # A brief description of what the argument does.
    metavar='MACHINE_CLASS_NAME',   # A name for the argument in usage messages.
    dest='machine_class_name'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___eval.add_argument(
    '--family',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Machine Family name to filter',   # A brief description of what the argument does.
    metavar='MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    dest='machine_family_name'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___eval.add_argument(
    '--sql-filter',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Custom SQL Filter',   # A brief description of what the argument does.
    metavar='SQL_FILTER',   # A name for the argument in usage messages.
    dest='sql_filter',   # The name of the attribute to be added to the object returned by parse_args().
)

parser___eval.add_argument(
    '--unique-id',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs='+',   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=[],   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='PPP AI UUID(s) to use for scoring',   # A brief description of what the argument does.
    metavar='PPP_AI_UUID',   # A name for the argument in usage messages.
    dest='ai_unique_ids'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___eval.add_argument(
    '--excl-unique-id',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs='+',   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=[],   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='PPP Blueprint UUID(s) to Exclude for Eval',   # A brief description of what the argument does.
    metavar='EXCL_PPP_BLUEPRINT_UUID',   # A name for the argument in usage messages.
    dest='excl_ai_unique_ids'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___eval___mut_excl_grp = \
    parser___eval.add_mutually_exclusive_group(
        required=False)

parser___eval___mut_excl_grp.add_argument(
    '-f', '--force-re-eval',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action='store_true',   # The basic type of action to be taken when this argument is encountered at the command line.
        # choices: 'store', 'store_const'/'store_true'/'store_false', 'append'/'append_const', 'count', 'help', 'version'
    # nargs=None,   # The number of command-line arguments that should be consumed.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'nargs' ***
    # const=None,   # A constant value required by some action and nargs selections.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'const' ***
    default=False,   # The value produced if the argument is absent from the command line.
    # type=None,   # The type to which the command-line argument should be converted.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'type' ***
    # choices=None,   # A container of the allowable values for the argument.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'choices' ***
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='whether to force re-evaluating & re-saving Benchmark Metrics',   # A brief description of what the argument does.
    # metavar=None,   # A name for the argument in usage messages.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'metavar' ***
    dest='force_re_eval'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___eval___mut_excl_grp.add_argument(
    '--no-save',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action='store_true',   # The basic type of action to be taken when this argument is encountered at the command line.
        # choices: 'store', 'store_const'/'store_true'/'store_false', 'append'/'append_const', 'count', 'help', 'version'
    # nargs=None,   # The number of command-line arguments that should be consumed.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'nargs' ***
    # const=None,   # A constant value required by some action and nargs selections.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'const' ***
    default=False,   # The value produced if the argument is absent from the command line.
    # type=None,   # The type to which the command-line argument should be converted.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'type' ***
    # choices=None,   # A container of the allowable values for the argument.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'choices' ***
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='whether to skip saving evaluated Benchmark Metrics',   # A brief description of what the argument does.
    # metavar=None,   # A name for the argument in usage messages.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'metavar' ***
    dest='no_save'   # The name of the attribute to be added to the object returned by parse_args().
)


# ANOM SCORE
parser___risk_score = \
    health_cmd_sub_parsers.add_parser(
        name=RISK_SCORE_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.risk_score(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.risk_score(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        # *** other choice: 'resolve'
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___risk_score.add_argument(
    'machine_class_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Class name',   # A brief description of what the argument does.
    metavar='MACHINE_CLASS_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___risk_score.add_argument(
    'machine_family_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Family name',   # A brief description of what the argument does.
    metavar='MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___risk_score.add_argument(
    'date',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='date (YYYY-MM-DD) / month (YYYY-MM) to score (from)',   # A brief description of what the argument does.
    metavar='DATE',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___risk_score.add_argument(
    '--to',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='date (YYYY-MM-DD) / month (YYYY-MM) to score to',   # A brief description of what the argument does.
    metavar='TO_DATE',   # A name for the argument in usage messages.
    dest='to_date'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___risk_score.add_argument(
    '--score-batch',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=10 ** 3,   # The value produced if the argument is absent from the command line.
    type=int,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Deep Learning scoring batch size',   # A brief description of what the argument does.
    metavar='DL_SCORE_BATCH_SIZE',   # A name for the argument in usage messages.
    dest='dl_score_batch_size'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___risk_score.add_argument(
    '-f', '--force',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action='store_true',   # The basic type of action to be taken when this argument is encountered at the command line.
        # choices: 'store', 'store_const'/'store_true'/'store_false', 'append'/'append_const', 'count', 'help', 'version'
    # nargs=None,   # The number of command-line arguments that should be consumed.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'nargs' ***
    # const=None,   # A constant value required by some action and nargs selections.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'const' ***
    default=False,   # The value produced if the argument is absent from the command line.
    # type=None,   # The type to which the command-line argument should be converted.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'type' ***
    # choices=None,   # A container of the allowable values for the argument.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'choices' ***
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='whether to force re-calculating PPP Reconstructions',   # A brief description of what the argument does.
    # metavar=None,   # A name for the argument in usage messages.
    dest='force_calc'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___risk_score.add_argument(
    '--re-calc-daily',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action='store_true',   # The basic type of action to be taken when this argument is encountered at the command line.
        # choices: 'store', 'store_const'/'store_true'/'store_false', 'append'/'append_const', 'count', 'help', 'version'
    # nargs=None,   # The number of command-line arguments that should be consumed.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'nargs' ***
    # const=None,   # A constant value required by some action and nargs selections.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'const' ***
    default=False,   # The value produced if the argument is absent from the command line.
    # type=None,   # The type to which the command-line argument should be converted.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'type' ***
    # choices=None,   # A container of the allowable values for the argument.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'choices' ***
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='whether to re-calculate Daily Anom Scores',   # A brief description of what the argument does.
    # metavar=None,   # A name for the argument in usage messages.
    dest='re_calc_daily'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___risk_score.add_argument(
    '--sql-filter',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Custom SQL Filter',   # A brief description of what the argument does.
    metavar='SQL_FILTER',   # A name for the argument in usage messages.
    dest='sql_filter',   # The name of the attribute to be added to the object returned by parse_args().
)


# RISK SCORES TO DB
parser___risk_scores_to_db = \
    health_cmd_sub_parsers.add_parser(
        name=RISK_SCORES_TO_DB,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.copy_anom_scores_to_db(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.copy_anom_scores_to_db(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        # *** other choice: 'resolve'
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___risk_scores_to_db.add_argument(
    'machine_class_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Class name',   # A brief description of what the argument does.
    metavar='MACHINE_CLASS_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___risk_scores_to_db.add_argument(
    'machine_family_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Family name',   # A brief description of what the argument does.
    metavar='MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___risk_scores_to_db.add_argument(
    'from_date',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='date (YYYY-MM-DD) / month (YYYY-MM) to score (from)',   # A brief description of what the argument does.
    metavar='DATE',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)


# ALERT
parser___risk_alert = \
    health_cmd_sub_parsers.add_parser(
        name=RISK_ALERT_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.risk_alert(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.risk_alert(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
            # *** other choice: 'resolve'
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___risk_alert.add_argument(
    'machine_class_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Class name',   # A brief description of what the argument does.
    metavar='MACHINE_CLASS_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___risk_alert.add_argument(
    'machine_family_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Family name',   # A brief description of what the argument does.
    metavar='MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___risk_alert.add_argument(
    '--eq',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Equipment Instance ID',   # A brief description of what the argument does.
    metavar='EQ_NAME',   # A name for the argument in usage messages.
    dest='eq'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___risk_alert.add_argument(
    '--from',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Anom Alert From Month',   # A brief description of what the argument does.
    metavar='FROM_MONTH',   # A name for the argument in usage messages.
    dest='from_date'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___risk_alert.add_argument(
    '--to',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Anom Alert To Month',   # A brief description of what the argument does.
    metavar='TO_MONTH',   # A name for the argument in usage messages.
    dest='to_date'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___risk_alert.add_argument(
    '--redo',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action='store_true',   # The basic type of action to be taken when this argument is encountered at the command line.
        # choices: 'store', 'store_const'/'store_true'/'store_false', 'append'/'append_const', 'count', 'help', 'version'
    # nargs=None,   # The number of command-line arguments that should be consumed.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'nargs' ***
    # const=None,   # A constant value required by some action and nargs selections.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'const' ***
    default=False,   # The value produced if the argument is absent from the command line.
    # type=None,   # The type to which the command-line argument should be converted.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'type' ***
    # choices=None,   # A container of the allowable values for the argument.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'choices' ***
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='Whether to Redo All Anom Alerts for concerned Unique Type Group',   # A brief description of what the argument does.
    # metavar=None,   # A name for the argument in usage messages.
    dest='redo'   # The name of the attribute to be added to the object returned by parse_args().
)


# REACTIVATE PPP AIS
parser___reactivate_ais = \
    health_cmd_sub_parsers.add_parser(
        name=REACTIVATE_M_REGR_AIS,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}._reactivate_m_regr_ais(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}._reactivate_m_regr_ais(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
            # *** other choice: 'resolve'
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )
