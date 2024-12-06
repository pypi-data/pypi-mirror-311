import click
import os
import sys

import et_engine as et
engine = et.Engine()


def check_api_key():
    """check if the api key exists"""
    if "ET_ENGINE_API_KEY" not in os.environ:
        click.echo("Error: ET_ENGINE_API_KEY environment variable is not set.", err=True)
        sys.exit(1)


@click.group()
def batches():
    """Batches operations"""
    check_api_key()


@batches.command()
def list():
    """List all batches for the user"""
    try:
        batch_list = engine.batches.list_batches()
        for b in batch_list:
            click.echo(b)
    except PermissionError as e: #used to be AuthenticationError from et_engine.errors
        click.echo(f"Authentication Error: {str(e)}", err=True)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@batches.command()
def clear():
    """Deletes all batches for the user"""
    try:
        engine.batches.clear_batches()
        click.echo("Successfully cleared batches")
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)


@batches.command()
@click.argument('batch_id')
def delete(batch_id):
    """Deletes the batch without canceling any jobs [NOTE: This action cannot be un-done!]"""
    try:
        batch = engine.batches.connect(batch_id)
        if not click.confirm(f"Are you sure you want to delete Batch '{batch_id}'?"):
            click.echo("Aborted")
            return
        batch.delete()
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)

@batches.command()
@click.argument('batch_id')
def status(batch_id):
    """Summarizes the status of a Batch"""
    try:
        batch = engine.batches.connect(batch_id)
        status = batch.status()
        click.echo(status)
    except Exception as e:
        click.echo(f"Error: {str(e)}", err=True)