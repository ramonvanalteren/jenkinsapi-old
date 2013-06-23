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


    def __enter__(self):
        """
        Start watching the job
        """

    def __exit__(self, type, value, traceback):
        """
        Finish watching the job - it will track which new queue items or builds have
        been created as a consequence of invoking the job.
        """

    def block(self, until='completed'):
        """
        Block this item until a condition is met.
        Setting until to 'running' blocks the item until it is running (i.e. it's no longer queued)
        """

    def stop(self):
        """
        Stop this item, whether it is on the queue or blocked.
        """

    def is_queued(self):
        """
        Returns True if this item is on the queue
        """

    def is_running(self):
        """
        Returns True if this item is executing now
        """

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
