import click

# Global list to simulate a database for now
_snippets = []
_next_id = 1

def init_db():
    """
    Initializes the database, creating necessary files and tables if they don't exist.
    This function should be called once when the CLI is first run or started.
    """
    # Placeholder for actual database initialization logic
    # In a real application, this would involve:
    # 1. Checking for the database file (e.g., SQLite .db file)
    # 2. Creating the database file if it doesn't exist
    # 3. Connecting to the database
    # 4. Running schema migrations or creating tables if they don't exist
    # For the in-memory store, this function does not need to perform any action
    # as the global list `_snippets` is initialized on module load.
    pass

def add_snippet(content: str, tags: str):
    global _snippets, _next_id
    """
    Adds a new code snippet to the database.
    """
    # Placeholder for actual database insertion logic
    # In a real application, this would involve:
    # 1. Connecting to the database
    # 2. Inserting the content and tags into a snippets table
    # 3. Handling potential errors (e.g., database write failure)
    # For now, append to an in-memory list
    snippet = {
        'id': _next_id,
        'content': content,
        'tags': tags
    }
    _snippets.append(snippet)
    _next_id += 1

def list_snippets():
    """
    Retrieves all stored code snippets from the database.
    Returns a list of dictionaries, each representing a snippet.
    """
    # Placeholder for actual database retrieval logic
    # In a real application, this would involve:
    # 1. Connecting to the database
    # 2. Querying all snippets from the snippets table
    # 3. Returning them as a list of dicts/objects
    # For now, return the in-memory list
    return _snippets

@click.group()
def cli():
    """
    snipcli is a command-line tool for managing code snippets.
    """
    init_db()
    pass

@cli.command('add')
@click.argument('content')
@click.option('--tags', '-t', default='', help='Comma-separated tags for the snippet.')
def add_command(content, tags):
    """
    Adds a new code snippet.

    CONTENT is the code snippet text.
    """
    add_snippet(content, tags)
    click.echo(f"Snippet added successfully. Content: '{content[:50]}...' Tags: '{tags}'")

@cli.command('list')
def list_command():
    """
    Lists all stored code snippets.
    """
    snippets = list_snippets()
    if not snippets:
        click.echo("No snippets found.")
        return

    click.echo("--- Stored Snippets ---")
    for snippet in snippets:
        click.echo(f"ID: {snippet['id']}")
        click.echo(f"  Tags: {snippet['tags'] if snippet['tags'] else 'None'}")
        # Indent multi-line content for better readability
        indented_content = "    " + snippet['content'].replace('\n', '\n    ')
        click.echo(f"  Content:\n{indented_content}")
        click.echo("-" * 25) # Separator for readability


if __name__ == '__main__':
    cli()