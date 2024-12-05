from bidict import bidict

NODE = "node"
PYTHON = "python"
CSHARP = "csharp"
RUBY = "ruby"
LANGUAGE_OPTIONS = [NODE, PYTHON, CSHARP, RUBY]
LANGUAGE_OPTIONS_STR = f"{NODE}, {PYTHON}, {CSHARP}, {RUBY}"
MEMORY_CHOICES = ["128", "256", "512", "1024"]

RUNTIME_LANGUAGE_MAPPING = bidict({
    "node18": NODE,
    "python3-http-debian": PYTHON,
    "dotnet8-csharp": CSHARP,
    "ruby": RUBY
})

LANGUAGE_REQUIREMENT_MAPPING = {
    NODE: "package.json",
    PYTHON: "requirements.txt",
    CSHARP: "Function.csproj",
    RUBY: "Gemfile",
}

SOURCE_CODE_FILE_NAME = {
    NODE: "code.js",
    PYTHON: "code.py",
    CSHARP: "code.cs",
    RUBY: "code.rb"
}

SETUP = "setup"
CREATE = "create"
UPDATE = "update"
DELETE = "delete"

VALIDATE_NAME_REGEX = r"^(?!-)(?!\\d+$)[a-z0-9-]{0,50}[a-z0-9](?<!-)$"
NAME_VALIDATION_MESSAGE = "Name can contain lowercase letters, digits, and hyphens, but hyphens are only allowed between characters, not at the start or end, with a maximum length of 50 characters."

RUNTIME_API_ENDPOINT = "api/v1/faas/runtimes/"
DEPLOY_API_ENDPOINT = "api/v1/faas/functions/"
GET_ALL_FUNCTION_API_ENDPOINT = "api/v1/faas/functions/"
DELETE_FUNCTION_API_ENDPOINT = "api/v1/faas/function/{function_name}/"
UPDATE_FUNCTION_API_ENDPOINT = "api/v1/faas/handler_file/{function_name}/"

DEFAULT_FUNCTION_CONFIG = {
    'function': {
        'name': 'test',
        'runtime': 'python',
        'limits': {
            'memory': '512',
            'timeout': '15'
        },
    }
}

DEFAULT_FUNCTION_CONFIG_NAME = "function_config.yaml"
