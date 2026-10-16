%{

#include "symbol_table.h"

#define YYSTYPE symbol_info*

extern FILE *yyin; 
int yyparse(void);
int yylex(void);

extern YYSTYPE yylval;

#define original_yylex yylex

static int (*real_yylex_ptr)(void) = yylex;


// create your symbol table here.
symbol_table* table;

// You can store the pointer to your symbol table in a global variable
// or you can create an object

string current_type;
string current_function_name = "";

vector<pair<string, string>> current_func_params;
bool error_found = false;

int lines = 1;
int error_count = 0;

ofstream outlog;
ofstream errorout;

// helper for to print the message

// you may declare other necessary variables here to store necessary info
// such as current variable type, variable list, function name, return type, function parameter types, parameters names etc.

void yyerror(char *s)
{
	outlog << "At line " << lines << " " << s << endl << endl;
	error_found = true;
}

bool is_function_declared(string name){
	symbol_info* temp = new symbol_info(name, "ID");
	symbol_info* found = table->lookup(temp);
	delete temp;
	return found != NULL && found->get_symbol_type() == "Function Definition";
}

bool variable_in_current_scope(string name){
    symbol_info* temp = new symbol_info(name, "ID");
    symbol_info* is_found = table->lookup_current_scope(temp);
    delete temp;
    return is_found != NULL;
}

void printSemanticError(string msg) {
    outlog << "At line no: " << lines << " " << msg << endl << endl;
    errorout << "At line no: " << lines << " " << msg << endl << endl;
    error_count++;
}

bool duplicate_param_name(string name)
{
    for(auto &p : current_func_params)
    {
        if(p.second == name && name != "") return true;
    }
    return false;
}

symbol_info* lookup_symbol_by_name(string name)
{
    symbol_info* temp = new symbol_info(name, "ID");
    symbol_info* found = table->lookup(temp);
    delete temp;
    return found;
}

void begin_function_definition(const string& name)
{
    current_function_name = name;
    current_func_params.clear();
}

void insert_current_function(const string& name, const string& return_type)
{
    symbol_info* prev = lookup_symbol_by_name(name);

    if(prev != NULL)
    {
        printSemanticError("Multiple declaration of function " + name);
        return;
    }

    vector<string> param_types;
    vector<string> param_names;

    for(const auto& param : current_func_params)
    {
        param_types.push_back(param.first);
        param_names.push_back(param.second);
    }

    symbol_info* func = new symbol_info(name, "ID");
    func->set_symbol_type("Function Definition");
    func->set_data_type(return_type);
    func->set_param_types(param_types);
    func->set_param_names(param_names);
    func->set_isFunction(true);
    func->set_isArray(false);
    table->insert(func);
}


%}

%token IF ELSE FOR WHILE DO BREAK INT CHAR FLOAT DOUBLE VOID RETURN SWITCH CASE DEFAULT CONTINUE PRINTLN ADDOP MULOP INCOP DECOP RELOP ASSIGNOP LOGICOP NOT LPAREN RPAREN LCURL RCURL LTHIRD RTHIRD COMMA SEMICOLON CONST_INT CONST_FLOAT ID

%nonassoc LOWER_THAN_ELSE
%nonassoc ELSE

%%

start : program
	{
		outlog<<"At line no: "<<lines<<" start : program "<<endl<<endl;
		outlog<<"Symbol Table"<<endl<<endl;

		// Print your whole symbol table here
		table->print_all_scopes(outlog);
	}
	;

program : program unit
	{
		outlog<<"At line no: "<<lines<<" program : program unit "<<endl<<endl;
		outlog<<$1->get_name()+"\n"+$2->get_name()<<endl<<endl;

		$$ = new symbol_info($1->get_name()+"\n"+$2->get_name(),"program");
	}
	| unit
	{
		outlog<<"At line no: "<<lines<<" program : unit "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;

		$$ = new symbol_info($1->get_name(),"program");
	}
	;

unit : var_declaration
	 {
		outlog<<"At line no: "<<lines<<" unit : var_declaration "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;

		$$ = new symbol_info($1->get_name(),"unit");
	 }
     | func_definition
     {
		outlog<<"At line no: "<<lines<<" unit : func_definition "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;

		$$ = new symbol_info($1->get_name(),"unit");
	 }
     ;

func_definition : type_specifier ID LPAREN
      {
          begin_function_definition($2->get_name());
      }
      parameter_list RPAREN
      {
          insert_current_function($2->get_name(), $1->get_name());
      }
      compound_statement
      {
          outlog << "At line no: " << lines << " func_definition : type_specifier ID LPAREN parameter_list RPAREN compound_statement " << endl << endl;
          outlog << $1->get_name() << " " << $2->get_name() << "(" << $5->get_name() << ")\n" << $8->get_name() << endl << endl;

          $$ = new symbol_info($1->get_name() + " " + $2->get_name() + "(" + $5->get_name() + ")\n" + $8->get_name(), "func_def");

          current_func_params.clear();
          current_function_name = "";
      }

    | type_specifier ID LPAREN RPAREN
      {
          begin_function_definition($2->get_name());
          insert_current_function($2->get_name(), $1->get_name());
      }
      compound_statement
      {
          outlog << "At line no: " << lines << " func_definition : type_specifier ID LPAREN RPAREN compound_statement " << endl << endl;
          outlog << $1->get_name() << " " << $2->get_name() << "()\n" << $6->get_name() << endl << endl;

          $$ = new symbol_info($1->get_name() + " " + $2->get_name() + "()\n" + $6->get_name(), "func_def");

          current_func_params.clear();
          current_function_name = "";
      }
    ;

parameter_list : parameter_list COMMA type_specifier ID
		{
			outlog<<"At line no: "<<lines<<" parameter_list : parameter_list COMMA type_specifier ID "<<endl<<endl;
			outlog<<$1->get_name()<<","<<$3->get_name()<<" "<<$4->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name()+","+$3->get_name()+" "+$4->get_name(),"param_list");

			if(duplicate_param_name($4->get_name()))
			{
				printSemanticError("Multiple declaration of variable " + $4->get_name() + " in parameter of " + current_function_name);
			}
			current_func_params.push_back({$3->get_name(), $4->get_name()});
		}
		| parameter_list COMMA type_specifier
		{
			outlog<<"At line no: "<<lines<<" parameter_list : parameter_list COMMA type_specifier "<<endl<<endl;
			outlog<<$1->get_name()<<","<<$3->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name()+","+$3->get_name(),"param_list");

            // store the necessary information about the function parameters
            // They will be needed when you want to enter the function into the symbol table
			current_func_params.push_back({$3->get_name(), ""});
		}
 		| type_specifier ID
 		{
			outlog<<"At line no: "<<lines<<" parameter_list : type_specifier ID "<<endl<<endl;
			outlog<<$1->get_name()<<" "<<$2->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name()+" "+$2->get_name(),"param_list");

			if(duplicate_param_name($2->get_name()))
			{
				printSemanticError("Multiple declaration of variable " + $2->get_name() + " in parameter of " + current_function_name);
			}
			current_func_params.push_back({$1->get_name(), $2->get_name()});
		}
		| type_specifier
		{
			outlog<<"At line no: "<<lines<<" parameter_list : type_specifier "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name(),"param_list");

        
			current_func_params.push_back({$1->get_name(), ""});
		}
 		;

compound_statement : LCURL {
		// Enter a new scope
		table->enter_scope();

		// If we're in a function definition, add parameters to current scope
		if(!current_func_params.empty()) {
			for(auto param : current_func_params) {
				if(!param.second.empty()) {
					symbol_info* param_symbol = new symbol_info(param.second, "ID");
					param_symbol->set_symbol_type("Variable");
					param_symbol->set_data_type(param.first);
					param_symbol->set_isArray(false);
					param_symbol->set_isFunction(false);
					table->insert(param_symbol);
				}
			}
		}
	} statements RCURL
	{
		outlog << "At line no: " << lines << " compound_statement : LCURL statements RCURL " << endl << endl;
		outlog << "{\n" + $3->get_name() + "\n}" << endl << endl;

		// Print current scope before exiting
		table->print_current_scope();

		// Exit the current scope
		table->exit_scope();

		$$ = new symbol_info("{\n" + $3->get_name() + "\n}", "comp_stmnt");
	}
	| LCURL {
		// Enter a new scope
		table->enter_scope();
	} RCURL
	{
		outlog << "At line no: " << lines << " compound_statement : LCURL RCURL " << endl << endl;
		outlog << "{\n}" << endl << endl;

		// Print current scope before exiting
		table->print_current_scope();

		// Exit the current scope
		table->exit_scope();

		$$ = new symbol_info("{\n}", "comp_stmnt");
	}
	;

var_declaration : type_specifier declaration_list SEMICOLON
		 {
			outlog<<"At line no: "<<lines<<" var_declaration : type_specifier declaration_list SEMICOLON "<<endl<<endl;
			outlog<<$1->get_name()<<" "<<$2->get_name()<<";"<<endl<<endl;

			$$ = new symbol_info($1->get_name()+" "+$2->get_name()+";","var_dec");

			// Insert necessary information about the variables in the symbol table
			current_type = $1->get_name();

			if(current_type == "void"){
				printSemanticError("variable type can not be void");
			}
		 }
 		 ;

type_specifier : INT
		{
			outlog<<"At line no: "<<lines<<" type_specifier : INT "<<endl<<endl;
			outlog<<"int"<<endl<<endl;

			$$ = new symbol_info("int","type");
			$$->set_data_type("int");
			current_type = "int";
	    }
 		| FLOAT
 		{
			outlog<<"At line no: "<<lines<<" type_specifier : FLOAT "<<endl<<endl;
			outlog<<"float"<<endl<<endl;

			$$ = new symbol_info("float","type");
			$$->set_data_type("float");
			current_type = "float";
	    }
 		| VOID
 		{
			outlog<<"At line no: "<<lines<<" type_specifier : VOID "<<endl<<endl;
			outlog<<"void"<<endl<<endl;

			$$ = new symbol_info("void","type");
			$$->set_data_type("void");
			current_type = "void";
	    }
 		;

declaration_list : declaration_list COMMA ID
		  {
 		  	outlog << "At line no: " << lines << " declaration_list : declaration_list COMMA ID " << endl << endl;
 		  	outlog << $1->get_name() + "," << $3->get_name() << endl << endl;
			$$ = new symbol_info($1->get_name() + "," + $3->get_name(), "decl_list");

            // check if variable already declared in current scope
            if(variable_in_current_scope($3->get_name())) {

                printSemanticError("Multiple declaration of variable " + $3->get_name());
            } 
			else
			{
				symbol_info* new_var = new symbol_info($3->get_name(), "ID");
				new_var->set_symbol_type("Variable");
				if(current_type == "void") new_var->set_data_type("error");
				else new_var->set_data_type(current_type);
				new_var->set_isArray(false);
				new_var->set_isFunction(false);
				table->insert(new_var);
			}
 		  }
 		  | declaration_list COMMA ID LTHIRD CONST_INT RTHIRD //array after some declaration
 		  {
 		  	outlog << "At line no: " << lines << " declaration_list : declaration_list COMMA ID LTHIRD CONST_INT RTHIRD " << endl << endl;
 		  	outlog << $1->get_name() + "," << $3->get_name() << "[" << $5->get_name() << "]" << endl << endl;
			$$ = new symbol_info($1->get_name() + "," + $3->get_name() + "[" + $5->get_name() + "]", "decl_list");

            // Check if array already declared in current scope
            if(variable_in_current_scope($3->get_name()))
			{
				printSemanticError("Multiple declaration of variable " + $3->get_name());
			}
			else
			{
				int size = stoi($5->get_name());
				symbol_info* new_array = new symbol_info($3->get_name(), "ID");
				new_array->set_symbol_type("Array");
				if(current_type == "void") new_array->set_data_type("error");
				else new_array->set_data_type(current_type);
				new_array->set_array_size(size);
				new_array->set_isArray(true);
				new_array->set_isFunction(false);
				table->insert(new_array);
			}
 		  }
 		  |ID
 		  {
			outlog << "At line no: " << lines << " declaration_list : ID " << endl << endl;
			outlog << $1->get_name() << endl << endl;

			$$ = new symbol_info($1->get_name(), "decl_list");

			if(variable_in_current_scope($1->get_name()))
			{
				printSemanticError("Multiple declaration of variable " + $1->get_name());
			}
			else
			{
				symbol_info* new_var = new symbol_info($1->get_name(), "ID");
				new_var->set_symbol_type("Variable");
				if(current_type == "void") new_var->set_data_type("error");
				else new_var->set_data_type(current_type);
				new_var->set_isArray(false);
				new_var->set_isFunction(false);
				table->insert(new_var);
			}
		}
 		| ID LTHIRD CONST_INT RTHIRD //array
 		  {
 		  	outlog << "At line no: " << lines << " declaration_list : ID LTHIRD CONST_INT RTHIRD " << endl << endl;
			outlog << $1->get_name() << "[" << $3->get_name() << "]" << endl << endl;
			$$ = new symbol_info($1->get_name() + "[" + $3->get_name() + "]", "decl_list");

            // Check if array already declared in current scope
            if(variable_in_current_scope($1->get_name()))
			{
				printSemanticError("Multiple declaration of variable " + $1->get_name());
			}
			else
			{
				int size = stoi($3->get_name());
				symbol_info* new_array = new symbol_info($1->get_name(), "ID");
				new_array->set_symbol_type("Array");
				if(current_type == "void") new_array->set_data_type("error");
				else new_array->set_data_type(current_type);
				new_array->set_array_size(size);
				new_array->set_isArray(true);
				new_array->set_isFunction(false);
				table->insert(new_array);
			}
 		  }
 		  ;


statements : statement
	   {
	    	outlog<<"At line no: "<<lines<<" statements : statement "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name(),"stmnts");
	   }
	   | statements statement
	   {
	    	outlog<<"At line no: "<<lines<<" statements : statements statement "<<endl<<endl;
			outlog<<$1->get_name()<<"\n"<<$2->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name()+"\n"+$2->get_name(),"stmnts");
	   }
	   ;

statement : var_declaration
	  {
	    	outlog<<"At line no: "<<lines<<" statement : var_declaration "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name(),"stmnt");
	  }
	  | func_definition
	  {
	  		outlog<<"At line no: "<<lines<<" statement : func_definition "<<endl<<endl;
            outlog<<$1->get_name()<<endl<<endl;

            $$ = new symbol_info($1->get_name(),"stmnt");

	  }
	  | expression_statement
	  {
	    	outlog<<"At line no: "<<lines<<" statement : expression_statement "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name(),"stmnt");
	  }
	  | compound_statement
	  {
	    	outlog<<"At line no: "<<lines<<" statement : compound_statement "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name(),"stmnt");
	  }
	  | FOR LPAREN expression_statement expression_statement expression RPAREN statement
	  {
	    	outlog<<"At line no: "<<lines<<" statement : FOR LPAREN expression_statement expression_statement expression RPAREN statement "<<endl<<endl;
			outlog<<"for("<<$3->get_name()<<$4->get_name()<<$5->get_name()<<")\n"<<$7->get_name()<<endl<<endl;

			$$ = new symbol_info("for("+$3->get_name()+$4->get_name()+$5->get_name()+")\n"+$7->get_name(),"stmnt");
	  }
	  | IF LPAREN expression RPAREN statement %prec LOWER_THAN_ELSE
	  {
	    	outlog<<"At line no: "<<lines<<" statement : IF LPAREN expression RPAREN statement "<<endl<<endl;
			outlog<<"if("<<$3->get_name()<<")\n"<<$5->get_name()<<endl<<endl;

			$$ = new symbol_info("if("+$3->get_name()+")\n"+$5->get_name(),"stmnt");
	  }
	  | IF LPAREN expression RPAREN statement ELSE statement
	  {
	    	outlog<<"At line no: "<<lines<<" statement : IF LPAREN expression RPAREN statement ELSE statement "<<endl<<endl;
			outlog<<"if("<<$3->get_name()<<")\n"<<$5->get_name()<<"\nelse\n"<<$7->get_name()<<endl<<endl;

			$$ = new symbol_info("if("+$3->get_name()+")\n"+$5->get_name()+"\nelse\n"+$7->get_name(),"stmnt");
	  }
	  | WHILE LPAREN expression RPAREN statement
	  {
	    	outlog<<"At line no: "<<lines<<" statement : WHILE LPAREN expression RPAREN statement "<<endl<<endl;
			outlog<<"while("<<$3->get_name()<<")\n"<<$5->get_name()<<endl<<endl;

			$$ = new symbol_info("while("+$3->get_name()+")\n"+$5->get_name(),"stmnt");
	  }
	  | PRINTLN LPAREN ID RPAREN SEMICOLON
	  {
	    	outlog<<"At line no: "<<lines<<" statement : PRINTLN LPAREN ID RPAREN SEMICOLON "<<endl<<endl;
			outlog<<"printf("<<$3->get_name()<<");"<<endl<<endl;
			symbol_info* found = lookup_symbol_by_name($3->get_name());
			if(found == NULL)
			{
				printSemanticError("Undeclared variable " + $3->get_name());
			}
			$$ = new symbol_info("printf("+$3->get_name()+");","stmnt");
	  }
	  | RETURN expression SEMICOLON
	  {
	    	outlog<<"At line no: "<<lines<<" statement : RETURN expression SEMICOLON "<<endl<<endl;
			outlog<<"return "<<$2->get_name()<<";"<<endl<<endl;

			$$ = new symbol_info("return "+$2->get_name()+";","stmnt");
	  }
	  ;

expression_statement : SEMICOLON
			{
				outlog<<"At line no: "<<lines<<" expression_statement : SEMICOLON "<<endl<<endl;
				outlog<<";"<<endl<<endl;

				$$ = new symbol_info(";","expr_stmt");
	        }
			| expression SEMICOLON
			{
				outlog<<"At line no: "<<lines<<" expression_statement : expression SEMICOLON "<<endl<<endl;
				outlog<<$1->get_name()<<";"<<endl<<endl;

				$$ = new symbol_info($1->get_name()+";","expr_stmt");
	        }
			;

variable : ID
      {
	  	outlog<<"At line no: "<<lines<<" variable : ID "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;

		$$ = new symbol_info($1->get_name(),"varbl");

		symbol_info* found = lookup_symbol_by_name($1->get_name());

		if(found == NULL)
		{
			printSemanticError("Undeclared variable " + $1->get_name());
			$$->set_data_type("error");
		}
		else
		{
			if(found->get_symbol_type() == "Array")
			{
				printSemanticError("variable is of array type : " + $1->get_name());
				$$->set_data_type("error");
				$$->set_isArray(true);
				$$->set_isFunction(false);
			}
			else
			{
				$$->set_data_type(found->get_data_type());
				$$->set_isArray(false);
				$$->set_isFunction(found->get_symbol_type() == "Function Definition");
			}
		}

	 }
	 | ID LTHIRD expression RTHIRD
	 {
		outlog<<"At line no: "<<lines<<" variable : ID LTHIRD expression RTHIRD "<<endl<<endl;
		outlog<<$1->get_name()<<"["<<$3->get_name()<<"]"<<endl<<endl;

		$$ = new symbol_info($1->get_name()+"["+$3->get_name()+"]","varbl");

		symbol_info* found = lookup_symbol_by_name($1->get_name());

		if(found == NULL)
		{
			printSemanticError("Undeclared variable " + $1->get_name());
			$$->set_data_type("error");
		}
		else
		{
			if(found->get_symbol_type() != "Array")
			{
					printSemanticError("variable is not of array type : " + $1->get_name());
				}
				if($3->get_data_type() != "int" && $3->get_data_type() != "error")
				{
					printSemanticError("array index is not of integer type : " + $1->get_name());
				}

				$$->set_data_type(found->get_data_type());
				$$->set_isArray(false);
				$$->set_isFunction(false);
			}
		}
	 ;

expression : logic_expression
	   {
	    	outlog<<"At line no: "<<lines<<" expression : logic_expression "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name(),"expr");
			$$->set_data_type($1->get_data_type());
			$$->set_isZero($1->get_isZero());
	   }
	   | variable ASSIGNOP logic_expression
	   {
	        outlog<<"At line no: "<<lines<<" expression : variable ASSIGNOP logic_expression "<<endl<<endl;
			outlog<<$1->get_name()<<"="<<$3->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name()+"="+$3->get_name(),"expr");
			$$->set_data_type($1->get_data_type());

			if($3->get_data_type() == "void")
			{
				printSemanticError("operation on void type");
			}

			if($1->get_data_type() == "int" && $3->get_data_type() == "float")
			{
				printSemanticError("Warning: Assignment of float value into variable of integer type");
			}
	   }
	   ;

logic_expression : rel_expression
	     {
	    	outlog<<"At line no: "<<lines<<" logic_expression : rel_expression "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name(),"lgc_expr");
			$$->set_data_type($1->get_data_type());
	     }
		 | rel_expression LOGICOP rel_expression
		 {
	    	outlog<<"At line no: "<<lines<<" logic_expression : rel_expression LOGICOP rel_expression "<<endl<<endl;
			outlog<<$1->get_name()<<$2->get_name()<<$3->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"lgc_expr");
			$$->set_data_type("int");
	     }
		 ;

rel_expression	: simple_expression
		{
	    	outlog<<"At line no: "<<lines<<" rel_expression : simple_expression "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name(),"rel_expr");
			$$->set_data_type($1->get_data_type());
			$$->set_isZero($1->get_isZero());
	    }
		| simple_expression RELOP simple_expression
		{
	    	outlog<<"At line no: "<<lines<<" rel_expression : simple_expression RELOP simple_expression "<<endl<<endl;
			outlog<<$1->get_name()<<$2->get_name()<<$3->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"rel_expr");
			$$->set_data_type("int");
	    }
		;

simple_expression : term
          {
	    	outlog<<"At line no: "<<lines<<" simple_expression : term "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name(),"simp_expr");
			$$->set_data_type($1->get_data_type());
			$$->set_isZero($1->get_isZero());

	      }
		  | simple_expression ADDOP term
		  {
	    	outlog<<"At line no: "<<lines<<" simple_expression : simple_expression ADDOP term "<<endl<<endl;
			outlog<<$1->get_name()<<$2->get_name()<<$3->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"simp_expr");
			if($1->get_data_type() == "void" || $3->get_data_type() == "void")
			{
				printSemanticError("operation on void type");
				$$->set_data_type("error");
			}
			else if($1->get_data_type() == "float" || $3->get_data_type() == "float")
			{
				$$->set_data_type("float");
			}
			else
			{
				$$->set_data_type("int");
			}
	      }
		  ;

term :	unary_expression //term can be void because of un_expr->factor
     {
	    	outlog<<"At line no: "<<lines<<" term : unary_expression "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name(),"term");
			$$->set_data_type($1->get_data_type());
			$$->set_isZero($1->get_isZero());

	 }
     |  term MULOP unary_expression
		{
			outlog<<"At line no: "<<lines<<" term : term MULOP unary_expression "<<endl<<endl;
			outlog<<$1->get_name()<<$2->get_name()<<$3->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name()+$2->get_name()+$3->get_name(),"term");

			string op = $2->get_name();

			if($1->get_data_type() == "void" || $3->get_data_type() == "void")
			{
				printSemanticError("operation on void type");
				$$->set_data_type("error");
			}
			else if(op == "%")
			{
				if($1->get_data_type() != "int" || $3->get_data_type() != "int")
				{
					printSemanticError("Modulus operator on non integer type");
				}
				if($3->get_isZero())
				{
					printSemanticError("Modulus by 0");
				}
				$$->set_data_type("int");
			}
			else
			{
				if(op == "/" && $3->get_isZero())
				{
					printSemanticError("Division by 0");
				}

				if($1->get_data_type() == "float" || $3->get_data_type() == "float")
					$$->set_data_type("float");
				else
					$$->set_data_type("int");
			}
		}
     ;

unary_expression : ADDOP unary_expression  // un_expr can be void because of factor
		 {
	    	outlog<<"At line no: "<<lines<<" unary_expression : ADDOP unary_expression "<<endl<<endl;
			outlog<<$1->get_name()<<$2->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name()+$2->get_name(),"un_expr");
			$$->set_data_type($2->get_data_type());
			$$->set_isZero($2->get_isZero());
	     }
		 | NOT unary_expression
		 {
	    	outlog<<"At line no: "<<lines<<" unary_expression : NOT unary_expression "<<endl<<endl;
			outlog<<"!"<<$2->get_name()<<endl<<endl;

			$$ = new symbol_info("!"+$2->get_name(),"un_expr");
			$$->set_data_type("int");
	     }
		 | factor
		 {
	    	outlog<<"At line no: "<<lines<<" unary_expression : factor "<<endl<<endl;
			outlog<<$1->get_name()<<endl<<endl;

			$$ = new symbol_info($1->get_name(),"un_expr");
			$$->set_data_type($1->get_data_type());
			$$->set_isZero($1->get_isZero());
	     }
		 ;

factor	: variable
    {
	    outlog<<"At line no: "<<lines<<" factor : variable "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;

		$$ = new symbol_info($1->get_name(),"fctr");
		$$->set_data_type($1->get_data_type());
		$$->set_isZero(false);
	}
	| ID LPAREN argument_list RPAREN
	{
		outlog<<"At line no: "<<lines<<" factor : ID LPAREN argument_list RPAREN "<<endl<<endl;
		outlog<<$1->get_name()<<"("<<$3->get_name()<<")"<<endl<<endl;

		$$ = new symbol_info($1->get_name()+"("+$3->get_name()+")","fctr");

		symbol_info* found = lookup_symbol_by_name($1->get_name());

		if(found == NULL)
		{
			printSemanticError("Undeclared function: " + $1->get_name());
			$$->set_data_type("error");
		}
		else if(found->get_symbol_type() != "Function Definition")
		{
			printSemanticError("Not a function: " + $1->get_name());
			$$->set_data_type("error");
		}
		else
		{
			vector<string> expected = found->get_param_types();
			vector<string> given = $3->get_arg_types();

			if(expected.size() != given.size())
			{
				printSemanticError("Inconsistencies in number of arguments in function call: " + $1->get_name());
			}
			else
			{
				for(int i = 0; i < (int)expected.size(); i++)
				{
					if(given[i] == "error") continue;
					if(expected[i] != given[i])
					{
						printSemanticError("argument " + to_string(i+1) + " type mismatch in function call: " + $1->get_name());
					}
				}
			}

			$$->set_data_type(found->get_data_type());
		}
	}
	| LPAREN expression RPAREN
	{
	   	outlog<<"At line no: "<<lines<<" factor : LPAREN expression RPAREN "<<endl<<endl;
		outlog<<"("<<$2->get_name()<<")"<<endl<<endl;

		$$ = new symbol_info("("+$2->get_name()+")","fctr");
		$$->set_data_type($2->get_data_type());
		$$->set_isZero($2->get_isZero());
	}
	| CONST_INT
	{
		outlog<<"At line no: "<<lines<<" factor : CONST_INT "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;

		$$ = new symbol_info($1->get_name(),"fctr");
		$$->set_data_type("int");

		if($1->get_name() == "0") $$->set_isZero(true);
		else $$->set_isZero(false);
	}
	| CONST_FLOAT
	{
		outlog<<"At line no: "<<lines<<" factor : CONST_FLOAT "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;

		$$ = new symbol_info($1->get_name(),"fctr");
		$$->set_data_type("float");

		try
		{
			$$->set_isZero(stod($1->get_name()) == 0.0);
		}
		catch(...)
		{
			$$->set_isZero(false);
		}
		}
	| variable INCOP
	{
	    outlog<<"At line no: "<<lines<<" factor : variable INCOP "<<endl<<endl;
		outlog<<$1->get_name()<<"++"<<endl<<endl;

		$$ = new symbol_info($1->get_name()+"++","fctr");
		$$->set_data_type($1->get_data_type());
		$$->set_isZero(false);
	}
	| variable DECOP
	{
	    outlog<<"At line no: "<<lines<<" factor : variable DECOP "<<endl<<endl;
		outlog<<$1->get_name()<<"--"<<endl<<endl;

		$$ = new symbol_info($1->get_name()+"--","fctr");
		$$->set_data_type($1->get_data_type());
		$$->set_isZero(false);
	}
	;

argument_list : arguments
	{
		outlog<<"At line no: "<<lines<<" argument_list : arguments "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;

		$$ = new symbol_info($1->get_name(),"arg_list");
		$$->set_arg_types($1->get_arg_types());
	}
	|
	{
		outlog<<"At line no: "<<lines<<" argument_list : "<<endl<<endl;
		outlog<<""<<endl<<endl;

		$$ = new symbol_info("","arg_list");
		$$->set_arg_types({});
	}
	;

arguments : arguments COMMA logic_expression
	{
		outlog<<"At line no: "<<lines<<" arguments : arguments COMMA logic_expression "<<endl<<endl;
		outlog<<$1->get_name()<<","<<$3->get_name()<<endl<<endl;

		$$ = new symbol_info($1->get_name()+","+$3->get_name(),"arg");
		vector<string> v = $1->get_arg_types();
		v.push_back($3->get_data_type());
		$$->set_arg_types(v);
	}
	| logic_expression
	{
		outlog<<"At line no: "<<lines<<" arguments : logic_expression "<<endl<<endl;
		outlog<<$1->get_name()<<endl<<endl;

		$$ = new symbol_info($1->get_name(),"arg");
		vector<string> v;
		v.push_back($1->get_data_type());
		$$->set_arg_types(v);
	}
	;


%%

int main(int argc, char *argv[])
{
    if(argc != 2)
    {
        cout<<"Please input file name"<<endl;
        return 0;
    }

    yyin = fopen(argv[1], "r");
    outlog.open("22301532_log.txt", ios::trunc);
    errorout.open("22301532_error.txt", ios::trunc);

    if(yyin == NULL)
    {
        cout<<"Couldn't open file"<<endl;
        return 0;
    }

    table = new symbol_table(10);

    yyparse();

    delete table;

    outlog << endl << "Total lines: " << lines << endl;
    outlog << "Total errors: " << error_count << endl;

    errorout << "Total errors: " << error_count << endl;

    outlog.close();
    errorout.close();
    fclose(yyin);

    return 0;
}

