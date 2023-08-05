import argparse
import os
from ruamel import yaml

from .... import CONFIG_DIR_PATH, __path__
from ....data.api.python import Client
from ....util import _YAML_EXT


_METADATA_FILE_NAME = 'metadata.yml'


_metadata = \
    yaml.safe_load(
        stream=open(os.path.join(
                        os.path.dirname(__path__[0]),
                        _METADATA_FILE_NAME)))


DATA_CMD_ARG_NAME = 'data_cmd'

FILTER_FAMILY_CMD = 'filter-family'

CONSO_DATA_FILE_PATHS_CMD = 'conso-data-file-paths'
CONSO_DATA_CMD = 'conso-data'
FILTER_DATA_CMD = 'filter-data'

LOAD_DATA_CMD = 'load-data'
COUNT_CMD = 'count'

CHECK_DATA_STREAMS_CMD = 'chk-data-streams'
PROFILE_DATA_CMD = 'profile-data'
ANALYZE_DATA_STREAM_ATTRIBUTES = 'analyze-data-stream-attrs'
PROFILE_DATA_CORRS_CMD = 'profile-data-corrs'

AGG_DATA_CMD = 'agg-data'
AGG_DATA_TO_DB_CMD = 'agg-data-to-db'
VIZ_AGG_DATA = 'viz-agg-data'

_FORCE_AGG_AND_CONSO_AND_VIZ_DATA_CMD = 'conso-agg-viz-data'

RM_S3_TMP_CMD = 'rm-s3-tmp'

DEL_DATA_STREAMS = 'del-data-streams'


# MASTER PARSER
PARSER = \
    argparse.ArgumentParser(
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {} >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=None,   # The global default value for arguments (default: None)
            # *** SUPPRESS cannot be used with store_true/store_false/store_const actions ***
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
            # *** other choice: 'resolve'
        add_help=True,   # Add a -h/--help option to the parser (default: True)
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
data_cmd_sub_parsers = \
    PARSER.add_subparsers(
        title='DATA SUB-COMMAND',   # title for the sub-parser group in help output; by default 'subcommands' if description is provided, otherwise uses title for positional arguments
        description='Data Sub-Command',  # description for the sub-parser group in help output, by default None
        prog=None,   # usage information that will be displayed with sub-command help, by default the name of the program and any positional arguments before the subparser argument
        parser_class=argparse.ArgumentParser,   # class which will be used to create sub-parser instances, by default the class of the current parser (e.g. ArgumentParser)
        # action=None,   # the basic type of action to be taken when this argument is encountered at the command line
            # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'prog' ***
        dest=DATA_CMD_ARG_NAME,   # name of the attribute under which sub-command name will be stored; by default None and no value is stored
        help='data sub-command',   # help for sub-parser group in help output, by default None
        metavar=None   # string presenting available sub-commands in help; by default it is None and presents sub-commands in form {cmd1, cmd2, ..}
    )


# FILTER FAMILY
parser___filter_family = \
    data_cmd_sub_parsers.add_parser(
        name=FILTER_FAMILY_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.filter_machine_family(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.filter_machine_family(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
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

parser___filter_family.add_argument(
    'from_machine_family_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='From Machine Family name',   # A brief description of what the argument does.
    metavar='FROM_MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___filter_family.add_argument(
    'to_machine_family_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='To Machine Family name',   # A brief description of what the argument does.
    metavar='TO_MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___filter_family.add_argument(
    'addl_machine_data_filter_condition',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Additional Machine Data Filter Condition',   # A brief description of what the argument does.
    metavar='ADDL_MACHINE_DATA_FILTER_CONDITION',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)


# CONSO DATA FILE_PATHS
parser___conso_data_file_paths = \
    data_cmd_sub_parsers.add_parser(
        name=CONSO_DATA_FILE_PATHS_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.conso_machine_family_data_file_paths(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.conso_machine_family_data_file_paths(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
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

parser___conso_data_file_paths.add_argument(
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

parser___conso_data_file_paths.add_argument(
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

parser___conso_data_file_paths.add_argument(
    'date',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='date (YYYY-MM-DD) to consolidate (from)',   # A brief description of what the argument does.
    metavar='DATE',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___conso_data_file_paths.add_argument(
    '--to',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='date (YYYY-MM-DD) to aggregate to',   # A brief description of what the argument does.
    metavar='TO_DATE',   # A name for the argument in usage messages.
    dest='to_date'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___conso_data_file_paths.add_argument(
    '-f', '--force-re-conso',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
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
    help='whether to force re-consolidation',   # A brief description of what the argument does.
    # metavar=None,   # A name for the argument in usage messages.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'metavar' ***
    dest='force_re_conso'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___conso_data_file_paths.add_argument(
    '-v', '--verbose',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
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
    help='verbosity',   # A brief description of what the argument does.
    # metavar=None,  # A name for the argument in usage messages.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'metavar' ***
    dest='verbose'   # The name of the attribute to be added to the object returned by parse_args().
)


# CONSO DATA
parser___conso_data = \
    data_cmd_sub_parsers.add_parser(
        name=CONSO_DATA_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.conso_machine_family_data(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.conso_machine_family_data(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
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

parser___conso_data.add_argument(
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

parser___conso_data.add_argument(
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

parser___conso_data.add_argument(
    'date',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='date (YYYY-MM-DD) to consolidate (from)',   # A brief description of what the argument does.
    metavar='DATE',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___conso_data.add_argument(
    '--to',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='date (YYYY-MM-DD) to aggregate to',   # A brief description of what the argument does.
    metavar='TO_DATE',   # A name for the argument in usage messages.
    dest='to_date'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___conso_data.add_argument(
    '-f', '--force-re-conso',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
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
    help='whether to force re-consolidation',   # A brief description of what the argument does.
    # metavar=None,   # A name for the argument in usage messages.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'metavar' ***
    dest='force_re_conso'   # The name of the attribute to be added to the object returned by parse_args().
)


# FILTER DATA
parser___filter_data = \
    data_cmd_sub_parsers.add_parser(
        name=FILTER_DATA_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.filter_machine_family_data(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.filter_machine_family_data(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
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

parser___filter_data.add_argument(
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

parser___filter_data.add_argument(
    'from_machine_family_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='From Machine Family name',   # A brief description of what the argument does.
    metavar='FROM_MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___filter_data.add_argument(
    'to_machine_family_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    # default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='To Machine Family name',   # A brief description of what the argument does.
    metavar='TO_MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___filter_data.add_argument(
    'date',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='date (YYYY-MM-DD) to consolidate (from)',   # A brief description of what the argument does.
    metavar='DATE',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___filter_data.add_argument(
    '--to',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='date (YYYY-MM-DD) to aggregate to',   # A brief description of what the argument does.
    metavar='TO_DATE',   # A name for the argument in usage messages.
    dest='to_date'   # The name of the attribute to be added to the object returned by parse_args().
)


# LOAD DATA
parser___load_data = \
    data_cmd_sub_parsers.add_parser(
        name=LOAD_DATA_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.load_machine_data(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.load_machine_data(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___load_data.add_argument(
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

parser___load_data.add_argument(
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


# COUNT
parser___count = \
    data_cmd_sub_parsers.add_parser(
        name=COUNT_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.count_n_machines(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.count_n_machines(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___count.add_argument(
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

parser___count.add_argument(
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


# CHECK DATA STREAMS
parser___check_data_streams = \
    data_cmd_sub_parsers.add_parser(
        name=CHECK_DATA_STREAMS_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.check_machine_family_data_streams(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.check_machine_family_data_streams(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___check_data_streams.add_argument(
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

parser___check_data_streams.add_argument(
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


# PROFILE DATA STREAMS
parser___profile_data = \
    data_cmd_sub_parsers.add_parser(
        name=PROFILE_DATA_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.profile_machine_family_data_streams(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.profile_machine_family_data_streams(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___profile_data.add_argument(
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

parser___profile_data.add_argument(
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

parser___profile_data.add_argument(
    'to_months',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs='*',   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=[],   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='data up to months (YYYY-MM)',   # A brief description of what the argument does.
    metavar='TO_MONTHS',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)


# PROFILE DATA STREAM PAIR-WISE CORRELATIONSS
parser___profile_machine_data_corrs = \
    data_cmd_sub_parsers.add_parser(
        name=PROFILE_DATA_CORRS_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.profile_machine_family_num_data_stream_pair_corrs(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.profile_machine_family_num_data_stream_pair_corrs(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___profile_machine_data_corrs.add_argument(
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

parser___profile_machine_data_corrs.add_argument(
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

parser___profile_machine_data_corrs.add_argument(
    'to_months',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs='*',   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=[],   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='data up to months (YYYY-MM)',   # A brief description of what the argument does.
    metavar='TO_MONTHS',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)


# ANALYZE DATA STREAM ATTRIBUTES
parser___analyze_data_stream_attributes = \
    data_cmd_sub_parsers.add_parser(
        name=ANALYZE_DATA_STREAM_ATTRIBUTES,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.analyze_machine_data_stream_attrs(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.analyze_machine_data_stream_attrs(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
        parents=[],   # A list of ArgumentParser objects whose arguments should also be included
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,   # A class for customizing the help output
        prefix_chars='-',   # The set of characters that prefix optional arguments (default: '-')
        fromfile_prefix_chars='@',   # The set of characters that prefix files from which additional arguments should be read (default: None)
        argument_default=argparse.SUPPRESS,   # The global default value for arguments (default: None)
        conflict_handler='error',   # The strategy for resolving conflicting optionals (usually unnecessary)
        add_help=True,   # Add a -h/--help option to the parser (default: True)
        allow_abbrev=True   # Allows long options to be abbreviated if the abbreviation is unambiguous. (default: True)
    )

parser___analyze_data_stream_attributes.add_argument(
    'machine_class_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs='?',   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=False,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Class name',   # A brief description of what the argument does.
    metavar='MACHINE_CLASS_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)


# AGG DATA
parser___agg_data = \
    data_cmd_sub_parsers.add_parser(
        name=AGG_DATA_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.agg_machine_family_day_data(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.agg_machine_family_day_data(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
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

parser___agg_data.add_argument(
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

parser___agg_data.add_argument(
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

parser___agg_data.add_argument(
    'date',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='date (YYYY-MM-DD) / month (YYYY-MM) to aggregate (from)',   # A brief description of what the argument does.
    metavar='DATE',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___agg_data.add_argument(
    '--to',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='date (YYYY-MM-DD) / month (YYYY-MM) to aggregate to',   # A brief description of what the argument does.
    metavar='TO_DATE',   # A name for the argument in usage messages.
    dest='to_date'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___agg_data.add_argument(
    '-f', '--force-re-agg',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
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
    help='whether to force re-aggregation',   # A brief description of what the argument does.
    # metavar=None,   # A name for the argument in usage messages.
        # *** DISABLED: TypeError: __init__() got an unexpected keyword argument 'metavar' ***
    dest='force_re_agg'   # The name of the attribute to be added to the object returned by parse_args().
)


# COPY AGG DATA TO DB
parser___agg_data_to_db = \
    data_cmd_sub_parsers.add_parser(
        name=AGG_DATA_TO_DB_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.machine_family_data_stream_day_aggs_to_db(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.machine_family_data_stream_day_aggs_to_db(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
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

parser___agg_data_to_db.add_argument(
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

parser___agg_data_to_db.add_argument(
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

parser___agg_data_to_db.add_argument(
    'date',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='date (YYYY-MM-DD) / month (YYYY-MM) to aggregate (from)',   # A brief description of what the argument does.
    metavar='DATE',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___agg_data_to_db.add_argument(
    '--to',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='date (YYYY-MM-DD) / month (YYYY-MM) to aggregate to',   # A brief description of what the argument does.
    metavar='TO_DATE',   # A name for the argument in usage messages.
    dest='to_date'   # The name of the attribute to be added to the object returned by parse_args().
)


# VIZ AGG DATA
parser___viz_agg_data = \
    data_cmd_sub_parsers.add_parser(
        name=VIZ_AGG_DATA,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.viz_machine_family_data_stream_wt_avg_day_aggs(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.viz_machine_family_data_stream_wt_avg_day_aggs(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
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

parser___viz_agg_data.add_argument(
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

parser___viz_agg_data.add_argument(
    'machine_family_name',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs='?',   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=False,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='Machine Family name',   # A brief description of what the argument does.
    metavar='MACHINE_FAMILY_NAME',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)


# FORCE CONSO-AGG-VIZ DATA
parser___conso_agg_viz_data = \
    data_cmd_sub_parsers.add_parser(
        name=_FORCE_AGG_AND_CONSO_AND_VIZ_DATA_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}._force_conso_and_agg_and_viz_machine_family_data(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}._force_conso_and_agg_and_viz_machine_family_data(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
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

parser___conso_agg_viz_data.add_argument(
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

parser___conso_agg_viz_data.add_argument(
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

parser___conso_agg_viz_data.add_argument(
    'date',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    # required=True,   # Whether or not the command-line option may be omitted (optionals only).
        # *** DISABLED: TypeError: 'required' is an invalid argument for positionals ***
    help='date (YYYY-MM-DD) / month (YYYY-MM) to aggregate (from)',   # A brief description of what the argument does.
    metavar='DATE',   # A name for the argument in usage messages.
    # dest=None,   # The name of the attribute to be added to the object returned by parse_args().
        # *** DISABLED: ValueError: dest supplied twice for positional argument
)

parser___conso_agg_viz_data.add_argument(
    '--to',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs=None,   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=None,   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=False,   # Whether or not the command-line option may be omitted (optionals only).
    help='date (YYYY-MM-DD) / month (YYYY-MM) to aggregate to',   # A brief description of what the argument does.
    metavar='TO_DATE',   # A name for the argument in usage messages.
    dest='to_date'   # The name of the attribute to be added to the object returned by parse_args().
)


# RM S3 TMP
parser___rm_s3_tmp = \
    data_cmd_sub_parsers.add_parser(
        name=RM_S3_TMP_CMD,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}.rm_s3_tmp(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}.rm_s3_tmp(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
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


# DEL DATA STREAMS
parser___del_data_streams = \
    data_cmd_sub_parsers.add_parser(
        name=DEL_DATA_STREAMS,
        prog=None,   # The name of the program (default: sys.argv[0])
        usage=None,   # The string describing the program usage (default: generated from arguments added to parser)
        description='%(prog)s: CLI for {}._delete_machine_data_streams(...) >>>'.format(Client.__qual_name__()),   # Text to display before the argument help (default: none)
        epilog='^^^ %(prog)s: CLI for {}._delete_machine_data_streams(...)\n'.format(Client.__qual_name__()),   # Text to display after the argument help (default: none)
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

parser___del_data_streams.add_argument(
    '--classes',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs='+',   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=[],   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=True,   # Whether or not the command-line option may be omitted (optionals only).
    help='Machine Class name(s) to filter',   # A brief description of what the argument does.
    metavar='MACHINE_CLASS_NAMES',   # A name for the argument in usage messages.
    dest='machine_class_names'   # The name of the attribute to be added to the object returned by parse_args().
)

parser___del_data_streams.add_argument(
    '--names',   # name or flags - Either a name or a list of option strings, e.g. foo or -f, --foo.
    action=None,   # The basic type of action to be taken when this argument is encountered at the command line.
    nargs='+',   # The number of command-line arguments that should be consumed.
    const=None,   # A constant value required by some action and nargs selections.
    default=[],   # The value produced if the argument is absent from the command line.
    type=str,   # The type to which the command-line argument should be converted.
    choices=None,   # A container of the allowable values for the argument.
    required=True,   # Whether or not the command-line option may be omitted (optionals only).
    help='Machine Data Stream name(s) to delete',   # A brief description of what the argument does.
    metavar='MACHINE_DATA_STREAM_NAMES',   # A name for the argument in usage messages.
    dest='machine_data_stream_names'   # The name of the attribute to be added to the object returned by parse_args().
)
