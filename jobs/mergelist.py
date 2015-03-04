__author__ = 'tieni'


class SegObject:
    def __init__(self, obj_id=None, todo=None, position=None, supervoxels=None, category="", comment=""):
        self.id = obj_id
        self.todo = todo
        self.pos = position
        self.category = category
        self.comment = comment
        self.supervoxels = [] if supervoxels is None else supervoxels

    def __str__(self):
        return "object {0} at {1}: {2}".format(self.id, self.pos, self.supervoxels)


class Mergelist:
    def __init__(self, chunk_number, mergelist_path):
        self.chunk_number = chunk_number
        self.seg_objects = []
        try:
            with open(mergelist_path, 'r') as txt:
                index = 0
                obj_id = None; todo = None; supervoxels = []; coord = []; category = None; comment = None
                for line in txt:
                    if index == 0:
                        content = line.split()
                        obj_id = int(content[0])
                        todo = True if content[1] == "1" else False
                        supervoxels = [int(sub_id) for sub_id in content[3:]]
                    if index == 1:
                        coord = [int(coordinate) for coordinate in line.split()]
                    if index == 2:
                        category = line
                    if index == 3:
                        comment = line
                        self.seg_objects.append(SegObject(obj_id, todo, coord, supervoxels, category, comment))
                        index = 0
                        continue
                    index += 1
            print('\n'.join([str(seg_object) for seg_object in self.seg_objects]))
        except IOError:
            print("No mergelist " + mergelist_path)

    def count_comment(self, comment):
        count = 0
        for seg_obj in self.seg_objects:
            if seg_obj.comment == comment:
                count += 1
        return count

    def number_todos(self):
        count = 0
        for seg_obj in self.seg_objects:
            count += 1 if seg_obj.todo else 0
        return count

    def are_merged(self, id1, id2):
        for seg_obj in self.seg_objects:
            if id1 in seg_obj.supervoxels and id2 in seg_obj.supervoxels:
                return True
        return False

    def write(self, absolute_path):
        with open(absolute_path, 'w') as mergelist:
            for seg_obj in self.seg_objects:
                mergelist.write("{0} {1} {2} {3}\n{4}\n{5}\n{6}\n"
                                .format(seg_obj.id, seg_obj.todo, seg_obj.immutable, ' '.join(seg_obj.supervoxels),
                                        ' '.join(seg_obj.pos),
                                        seg_obj.category,
                                        seg_obj.comment))