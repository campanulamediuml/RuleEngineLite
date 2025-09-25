from typing import List, Dict, Callable, Tuple, Any


class RuleEngine:
    def __init__(self, rules: List[str], data_keys: List[str]):
        self.data_keys = data_keys
        self.compiled: List[Callable[[List[float]], bool]] = []
        for rule in rules:
            self.compiled.append(self.__compile(rule))

    # ---------- 对外唯一 API ----------
    def check_expr(self, data: Dict[str, float]) -> List[bool]:
        values = [data[k] for k in self.data_keys]

        return [fn(values) for fn in self.compiled]

    # ---------- 编译 ----------
    def __compile(self, rule: str) -> Callable[[List[float]], bool]:
        tokens = self.__tokenize(rule)
        ast = self.__parse(tokens)
        return lambda ctx: bool(self.__eval(ast, ctx))

    # ---------- 词法：手工扫描 ----------
    def __tokenize(self, s: str) -> List[Tuple[str, Any]]:
        i, n = 0, len(s)
        tokens: List[Tuple[str, Any]] = []
        while i < n:
            ch = s[i]
            if ch.isspace():
                i += 1
                continue
            if ch == '{':
                j = i + 1
                while j < n and s[j].isdigit():
                    j += 1
                if j < n and s[j] == '}':
                    tokens.append(('VAR', int(s[i + 1:j])))
                    i = j + 1
                    continue
                raise SyntaxError('bad {index}')
            if ch.isdigit() or ch == '.':
                j = i + 1
                while j < n and (s[j].isdigit() or s[j] == '.'):
                    j += 1
                tokens.append(('NUM', float(s[i:j])))
                i = j
                continue
            if ch == '&' and i + 1 < n and s[i + 1] == '&':
                tokens.append(('AND', '&&'))
                i += 2
                continue
            if ch == '|' and i + 1 < n and s[i + 1] == '|':
                tokens.append(('OR', '||'))
                i += 2
                continue
            if ch in '><=!':
                if i + 1 < n and s[i + 1] == '=':
                    tokens.append(('CMP', ch + '='))
                    i += 2
                    continue
                tokens.append(('CMP', ch))
                i += 1
                continue
            if ch in '()+-*/%!':
                tokens.append(('OP', ch))
                i += 1
                continue
            raise SyntaxError(f'bad char {ch!r}')
        return tokens

    # ---------- 递归下降 ----------
    def __parse(self, tokens: List[Tuple[str, Any]]):
        self.tokens = tokens
        self.pos = 0
        node = self.__expr()
        if self.pos != len(self.tokens):
            raise SyntaxError('extra token')
        return node

    def __expr(self):
        return self.__or_expr()

    def __or_expr(self):
        node = self.__and_expr()
        while self.__curtype() == 'OR':
            op = self.__consume('OR')[1]
            node = ('or', node, self.__and_expr())
        return node

    def __and_expr(self):
        node = self.__cmp_expr()
        while self.__curtype() == 'AND':
            op = self.__consume('AND')[1]
            node = ('and', node, self.__cmp_expr())
        return node

    def __cmp_expr(self):
        node = self.__add_expr()
        while self.__curtype() == 'CMP':
            op = self.__consume('CMP')[1]
            node = ('cmp', op, node, self.__add_expr())
        return node

    def __add_expr(self):
        node = self.__mul_expr()
        while self.__curtype() == 'OP' and self.tokens[self.pos][1] in '+-':
            op = self.__consume('OP')[1]
            node = ('bin', op, node, self.__mul_expr())
        return node

    def __mul_expr(self):
        node = self._unary_expr()
        while self.__curtype() == 'OP' and self.tokens[self.pos][1] in '*/%':
            op = self.__consume('OP')[1]
            node = ('bin', op, node, self._unary_expr())
        # print(node)
        return node

    def _unary_expr(self):
        if self.__curtype() == 'OP' and self.tokens[self.pos][1] in '!-':
            op = self.__consume('OP')[1]
            return ('una', op, self._unary_expr())
        if self.__curtype() == 'NUM':
            return ('num', self.__consume('NUM')[1])
        if self.__curtype() == 'VAR':
            return ('var', self.__consume('VAR')[1])
        if self.__curtype() == 'OP' and self.tokens[self.pos][1] == '(':
            self.__consume('OP')  # '('
            node = self.__expr()
            if not (self.__curtype() == 'OP' and self.tokens[self.pos][1] == ')'):
                raise SyntaxError('missing )')
            self.__consume('OP')
            return node
        raise SyntaxError('unexpected token')

    # ---------- 小工具 ----------
    def __curtype(self):
        return self.tokens[self.pos][0] if self.pos < len(self.tokens) else None

    def __consume(self, kind: str):
        if self.__curtype() != kind:
            raise SyntaxError(f'want {kind} got {self.__curtype()}')
        t = self.tokens[self.pos]
        self.pos += 1
        return t

    # ---------- 执行 ----------
    def __eval(self, node, ctx: List[float]):
        if node[0] == 'num':
            return node[1]
        if node[0] == 'var':
            idx = node[1]
            if idx >= len(ctx):
                raise IndexError(f'index {idx} out of range')
            return ctx[idx]
        if node[0] == 'una':
            op, v = node[1], self.__eval(node[2], ctx)
            if op == '!':
                return not v
            if op == '-':
                return -v
        if node[0] == 'bin':
            op, l, r = node[1], self.__eval(node[2], ctx), self.__eval(node[3], ctx)
            return {'+': l + r, '-': l - r, '*': l * r, '/': l / r, '%': l % r}[op]
        if node[0] == 'cmp':
            op, l, r = node[1], self.__eval(node[2], ctx), self.__eval(node[3], ctx)
            return {'==': l == r, '!=': l != r, '>': l > r, '<': l < r, '>=': l >= r, '<=': l <= r}[op]
        if node[0] == 'and':
            return self.__eval(node[1], ctx) and self.__eval(node[2], ctx)
        if node[0] == 'or':
            return self.__eval(node[1], ctx) or self.__eval(node[2], ctx)
        raise RuntimeError('unknown node')
