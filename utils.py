"""
Module containing utility functions.
"""

from graphviz import Digraph

def get_qualifier_subsequence(function_qualifier):
	"""
	Given a fully qualified function name, iterate over it and find the file
	in which the function is defined (this is the entry in the qualifier chain
	before the one that causes an import error)/
	"""

	# tokenise the qualifier string so we have names and symbols
	# the symbol used to separate two names tells us what the relationship is
	# a/b means a is a directory and b is contained within it
	# a.b means b is a member of a, so a is either a module or a class

	tokens = []
	last_position = 0
	for (n, character) in enumerate(list(function_qualifier)):
		if character in [".", "/"]:
			tokens.append(function_qualifier[last_position:n])
			tokens.append(function_qualifier[n])
			last_position = n + 1
		elif n == len(function_qualifier)-1:
			tokens.append(function_qualifier[last_position:])

	return tokens

def verdict_severity(obs):
    return obs.verdict_severity()


def write_scfg(scfg_object,file_name):
    graph = Digraph()
    graph.attr("graph", splines="true", fontsize="10")
    shape = "rectangle"
    for vertex in scfg_object.vertices:
        graph.node(str(id(vertex)), str(vertex._name_changed), shape=shape)
        for edge in vertex.edges:
            graph.edge(str(id(vertex)),	str(id(edge._target_state)),"%s - %s - path length = %s" % (str(edge._operates_on) if not(type(edge._operates_on[0]) is ast.Print) else "print stmt",edge._condition,str(edge._target_state._path_length)))
    graph.render(file_name)
    print("Writing SCFG to file '%s'." % file_name)