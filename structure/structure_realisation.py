
class StructureRealisation:
    def __init__(self):
        self.global_ids_to_locals = {}  # global_id: id_in_cogmap
    def add_new_event_realisation(self, id_in_cogmap, global_id):
        self.global_ids_to_localsp[global_id] = id_in_cogmap

    def __len__(self):
        return len(self.global_ids_to_locals)

    def get_local_id_by_global(self, global_id):
        return self.global_ids_to_locals[global_id]
