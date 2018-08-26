package cli

var commands = map[string]Command{}

var aliases = map[string]string{}

func Register(name string, c Command) {
	commands[name] = c
}

func Alias(name string, alias string) {
	aliases[alias] = name
}

func Commands() map[string]Command {
	return commands
}
