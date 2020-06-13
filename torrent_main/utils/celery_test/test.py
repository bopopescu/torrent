# import celery
#
# app = celery.Celery('test', broker='redis://localhost:6379')
#
#
# class MyCelery(celery.Celery):
#
#     def gen_task_name(self, name, module):
#         if module.endwith('.tasks'):
#             module = module[:-6]
#         return super(MyCelery, self).gen_task_name(name, module)
# # app = MyCelery('main')
#
#
# class MyTask(celery.Task):
#
#     def on_success(self, retval, task_id, args, kwargs):
#         print('Success!!')
#
#     def on_failure(self, exc, task_id, args, kwargs, einfo):
#         print('Fail')
#
#
# @app.task(base=MyTask, name='add-two-numbers', bind=True, ignore_result=True)
# def add(self, x, y):
#     print(self.request)
#     return x + y
#
