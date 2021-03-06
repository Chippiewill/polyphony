from enum import Enum


class CompileError(Exception):
    pass


class InterpretError(Exception):
    pass


class Errors(Enum):
    # type errors
    MUST_BE_X_TYPE = 100
    MISSING_REQUIRED_ARG = 101
    MISSING_REQUIRED_ARG_N = 102
    TAKES_TOOMANY_ARGS = 103
    UNKNOWN_ATTRIBUTE = 104
    INCOMPATIBLE_TYPES = 105
    INCOMPATIBLE_RETURN_TYPE = 106
    INCOMPATIBLE_PARAMETER_TYPE = 107
    LEN_TAKES_ONE_ARG = 108
    LEN_TAKES_SEQ_TYPE = 109
    IS_NOT_CALLABLE = 110
    IS_NOT_SUBSCRIPTABLE = 111
    CONFLICT_TYPE_HINT = 112
    UNSUPPORTED_ATTRIBUTE_TYPE_HINT = 113
    UNKNOWN_TYPE_NAME = 114
    MUST_BE_X = 115

    # semantic errors
    REFERENCED_BEFORE_ASSIGN = 200
    UNDEFINED_NAME = 201
    CANNOT_IMPORT = 202

    # polyphony language restrictions
    UNSUPPORTED_LETERAL_TYPE = 800
    UNSUPPORTED_BINARY_OPERAND_TYPE = 801
    SEQ_ITEM_MUST_BE_INT = 802
    SEQ_MULTIPLIER_MUST_BE_CONST = 803
    UNSUPPORTED_OPERATOR = 804
    SEQ_CAPACITY_OVERFLOWED = 805
    UNSUPPORTED_EXPR = 806
    GLOBAL_VAR_MUST_BE_CONST = 807
    GLOBAL_OBJECT_CANT_BE_MUTABLE = 808
    GLOBAL_INSTANCE_IS_NOT_SUPPORTED = 809
    UNSUPPORTED_SYNTAX = 810
    UNSUPPORTED_DEFAULT_SEQ_PARAM = 811
    UNSUPPORTED_DECORATOR = 812
    METHOD_MUST_HAVE_SELF = 813
    REDEFINED_NAME = 814
    LOCAL_CLASS_DEFINITION_NOT_ALLOWED = 815

    # polyphony library restrictions
    MUDULE_MUST_BE_IN_GLOBAL = 900
    MODULE_PORT_MUST_ASSIGN_ONLY_ONCE = 901
    MODULE_FIELD_MUST_ASSIGN_IN_CTOR = 902
    CALL_APPEND_WORKER_IN_CTOR = 903
    CALL_MODULE_METHOD = 904
    UNSUPPORTED_TYPES_IN_FUNC = 905
    WORKER_ARG_MUST_BE_X_TYPE = 906
    PORT_MUST_BE_IN_MODULE = 907
    PORT_PARAM_MUST_BE_CONST = 908
    PORT_IS_NOT_USED = 909
    WORKER_MUST_BE_METHOD_OF_MODULE = 910
    PORT_ACCESS_IS_NOT_ALLOWED = 911

    READING_IS_CONFLICTED = 920
    WRITING_IS_CONFLICTED = 921
    DIRECTION_IS_CONFLICTED = 922
    CANNOT_WAIT_OUTPUT = 923

    PURE_ERROR = 930
    PURE_MUST_BE_GLOBAL = 931
    PURE_ARGS_MUST_BE_CONST = 932
    PURE_IS_DISABLED = 933
    PURE_CTOR_MUST_BE_MODULE = 934
    PURE_RETURN_NO_SAME_TYPE = 935

    def __str__(self):
        return ERROR_MESSAGES[self]


ERROR_MESSAGES = {
    # type errors
    Errors.MUST_BE_X_TYPE: "Type of '{}' must be {}, not {}",
    Errors.MISSING_REQUIRED_ARG: "{}() missing required argument",
    Errors.MISSING_REQUIRED_ARG_N: "{}() missing required argument {}",
    Errors.TAKES_TOOMANY_ARGS: "{}() takes {} positional arguments but {} were given",
    Errors.UNKNOWN_ATTRIBUTE: "Unknown attribute name '{}'",
    Errors.INCOMPATIBLE_TYPES: "{} and {} are incompatible types",
    Errors.INCOMPATIBLE_RETURN_TYPE: "Type of return value must be {}, not {}",
    Errors.INCOMPATIBLE_PARAMETER_TYPE: "'{}' is incompatible type as a parameter of {}()",
    Errors.CONFLICT_TYPE_HINT: "A type hint is conflicted",
    Errors.UNSUPPORTED_ATTRIBUTE_TYPE_HINT: "A type hint for other than 'self.*' is not supported",
    Errors.UNKNOWN_TYPE_NAME: "Unknown type name '{}'",
    Errors.MUST_BE_X: "{} is expected",

    Errors.LEN_TAKES_ONE_ARG: "len() takes exactly one argument",
    Errors.LEN_TAKES_SEQ_TYPE: "len() takes sequence type argument",
    Errors.IS_NOT_CALLABLE: "'{}' is not callable",
    Errors.IS_NOT_SUBSCRIPTABLE: "'{}' is not subscriptable",

    # semantic errors
    Errors.REFERENCED_BEFORE_ASSIGN: "local variable '{}' referenced before assignment",
    Errors.UNDEFINED_NAME: "'{}' is not defined",
    Errors.CANNOT_IMPORT: "cannot import name '{}'",

    # polyphony language restrictions
    Errors.UNSUPPORTED_LETERAL_TYPE: "Unsupported literal type {}",
    Errors.UNSUPPORTED_BINARY_OPERAND_TYPE: "Unsupported operand type(s) for {}: {} and {}",
    Errors.SEQ_ITEM_MUST_BE_INT: "Type of sequence item must be int, not {}",
    Errors.SEQ_MULTIPLIER_MUST_BE_CONST: "Type of sequence multiplier must be constant",
    Errors.UNSUPPORTED_OPERATOR: "Unsupported operator {}",
    Errors.SEQ_CAPACITY_OVERFLOWED: "Sequence capacity is overflowing",
    Errors.UNSUPPORTED_EXPR: "Unsupported expression",
    Errors.GLOBAL_VAR_MUST_BE_CONST: "A global or class variable must be a constant value",
    Errors.GLOBAL_OBJECT_CANT_BE_MUTABLE: "Writing to a global object is not allowed",
    Errors.GLOBAL_INSTANCE_IS_NOT_SUPPORTED: "A global instance is not supported",
    Errors.UNSUPPORTED_SYNTAX: "{} is not supported",
    Errors.UNSUPPORTED_DEFAULT_SEQ_PARAM:"cannot set the default value to the sequence type parameter",
    Errors.UNSUPPORTED_DECORATOR: "Unsupported decorator '@{}' is specified",
    Errors.METHOD_MUST_HAVE_SELF: "Class method must have a 'self' parameter",
    Errors.REDEFINED_NAME: "'{}' has been redefined",
    Errors.LOCAL_CLASS_DEFINITION_NOT_ALLOWED: "Local class definition in the function is not allowed",

    # polyphony library restrictions
    Errors.MUDULE_MUST_BE_IN_GLOBAL: "the module class must be in the global scope",
    Errors.MODULE_PORT_MUST_ASSIGN_ONLY_ONCE: "Assignment to a module port can only be done once",
    Errors.MODULE_FIELD_MUST_ASSIGN_IN_CTOR: "Assignment to a module field can only at the constructor",
    Errors.CALL_APPEND_WORKER_IN_CTOR: "Calling append_worker method can only at the constructor",
    Errors.CALL_MODULE_METHOD: "Calling a method of the module class can only in the module itself",
    Errors.UNSUPPORTED_TYPES_IN_FUNC: "It is not supported to pass the {} type argument to {}()",
    Errors.WORKER_ARG_MUST_BE_X_TYPE: "The type of Worker argument must be an object of Port or constant, not {}",
    Errors.PORT_MUST_BE_IN_MODULE: "Port object must created in the constructor of the module class",
    Errors.PORT_PARAM_MUST_BE_CONST: "The port class constructor accepts only constants",
    Errors.PORT_IS_NOT_USED: "Port '{}' is not used at all",
    Errors.WORKER_MUST_BE_METHOD_OF_MODULE: "The worker must be a method of the module",
    Errors.PORT_ACCESS_IS_NOT_ALLOWED: "'any' port cannot be accessed from outside of the module",

    Errors.READING_IS_CONFLICTED: "Reading from '{}' is conflicted",
    Errors.WRITING_IS_CONFLICTED: "Writing to '{}' is conflicted",
    Errors.DIRECTION_IS_CONFLICTED: "Port direction of '{}' is conflicted",
    Errors.CANNOT_WAIT_OUTPUT: "Cannot wait for the output port",

    Errors.PURE_ERROR: "@pure Python execution is failed",
    Errors.PURE_MUST_BE_GLOBAL: "@pure function must be in the global scope",
    Errors.PURE_ARGS_MUST_BE_CONST: "An argument of @pure function must be constant",
    Errors.PURE_IS_DISABLED: "@pure Python execution is disabled",
    Errors.PURE_CTOR_MUST_BE_MODULE: "Classes other than @module class can not use @pure decorator",
    Errors.PURE_RETURN_NO_SAME_TYPE: "@pure function must return the same type values",
}


class Warnings(Enum):
    # warnings
    ASSERTION_FAILED = 100
    EXCEPTION_RAISED = 101

    def __str__(self):
        return WARNING_MESSAGES[self]


WARNING_MESSAGES = {
    Warnings.ASSERTION_FAILED: "The expression of assert always evaluates to False",
    Warnings.EXCEPTION_RAISED: "An exception occurred while executing the Python interpreter at compile time\n(For more information you can use '--verbose' option)",
}
