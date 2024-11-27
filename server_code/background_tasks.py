import anvil.server
from anvil.tables import app_tables

from .helpers import print_timestamp


def proceed_or_abort_scheduled(taskid):
    """Abort any duplicate scheduled tasks."""
    task_name = anvil.server.get_background_task(taskid).get_task_name()

    existing_tasks = app_tables.tasks.get(task_name=task_name)

    if existing_tasks and existing_tasks['task_id']:
        try:
            existing_running_tasks = anvil.server.get_background_task(existing_tasks['task_id'])
            if existing_running_tasks.is_running():
                print("\n This scheduled task is already running. Abort.")
                return False
            else:
                existing_tasks['task_id'] = taskid
        except anvil.server.BackgroundTaskNotFound:
            pass
    elif not existing_tasks:
        existing_tasks = app_tables.tasks.add_row(task_id=taskid, task_name=task_name)
    # print(existing_tasks)
    # print(taskid)
    # print(existing_tasks['task_id'])
    existing_tasks['task_id'] = taskid
    existing_tasks['task_name'] = task_name
    return True


def proceed_or_abort(row, taskid, func_name=None):
    """
    Abort any duplicate background tasks.

    func_name is provided separately as sometimes background tasks
    call other background tasks as functions, which makes func_name
    distinct from the background task.
    """
    print_timestamp(f'proceed_or_abort : {func_name}')

    if not row['bk_tasks']:
        return proceed_or_wait(row, taskid, func_name)
        
    bk_tasks = [i for i in row['bk_tasks'] if i['task_name'] == func_name]
    if len(bk_tasks) > 0:
        bk_task = bk_tasks[0]
    else:
        return proceed_or_wait(row, taskid, func_name)
    
    if bk_task:
        try:
            task = anvil.server.get_background_task(bk_task['task_id'])
        except anvil.server.BackgroundTaskNotFound:
            return proceed_or_wait(row, taskid, func_name)
        if task.is_running():
            print(f'proceed_or_abort: aborting background task {func_name}')
            return False
    # This background task name is not running. So you can run it.
    return proceed_or_wait(row, taskid, func_name)

    

def proceed_or_wait(row, taskid, func_name=None, extra_keys=None):
    """Helper function to queue up duplicate background tasks to run sequentially."""
    import time
    print_timestamp('proceed_or_wait: ' + str(taskid) + ': ' + func_name)
    task_name = anvil.server.get_background_task(taskid).get_task_name()
    task_dict = {'task_id': taskid, 'task_name': task_name}
    
    if extra_keys:
        for key, val in extra_keys.items():
            task_dict[key] = val

    if not row['bk_tasks']:
        # Add this task in the queue and start it.
        row['bk_tasks'] = [task_dict]
        print_timestamp(f"\nA new bk task {taskid} was added: {row['bk_tasks']}")
        return row

    if taskid in [i['task_id'] for i in row['bk_tasks']]:
        print_timestamp(f"\nYou called this bk task {func_name} as a function within another bk task: {taskid}. Proceed.")
        return row

    print_timestamp(f"\n{func_name} ({taskid}) Possibly waiting on some background tasks: {row['bk_tasks']}")

    # Add this task to the queue
    row['bk_tasks'] = row['bk_tasks'] + [task_dict]
    print_timestamp(f"\nA new bk task {taskid} was added: {row['bk_tasks']}")

    # While there is a queue and the current taskid is not at bat yet
    while row['bk_tasks'] and taskid != row['bk_tasks'][0]['task_id']:
        # print(f"\nCurrently running task: {running_task}")
        try:
            task = anvil.server.get_background_task(row['bk_tasks'][0]['task_id'])
            if not task.is_running():
                print_timestamp(f"\nTask {row['bk_tasks'][0]} is no longer running")
                # Remove task and update db.
                row['bk_tasks'] = row['bk_tasks'][1:]  # Might cause an error
                print_timestamp(f"\nRemoval check: {row['bk_tasks']}")
        except anvil.server.BackgroundTaskNotFound:
            row['bk_tasks'] = row['bk_tasks'][1:]
            print_timestamp(f"\nRemoval check: {row['bk_tasks']}")

        time.sleep(1)

    print_timestamp(f"\nNow running {taskid}")
    return row


def user_bk_running(table_name, bk_name):
    """Check if a particular background task is running on this user."""
    user = anvil.users.get_user(allow_remembered=True)
    print_timestamp('user_bk_running: ' + user['email'] + ' bk_name: ' + bk_name)

    row = getattr(app_tables, table_name).get(user=user)
    
    if not row['bk_tasks']:
        return False
    for i in row['bk_tasks']:
        if i['task_name'] == bk_name:
            print_timestamp('Found bk task')
            try:
                task = anvil.server.get_background_task(i['task_id'])
                if task.is_running():  # Ignore errors
                    return True
            except anvil.server.BackgroundTaskNotFound:
                pass
    return False