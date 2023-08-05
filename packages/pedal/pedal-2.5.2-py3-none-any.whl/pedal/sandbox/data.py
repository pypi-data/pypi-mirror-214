"""
Helper classes for storing data about executions.

NameSpace
    A dictionary that maps names to values. Represents the results of executing
    code, specifically the variables/functions/classes/etc. that exist
    afterwards. Think of it as "locals()". Represented to instructors via
    the `data` attribute.

Context
    The code that was previously executed. This is a history of what was
    executed, that can be used to augment stack traces and such. There are
    commands available to "chunk" contexts so that executions can be grouped
    as a single series of concepts.

Context ID
    A unique identifier for an execution

Execute
    Given some Python code, AST, or filename, uses ``compile`` and ``exec``
    to actually run the code.

Run
    To execute an arbitrary chunk of code, as opposed to being a ``call`` or
    ``eval``.

Call
    To execute a specific function that exists in the current NameSpace.

Eval
    To execute a chunk of code that represents an expression, storing the
    result in a temporary variable.

Target
    When code is Called or Evaled, the result is stored in a Target. This
    can be a variable, or a more complex expression.
"""
from pedal.sandbox.mocked import MockDictModule, MockModule, create_module


class SandboxContextKind:
    """ Enumeration of sandbox execution kind's. """
    RUN = 'run'
    EVAL = 'eval'
    CALL = 'call'
    GETITEM = 'getitem'

    @staticmethod
    def describe_action(context):
        """
        Produces the relevant Action message for the given kind of context.

        Args:
            context (SandboxContext): The context to describe.
        Returns:
            str: The description of the action.
        """
        if context.kind == SandboxContextKind.EVAL and context.target in ("", "_"):
            return 'I evaluated the expression'
        else:
            return 'I ran the code'

    def __repr__(self):
        return f"<SandboxContextKind {self.value}>"


class SandboxContext:
    """
    Simple data class holding information about an execution within a sandbox.
    Includes such information as the code that was run, its filename, inputs,
    outputs, exceptions, etc.

    Args:
        context_id (int): The unique ID representing this sandbox execution.
        code (str): The code that was executed.
        filename (str): The filename of the code that was executed.
        kind (SandboxContextKind): The kind of execution that generated this.
        target (str or None): If the result was stored in a variable/expression,
            this will be its name.
        inputs (list[str]): Any inputs that were used during the code's
            execution.
        output (str): The output that was generated by this execution.
        exception (Exception or None): The exception that occurred during this
            execution, or None if none occurred.
        submission (:py:class:`pedal.core.submission.Submission`): The
            submission object that this context was attached to.
        called (str): The name of the function that was called, if one was
            called.
        args (list[str]): A string representation of the arguments that were
            called.
    """

    def __init__(self, context_id, code, filename, kind, target, inputs, output,
                 exception, submission, called=None, args=None):
        self.context_id = context_id
        self.kind = kind
        # Hack: Chomp off the "_ =" if the target is "_"
        if target == "_":
            code = code[len("_ = "):]
        self.code = code
        self.filename = filename
        self.target = target
        self.inputs = inputs
        self.output = output
        self.exception = exception
        self.submission = submission
        self.called = called
        self.args = args

    def clone(self, context_id):
        """
        Create a separate copy of this item. Inputs will be deep-copied.

        Args:
            context_id (int): The new context ID.
        Returns:
            SandboxContext: The new context, copied from the old one except with a new ID.
        """
        return SandboxContext(context_id, self.code, self.filename,
                              self.kind, self.target, list(self.inputs),
                              self.output, self.exception, self.submission)

    def __repr__(self):
        return f"<SandboxContext {self.context_id}>"


class ExecutionTextHolder:
    """
    Helper class for formatting the text of an execution. Keeps track of the last action taken, the current body,
    and the current formatter for this Report.

    Args:
        format (ReportFormatter): The formatter to use for this Report.
    """
    def __init__(self, report_format):
        self._result = []
        self._last_action = None
        self._current_body = []
        self._format = report_format

    def add_message(self, action_message, body=None):
        """
        Add a message to the text of the execution.

        Args:
            action_message (str): The message to add.
            body (str): The body of the message, if any.
        """
        if action_message != self._last_action and self._last_action is not None:
            self._finish_body()
        if body:
            self._current_body.append(body)
        self._last_action = action_message

    def _finish_body(self):
        """
        Finish the current body, if any, and add it to the result.
        """
        if self._current_body:
            code_message = self._format.python_code("\n".join(self._current_body))
            message = self._last_action + "\n"+code_message + "\n"
            self._result.append(message)
            self._current_body = []
        elif self._last_action:
            self._result.append(self._last_action+"\n")

    def get_lines(self):
        """
        Get the lines of the execution text, as a single string.

        Returns:
            str: The lines of the execution text.
        """
        self._finish_body()
        return "".join(self._result)


INPUT_MAXIMUM_LINES = 30


def format_contexts(contexts, format):
    """
    Create a text string representation from a list of contexts.

    Args:
        contexts (list[list[SandboxContext]]): The list of list of sandbox
            executions. The inner list is because we could have a group of
            contexts (although more likely it'll be a single one).
        format (:py:class:`pedal.core.formatting.Formatter`): The formatter
            to use to augment the context message.

    Returns:
        str: The string representation of the contexts.
    """
    execution_text = ExecutionTextHolder(format)
    inputs_text = []
    for context_group in contexts:
        for context in context_group:
            if context.filename in (None, context.submission.instructor_file):
                action_message = SandboxContextKind.describe_action(context)
                execution_text.add_message(action_message+":", context.code)
            elif context.filename in (context.submission.main_file, ):
                execution_text.add_message(f"I ran your code.")
            else:
                filename_message = format.filename(context.filename)
                execution_text.add_message(f"I ran the file {filename_message}.")
            inputs_text.extend(context.inputs)
    final_text = [execution_text.get_lines()]
    if inputs_text:
        if len(inputs_text) > INPUT_MAXIMUM_LINES:
            midpoint = int(INPUT_MAXIMUM_LINES / 2)
            missed = len(inputs_text) - INPUT_MAXIMUM_LINES
            inputs_text = inputs_text[:midpoint] + [f"... (Skipping {missed} other inputs) ..."] + inputs_text[-midpoint:]
        inputs = "\n".join(inputs_text) + " "
        inputs_message = format.inputs(inputs)
        final_text.append(f"And I entered as input:{inputs_message}")
    return "\n".join(final_text)


class SandboxModules:
    """
    Container for any mocked modules and their data.
    """

    def __init__(self):
        self._modules = {}

    def clear(self):
        """ Removes any existing modules. """
        self._modules.clear()

    def new_module(self, data, import_name, friendly_name):
        """
        Creates a new mocked module.

        Args:
            data (dict or MockModule): The data to use for the new mocked module
            import_name (str): The name that is associated with ``import``.
            friendly_name (str): The name to use when accessing this module's
                data via attribute lookup.

        Returns:
            dict[str,:py:class:`types.ModuleType`]: The newly created modules
                mapped by their imported path names.
        """
        if isinstance(data, MockModule):
            import_name = [import_name, *data.SUBMODULES]
        root, modules, target = create_module(import_name)
        if isinstance(data, dict):
            mocked_module = MockDictModule(data)
            mocked_module.add_to_module(target)
        elif isinstance(data, MockModule):
            data.add_to_module(target, modules)
        else:
            raise ValueError("Given data must be either MockModule or dict.")
        self._modules[friendly_name] = data
        return modules

    def __getattr__(self, name):
        return self._modules[name]

    def __dir__(self):
        return self._modules.keys()


class SandboxVariable:
    """
    A representation of a variable in the student's data namespace. This
    has limited application, but can be used to improve the data passed into
    :py:func:`pedal.sandbox.commands.call` so that the local variables are used.
    Largely superceded by the ``locals_args`` parameter.
    """

    def __init__(self, name, value):
        self.name = name
        self.value = value
