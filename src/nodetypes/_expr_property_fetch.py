from utils.support import Print

'''
    Describes a scenario like below
    e.g. $something = $user->password;

    NOTE
    See "stmt_expression" for calls for these functions

    $user->password
    $user = expr['var']['name']
    password = expr['name']['name']
'''
def expr_property_fetch_rhs(self, expr, parent_node, parent_node_type, scope, relationship_type):
    # If it is not a "$this->variable"
    if expr['var']['nodeType'] == 'Expr_Variable' and expr['var']['name'] != 'this':
        # Create "$user->password"
        self.expr_property_fetch_lhs(expr, scope)

        # Create relationship "$something -[ASSIGNS]-> $password"
        if not self.graph.find_relationship(parent_node, parent_node_type, expr['name']['name'], '{scope}:PROPERTY'.format(scope=scope), relationship_type):
            self.graph.create_relationship(parent_node, parent_node_type, expr['name']['name'], '{scope}:PROPERTY'.format(scope=scope), relationship_type)
        else:
            Print.error_print('[404]', 'Node not found: {}'.format(expr['var']['name']))

'''
    Describes a scenario like below
    e.g. $user->password = something();

    Parent node     = $user ('VARIABLE') ('GLOBAL_VARIABLE') ('PARAM')
    Child node      = password ('PROPERTY')
    Relationship    = $user -['IS_PROPERTY']-> password

    1.) Search for "$user" in a "variable", "global variable" if not search for a function "parameter",
    it should be in one of those. If not it should be an error.
    2.) Once found, "password" is a property of "$user"
    3.) Search for "password" within the scope
        3.1.) If found then search for a relationship "$user -> IS_PROPERTY -> password"
        3.2.) If not found create the "password" node
        3.3.) And create the relationship "$user -> IS_PROPERTY -> password"
    4.) Once created, create the relationship "$something -> ASSIGNS -> password"
'''
def expr_property_fetch_lhs(self, var, scope):
    # If it is not a "$this->variable"
    if var['var']['nodeType'] == 'Expr_Variable' and var['var']['name'] != 'this':
        # Check "$user" in "$user->$password" in VARIABLEs
        if self.graph.find_node(var['var']['name'], '{scope}:VARIABLE'.format(scope=scope)):
            # Check "$password" in "$user->$password" in PROPERTYs
            if self.graph.find_node(var['name']['name'], '{scope}:PROPERTY'.format(scope=scope)):
                # FOUND
                # Check for "$user -[IS_PROPERTY]-> $password"
                if not self.graph.find_relationship(var['var']['name'], '{scope}:VARIABLE'.format(scope=scope), var['name']['name'], '{scope}:PROPERTY'.format(scope=scope), 'IS_PROPERTY'):
                    self.graph.create_relationship(var['var']['name'], '{scope}:VARIABLE'.format(scope=scope), var['name']['name'], '{scope}:PROPERTY'.format(scope=scope), 'IS_PROPERTY')
            else:
                # NOT FOUND
                # Create node
                self.graph.create_node(var['name']['name'], '{scope}:PROPERTY'.format(scope=scope))
                # Create relationship
                self.graph.create_relationship(var['var']['name'], '{scope}:VARIABLE'.format(scope=scope), var['name']['name'], '{scope}:PROPERTY'.format(scope=scope), 'IS_PROPERTY')

        # Check "$user" in "$user->$password" in GLOBAL_VARIABLEs
        elif self.graph.find_node(var['var']['name'], '{scope}:GLOBAL_VARIABLE'.format(scope=scope)):
            # Check "$password" in "$user->$password" in PROPERTYs
            if self.graph.find_node(var['name']['name'], '{scope}:PROPERTY'.format(scope=scope)):
                # FOUND
                # Check for "$user -[IS_PROPERTY]-> $password"
                if not self.graph.find_relationship(var['var']['name'], '{scope}:GLOBAL_VARIABLE'.format(scope=scope), var['name']['name'], '{scope}:PROPERTY'.format(scope=scope), 'IS_PROPERTY'):
                    self.graph.create_relationship(var['var']['name'], '{scope}:GLOBAL_VARIABLE'.format(scope=scope), var['name']['name'], '{scope}:PROPERTY'.format(scope=scope), 'IS_PROPERTY')
            else:
                # NOT FOUND
                # Create node
                self.graph.create_node(var['name']['name'], '{scope}:PROPERTY'.format(scope=scope))
                # Create relationship
                self.graph.create_relationship(var['var']['name'], '{scope}:GLOBAL_VARIABLE'.format(scope=scope), var['name']['name'], '{scope}:PROPERTY'.format(scope=scope), 'IS_PROPERTY')

        # Check "$user" in "$user->$password" in Function's parameters PARAMs
        elif self.graph.find_node(var['var']['name'], '{scope}:PARAM'.format(scope=scope)):
            # Check "$password" in "$user->$password" in PROPERTYs
            if self.graph.find_node(var['name']['name'], '{scope}:PROPERTY'.format(scope=scope)):
                # FOUND
                # Check for "$user -[IS_PROPERTY]-> $password"
                if not self.graph.find_relationship(var['var']['name'], '{scope}:PARAM'.format(scope=scope), var['name']['name'], '{scope}:PROPERTY'.format(scope=scope), 'IS_PROPERTY'):
                    self.graph.create_relationship(var['var']['name'], '{scope}:PARAM'.format(scope=scope), var['name']['name'], '{scope}:PROPERTY'.format(scope=scope), 'IS_PROPERTY')
            else:
                # NOT FOUND
                # Create node
                self.graph.create_node(var['name']['name'], '{scope}:PROPERTY'.format(scope=scope))
                # Create relationship
                self.graph.create_relationship(var['var']['name'], '{scope}:PARAM'.format(scope=scope), var['name']['name'], '{scope}:PROPERTY'.format(scope=scope), 'IS_PROPERTY')

        else:
            Print.error_print('[404]', 'Node not found: {}'.format(var['var']['name']))

