#include<bits/stdc++.h>
using namespace std;

class symbol_info
{
private:
    string name;
    string type;
    string *next; 


    // Write necessary attributes to store what type of symbol it is (variable/array/function)
    string symbol_type; 
    // Write necessary attributes to store the type/return type of the symbol (int/float/void/...)
    string d_type;
    // Write necessary attributes to store the parameters of a function
    vector<string> param_types;
    vector<string> param_names;
    // Write necessary attributes to store the array size if the symbol is an array
    int array_size;

    bool isFunction = false;
    bool isArray = false;
    bool isZero = false;
    vector<string> arg_types;

public:
    symbol_info(string name, string type, string symbol_type="", vector<string> param_types = vector<string>(), vector<string> param_names = vector<string>())
    {
        this->name = name;
        this->type = type;
        this->symbol_type = symbol_type;
        this->param_types = param_types;
        this->param_names = param_names;
        this->array_size = 0;
    }
    string get_name()
    {
        return name;
    }
    string get_type()
    {
        return type;
    }
    void set_name(string name)
    {
        this->name = name;
    }
    void set_type(string type)
    {
        this->type = type;
    }
    // Write necessary functions to set and get the attributes
    void set_symbol_type(string symbol_type)
    {
        this->symbol_type = symbol_type;
    }
    void set_data_type(string d_type)
    {
        this->d_type = d_type;
    }
    void set_param_types(const vector<string>& types) 
    { 
        param_types = types; 
    } 
    void set_param_names(const vector<string>& names) 
    { 
        param_names = names; 
    }
    void set_array_size(int size) 
    { 
        array_size = size; 
    }   
    void add_parameter(string type, string name)
    {
        param_types.push_back(type);
        param_names.push_back(name);
    }

    void set_isFunction(bool v){ 
        isFunction = v; 
    }
    bool get_isFunction(){ 
        return isFunction; 
    }

    void set_isArray(bool v){ 
        isArray = v; 
    }
    bool get_isArray(){ 
        return isArray; 
    }

    void set_isZero(bool v){ 
        isZero = v; 
    }
    bool get_isZero(){ 
        return isZero; 
    }

    void set_arg_types(vector<string> v){ 
        arg_types = v; 
    }
    vector<string> get_arg_types(){ 
        return arg_types; 
    }
    string get_symbol_type()
    { 
        return symbol_type; 
    }
    
    string get_data_type()
    {
        return d_type;
    }

    vector<string> get_param_types() 
    { 
        return param_types; 
    }

    vector<string> get_param_names() 
    { 
        return param_names; 
    }

    int get_array_size()
    { 
        return array_size; 
    }
    ~symbol_info()
    {
        // Write necessary code to deallocate memory, if necessary
        
    }
};