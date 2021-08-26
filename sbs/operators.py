import bpy

def GetJsonFromFile(filePath):
    contents = ""
    fh = open(filePath)
    for line in fh:
        cleanedLine = line.split("//", 1)[0]
        if len(cleanedLine) > 0 and line.endswith("\n") and "\n" not in cleanedLine:
            cleanedLine += "\n"
        contents += cleanedLine
    fh.close
    while "/*" in contents:
        preComment, postComment = contents.split("/*", 1)
        contents = preComment + postComment.split("*/", 1)[1]
    return contents

class SbsImportOperator(bpy.types.Operator):
    """ This is an example operator"""
    bl_idname = "object.sbs_import"
    bl_label = "sbs import"

    def execute(self, context):
        return {'FINISHED'}
