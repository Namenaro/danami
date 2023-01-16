from structure_memory import StructureMemory
class StructureRealisation:
    def __init__(self):
        self.global_ids_to_locals = {}  # global_id: id_in_cogmap

    def __len__(self):
        return len(self.global_ids_to_locals)

    def get_local_id_by_global(self, global_id):
        return self.global_ids_to_locals.get(global_id, None)

    def get_list_of_local_ids(self):
        return list(self.global_ids_to_locals.values())

    def try_get_event_check_result_by_linked_event(self, structure, target_global_node_id):
        # смотрим, есть ли в стр-ре событие, слинкованное с данным
        linked_global_event = structure.get_linked_to_this_event(target_global_node_id)
        if linked_global_event is None:
            return None
        # смотрим, зарегистрировано ли оно уже в этой реализации
        linked_local_id = self.global_ids_to_locals.get(linked_global_event, None)
        return linked_local_id

    def add_new_check_result(self, global_id, id_in_cogmap):
        self.global_ids_to_locals[global_id] = id_in_cogmap
