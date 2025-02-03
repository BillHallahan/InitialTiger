type pos = int
type lexresult = Tokens.token

val lineNum = ErrorMsg.lineNum
val linePos = ErrorMsg.linePos
fun err(p1,p2) = ErrorMsg.error p1

fun eof() = let val pos = hd(!linePos) in Tokens.EOF(pos, pos) end


%%
%structure TigerLexFun
%%
\n	    => (lineNum := !lineNum+1; linePos := yypos :: !linePos; continue());
var  	=> (Tokens.VAR(yypos, yypos + 3));
","	=> (Tokens.COMMA(yypos, yypos + 1));
"123"	=> (Tokens.INT(123, yypos, yypos + 3));
.       => (ErrorMsg.error yypos ("illegal character " ^ yytext); continue());
