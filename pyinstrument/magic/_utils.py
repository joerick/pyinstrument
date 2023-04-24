from __future__ import annotations

# This file is largely based on https://gist.github.com/Carreau/0f051f57734222da925cd364e59cc17e which is in the public domain
# This (or something similar) may eventually be moved into IPython
import ast
from ast import Assign, Expr, Load, Name, NodeTransformer, Store, parse
from textwrap import dedent


class PrePostAstTransformer(NodeTransformer):
    """
    Allow to safely wrap user code with pre/post execution hooks that
    run just before and just after usercode, __inside__ the execution loop,
    But still returns the value of the last Expression.

    This might not behave as expected if the user change the InteractiveShell.ast_node_interactivity option.

    This is currently not hygienic and care must be taken to use uncommon names in the pre/post block.

    Assuming the user have

    ```
    code_block:
        [with many expressions]
    last_expression
    ```

    It will transform it into

    ```
    try:
        pre_block
        code_block:
            [with many expressions]
        return_value = last_expression
    finally:
        post_block
    return_value
    ```

    Thus making sure that post is always executed even if pre or user code fails.
    """

    def __init__(self, pre: str | ast.Module, post: str | ast.Module):
        """
        pre and post are either strings, or ast.Modules object that need to be run just before or after
        the user code.

        While strings are possible, we suggest using ast.Modules
        object and mangling the corresponding variable names
        to be invalid python identifiers to avoid name conflicts.
        """
        if isinstance(pre, str):
            pre = parse(pre)
        if isinstance(post, str):
            post = parse(post)

        self.pre = pre.body
        self.post = post.body
        self.active = True

    def reset(self):
        self.core = parse(
            dedent(
                """
            try:
                pass
            finally:
                pass
            """
            )
        )
        self.try_ = self.core.body[0].body = []  # type: ignore
        self.fin = self.core.body[0].finalbody = []  # type: ignore

    def visit_Module(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", ctx=Store())], value=last.value))
            ret = Expr(value=Name("ast-tmp", ctx=Load()))
        # self.core.body.insert(0, Assign([Name('_p', ctx=Store())], value=ast.Constant(None) ))
        if ret:
            self.core.body.insert(
                0, Assign([Name("ast-tmp", ctx=Store())], value=ast.Constant(None))
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core
