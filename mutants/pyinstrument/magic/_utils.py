from __future__ import annotations

# This file is largely based on https://gist.github.com/Carreau/0f051f57734222da925cd364e59cc17e which is in the public domain
# This (or something similar) may eventually be moved into IPython
import ast
from ast import Assign, Expr, Load, Name, NodeTransformer, Store, parse
from textwrap import dedent
from inspect import signature as _mutmut_signature
from typing import Annotated
from typing import Callable
from typing import ClassVar


MutantDict = Annotated[dict[str, Callable], "Mutant"]


def _mutmut_trampoline(orig, mutants, call_args, call_kwargs, self_arg = None):
    """Forward call to original or mutated function, depending on the environment"""
    import os
    mutant_under_test = os.environ['MUTANT_UNDER_TEST']
    if mutant_under_test == 'fail':
        from mutmut.__main__ import MutmutProgrammaticFailException
        raise MutmutProgrammaticFailException('Failed programmatically')      
    elif mutant_under_test == 'stats':
        from mutmut.__main__ import record_trampoline_hit
        record_trampoline_hit(orig.__module__ + '.' + orig.__name__)
        result = orig(*call_args, **call_kwargs)
        return result
    prefix = orig.__module__ + '.' + orig.__name__ + '__mutmut_'
    if not mutant_under_test.startswith(prefix):
        result = orig(*call_args, **call_kwargs)
        return result
    mutant_name = mutant_under_test.rpartition('.')[-1]
    if self_arg:
        # call to a class method where self is not bound
        result = mutants[mutant_name](self_arg, *call_args, **call_kwargs)
    else:
        result = mutants[mutant_name](*call_args, **call_kwargs)
    return result


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

    def xǁPrePostAstTransformerǁ__init____mutmut_orig(self, pre: str | ast.Module, post: str | ast.Module):
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

    def xǁPrePostAstTransformerǁ__init____mutmut_1(self, pre: str | ast.Module, post: str | ast.Module):
        """
        pre and post are either strings, or ast.Modules object that need to be run just before or after
        the user code.

        While strings are possible, we suggest using ast.Modules
        object and mangling the corresponding variable names
        to be invalid python identifiers to avoid name conflicts.
        """
        if isinstance(pre, str):
            pre = None
        if isinstance(post, str):
            post = parse(post)

        self.pre = pre.body
        self.post = post.body
        self.active = True

    def xǁPrePostAstTransformerǁ__init____mutmut_2(self, pre: str | ast.Module, post: str | ast.Module):
        """
        pre and post are either strings, or ast.Modules object that need to be run just before or after
        the user code.

        While strings are possible, we suggest using ast.Modules
        object and mangling the corresponding variable names
        to be invalid python identifiers to avoid name conflicts.
        """
        if isinstance(pre, str):
            pre = parse(None)
        if isinstance(post, str):
            post = parse(post)

        self.pre = pre.body
        self.post = post.body
        self.active = True

    def xǁPrePostAstTransformerǁ__init____mutmut_3(self, pre: str | ast.Module, post: str | ast.Module):
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
            post = None

        self.pre = pre.body
        self.post = post.body
        self.active = True

    def xǁPrePostAstTransformerǁ__init____mutmut_4(self, pre: str | ast.Module, post: str | ast.Module):
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
            post = parse(None)

        self.pre = pre.body
        self.post = post.body
        self.active = True

    def xǁPrePostAstTransformerǁ__init____mutmut_5(self, pre: str | ast.Module, post: str | ast.Module):
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

        self.pre = None
        self.post = post.body
        self.active = True

    def xǁPrePostAstTransformerǁ__init____mutmut_6(self, pre: str | ast.Module, post: str | ast.Module):
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
        self.post = None
        self.active = True

    def xǁPrePostAstTransformerǁ__init____mutmut_7(self, pre: str | ast.Module, post: str | ast.Module):
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
        self.active = None

    def xǁPrePostAstTransformerǁ__init____mutmut_8(self, pre: str | ast.Module, post: str | ast.Module):
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
        self.active = False
    
    xǁPrePostAstTransformerǁ__init____mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPrePostAstTransformerǁ__init____mutmut_1': xǁPrePostAstTransformerǁ__init____mutmut_1, 
        'xǁPrePostAstTransformerǁ__init____mutmut_2': xǁPrePostAstTransformerǁ__init____mutmut_2, 
        'xǁPrePostAstTransformerǁ__init____mutmut_3': xǁPrePostAstTransformerǁ__init____mutmut_3, 
        'xǁPrePostAstTransformerǁ__init____mutmut_4': xǁPrePostAstTransformerǁ__init____mutmut_4, 
        'xǁPrePostAstTransformerǁ__init____mutmut_5': xǁPrePostAstTransformerǁ__init____mutmut_5, 
        'xǁPrePostAstTransformerǁ__init____mutmut_6': xǁPrePostAstTransformerǁ__init____mutmut_6, 
        'xǁPrePostAstTransformerǁ__init____mutmut_7': xǁPrePostAstTransformerǁ__init____mutmut_7, 
        'xǁPrePostAstTransformerǁ__init____mutmut_8': xǁPrePostAstTransformerǁ__init____mutmut_8
    }
    
    def __init__(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPrePostAstTransformerǁ__init____mutmut_orig"), object.__getattribute__(self, "xǁPrePostAstTransformerǁ__init____mutmut_mutants"), args, kwargs, self)
        return result 
    
    __init__.__signature__ = _mutmut_signature(xǁPrePostAstTransformerǁ__init____mutmut_orig)
    xǁPrePostAstTransformerǁ__init____mutmut_orig.__name__ = 'xǁPrePostAstTransformerǁ__init__'

    def xǁPrePostAstTransformerǁreset__mutmut_orig(self):
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

    def xǁPrePostAstTransformerǁreset__mutmut_1(self):
        self.core = None
        self.try_ = self.core.body[0].body = []  # type: ignore
        self.fin = self.core.body[0].finalbody = []  # type: ignore

    def xǁPrePostAstTransformerǁreset__mutmut_2(self):
        self.core = parse(
            None
        )
        self.try_ = self.core.body[0].body = []  # type: ignore
        self.fin = self.core.body[0].finalbody = []  # type: ignore

    def xǁPrePostAstTransformerǁreset__mutmut_3(self):
        self.core = parse(
            dedent(
                None
            )
        )
        self.try_ = self.core.body[0].body = []  # type: ignore
        self.fin = self.core.body[0].finalbody = []  # type: ignore

    def xǁPrePostAstTransformerǁreset__mutmut_4(self):
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
        self.try_ = self.core.body[0].body = None  # type: ignore
        self.fin = self.core.body[0].finalbody = []  # type: ignore

    def xǁPrePostAstTransformerǁreset__mutmut_5(self):
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
        self.try_ = self.core.body[1].body = []  # type: ignore
        self.fin = self.core.body[0].finalbody = []  # type: ignore

    def xǁPrePostAstTransformerǁreset__mutmut_6(self):
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
        self.fin = self.core.body[0].finalbody = None  # type: ignore

    def xǁPrePostAstTransformerǁreset__mutmut_7(self):
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
        self.fin = self.core.body[1].finalbody = []  # type: ignore
    
    xǁPrePostAstTransformerǁreset__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPrePostAstTransformerǁreset__mutmut_1': xǁPrePostAstTransformerǁreset__mutmut_1, 
        'xǁPrePostAstTransformerǁreset__mutmut_2': xǁPrePostAstTransformerǁreset__mutmut_2, 
        'xǁPrePostAstTransformerǁreset__mutmut_3': xǁPrePostAstTransformerǁreset__mutmut_3, 
        'xǁPrePostAstTransformerǁreset__mutmut_4': xǁPrePostAstTransformerǁreset__mutmut_4, 
        'xǁPrePostAstTransformerǁreset__mutmut_5': xǁPrePostAstTransformerǁreset__mutmut_5, 
        'xǁPrePostAstTransformerǁreset__mutmut_6': xǁPrePostAstTransformerǁreset__mutmut_6, 
        'xǁPrePostAstTransformerǁreset__mutmut_7': xǁPrePostAstTransformerǁreset__mutmut_7
    }
    
    def reset(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPrePostAstTransformerǁreset__mutmut_orig"), object.__getattribute__(self, "xǁPrePostAstTransformerǁreset__mutmut_mutants"), args, kwargs, self)
        return result 
    
    reset.__signature__ = _mutmut_signature(xǁPrePostAstTransformerǁreset__mutmut_orig)
    xǁPrePostAstTransformerǁreset__mutmut_orig.__name__ = 'xǁPrePostAstTransformerǁreset'

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_orig(self, node: ast.Module):
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_1(self, node: ast.Module):
        if self.active:
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_2(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = None
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_3(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[+1]
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_4(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-2]
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_5(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = ""
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_6(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(None)
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_7(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign(None, value=last.value))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_8(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", ctx=Store())], value=None))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_9(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign(value=last.value))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_10(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", ctx=Store())], ))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_11(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name(None, ctx=Store())], value=last.value))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_12(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", ctx=None)], value=last.value))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_13(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name(ctx=Store())], value=last.value))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_14(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", )], value=last.value))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_15(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("XXast-tmpXX", ctx=Store())], value=last.value))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_16(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("AST-TMP", ctx=Store())], value=last.value))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_17(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", ctx=Store())], value=last.value))
            ret = None
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_18(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", ctx=Store())], value=last.value))
            ret = Expr(value=None)
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_19(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", ctx=Store())], value=last.value))
            ret = Expr(value=Name(None, ctx=Load()))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_20(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", ctx=Store())], value=last.value))
            ret = Expr(value=Name("ast-tmp", ctx=None))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_21(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", ctx=Store())], value=last.value))
            ret = Expr(value=Name(ctx=Load()))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_22(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", ctx=Store())], value=last.value))
            ret = Expr(value=Name("ast-tmp", ))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_23(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", ctx=Store())], value=last.value))
            ret = Expr(value=Name("XXast-tmpXX", ctx=Load()))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_24(self, node: ast.Module):
        if not self.active:
            return node
        self.reset()
        last = node.body[-1]
        ret = None
        if isinstance(last, Expr):
            node.body.pop()
            node.body.append(Assign([Name("ast-tmp", ctx=Store())], value=last.value))
            ret = Expr(value=Name("AST-TMP", ctx=Load()))
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

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_25(self, node: ast.Module):
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
                None, Assign([Name("ast-tmp", ctx=Store())], value=ast.Constant(None))
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_26(self, node: ast.Module):
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
                0, None
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_27(self, node: ast.Module):
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
                Assign([Name("ast-tmp", ctx=Store())], value=ast.Constant(None))
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_28(self, node: ast.Module):
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
                0, )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_29(self, node: ast.Module):
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
                1, Assign([Name("ast-tmp", ctx=Store())], value=ast.Constant(None))
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_30(self, node: ast.Module):
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
                0, Assign(None, value=ast.Constant(None))
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_31(self, node: ast.Module):
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
                0, Assign([Name("ast-tmp", ctx=Store())], value=None)
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_32(self, node: ast.Module):
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
                0, Assign(value=ast.Constant(None))
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_33(self, node: ast.Module):
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
                0, Assign([Name("ast-tmp", ctx=Store())], )
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_34(self, node: ast.Module):
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
                0, Assign([Name(None, ctx=Store())], value=ast.Constant(None))
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_35(self, node: ast.Module):
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
                0, Assign([Name("ast-tmp", ctx=None)], value=ast.Constant(None))
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_36(self, node: ast.Module):
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
                0, Assign([Name(ctx=Store())], value=ast.Constant(None))
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_37(self, node: ast.Module):
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
                0, Assign([Name("ast-tmp", )], value=ast.Constant(None))
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_38(self, node: ast.Module):
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
                0, Assign([Name("XXast-tmpXX", ctx=Store())], value=ast.Constant(None))
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_39(self, node: ast.Module):
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
                0, Assign([Name("AST-TMP", ctx=Store())], value=ast.Constant(None))
            )
        for p in self.pre + node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_40(self, node: ast.Module):
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
        for p in self.pre - node.body:
            self.try_.append(p)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_41(self, node: ast.Module):
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
            self.try_.append(None)
        for p in self.post:
            self.fin.append(p)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_42(self, node: ast.Module):
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
            self.fin.append(None)
        if ret is not None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_43(self, node: ast.Module):
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
        if ret is None:
            self.core.body.append(ret)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_44(self, node: ast.Module):
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
            self.core.body.append(None)

        ast.fix_missing_locations(self.core)
        return self.core

    def xǁPrePostAstTransformerǁvisit_Module__mutmut_45(self, node: ast.Module):
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

        ast.fix_missing_locations(None)
        return self.core
    
    xǁPrePostAstTransformerǁvisit_Module__mutmut_mutants : ClassVar[MutantDict] = {
    'xǁPrePostAstTransformerǁvisit_Module__mutmut_1': xǁPrePostAstTransformerǁvisit_Module__mutmut_1, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_2': xǁPrePostAstTransformerǁvisit_Module__mutmut_2, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_3': xǁPrePostAstTransformerǁvisit_Module__mutmut_3, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_4': xǁPrePostAstTransformerǁvisit_Module__mutmut_4, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_5': xǁPrePostAstTransformerǁvisit_Module__mutmut_5, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_6': xǁPrePostAstTransformerǁvisit_Module__mutmut_6, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_7': xǁPrePostAstTransformerǁvisit_Module__mutmut_7, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_8': xǁPrePostAstTransformerǁvisit_Module__mutmut_8, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_9': xǁPrePostAstTransformerǁvisit_Module__mutmut_9, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_10': xǁPrePostAstTransformerǁvisit_Module__mutmut_10, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_11': xǁPrePostAstTransformerǁvisit_Module__mutmut_11, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_12': xǁPrePostAstTransformerǁvisit_Module__mutmut_12, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_13': xǁPrePostAstTransformerǁvisit_Module__mutmut_13, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_14': xǁPrePostAstTransformerǁvisit_Module__mutmut_14, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_15': xǁPrePostAstTransformerǁvisit_Module__mutmut_15, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_16': xǁPrePostAstTransformerǁvisit_Module__mutmut_16, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_17': xǁPrePostAstTransformerǁvisit_Module__mutmut_17, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_18': xǁPrePostAstTransformerǁvisit_Module__mutmut_18, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_19': xǁPrePostAstTransformerǁvisit_Module__mutmut_19, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_20': xǁPrePostAstTransformerǁvisit_Module__mutmut_20, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_21': xǁPrePostAstTransformerǁvisit_Module__mutmut_21, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_22': xǁPrePostAstTransformerǁvisit_Module__mutmut_22, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_23': xǁPrePostAstTransformerǁvisit_Module__mutmut_23, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_24': xǁPrePostAstTransformerǁvisit_Module__mutmut_24, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_25': xǁPrePostAstTransformerǁvisit_Module__mutmut_25, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_26': xǁPrePostAstTransformerǁvisit_Module__mutmut_26, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_27': xǁPrePostAstTransformerǁvisit_Module__mutmut_27, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_28': xǁPrePostAstTransformerǁvisit_Module__mutmut_28, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_29': xǁPrePostAstTransformerǁvisit_Module__mutmut_29, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_30': xǁPrePostAstTransformerǁvisit_Module__mutmut_30, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_31': xǁPrePostAstTransformerǁvisit_Module__mutmut_31, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_32': xǁPrePostAstTransformerǁvisit_Module__mutmut_32, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_33': xǁPrePostAstTransformerǁvisit_Module__mutmut_33, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_34': xǁPrePostAstTransformerǁvisit_Module__mutmut_34, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_35': xǁPrePostAstTransformerǁvisit_Module__mutmut_35, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_36': xǁPrePostAstTransformerǁvisit_Module__mutmut_36, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_37': xǁPrePostAstTransformerǁvisit_Module__mutmut_37, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_38': xǁPrePostAstTransformerǁvisit_Module__mutmut_38, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_39': xǁPrePostAstTransformerǁvisit_Module__mutmut_39, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_40': xǁPrePostAstTransformerǁvisit_Module__mutmut_40, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_41': xǁPrePostAstTransformerǁvisit_Module__mutmut_41, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_42': xǁPrePostAstTransformerǁvisit_Module__mutmut_42, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_43': xǁPrePostAstTransformerǁvisit_Module__mutmut_43, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_44': xǁPrePostAstTransformerǁvisit_Module__mutmut_44, 
        'xǁPrePostAstTransformerǁvisit_Module__mutmut_45': xǁPrePostAstTransformerǁvisit_Module__mutmut_45
    }
    
    def visit_Module(self, *args, **kwargs):
        result = _mutmut_trampoline(object.__getattribute__(self, "xǁPrePostAstTransformerǁvisit_Module__mutmut_orig"), object.__getattribute__(self, "xǁPrePostAstTransformerǁvisit_Module__mutmut_mutants"), args, kwargs, self)
        return result 
    
    visit_Module.__signature__ = _mutmut_signature(xǁPrePostAstTransformerǁvisit_Module__mutmut_orig)
    xǁPrePostAstTransformerǁvisit_Module__mutmut_orig.__name__ = 'xǁPrePostAstTransformerǁvisit_Module'
