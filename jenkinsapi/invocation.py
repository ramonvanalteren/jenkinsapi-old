import time
from jenkinsapi.exceptions import UnknownQueueItem

class Invocation(object):
    """
    Represents the state and consequences of a single attempt to start a job.
    This class provides a context manager which is intended to watch the state of the job
    before and after the invoke. It will detect whether a process got queued, launched
    or whether nothing at all happened.

    An instance of this object will be returned by job.invoke()
    """

    def __init__(self, job):
        self.job = job
        self.initial_builds = None
        self.queue_item = None
        self.build_number = None


    def __enter__(self):
        """
        Start watching the job
        """
        self.job.poll()
        self.initial_builds = set(self.job.get_build_dict().keys())


    def __exit__(self, type, value, traceback):
        """
        Finish watching the job - it will track which new queue items or builds have
        been created as a consequence of invoking the job.
        """
        self.job.poll()
        newly_created_builds = set(self.job.get_build_dict().keys())
        if newly_created_builds:
            self.build_number = newly_created_builds.pop()
        else:
            try:
                self.queue_item = self.job.get_queue_item()
                self.build_number = self.job.get_next_build_number()
            except UnknownQueueItem:
                pass

    def get_build_number(self):
        """
        If this job is building or complete then provide it's build-number
        """
        return self.build_number

    def get_build(self):
        return self.job[self.get_build_number()]

    def block_until_not_queued(self):
        while True:
            if not self.is_queued():
                break
            time.sleep(0.5)


    def block(self, until='completed'):
        """
        Block this item until a condition is met.
        Setting until to 'running' blocks the item until it is running (i.e. it's no longer queued)
        """
        assert until in ['completed', 'not_queued'], 'Unknown block condition: %s' % until
        self.block_until_not_queued()
        if until=='completed':
            self.block_until_completed()

    def stop(self):
        """
        Stop this item, whether it is on the queue or blocked.
        """

    def is_queued(self):
        """
        Returns True if this item is on the queue
        """

        import ipdb
        ipdb.set_trace

        return True

    def is_running(self):
        """
        Returns True if this item is executing now
        """
        return True

    def is_queued_or_running(self):
        return self.is_queued() or self.is_running()

    def get_queue_item(self):
        """
        If the item is queued it will return that QueueItem, otherwise it will
        raise an exception.
        """

    def get_build(self):
        """
        If the item is building it will return a Build object, otherwise it will
        raise an exception.
        """
