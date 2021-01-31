#!/usr/bin/env python
from __future__ import print_function
#
# Processed by pycodetool https://github.com/expertmm/PythonCodeTranslators 2015-11-30 11:08:58
import sys
# * Created by SharpDevelop.
# * User: jgustafson
# * Date: 3/25/2015
# * Time: 9:02 AM
# * see python version in ../../d.pygame/ via www.developerfusion.com/tools/convert/csharp-to-python
# * To change this template use Tools | Options | Coding | Edit Standard Headers.
#

# as converted from C# by SharpDevelop 3.0, SharpDevelop 5.1, or http://codeconverter.sharpdevelop.net/SnippetConverter.aspx

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

#    def __init__(self, name, val, Parent):
#        self._Name = None
#        self._Value = None
#        self._arrayValues = None
#        self._namedSubObjects = None
#        self._depthCount = 0
#        self._indentCount = 0
#        self._whitespaceCount = 0
#        self._whitespaceString = ""
#        self._lineIndex = -1
#        self._parent = None
#        self._thisYAMLSyntaxErrors = None
#        self._IsVerbose = False
#        self._indentDefaultString = "  "
#        self._Name = name
#        self._Value = val
#        self._parent = Parent
#
#    def __init__(self, name, val, Parent):
#        self._Name = None
#        self._Value = None
#        self._arrayValues = None
#        self._namedSubObjects = None
#        self._depthCount = 0
#        self._indentCount = 0
#        self._whitespaceCount = 0
#        self._whitespaceString = ""
#        self._lineIndex = -1
#        self._parent = None
#        self._thisYAMLSyntaxErrors = None
#        self._IsVerbose = False
#        self._indentDefaultString = "  "
#        self._Name = name
#        self._Value = val
#        self._parent = Parent
#
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
                    sys.stderr.write("setValue error: setValue could neither find nor create an object (this should never happen) {name:\"" + name.replace("\"", "\\\"") + "\"}.")
                    sys.stderr.write("\n")
                    sys.stderr.flush()
            else:
                sys.stderr.write("Programmer error: setValue cannot do anything since name is empty (0-length).")
                sys.stderr.write("\n")
                sys.stderr.flush()
        else:
            sys.stderr.write("Programmer error: setValue cannot do anything since name is null")
            sys.stderr.write("\n")
            sys.stderr.flush()

    def getObject(self, name):
        foundObject = None
        if name is not None:
            if name.Length > 0:
                dotIndex = -1
                nameSub = None
                if dotIndex >= 0:
                    nameSub = name[dotIndex + 1:].strip()
                    name = name[0:0+ dotIndex].strip()
#                enumerator = namedSubObjects.GetEnumerator()
#                while enumerator.MoveNext():
                for thisObject in self._namedSubObjects:
                    if thisObject.Name == name:
                        if nameSub is not None:
                            foundObject = thisObject.getObject(nameSub)
                        else:
                            foundObject = thisObject
                        break
            else:
                sys.stderr.write("Programmer error: getObject cannot do anything since name is empty (0-length).")
                sys.stderr.write("\n")
                sys.stderr.flush()
        else:
            sys.stderr.write("Programmer error: getObject cannot do anything since name is null.")
            sys.stderr.write("\n")
            sys.stderr.flush()
        return foundObject
 #end getObject
    def createObject(self, name):
        dotIndex = -1
        nameSub = None
        if name is not None:
            name = name.strip()
            dotIndex = name.IndexOf(".")
            if dotIndex >= 0:
                nameSub = name[dotIndex + 1:].strip()
                name = name[0:0+ dotIndex].strip()
            if name.Length > 0:
                newObject = None
                newObject = self.getObject(name)
                if newObject is None:
                    newObject = YAMLObject(name, None, self)
                    self._namedSubObjects.Add(newObject)
                if nameSub is not None:
                    newObject.createObject(nameSub)
            else:
                sys.stderr.write("Programmer error: createObject cannot do anything since name is empty (0-length) string.")
                sys.stderr.write("\n")
                sys.stderr.flush()
        else:
            sys.stderr.write("Programmer error: createObject cannot do anything since name is null.")
            sys.stderr.write("\n")
            sys.stderr.flush()

    def addArrayValue(self, val):
        if self._arrayValues is None:
            self._arrayValues = list()
        if val is not None:
            self._arrayValues.Add(YAMLObject(None, val))
        else:
            sys.stderr.write("WARNING: addArrayValue skipped null value.")
            sys.stderr.write("\n")
            sys.stderr.flush()

    def isArray(self):
        return self._arrayValues is not None

    def getSubValue(self, name):
        """ <summary>

         </summary>
         <param name="name">full variable name (with dot notation if necessary)</param>
         <returns></returns>
        """
        foundValue = None
        if name is not None:
            if name.Length > 0:
                foundObject = self.getObject(name)
                if foundObject is not None:
                    foundValue = foundObject.Value
                else:
                    sys.stderr.write("Programmer error: createObject cannot get value since object does not exist {name:\"" + name.replace("\"", "\\\"") + "\"}.")
                    sys.stderr.write("\n")
                    sys.stderr.flush()
            else:
                sys.stderr.write("Programmer error: createObject cannot do anything since name is empty (0-length) string.")
                sys.stderr.write("\n")
                sys.stderr.flush()
        else:
            sys.stderr.write("Programmer error: createObject cannot do anything since name is null.")
            sys.stderr.write("\n")
            sys.stderr.flush()
        return foundValue

    def getValue(self):
        val = None
        if self._arrayValues is None:
            val = self._Value
        return val

    def getSubTrees(self):
        thisAL = None
        if self._namedSubObjects is not None:
            thisAL = list()
#            enumerator = namedSubObjects.GetEnumerator()
#            while enumerator.MoveNext():
            for thisYT in self._namedSubObjects:
                thisAL.Add(thisYT)
        return thisAL

    def getArrayValues(self):
        thisAL = None
        if self._arrayValues is not None:
            thisAL = list()
#            enumerator = arrayValues.GetEnumerator()
#            while enumerator.MoveNext():
            for thisValue in self._arrayValues:
                thisAL.Add(thisValue)
        return thisAL

    def addSub(self, addObject):
        if self._namedSubObjects is None:
            self._namedSubObjects = list()
        self._namedSubObjects.Add(addObject)

    def isLeaf(self):
        return not self.isRoot() and self._namedSubObjects is None

    def isRoot(self):
        return self._parent is None

    #       public void loadLine(string original_line, ref int currentFileLineIndex) {
    #
    #       }
    def getLines(fileName):
        thisAL = None
        inStream = None
        original_line = None
        try:
            inStream = open(fileName, 'r')
            thisAL = list()
            for original_line_with_newline in inStream:
                original_line = original_line_with_newline.rstrip()
                thisAL.Add(original_line)
            inStream.close()
            inStream = None
        except:
            sys.stderr.write("Could not finish YAMLObject static getLines: " + traceback.format_exc())
            sys.stderr.write("\n")
            sys.stderr.flush()
            if inStream is not None:
                try:
                    inStream.Close()
                    inStream = None
                except:
                    pass
                finally:
                    pass
        finally: #don't care
            pass
        return thisAL

    getLines = staticmethod(getLines)

    def deqErrorsInYAMLSyntax(self):
        thisAL = self._thisYAMLSyntaxErrors
        self._thisYAMLSyntaxErrors = list()
        return thisAL

    def getAncestorWithIndent(self, theoreticalWhitespaceCount, lineOfSibling_ForSyntaxCheckingMessage):
        ancestor = None
        if self._whitespaceCount == theoreticalWhitespaceCount:
            ancestor = self
            self.addVerboseSyntaxMessage("...this (" + self.getDebugNounString() + ") is ancestor since has whitespace count " + str(self._whitespaceCount))
        else:
            if self._parent is not None:
                IsCircularReference = False
                if self._parent.parent is not None:
                    if self._parent.parent == self:
                        IsCircularReference = True
                        msg = "YAML syntax error on line " + str((lineOfSibling_ForSyntaxCheckingMessage + 1)) + ": circular reference (parent of object on line " + str((self._lineIndex + 1)) + "'s parent is said object)."
                        self._thisYAMLSyntaxErrors.Add(msg)
                        sys.stderr.write(msg)
                        sys.stderr.write("\n")
                        sys.stderr.flush()
                if not IsCircularReference:
                    ancestor = self._parent.getAncestorWithIndent(theoreticalWhitespaceCount, lineOfSibling_ForSyntaxCheckingMessage)
            else:
                msg = "YAML syntax error on line " + str((lineOfSibling_ForSyntaxCheckingMessage + 1)) + ": unexpected indent (there is no previous line with this indentation level, yet it is further back than a previous line indicating it should have a sibling)."
                self._thisYAMLSyntaxErrors.Add(msg)
                sys.stderr.write(msg)
                sys.stderr.write("\n")
                sys.stderr.flush()
        return ancestor
 #end getAncestorWithIndent
    def addVerboseSyntaxMessage(msg):
        if self._IsVerbose:
            if msg is not None:
                msg = "#Verbose message: " + msg
                if self._thisYAMLSyntaxErrors is not None:
                    self._thisYAMLSyntaxErrors.Add(msg)
                print(msg)

    addVerboseSyntaxMessage = staticmethod(addVerboseSyntaxMessage)

    def getArrayValueCount(self):
        count = 0
        if self._arrayValues is not None:
            count = self._arrayValues.Count
        return count

    def getYAMLObject(lines, currentFileLineIndex, rootObject, prevLineYAMLObject):
        """ <summary>
         Parses a line and gets the yaml object, setting the parent properly.
         </summary>
         <param name="lines"></param>
         <param name="currentFileLineIndex"></param>
         <param name="prevWhitespaceCount"></param>
         <param name="rootObject"></param>
         <param name="prevLineYAMLObject"></param>
         <returns>A new YAML Object EXCEPT when an array element, then returns prevLineYAMLObject</returns>
        """
        #YAMLObject nextLineParentYAMLObject=null;
        newObject = None
        try:
            if lines is not None:
                prevWhitespaceCount = 0
                if prevLineYAMLObject is not None:
                    prevWhitespaceCount = prevLineYAMLObject.whitespaceCount
                original_line = lines[currentFileLineIndex]
                line_TrimStart = original_line.TrimStart()
                line_Trim = original_line.strip()
                if line_Trim.Length > 0:
                    line_whitespaceCount = original_line.Length - line_TrimStart.Length
                    #thisWhitespace=original_line.Substring(0,
                    #if (whitespaceCount==prevWhitespaceCount) {
                    if line_Trim.StartsWith("- "): #this line is part of an array
                        IsSyntaxErrorShown = False
                        if prevLineYAMLObject is not None:
                            newObject = prevLineYAMLObject
                            prevLineYAMLObject.addArrayValue(line_Trim[2:].strip()) #do it regardless for fault tolerance
                            YAMLObject.addVerboseSyntaxMessage("line " + str((currentFileLineIndex + 1)) + "...array value at index [" + str((prevLineYAMLObject.getArrayValueCount() - 1)) + "]...")
                        else:
                            newObject = rootObject
                            rootObject.addArrayValue(line_Trim[2:].strip())
                            #string msg="YAML syntax error on line "+(currentFileLineIndex+1).ToString()+": array element was found without a name at same indent level on a previous line, so the value was added to the variable on line "+(newObject.lineIndex+1).ToString()+".";
                            msg = "YAML syntax error on line " + str((currentFileLineIndex + 1)) + ": array element was found without a name at same indent level on a previous line, so the value was added to the root object to prevent data loss."
                            IsSyntaxErrorShown = True
                            self._thisYAMLSyntaxErrors.Add(msg)
                            sys.stderr.write(msg)
                            sys.stderr.write("\n")
                            sys.stderr.flush()
                        if line_whitespaceCount != prevWhitespaceCount:
                            if not IsSyntaxErrorShown:
                                msg = "YAML syntax error on line " + str((currentFileLineIndex + 1)) + ": array element should not be indented by " + str(line_whitespaceCount) + " characters but was added to the variable above it {line:" + str((newObject.lineIndex + 1)) + "} to prevent data loss."
                                self._thisYAMLSyntaxErrors.Add(msg)
                                sys.stderr.write(msg)
                                sys.stderr.write("\n")
                                sys.stderr.flush()
                    else: #end if line is an array element #this line is an object, single-value variable, or array name)
                        newObject = YAMLObject()
                        newObject.whitespaceCount = line_whitespaceCount
                        newObject.whitespaceString = original_line[0:0+ line_whitespaceCount]
                        newObject.lineIndex = currentFileLineIndex
                        if newObject.whitespaceCount == prevWhitespaceCount:
                            newObject.parent = prevLineYAMLObject.parent if (prevLineYAMLObject is not None) else rootObject #nextLineParentYAMLObject=prevLineYAMLObject;
                            if newObject.parent is not None:
                                newObject.parent.addSub(newObject)
                            YAMLObject.addVerboseSyntaxMessage("line " + str((currentFileLineIndex + 1)) + "...same parent as previous line...")
                        elif newObject.whitespaceCount > prevWhitespaceCount:
                            newObject.parent = prevLineYAMLObject
                            if newObject.parent is not None:
                                newObject.parent.addSub(newObject)
                            YAMLObject.addVerboseSyntaxMessage("line " + str((currentFileLineIndex + 1)) + "...child of previous line...")
                        else: #indented less than previous line
                            if prevLineYAMLObject is not None:
                                newObject.parent = prevLineYAMLObject.getAncestorWithIndent(newObject.whitespaceCount - 2, currentFileLineIndex)
                                ancestorLineIndex = -1
                                if newObject.parent is not None:
                                    newObject.parent.addSub(newObject)
                                    ancestorLineIndex = newObject.parent.lineIndex
                                    YAMLObject.addVerboseSyntaxMessage("line " + str((currentFileLineIndex + 1)) + "...indented less than previous line, so ancestor set to object on line " + str((ancestorLineIndex + 1)) + "(" + newObject.parent.getDebugNounString() + ")...")
                                else:
                                    msg = "line " + str((currentFileLineIndex + 1)) + ": could not find ancestor via decreasing indent, though this object is a child and should have a parent indented by 2 fewer characters."
                                    self._thisYAMLSyntaxErrors.Add(msg)
                                    sys.stderr.write(msg)
                                    sys.stderr.write("\n")
                                    sys.stderr.flush()
                            else:
                                msg = "YAML parser failure on line " + str((currentFileLineIndex + 1)) + ": could not find previous line, though this line is less indented than previous line."
                                self._thisYAMLSyntaxErrors.Add(msg)
                                sys.stderr.write(msg)
                                sys.stderr.write("\n")
                                sys.stderr.flush()
                        colonIndex = line_Trim.IndexOf(":")
                        if colonIndex > 0: #indentionally > instead of >= since starting with colon would be YAML syntax error
                            thisName = line_Trim[0:0+ colonIndex].strip()
                            thisValue = line_Trim[colonIndex + 1:].strip()
                            if thisName.Length > 0:
                                newObject.Name = thisName
                                if thisValue.Length > 0: #this line is a variable
                                    newObject.Value = thisValue
                                    YAMLObject.addVerboseSyntaxMessage("line " + str((currentFileLineIndex + 1)) + "...OK (variable)")
                                else: #this line is an object or array
                                    #newObject.Name=thisName;
                                    YAMLObject.addVerboseSyntaxMessage("line " + str((currentFileLineIndex + 1)) + "...OK (name of object or of array)")
                            else:
                                msg = "YAML syntax error on line " + str((currentFileLineIndex + 1)) + ": missing name--got colon instead."
                                self._thisYAMLSyntaxErrors.Add(msg)
                                sys.stderr.write(msg)
                                sys.stderr.write("\n")
                                sys.stderr.flush()
                        else:
                            msg = "YAML syntax error on line " + str((currentFileLineIndex + 1)) + ": missing colon where new object should start"
                            self._thisYAMLSyntaxErrors.Add(msg)
                            sys.stderr.write(msg)
                            sys.stderr.write("\n")
                            sys.stderr.flush()
                else: #end else line is an object or variable
                    #} #end if line_Trim.Length>0
                    newObject = prevLineYAMLObject
        except:
            #           int currentFileLineIndex=0;
            #           string original_line=null;
            #           while ( (original_line=inStream.ReadLine()) != null ) {
            #               //loadNext(inStream, ref currentFileLineIndex);
            #               //loadLine(original_line, ref currentFileLineIndex);
            #           }
            msg = "YAML parser failure (parser could not finish) on line " + str((currentFileLineIndex + 1)) + ": " + traceback.format_exc()
            self._thisYAMLSyntaxErrors.Add(msg)
            sys.stderr.write(msg)
            sys.stderr.write("\n")
            sys.stderr.flush()
        finally:
            pass
        return newObject

    getYAMLObject = staticmethod(getYAMLObject)
 #end loadYAMLObject
    def loadYAMLLines(self, lines):
        if lines is not None:
            if self._thisYAMLSyntaxErrors is None:
                self._thisYAMLSyntaxErrors = list()
            else:
                self._thisYAMLSyntaxErrors.Clear()
            #int prevWhitespaceCount=0;
            #int whitespaceCount=0;
            currentFileLineIndex = 0
            prevObject = None
            #int prevLineType
            while currentFileLineIndex < lines.Length:
                prevObject = self.getYAMLObject(lines, currentFileLineIndex, self, prevObject)
                currentFileLineIndex += 1
 #end loadYAMLLines
    def loadYAML(self, fileName):
        """ <summary>
         Top level is self, but with no name is needed, to allow for multiple variables--for example, if file begins with "groups," this object will have no name but this object's subtree will contain an object named groups, and then you can get the values like: getArrayAsStrings("groups.SuperAdmin.permissions")
         </summary>
         <param name="fileName"></param>
        """
        thisAL = self.getLines(fileName)
        lines = None
        if thisAL is not None and thisAL.Count > 0:
            lines = Array.CreateInstance(str, thisAL.Count)
            index = 0
#            enumerator = thisAL.GetEnumerator()
#            while enumerator.MoveNext():
            for line in thisAL:
                lines[index] = line
                index += 1
        self.loadYAMLLines(lines)
 #end loadYAML
    def saveYAMLSelf(self, outStream, setIndentCount):
        #string thisIndentString=getMyIndent();
        try:
            myRealIndentString = self.getMyRealIndent()
            if not self.isLeaf():
                subTreeIndentCount = setIndentCount + 1
                if self._parent is not None:
                    outStream.write(myRealIndentString + self._Name + ":"+"\n")
                else:
                    subTreeIndentCount = 0
                foundSubTreeCount = 0
                if self._namedSubObjects is not None:
#                    enumerator = namedSubObjects.GetEnumerator()
#                    while enumerator.MoveNext():
                    for subTree in self._namedSubObjects:
                        subTree.saveYAMLSelf(outStream, subTreeIndentCount)
                        foundSubTreeCount += 1
                else:
                    self.addVerboseSyntaxMessage("namedSubObjects is null though this is not a leaf")
                msg = myRealIndentString + "Saved " + str(foundSubTreeCount) + " subtrees for YAMLObject named " + self.ValueToCSharp(self._Name)
                if self._lineIndex >= 0:
                    msg += " that had been loaded from line " + str((self._lineIndex + 1))
                else:
                    msg += " that had been generated (not loaded from a file)"
                self.addVerboseSyntaxMessage(msg)
            elif self.isArray():
                outStream.write(myRealIndentString + self._Name + ":"+"\n")
                count = 0
#                enumerator = arrayValues.GetEnumerator()
#                while enumerator.MoveNext():
                for thisValue in self._arrayValues:
                    outStream.write(myRealIndentString + "- " + thisValue.getValue()+"\n")
                    count += 1
                self.addVerboseSyntaxMessage(myRealIndentString + "Saved " + str(count) + "-length array")
            elif self._Value is not None:
                self.addVerboseSyntaxMessage("Saved variable")
                outStream.write(myRealIndentString + self._Name + ": " + self._Value+"\n")
            else:
                msg = "ERROR in saveSelf: null Value (" + self.getDebugNounString() + ")"
                if YAMLObject.thisYAMLSyntaxErrors is None:
                    YAMLObject.thisYAMLSyntaxErrors = list()
                YAMLObject.thisYAMLSyntaxErrors.Add(msg)
                sys.stderr.write(msg)
                sys.stderr.write("\n")
                sys.stderr.flush()
        except:
            msg = "Could not finish saveYAMLSelf: " + traceback.format_exc()
            sys.stderr.write(msg)
            sys.stderr.write("\n")
            sys.stderr.flush()
            YAMLObject.thisYAMLSyntaxErrors.Add(msg)
        finally:
            pass
 #end saveYAMLSelf
    def getDebugNounString(self):
        """ <summary>
         formerly getDescription
         </summary>
         <returns></returns>
        """
        typeString = "array" if (self._arrayValues is not None) else "object"
        lineTypeMessage = ""
        if self._lineIndex >= 0:
            lineTypeMessage += " that had been loaded from line " + str((self._lineIndex + 1))
        else:
            lineTypeMessage += " that had been generated (not loaded from a file)"
        descriptionString = typeString + " named: " + self.ValueToCSharp(self._Name) + lineTypeMessage + "; is" + ("" if self.isLeaf() else " not") + " leaf"
        descriptionString += "; Value:" + self.ValueToCSharp(self._Value)
        descriptionString += "; parent:" + ((".Name:" + self.ValueToCSharp(self._parent.Name)) if (self._parent is not None) else "null")
        return descriptionString

    def saveYAML(self, fileName):
        outStream = None
        try:
            outStream = open(fileName, 'r')
            self.saveYAMLSelf(outStream, 0)
            outStream.close()
            outStream = None
        except:
            msg = "YAMLObject: Could not finish save: " + traceback.format_exc()
            self.addVerboseSyntaxMessage(msg)
            sys.stderr.write(msg)
            sys.stderr.write("\n")
            sys.stderr.flush()
            if outStream is not None:
                try:
                    outStream.Close()
                    outStream = None
                except:
                    pass
                finally:
                    pass
        finally:
            pass
 #don't care #end saveYAML
    def getIndent(count):
        val = System.String(self._indentDefaultString[0], count * self._indentDefaultString.Length)
        return val

    getIndent = staticmethod(getIndent)
 #return string.Concat(Enumerable.Repeat(indentDefaultString, count));
    def getMyIndent(self):
        return self.getIndent(self._indentCount)

    def getMyRealIndent(self):
        count = self.getMyRealIndentCount_Recursive(0)
        return self.getIndent(count)

    def getMyRealIndentCount_Recursive(self, i):
        if self._parent is not None:
            if not self._parent.isRoot():
                i = self._parent.getMyRealIndentCount_Recursive(i + 1)
        return i

    def ValueToCSharp(val):
        """ <summary>
         Returns the string in quotes, otherwise the word "null" without quotes.
         </summary>
         <param name="val"></param>
         <returns></returns>
        """
        return (("\"" + val + "\"") if val is not None else "null")

    ValueToCSharp = staticmethod(ValueToCSharp)
