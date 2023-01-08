
class StructureRealisation:
    def __init__(self):
        self.global_ids_to_locals = {}  # global_id: id_in_cogmap
        self.last_recognised = None  # global_id

    def add_new_event_realisation(self, id_in_cogmap, global_id):
        self.last_recognised = global_id
        self.global_ids_to_localsp[global_id] = id_in_cogmap

    def __len__(self):
        return len(self.global_ids_to_locals)
