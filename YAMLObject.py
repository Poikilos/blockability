# 
# * Created by SharpDevelop.
# * User: jgustafson
# * Date: 3/25/2015
# * Time: 9:02 AM
# * see python version in ../../d.pygame/ via www.developerfusion.com/tools/convert/csharp-to-python
# * To change this template use Tools | Options | Coding | Edit Standard Headers.
# 
#from System import *
#from System.Collections import *
#from System.IO import *
#from System.Linq import * #Enumerable etc
#   public class YAMLLineInfo {
#       public const int TYPE_NOLINE=0;
#       public const int TYPE_OBJECTNAME=1;
#       public const int TYPE_ARRAYNAME=2;
#       public const int TYPE_ARRAYVALUE=3;
#       public const int TYPE_VARIABLE=4;
#       public int lineType=0;
#       public int lineIndex=-1;//for debugging only--line of file
#   }
class YAMLObject(object):
    """ <summary>
     YAMLObject. The first YAMLObject object is the root (one where you call load).
     Other YAMLObject can be either:
     * Root is the yaml object from which you called load--normally, use this object to get values: such as myrootyamlobject.getArrayValues("groups.Owner.inheritance") or myrootyamlobject.getValue("groups.SuperAdmin.default").
     * Object is stored in file like: name, colon, newline, additional indent, object/array/variable
     * Array is stored in file like: name, colon, newline, no additional indent, hyphen, space, value
     * Variable is stored in file like: name, colon, value (next line should have less or equal indent)
     </summary>
    """
    # <summary>
    # line from source file--for debugging only
    # </summary>
    def __init__(self, name, val, Parent):
        self._Name = None
        self._Value = None
        self._arrayValues = None
        self._namedSubObjects = None
        self._depthCount = 0
        self._indentCount = 0
        self._whitespaceCount = 0
        self._whitespaceString = ""
        self._lineIndex = -1
        self._parent = None
        self._thisYAMLSyntaxErrors = None
        self._IsVerbose = False
        self._indentDefaultString = "  "
        #       public YAMLObject(string val)
        #       {
        #           Value=val;
        #       }
        self._Name = name
        self._Value = val
        self._parent = Parent

    def __init__(self, name, val, Parent):
        self._Name = None
        self._Value = None
        self._arrayValues = None
        self._namedSubObjects = None
        self._depthCount = 0
        self._indentCount = 0
        self._whitespaceCount = 0
        self._whitespaceString = ""
        self._lineIndex = -1
        self._parent = None
        self._thisYAMLSyntaxErrors = None
        self._IsVerbose = False
        self._indentDefaultString = "  "
        self._Name = name
        self._Value = val
        self._parent = Parent

    def __init__(self, name, val, Parent):
        self._Name = None
        self._Value = None
        self._arrayValues = None
        self._namedSubObjects = None
        self._depthCount = 0
        self._indentCount = 0
        self._whitespaceCount = 0
        self._whitespaceString = ""
        self._lineIndex = -1
        self._parent = None
        self._thisYAMLSyntaxErrors = None
        self._IsVerbose = False
        self._indentDefaultString = "  "
        self._Name = name
        self._Value = val
        self._parent = Parent

    def getFullName(self):
        return self.getFullNameRecursive_DontCallMeDirectly(self._Name)

    def getFullNameRecursive_DontCallMeDirectly(self, child):
        if self.isRoot():
            return child
        else:
            return self._parent.getFullNameRecursive_DontCallMeDirectly(self._Name + "." + child)

    def setValue(self, name, new_value):
        """ <summary>
         This should always be called using the root YAMLObject (the one from which you loaded a YAML file).
         Sub-objects should be accessed using dot notation.
         </summary>
         <param name="Name">object name (must be in dot notation if indented more, such as groups.Administrator.default)</param>
         <returns></returns>
        """
        if name is not None:
            if name.Length > 0:
                foundObject = self.getObject(name)
                if foundObject is None:
                    self.createObject(name)
                    foundObject = self.getObject(name)
                if foundObject is not None:
                    foundObject.Value = new_value
                else:
                    print("setValue error: setValue could neither find nor create an object (this should never happen) {name:\"" + name.replace("\"", "\\\"") + "\"}.")
            else:
                print("Programmer error: setValue cannot do anything since name is empty (0-length).")
        else:
            print("Programmer error: setValue cannot do anything since name is null")

    def getObject(self, name):
        foundObject = None
        if name is not None:
            if name.Length > 0:
                dotIndex = -1
                nameSub = None
                if dotIndex >= 0:
                    nameSub =  name[dotIndex + 1:]
                    name =  name[0:0+ dotIndex]
#                enumerator = namedSubObjects.GetEnumerator()
#                while enumerator.MoveNext():
