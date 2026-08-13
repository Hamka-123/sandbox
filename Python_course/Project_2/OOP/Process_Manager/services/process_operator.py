# Business Logic / Operator

class ProcessOperator:
    
    def __init__(self, repository):
        self.repository = repository
    
    def get_processes_list(self, count = None):
        return self.repository.fetch_all(count)
    
    def get_accessible_processes(self, count = None):
        return self.repository.fetch_accessible(count)
    
    def kill_process(self, process_entity):
        if not process_entity.accessible:
            return {'success': False, 'message': f'Cannot kill {process_entity.pid} - no access'}
        return self.repository.kill_process(process_entity.pid)