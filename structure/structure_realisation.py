
class StructureRealisation:
    def __init__(self):
        self.global_ids_to_locals = {}  # global_id: id_in_cogmap


    def __len__(self):
        return len(self.global_ids_to_locals)

    def get_local_id_by_global(self, global_id):
        return self.global_ids_to_locals[global_id]

    def get_list_of_local_ids(self):
        return list_of_local_ids

    def try_get_event_check_result_by_linked_event(self, structure, target_global_node_id):
        # смотрим, есть ли в слинкованное событие
        # смотрим, зарегистрировано ли оно уже в этой реализации
        # если нет ,то возвращаем неудачу
        # если да, возвращаем его локальный айди


        return local_id или None
