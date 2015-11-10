import logging
import argparse
import sys
import psycopg2

# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet, hide):
    """Store a snippet with an associated name."""
    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    
    try:
        with connection, connection.cursor() as cursor:
            command = "insert into snippets values (%s, %s, %s)"
            cursor.execute(command, (name, snippet, hide))
    except:
        with connection, connection.cursor() as cursor:
            command = "update snippets set message=%s, hidden=%s where keyword=%s"
            cursor.execute(command, (snippet, hide, name))
        
    logging.debug("Snippet stored successfully.")
    return name, snippet, hide
    
def get(name):
    """Query a snippet with the sepecified name"""
    logging.info("Querying snippet {!r}".format(name))
    
    with connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword=%s", (name,))
        row = cursor.fetchone()

    if not row:
        return "Error! snippet not found!"
    else:
        logging.info("Query {!r} successfully".format(name))
        return row[0]

def catalog():
    """Query all the keywords from snippets"""
    with connection.cursor() as cursor:
        cursor.execute("select keyword from snippets where not hidden order by keyword")
        rows = cursor.fetchall()
   
    if not rows:
       return "Empty table!"
    else:
        return rows

def search(string):
    """Query snippet which contains a given string"""
    with connection.cursor() as cursor:
        cursor.execute("select message from snippets where keyword like %s", (string,))
        rows = cursor.fetchall()
   
    if not rows:
       return "No snippet contains " + string
    else:
        return rows
        
def main():
    """Main function"""
    logging.info("Constructing parser")
    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    put_parser.add_argument("--hide", help="this snippet is hidden to user. Default value is false", action="store_true")
    
    logging.debug("Construct get subparser")
    get_parser = subparsers.add_parser('get', help='Query a snippet')
    get_parser.add_argument("name", help="The name of the snippet")
    
    logging.debug("Construct catalog subparser")
    catalog_parser = subparsers.add_parser('catalog', help='Get all the available keywords')

    logging.debug("Construct search subparser")
    search_parser = subparsers.add_parser('search', help='Search all snippets that contains a given string')
    search_parser.add_argument("string", help="A given string contained in the snippet")
    
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")
    
    if command == "put":
        name, snippet, hidden = put(**arguments)
        print("Stored {!r} as {!r}, hidden is {!r}".format(snippet, name, hidden))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))
    elif command == "catalog":
        snippets = catalog()
        print("Retrieved keywords {!r}".format(snippets))
    elif command == "search":
        snippets = search(**arguments)
        print("Retrieved snippets {!r}".format(snippets))
    
if __name__ == "__main__":
    logging.debug("Connecting to PostgreSQL")
    connection = psycopg2.connect("dbname='snippets'")
    logging.debug("Database connection established.")
    main()
    