from __future__ import absolute_import

from celery import shared_task
from celery.utils.log import get_task_logger
from eulfedora.rdfns import relsext as relsextns

from keep.arrangement.models import ArrangementObject
from keep.collection.models import SimpleCollection
from keep.common.fedora import Repository

from eulcommon.djangoextras.taskresult.models import TaskResult

logger = get_task_logger(__name__)


@shared_task
def batch_set_status(pid, status):
    repo = Repository()
    batch = repo.get_object(pid, type=SimpleCollection)
    # keep track of totals for success and failure
    success = 0
    error = 0

    # translate form status codes to fedora state code
    # TODO: shift this logic to arrangement object for re-use ?
    codes = {'Processed': 'A', 'Accessioned': 'I'}

    # target state for every object in the collection
    if status not in codes:
        err_msg = 'Status %s unknown' % status
        logger.error(err_msg)
        raise Exception(err_msg)
    else:
        state = codes[status]

    # finp all pids associated with this object
    pids = list(batch.rels_ext.content.objects(batch.uriref, relsextns.hasMember))

    for pid in pids:
        try:
            # pass in api from batch object to retain user credentials
            obj = ArrangementObject(batch.api, pid)
            obj.state = state
            obj.save('Marking as %s via SimpleCollection %s'
                     % (status, batch.pid))
            success += 1
        except Exception as e:
            logger.error('Failed to update %s : %s' % (pid, e))
            error += 1

    info = {
        'success': success,
        'error': error,
        'success_plural': '' if success == 1 else 's',
        'error_plural': '' if error == 1 else 's',
        'status': status
    }

    summary_msg = "Successfully updated %(success)s item%(success_plural)s; error updating %(error)s" % info

    # if not all objects were updated correctly, exit with error
    if error > 0:
        raise Exception(summary_msg)

    # FIXME: this is based on the current form logic, but could leave
    # some member items stranded in a different status than the parent object

    batch.mods.content.create_restrictions_on_access()
    batch.mods.content.restrictions_on_access.text = status  # Change collection status
    try:
        batch.save('Marking as %(status)s; updated %(success)s member item%(success_plural)s'
                   % info)

    except Exception as e:
        save_err = "Error updating SimpleCollection %s - %s" % (obj.pid, e)
        logger.error(save_err)
        raise Exception('%s; %s' % (save_err, summary_msg))

    # success
    return 'Successfully updated %(success)s item%(success_plural)s' % info



def queue_batch_status_update(batch_obj, status):
    task = batch_set_status.delay(batch_obj.pid, status)
    # create a task result object to track conversion status
    result = TaskResult(label='Update status to %s' % (status),
                        object_id=batch_obj.pid,
                        url=batch_obj.get_absolute_url(), task_id=task.task_id)
    result.save()

