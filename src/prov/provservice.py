import click
import multiprocessing
import gunicorn.app.base
from prov.app import init_api
from prov.utils.queue import init_celery
from prov.utils.messaging import broker
from celery.bin import worker
from gunicorn.six import iteritems


@click.group()
def cli():
    """Run cli tool."""
    pass


@cli.command('server')
@click.option('--host', default='127.0.0.1', help='provservice host.')
@click.option('--port', default=7030, help='provservice server port.')
@click.option('--workers', default=2, help='provservice server workers.')
@click.option('--log', default='logs/server.log', help='log file for app.')
def server(host, port, log, workers):
    """Run web server with options."""
    options = {
        'bind': '{0}:{1}'.format(host, port),
        'workers': workers,
        'daemon': 'True',
        'errorlog': log
    }
    PROVService(init_api(), options).run()


@cli.command('queue')
@click.option('--address', default='localhost', help='message broker host.')
@click.option('--user', help='message broker user.')
@click.option('--password', help='message broker password.')
def queue(user, password, address):
    """Task execution with options."""
    username = broker['user'] if user is None else user
    key = broker['pass'] if password is None else password
    host = broker['host'] if address is None else address

    test = worker.worker(app=init_celery(username, key, host))
    options = {
        'broker': 'amqp://{0}:{1}@{2}:5672//'.format(username, key, host),
        'loglevel': 'INFO',
        'traceback': True,
    }
    test.run(**options)


class PROVService(gunicorn.app.base.BaseApplication):
    """Create Standalone Application Provenance Service."""

    def __init__(self, app, options=None):
        """The init."""
        self.options = options or {}
        self.application = app
        super(PROVService, self).__init__()

    def load_config(self):
        """Load configuration."""
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        """Load configuration."""
        return self.application


# Unless really needed to scale use this function. Otherwise 2 workers suffice.
def number_of_workers():
    """Establish the numberb or workers based on cpu_count."""
    return (multiprocessing.cpu_count() * 2) + 1


def main():
    """Main function."""
    cli()


if __name__ == '__main__':
    main()
