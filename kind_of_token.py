import enum


# class syntax
class Type(enum.Enum):
    # Kind,
    ENDMARKER = 1,  # EOF
    ERROR = 2,
    COMMENT = 3,  # aadsdsa, #= fdsf #=
    WHITESPACE = 4,  # '\n   \t'
    IDENTIFIER = 5,  # foo, Σxx
    AT_SIGN = 6,  # @
    COMMA = 7,  # ,
    SEMICOLON = 8,  # ;

    # begin_keywords,
    KEYWORD = 9,  # general
    ABSTRACT = 10,
    BAREMODULE = 11,
    BEGIN = 12,
    BREAK = 13,
    CATCH = 14,
    CONST = 15,
    CONTINUE = 16,
    DO = 17,
    ELSE = 18,
    ELSEIF = 19,
    END = 20,
    EXPORT = 21,
    FINALLY = 22,
    FOR = 23,
    FUNCTION = 24,
    GLOBAL = 25,
    IF = 26,
    IMPORT = 27,
    IMPORTALL = 28,
    LET = 29,
    LOCAL = 30,
    MACRO = 31,
    MODULE = 32,
    MUTABLE = 33,
    NEW = 34,
    OUTER = 35,
    PRIMITIVE = 36,
    QUOTE = 37,
    RETURN = 38,
    STRUCT = 39,
    TRY = 40,
    TYPE = 41,
    USING = 42,
    WHILE = 43,
    # end_keywords,

    # begin_literal,
    LITERAL = 44,  # general
    INTEGER = 45,  # 4
    BIN_INT = 46,  # 0b1
    HEX_INT = 47,  # 0x0
    OCT_INT = 48,  # 0o0
    FLOAT = 49,  # 3.5, 3.7e+3
    STRING = 50,  # "foo"
    TRIPLE_STRING = 51,  # """ foo \n """
    CHAR = 52,  # 'a'
    TRUE = 53,
    FALSE = 54,
    # end_literal,

    # begin_delimiters,
    LSQUARE = 55,  # [
    RSQUARE = 56,  # ]
    LBRACE = 57,  # {
    RBRACE = 58,  # }
    LPAREN = 59,  # (
    RPAREN = 60,  # )
    # end_delimiters,

    # begin_ops,
    OP = 61,  # general
    DDOT = 121, # ..
    DDDOT = 62,  # ...

    # begin_assignments,
    EQ = 63,  # =
    PLUS_EQ = 64,  # +=
    MINUS_EQ = 65,  # -=
    STAR_EQ = 66,  # *=
    FWD_SLASH_EQ = 67,  # /=
    FWDFWD_SLASH_EQ = 68,  # //=
    OR_EQ = 69,  # |=
    CIRCUMFLEX_EQ = 70,  # ^=
    DIVISION_EQ = 71 # ÷=
    REM_EQ = 72,  # %=
    LBITSHIFT_EQ = 73,  # <<=
    RBITSHIFT_EQ = 74,  # >>=
    UNSIGNED_BITSHIFT_EQ = 75,  # >>>=
    BACKSLASH_EQ = 76,  # \=
    AND_EQ = 77,  # &=
    COLON_EQ = 78,  # :=
    APPROX = 79,  # ~
    EX_OR_EQ = 80,  # $=
    RPIPE = 120 # |>
    LPIPE = 121 # <|
    # end_assignments,

    # begin_pairarrow,
    PAIR_ARROW = 81,  # =>
    # end_pairarrow,

    # begin_conditional,
    CONDITIONAL = 82,  # ?
    # end_conditional,

    # begin_lazyor,
    LAZY_OR = 83,  # ||
    # end_lazyor,

    # begin_lazyand,
    LAZY_AND = 84,  # &&
    # end_lazyand,

    # begin_comparison,
    ISSUBTYPE = 85,  # <:
    ISSUPERTYPE = 86,  # >:
    GREATER = 87,  # >
    LESS = 88,  # <
    GREATER_EQ = 89,  # >=
    LESS_EQ = 90,  # <=
    EQEQ = 91,  # ==
    EQEQEQ = 92,  # ===
    NOT_EQ = 93,  # !=
    NOT_IS = 94,  # !==
    IN = 95,  # in
    ISA = 96,  # isa
    # end_comparison,

    # begin_colon,
    COLON = 97,  # :
    # end_colon

    # begin_plus,
    EX_OR = 98,  # $
    PLUS = 99,  # +
    MINUS = 100,  # -
    PLUSPLUS = 101,  # ++
    OR = 102,  # |
    # end_plus,

    # begin_bitshifts,
    LBITSHIFT = 103,  # <<
    RBITSHIFT = 104,  # >>
    UNSIGNED_BITSHIFT = 105,  # >>>
    # end_bitshifts,

    # begin_times,
    STAR = 106,  # *
    FWD_SLASH = 107,  # /
    REM = 108,  # %
    AND = 109,  # &
    BACKSLASH = 110 # \\
    # end_times,

    # begin_rational,
    FWDFWD_SLASH = 110,  # //
    # end_rational,

    # begin_power,
    CIRCUMFLEX_ACCENT = 111,  # ^
    # end_power,

    # begin_decl,
    DECLARATION = 112,  # ::
    # end_decl,

    # begin_dot,
    DOT = 113,  # .
    # end_dot,

    NOT = 114,  # !
    TRANSPOSE = 116,  # .'
    ANON_FUNC = 117,  # ->
    RIGHT_ARROW = 118  # -->
    # end_ops,


KEYWORDS = {
    "abstract": Type.ABSTRACT,
    "baremodule": Type.BAREMODULE,
    "begin": Type.BEGIN,
    "break": Type.BREAK,
    "catch": Type.CATCH,
    "const": Type.CONST,
    "continue": Type.CONTINUE,
    "do": Type.DO,
    "else": Type.ELSE,
    "elseif": Type.ELSEIF,
    "end": Type.END,
    "export": Type.EXPORT,
    "finally": Type.FINALLY,
    "for": Type.FOR,
    "function": Type.FUNCTION,
    "global": Type.GLOBAL,
    "if": Type.IF,
    "import": Type.IMPORT,
    "importall": Type.IMPORTALL,
    "let": Type.LET,
    "local": Type.LOCAL,
    "macro": Type.MACRO,
    "module": Type.MODULE,
    "mutable": Type.MUTABLE,
    "new": Type.NEW,
    "outer": Type.OUTER,
    "primitive": Type.PRIMITIVE,
    "quote": Type.QUOTE,
    "return": Type.RETURN,
    "struct": Type.STRUCT,
    "try": Type.TRY,
    "type": Type.TYPE,
    "using": Type.USING,
    "while": Type.WHILE,
    "true": Type.TRUE,
    "false": Type.FALSE
}

COMPARISON_WORDS = ["in", "isa"]

OPEN_BRACKETS = {
    '[': Type.LSQUARE,
    '{': Type.LBRACE,
    '(': Type.LPAREN,
}

CLOSE_BRACKETS = {
    ']': Type.RSQUARE,
    '}': Type.RBRACE,
    ')': Type.RPAREN
}

OPS_REVERSE = {
    "=": Type.EQ,
    "+=": Type.PLUS_EQ,
    "-=": Type.MINUS_EQ,
    "*=": Type.STAR_EQ,
    "/=": Type.FWD_SLASH_EQ,
    "//=": Type.FWDFWD_SLASH_EQ,
    "|=": Type.OR_EQ,
    "^=": Type.CIRCUMFLEX_EQ,
    "÷=": Type.DIVISION_EQ,
    "%=": Type.REM_EQ,
    "<<=": Type.LBITSHIFT_EQ,
    ">>=": Type.RBITSHIFT_EQ,
    "<<": Type.LBITSHIFT,
    ">>": Type.RBITSHIFT,
    ">>>": Type.UNSIGNED_BITSHIFT,
    ">>>=": Type.UNSIGNED_BITSHIFT_EQ,
    "\\=": Type.BACKSLASH_EQ,
    "&=": Type.AND_EQ,
    ":=": Type.COLON_EQ,
    "=>": Type.PAIR_ARROW,
    "~": Type.APPROX,
    "$=": Type.EX_OR_EQ,
    "-->": Type.RIGHT_ARROW,
    "||": Type.LAZY_OR,
    "&&": Type.LAZY_AND,
    "<:": Type.ISSUBTYPE,
    ">:": Type.ISSUPERTYPE,
    ">": Type.GREATER,
    "<": Type.LESS,
    ">=": Type.GREATER_EQ,
    "<=": Type.LESS_EQ,
    "==": Type.EQEQ,
    "===": Type.EQEQEQ,
    "!=": Type.NOT_EQ,
    "!==": Type.NOT_IS,
    "in": Type.IN,
    "isa": Type.ISA,
    "<|": Type.LPIPE,
    "|>": Type.RPIPE,
    ":": Type.COLON,
    "..": Type.DDOT,
    "$": Type.EX_OR,
    "+": Type.PLUS,
    "-": Type.MINUS,
    "++": Type.PLUSPLUS,
    "|": Type.OR,
    "*": Type.STAR,
    "/": Type.FWD_SLASH,
    "%": Type.REM,
    "\\": Type.BACKSLASH,
    "&": Type.AND,
    "//": Type.FWDFWD_SLASH,
    "^": Type.CIRCUMFLEX_ACCENT,
    "::": Type.DECLARATION,
    "?": Type.CONDITIONAL,
    ".": Type.DOT,
    "!": Type.NOT,
    "...": Type.DDDOT,
    "'.": Type.TRANSPOSE,
    "->": Type.ANON_FUNC
}

WHITE_SPACE = {
    "\n": Type.WHITESPACE,
    "\t": Type.WHITESPACE,
}

LITERALS = [
    Type.INTEGER,
    Type.BIN_INT,
    Type.HEX_INT,
    Type.OCT_INT,
    Type.FLOAT,
    Type.STRING,
    Type.TRIPLE_STRING,
    Type.CHAR
]
