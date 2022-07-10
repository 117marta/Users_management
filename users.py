import argparse

# Deklaracja argumentów (parametrów)
parser = argparse.ArgumentParser()
parser.add_argument('-u', '--username', help='username')
parser.add_argument('-p', '--pass', help='password (min. 5 characters)')
parser.add_argument('-n', '--new_pass', help='new password (min. 5 characters)')
parser.add_argument('-l', '--list', help='list of all users', action='store_true')  # czy parametr jest ustawiony
parser.add_argument('-d', '--delete', help='delete user', action='store_true')
parser.add_argument('-e', '--edit', help='edit user', action='store_true')

# Metoda z parsera, która sparsuje wymagane argumenty
args = parser.parse_args()
