use std::{
    fs,
    path::{Path, PathBuf},
};

use clap::Parser as ClapParser;
use codespan_reporting::{diagnostic::Diagnostic, term::Chars};
use codespan_reporting::term;
use codespan_reporting::{
    files::SimpleFiles,
    term::termcolor::{ColorChoice, StandardStream},
};
use linter::lint_file;
use linter::Function;

#[derive(ClapParser)]
struct Args {
    file: PathBuf,
    config: PathBuf,
}

fn funcs_from_conf(path: &Path) -> Function {
    let file_contents = fs::read_to_string(path).unwrap();
    let mut tree = Function::default();

    for line in file_contents.lines() { 
        if line.starts_with("#") {
            continue;
        }

        let tokens = line.split_whitespace().collect::<Vec<_>>();
        let len = tokens.len();
        if len < 3 {
            continue;
        }

        let max_args = tokens[len - 1].parse::<usize>().unwrap();
        let min_args = tokens[len - 2].parse::<usize>().unwrap();

        tree.insert(&tokens[0..len - 2], min_args, max_args)
    }

    tree
}

fn main() {
    let args = Args::parse();
    let file_contents = &fs::read(&args.file).unwrap();
    let data = String::from_utf8_lossy(&file_contents).clone();
    let funcs = funcs_from_conf(&args.config);

    let mut files = SimpleFiles::new();
    let file_id = files.add(args.file.to_str().unwrap(), &data);

    let tokens = lexer::lex(&data);
    let (ast, diagnostics) = parser::parse(&tokens);

    let writer = StandardStream::stderr(ColorChoice::Auto);
    let config = codespan_reporting::term::Config {
        chars: Chars::ascii(),
        ..Default::default()
    };

    for diag in diagnostics {
        let _ = term::emit(
            &mut writer.lock(),
            &config,
            &files,
            &diag.to_codespan(file_id),
        );
    }

    for diag in preproc_linter::lint_preprocs(&tokens) {
        let _ = term::emit(
            &mut writer.lock(),
            &config,
            &files,
            &diag.to_codespan(file_id),
        );
    }

    let Ok(ast) = ast else { return };

    for diag in lint_file(&ast, &funcs) {
        let _ = term::emit(
            &mut writer.lock(),
            &config,
            &files,
            &diag.to_codespan(file_id),
        );
    }
}

pub trait Lint {
    fn to_codespan(&self, id: usize) -> Diagnostic<usize>;
}

pub mod preproc_linter {
    use std::ops::Range;

    use codespan_reporting::diagnostic::Diagnostic;
    use codespan_reporting::diagnostic::Label;

    use crate::lexer::Token;
    use crate::lexer::TokenKind;
    use crate::Lint;

    pub enum PreProcLint {
        Unmatched(Range<usize>),
        Extra(Range<usize>),
    }

    impl Lint for PreProcLint {
        fn to_codespan(&self, id: usize) -> Diagnostic<usize> {
            match self {
                Self::Unmatched(s) => Diagnostic::error()
                    .with_message("unmatched preprocessing directive")
                    .with_labels(vec![Label::primary(id, s.clone())]),
                Self::Extra(s) => Diagnostic::error()
                    .with_message("extraneous preprocessing directive")
                    .with_labels(vec![Label::primary(id, s.clone())]),
            }
        }
    }

    pub fn lint_preprocs(tokens: &[Token]) -> Vec<PreProcLint> {
        let mut directive_stack: Vec<(Range<usize>, bool)> = Vec::new();
        let mut lints = Vec::new();

        for token in tokens {
            match token.kind {
                TokenKind::IfNDef => {
                    directive_stack.push((token.span.clone(), false));
                }
                TokenKind::IfDef => {
                    directive_stack.push((token.span.clone(), false));
                }
                TokenKind::Else => {
                    if let Some(entry) = directive_stack.pop() {
                        if entry.1 {
                            lints.push(PreProcLint::Extra(token.span.clone()))
                        }
                        directive_stack.push((token.span.clone(), true));
                    } else {
                        lints.push(PreProcLint::Extra(token.span.clone()))
                    }
                }
                TokenKind::EndIf => {
                    if directive_stack.pop().is_none() {
                        lints.push(PreProcLint::Extra(token.span.clone()))
                    }
                }
                _ => (),
            }
        }

        lints.append(
            &mut directive_stack
                .into_iter()
                .map(|x| PreProcLint::Unmatched(x.0))
                .collect::<Vec<_>>(),
        );
        lints
    }
}

pub mod lexer {
    use std::ops::Range;

    use derive_more::{IsVariant, Unwrap};
    use logos::{Lexer, Logos};

    #[derive(Logos, Debug, PartialEq, IsVariant, Unwrap, Clone)]
    pub enum TokenKind {
        #[token("kDataUnhandled")]
        Unhandled,
        #[token("#ifdef")]
        IfDef,
        #[token("#else")]
        Else,
        #[token("#endif")]
        EndIf,
        #[token("(")]
        LParen,
        #[token(")")]
        RParen,
        #[token("{")]
        LBrace,
        #[token("}")]
        RBrace,
        #[token("[")]
        LBracket,
        #[token("]")]
        RBracket,
        #[token("#define")]
        Define,
        #[token("#include")]
        Include,
        #[token("#merge")]
        Merge,
        #[token("#ifndef")]
        IfNDef,
        #[token("#autorun")]
        Autorun,
        #[token("#undef")]
        UnDef,
        #[regex(r#"[\-\+]?[0-9]+"#, |lex| lex.slice().parse().ok(), priority=2)]
        Int(i32),
        #[regex(r#"[\-\+]?[0-9]+\.[0-9]+"#, |lex| lex.slice().parse().ok(), priority=2)]
        Float(f32),
        #[regex(r#"\$[0-9a-zA-Z_]+"#, |lex| lex.slice().parse().ok())]
        Var(String),
        #[regex(r#"[^ \t\n\r\f\(\[\{\}\]\)]+"#, |lex| lex.slice().parse().ok())]
        #[regex(r#"'(?:\.|[^'])+'"#, trim_delimiters)]
        Sym(String),
        #[regex(r#""(?:\.|[^"])+""#, trim_delimiters)]
        String(String),
        #[regex(r"(;[^\n]*|[ \t\s\f\n\r])", priority = 2, callback = logos::skip)]
        Invalid,
        EOF,
    }

    fn trim_delimiters(lex: &mut Lexer<TokenKind>) -> Option<String> {
        let slice = lex.slice();
        let len = slice.len();
        slice[1..len - 1].parse().ok()
    }

    #[derive(Debug, Clone)]
    pub struct Token {
        pub kind: TokenKind,
        pub span: Range<usize>,
    }

    pub fn lex(data: &str) -> Vec<Token> {
        let mut tokens: Vec<_> = TokenKind::lexer(&data)
            .spanned()
            .map(|(tok, span)| match tok {
                Ok(tok) => Token { kind: tok, span },
                Err(_) => Token {
                    kind: TokenKind::Invalid,
                    span,
                },
            })
            .collect();

        if tokens.len() == 0 {
            tokens.push(Token {
                kind: TokenKind::EOF,
                span: 0..0,
            })
        } else {
            let last = tokens.last().unwrap().span.end;
            tokens.push(Token {
                kind: TokenKind::EOF,
                span: last..last,
            })
        }

        tokens
    }
}

pub mod linter {
    use std::collections::HashMap;
    use std::ops::Range;

    use codespan_reporting::diagnostic::Diagnostic;
    use codespan_reporting::diagnostic::Label;

    use crate::parser::Node;
    use crate::parser::NodeKind;
    use crate::Lint;

    pub fn lint_file(ast: &[Node], funcs: &Function) -> Vec<Box<dyn Lint>> {
        let mut lints = Vec::new();
        lint_node(&mut lints, &ast, funcs);
        lints
    }

    fn lint_node(lints: &mut Vec<Box<dyn Lint>>, ast: &[Node], funcs: &Function) {
        fn is_preproc_directive(tok: &Node) -> bool {
            tok.kind.is_if_def()
                || tok.kind.is_else()
                || tok.kind.is_end_if()
                || tok.kind.is_define()
                || tok.kind.is_include()
                || tok.kind.is_merge()
                || tok.kind.is_if_n_def()
                || tok.kind.is_autorun()
                || tok.kind.is_undef()
        }

        for node in ast {
            match &node.kind {
                NodeKind::Array(array) => lint_node(lints, array, funcs),
                NodeKind::Stmt(array) => {
                    lint_node(lints, array, funcs);

                    let has_preprocessor_directive = array
                        .iter()
                        .fold(false, |curr, tok| curr || is_preproc_directive(tok));

                    if !has_preprocessor_directive {
                        lint_fn_args(lints, array, node.span.clone(), funcs);
                    }
                }
                NodeKind::Prop(array) => lint_node(lints, array, funcs),
                NodeKind::Define(_, array) => lint_node(lints, array, funcs),
                _ => (),
            }
        }
    }

    enum FunctionArgLint {
        TooManyArgs(String, Range<usize>),
        NotEnoughArgs(String, Range<usize>),
    }

    impl Lint for FunctionArgLint {
        fn to_codespan(&self, id: usize) -> Diagnostic<usize> {
            match self {
                Self::TooManyArgs(name, range) => Diagnostic::error()
                    .with_message(format!("calling `{name}` with too many arguments"))
                    .with_labels(vec![
                        Label::primary(id, range.clone()).with_message("too many arguments")
                    ]),
                Self::NotEnoughArgs(name, range) => Diagnostic::error()
                    .with_message(format!("calling `{name}` with too few arguments"))
                    .with_labels(vec![
                        Label::primary(id, range.clone()).with_message("not enough arguments")
                    ]),
            }
        }
    }

    pub struct Function {
        pub min_args: usize,
        pub max_args: usize,
        pub children: HashMap<String, Function>,
    }

    impl Default for Function {
        fn default() -> Self {
            Self {
                min_args: 0,
                max_args: usize::MAX,
                children: HashMap::default(),
            }
        }
    }

    impl Function {
        pub fn lookup(&self, stmt: &[Node]) -> (&Function, usize) {
            self.lookup_inner(stmt, 0)
        }

        fn lookup_inner(&self, stmt: &[Node], depth: usize) -> (&Function, usize) {
            if self.children.is_empty() {
                return (self, depth);
            };

            let Some(node) = stmt.first() else {
                return (self, depth);
            };

            let NodeKind::Symbol(ref sym) = node.kind else {
                return (self, depth);
            };

            let Some(func) = self.children.get(sym) else {
                return (self, depth);
            };

            func.lookup_inner(&stmt[1..], depth + 1)
        }

        pub fn insert(&mut self, path: &[&str], min_args: usize, max_args: usize) {
            if path.is_empty() {
                self.min_args = min_args;
                self.max_args = max_args;
                return;
            }

            if let Some(child) = self.children.get_mut(path[0]) {
                child.insert(&path[1..], min_args, max_args);
            } else {
                let mut child = Function::default();
                child.insert(&path[1..], min_args, max_args);
                self.children.insert(path[0].to_string(), child);
            }
        }
    }

    fn lint_fn_args(
        lints: &mut Vec<Box<dyn Lint>>,
        stmt: &[Node],
        span: Range<usize>,
        funcs: &Function,
    ) {
        let (func, depth) = funcs.lookup(stmt);
        let name = generate_function_name(&stmt[..depth]);
        if stmt.len() > func.max_args + depth {
            lints.push(Box::new(FunctionArgLint::TooManyArgs(name, span)))
        } else if stmt.len() < func.min_args + depth {
            lints.push(Box::new(FunctionArgLint::NotEnoughArgs(name, span)))
        }
    }

    fn generate_function_name(stmt: &[Node]) -> String {
        let list: Vec<&str> = stmt
            .iter()
            .map(|x| match &x.kind {
                NodeKind::Symbol(sym) => Some(sym),
                _ => None,
            })
            .take_while(|x| x.is_some())
            .map(|x| x.unwrap().as_str())
            .collect();

        list.join(" ")
    }
}

pub mod parser {
    use derive_more::IsVariant;
    use derive_more::Unwrap;
    use std::ops::Range;

    use codespan_reporting::diagnostic::{Diagnostic, Label};

    use crate::lexer::Token;
    use crate::lexer::TokenKind;

    use crate::Lint;

    #[derive(Default)]
    struct Parser<'a> {
        cursor: usize,
        brace_stack: Vec<Token>,
        tokens: &'a [Token],
        diagnostics: Vec<ParseLint>,
    }

    #[derive(Debug)]
    pub enum ParseLint {
        UnmatchedBrace(Range<usize>, Range<usize>),
        GenericError(Range<usize>),
    }

    impl Lint for ParseLint {
        fn to_codespan(&self, id: usize) -> Diagnostic<usize> {
            match self {
                Self::UnmatchedBrace(opening, closing) => Diagnostic::error()
                    .with_message("unmatched delimiter")
                    .with_labels(vec![
                        Label::primary(id, closing.clone()).with_message("unexpected token"),
                        Label::primary(id, opening.clone()).with_message("unmatched delimiter"),
                    ]),
                Self::GenericError(span) => Diagnostic::error()
                    .with_message("unexpected token")
                    .with_labels(vec![
                        Label::primary(id, span.clone()).with_message("unexpected token")
                    ]),
            }
        }
    }

    type ParseResult<T> = Result<T, ParseLint>;

    impl<'a> Parser<'a> {
        fn new(tokens: &'a [Token]) -> Self {
            Self {
                tokens,
                ..Default::default()
            }
        }

        fn bump(&mut self, amount: usize) {
            self.cursor += amount;
        }

        fn lookahead(&self, amount: usize) -> Token {
            self.tokens[self.cursor + amount].clone()
        }

        fn previous(&self) -> Token {
            self.tokens[self.cursor - 1].clone()
        }

        fn eat(&mut self, f: fn(&TokenKind) -> bool) -> ParseResult<Token> {
            let token = self.lookahead(0);

            if f(&token.kind) {
                self.bump(1);
                Ok(token)
            } else {
                Err(ParseLint::GenericError(token.span))
            }
        }

        fn eat_open_brace(&mut self, f: fn(&TokenKind) -> bool) -> ParseResult<Token> {
            let token = self.lookahead(0);

            if f(&token.kind) {
                self.brace_stack.push(token.clone());
                self.bump(1);
                Ok(token)
            } else {
                Err(ParseLint::GenericError(token.span))
            }
        }

        fn eat_if(&mut self, f: fn(&TokenKind) -> bool) -> bool {
            let token = self.lookahead(0);

            if f(&token.kind) {
                self.bump(1);
                true
            } else {
                false
            }
        }

        fn eat_if_open_brace(&mut self, f: fn(&TokenKind) -> bool) -> bool {
            let token = self.lookahead(0);

            if f(&token.kind) {
                self.brace_stack.push(token.clone());
                self.bump(1);
                true
            } else {
                false
            }
        }

        #[allow(clippy::if_same_then_else)]
        fn parse_node(&mut self) -> ParseResult<Node> {
            if self.eat_if(TokenKind::is_int) {
                Ok(Node::from(self.previous()))
            } else if self.eat_if(TokenKind::is_float) {
                Ok(Node::from(self.previous()))
            } else if self.eat_if(TokenKind::is_var) {
                Ok(Node::from(self.previous()))
            } else if self.eat_if(TokenKind::is_sym) {
                Ok(Node::from(self.previous()))
            } else if self.eat_if(TokenKind::is_unhandled) {
                Ok(Node::from(self.previous()))
            } else if self.eat_if(TokenKind::is_if_def) {
                let span = self.previous().span;
                let sym = self.eat(TokenKind::is_sym)?;
                Ok(Node::new_ifdef(span, sym))
            } else if self.eat_if(TokenKind::is_else) {
                Ok(Node::from(self.previous()))
            } else if self.eat_if(TokenKind::is_end_if) {
                Ok(Node::from(self.previous()))
            } else if self.eat_if_open_brace(TokenKind::is_l_paren) {
                let lower_span = self.previous().span;
                let array = self.parse_list(TokenKind::is_r_paren)?;
                let upper_span = self.previous().span;
                Ok(Node::new_array(array, lower_span.start..upper_span.end))
            } else if self.eat_if_open_brace(TokenKind::is_l_bracket) {
                let lower_span = self.previous().span;
                let array = self.parse_list(TokenKind::is_r_bracket)?;
                let upper_span = self.previous().span;
                Ok(Node::new_prop(array, lower_span.start..upper_span.end))
            } else if self.eat_if(TokenKind::is_string) {
                Ok(Node::from(self.previous()))
            } else if self.eat_if_open_brace(TokenKind::is_l_brace) {
                let lower_span = self.previous().span;
                let array = self.parse_list(TokenKind::is_r_brace)?;
                let upper_span = self.previous().span;
                Ok(Node::new_stmt(array, lower_span.start..upper_span.end))
            } else if self.eat_if(TokenKind::is_define) {
                let span = self.previous().span;
                let sym = self.eat(TokenKind::is_sym)?;
                self.eat_open_brace(TokenKind::is_l_paren)?;
                let array = self.parse_list(TokenKind::is_r_paren)?;
                Ok(Node::new_define(span, sym, array))
            } else if self.eat_if(TokenKind::is_include) {
                let span = self.previous().span;
                let sym = self.eat(TokenKind::is_sym)?;
                Ok(Node::new_include(span, sym))
            } else if self.eat_if(TokenKind::is_merge) {
                let span = self.previous().span;
                let sym = self.eat(TokenKind::is_sym)?;
                Ok(Node::new_merge(span, sym))
            } else if self.eat_if(TokenKind::is_if_n_def) {
                let span = self.previous().span;
                let sym = self.eat(TokenKind::is_sym)?;
                Ok(Node::new_ifndef(span, sym))
            } else if self.eat_if(TokenKind::is_autorun) {
                Ok(Node::from(self.previous()))
            } else if self.eat_if(TokenKind::is_un_def) {
                let span = self.previous().span;
                let sym = self.eat(TokenKind::is_sym)?;
                Ok(Node::new_undef(span, sym))
            } else {
                Err(ParseLint::GenericError(self.lookahead(0).span))
            }
        }

        fn parse_list(&mut self, stop: fn(&TokenKind) -> bool) -> ParseResult<Vec<Node>> {
            let mut nodes = Vec::new();
            loop {
                if self.eat_if(stop) {
                    if self.previous().kind != TokenKind::EOF {
                        self.brace_stack.pop().unwrap();
                    }
                    break;
                }
                match self.parse_node() {
                    Ok(x) => nodes.push(x),
                    Err(e) => {
                        if !self.brace_stack.is_empty() {
                            let token = self.lookahead(0);
                            let unmatched = self.brace_stack.last().unwrap().span.clone();
                            let current = token.span.clone();
                            let diag = ParseLint::UnmatchedBrace(unmatched, current);

                            if token.kind.is_r_bracket()
                                || token.kind.is_r_paren()
                                || token.kind.is_r_brace()
                            {
                                self.diagnostics.push(diag);
                                self.bump(1);
                                self.brace_stack.pop().unwrap();
                                break;
                            }

                            if token.kind.is_eof() {
                                self.diagnostics.push(diag);
                                self.brace_stack.pop().unwrap();
                                break;
                            }
                        }

                        return Err(e);
                    }
                }
            }
            Ok(nodes)
        }
    }

    pub fn parse(tokens: &[Token]) -> (Result<Vec<Node>, ()>, Vec<ParseLint>) {
        let mut parser = Parser::new(tokens);
        let parse_result = parser.parse_list(TokenKind::is_eof);
        let mut diagnostics = parser.diagnostics;

        let res = match parse_result {
            Ok(r) => Ok(r),
            Err(e) => {
                diagnostics.push(e);
                Err(())
            }
        };

        (res, diagnostics)
    }

    #[derive(Debug, IsVariant, Unwrap)]
    pub enum NodeKind {
        Int(i32),
        Float(f32),
        Var(String),
        Symbol(String),
        Unhandled,
        IfDef(String),
        Else,
        EndIf,
        Array(Vec<Node>),
        Stmt(Vec<Node>),
        String(String),
        Prop(Vec<Node>),
        Define(String, Vec<Node>),
        Include(String),
        Merge(String),
        IfNDef(String),
        Autorun,
        Undef(String),
    }

    #[derive(Debug)]
    #[allow(unused)]
    pub struct Node {
        pub kind: NodeKind,
        pub span: Range<usize>,
    }

    #[allow(clippy::reversed_empty_ranges)]
    fn combine_node_spans(list: &[Node]) -> Range<usize> {
        list.iter()
            .map(|x| &x.span)
            .fold(usize::MAX..0, |current, next| {
                let start = current.start.min(next.start);
                let end = current.end.max(next.end);
                start..end
            })
    }

    impl Node {
        fn new_array(list: Vec<Node>, span: Range<usize>) -> Node {
            Node {
                kind: NodeKind::Array(list),
                span,
            }
        }

        fn new_stmt(list: Vec<Node>, span: Range<usize>) -> Node {
            Node {
                kind: NodeKind::Stmt(list),
                span,
            }
        }

        fn new_prop(list: Vec<Node>, span: Range<usize>) -> Node {
            Node {
                kind: NodeKind::Prop(list),
                span,
            }
        }

        fn new_define(span: Range<usize>, sym: Token, array: Vec<Node>) -> Node {
            let vec_span = combine_node_spans(&array);
            let span = span.start..vec_span.end.min(sym.span.end);
            Node {
                kind: NodeKind::Define(sym.kind.unwrap_sym(), array),
                span,
            }
        }

        fn new_ifdef(span: Range<usize>, sym: Token) -> Node {
            let span = span.start..sym.span.end;
            Node {
                kind: NodeKind::IfDef(sym.kind.unwrap_sym()),
                span,
            }
        }
        fn new_ifndef(span: Range<usize>, sym: Token) -> Node {
            let span = span.start..sym.span.end;
            Node {
                kind: NodeKind::IfNDef(sym.kind.unwrap_sym()),
                span,
            }
        }
        fn new_include(span: Range<usize>, sym: Token) -> Node {
            let span = span.start..sym.span.end;
            Node {
                kind: NodeKind::Include(sym.kind.unwrap_sym()),
                span,
            }
        }
        fn new_merge(span: Range<usize>, sym: Token) -> Node {
            let span = span.start..sym.span.end;
            Node {
                kind: NodeKind::Merge(sym.kind.unwrap_sym()),
                span,
            }
        }
        fn new_undef(span: Range<usize>, sym: Token) -> Node {
            let span = span.start..sym.span.end;
            Node {
                kind: NodeKind::Undef(sym.kind.unwrap_sym()),
                span,
            }
        }
    }

    impl From<Token> for Node {
        fn from(value: Token) -> Self {
            match value.kind {
                TokenKind::Sym(s) => Node {
                    kind: NodeKind::Symbol(s),
                    span: value.span,
                },
                TokenKind::Int(s) => Node {
                    kind: NodeKind::Int(s),
                    span: value.span,
                },
                TokenKind::Float(s) => Node {
                    kind: NodeKind::Float(s),
                    span: value.span,
                },
                TokenKind::String(s) => Node {
                    kind: NodeKind::String(s),
                    span: value.span,
                },
                TokenKind::Var(s) => Node {
                    kind: NodeKind::Var(s),
                    span: value.span,
                },
                TokenKind::Else => Node {
                    kind: NodeKind::Else,
                    span: value.span,
                },
                TokenKind::EndIf => Node {
                    kind: NodeKind::EndIf,
                    span: value.span,
                },
                TokenKind::Unhandled => Node {
                    kind: NodeKind::Unhandled,
                    span: value.span,
                },
                TokenKind::Autorun => Node {
                    kind: NodeKind::Autorun,
                    span: value.span,
                },
                _ => unreachable!(),
            }
        }
    }
}