# тестовое надстроенное над сложившейся структурой событие, по которому будет собыираться статистика в семплере
class StructureTop:
    def __len__(self, u_from_parent, global_parent_id, mass, LUE_id, is_linked_to_parent):
        self.u_from_parent = u_from_parent
        self.global_parent_id = global_parent_id
        self.mass = mass
        self.LUE_id = LUE_id
        self.is_linked_to_parent = is_linked_to_parent