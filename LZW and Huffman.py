import io

"""
--Start huffman method--
"""


class QueueNodes:
    nodes = []

    def addNode(self, element):
        """
        Add node object to list
        :param element: node object to insert
        """
        i = 0
        while i < len(self.nodes) and self.nodes[i].weight < element.weight:
            i += 1
        self.nodes.insert(i, element)

    def removeNode(self, index):
        """
        Remove node object from list by index
        :param index: Integer index >=0
        """
        del self.nodes[index]

    def getNode(self, index):
        """
        Get node object by index
        :param index: Integer index >=0
        """
        return self.nodes[index]

    def size(self):
        """
        :return: size of list node objects
        """
        return len(self.nodes)

    def __str__(self):
        """
        String represent
        """
        return "[" + ','.join(map(str, self.nodes)) + "]"


class Node:
    leftSon = None
    rightSon = None
    weight = 0
    character = ''
    binaryCode = ''

    def __init__(self, leftSon = None, rightSon = None, weight = 0, character = '', binaryCode = ''):
        """

        :param leftSon: link to left node object
        :param rightSon: link to right node object
        :param weight: frequency of occurrence character
        :param character: char value
        :param binaryCode: string value
        """
        self.leftSon = leftSon
        self.rightSon = rightSon
        if leftSon is not None and rightSon is not None:
            self.weight = leftSon.weight + rightSon.weight
        else:
            self.weight = weight
        self.character = character
        self.binaryCode = binaryCode
        return

    def isSheet(self):
        """
        Checks whether the object is a sheet
        :return: bool
        """
        return True if self.leftSon is None and self.rightSon is None else False

    def __str__(self):
        """
        String represent
        """
        return '(weight = {}, character = \'{}\', leftSon = {}, rightSon = {}, binaryCode = {})'.format(self.weight,
                                                                                                        self.character,
                                                                                                        self.leftSon,
                                                                                                        self.rightSon,
                                                                                                        self.binaryCode)


class DecodeTree:
    """
    Decoded tree sample format

    {
        'A' : '001',
        'B' : '010'
    }
    """
    decodedTree = {}
    usedNodes = {}

    model = ''

    position = 0

    def __init__(self, model):
        """
        :param model: encoded binary tree string
        """
        self.model = model

    def decodeTree(self, currentCode = ''):
        """
        Decode character by binary codes
        :param currentCode: string binary codee
        """
        if len(self.model) <= self.position:
            return

        character = self.model[self.position]

        if currentCode in self.usedNodes and self.usedNodes[currentCode] == 2:
            return

        if character is not '0':
            self.position += 1
            character = self.model[self.position]
            if currentCode is '':
                currentCode = '0'
            self.decodedTree[currentCode] = character
            self.usedNodes[currentCode] = 2

            while currentCode in self.usedNodes and self.usedNodes[currentCode] == 2 and len(currentCode) > 0:
                currentCode = currentCode[:-1]

            self.position += 1
            self.decodeTree(currentCode + '1')
            return
        self.position += 1

        self.decodeTree(currentCode + '0')
        self.usedNodes[currentCode] = 1

        self.decodeTree(currentCode + '1')
        self.usedNodes[currentCode] = 2


class EncodeTree:
    nodes = QueueNodes()

    sheets = {}

    model = ''

    def merge(self):
        """
        Merge two first nodes with minimum weight
        """
        leftSon = self.nodes.getNode(0)
        rightSon = self.nodes.getNode(1)
        self.nodes.removeNode(0)
        self.nodes.removeNode(0)
        self.nodes.addNode(Node(leftSon, rightSon))

    def addNode(self, node):
        """
        :param node: node object to insert
        """
        self.nodes.addNode(node)

    def buildTree(self, statisticDictionary):
        """
        Create binary tree from dictionary with frequency of occurrence statistic

        :param statisticDictionary: dictionary where key is text's character and value is frequency of occurrence
        :return:
        """
        for character, weight in statisticDictionary.items():
            self.addNode(Node(weight = weight, character = character))
        while self.nodes.size() > 1:
            self.merge()
        self.defineSheetsBinaryCode('', self.getRootNode())
        self.buildTreeEncodedModel(self.getRootNode())

    def getRootNode(self):
        """
        :return: root node object
        """
        return self.nodes.getNode(0)

    def defineSheetsBinaryCode(self, currentCode, node):
        """
        Give binary code each node
        :param currentCode: string
        :param node: node object
        """
        if node.isSheet():
            node.binaryCode = currentCode if currentCode is not '' else '0'
            self.sheets[node.character] = node.binaryCode
            return
        self.defineSheetsBinaryCode(currentCode + '0', node.leftSon)
        self.defineSheetsBinaryCode(currentCode + '1', node.rightSon)

    def buildTreeEncodedModel(self, node):
        """
        Encode binary tree to string

        :param node: root node object
        """
        if node.isSheet():
            self.model += "1" + node.character
            return
        else:
            self.model += "0"
        self.buildTreeEncodedModel(node.leftSon)
        self.buildTreeEncodedModel(node.rightSon)

    def __str__(self):
        """
        String represent
        """
        return str(self.nodes)


class FileWork:

    @staticmethod
    def getFileContent(fileName, encoding = "UTF-8"):
        """
        Return string with file content

        :param encoding: file encoding
        :param fileName: string path to file
        :return: string file content
        """
        file = io.open(fileName, mode = "r", encoding = encoding)
        text = file.read()
        file.close()
        return text

    @staticmethod
    def writeToFile(fileName, content, encoding = "UTF-8"):
        """
        Write content to file

        :param content: file text content
        :param encoding: file encoding
        :param fileName: string path to file
        :return: string file content
        """
        file = io.open(fileName, mode = "w", encoding = encoding)
        file.write(content)
        file.close()


class Statistic:
    statisticDictionary = {}

    def getStatisticFromFile(self, fileName):
        """
        :param fileName: string file path
        :return: dictionary with frequency occurred statistic
        """
        text = FileWork.getFileContent(fileName)
        for character in text:
            self.statisticDictionary[character] = (lambda character: self.statisticDictionary[
                character] if character in self.statisticDictionary else 0)(character) + 1
        return self.statisticDictionary


class HuffmanAlgorithm:

    @staticmethod
    def encodeHuffman(fileIn, fileOut, encoding = "UTF-8"):
        """

        :param encoding: file encoding
        :param fileIn: string file path
        :param fileOut: string file path
        """

        try:
            frequencyOccurredStatistic = Statistic()
            frequencyOccurredStatistic = frequencyOccurredStatistic.getStatisticFromFile(fileIn)

            tree = EncodeTree()
            tree.buildTree(frequencyOccurredStatistic)

            treeSheets = tree.sheets

            text = FileWork.getFileContent(fileIn, encoding)

            encodeResult = ""
            for character in text:
                encodeResult += treeSheets[character]

            separator = ' '

            encodeResult += separator + tree.model

            file = io.open(fileOut, mode = "w", encoding = encoding)
            file.write(encodeResult)
            file.close()
            return True
        except Exception:
            return False

    @staticmethod
    def decodeHuffman(fileIn, fileOut, encoding = "UTF-8"):
        """

        :param encoding: file encoding
        :param fileIn: string file path
        :param fileOut: string file path
        """
        try:
            file = io.open(fileIn, mode = "r", encoding = encoding)
            fileContent = file.read()
            fileContent = fileContent.split(' ', 1)

            treeModel = fileContent[1]
            text = fileContent[0]

            tree = DecodeTree(treeModel)
            tree.decodeTree()

            charactersBinaryCodes = tree.decodedTree

            currentCharacterCode = ""
            result = ""
            for character in text:
                currentCharacterCode += character
                if currentCharacterCode in charactersBinaryCodes:
                    result += charactersBinaryCodes[currentCharacterCode]
                    currentCharacterCode = ""

            file = io.open(fileOut, mode = "w", encoding = encoding)
            file.write(result)
            file.close()
            return True
        except Exception:
            return False


if HuffmanAlgorithm.encodeHuffman("huffmanBest.txt", "huffmanEncodedBest.txt"):
    print("All done. Huffman encoded")
else:
    print("Huffman encoding error")

if HuffmanAlgorithm.decodeHuffman("huffmanEncodedBest.txt", "huffmanDecoded.txt"):
    print("All done. Huffman decoded")
else:
    print("Huffman decoding error")

"""
--End huffman method--
"""

"""
--Start LZW--
"""


class LZWAlgorithm:

    @staticmethod
    def encodeLZ(fileIn, fileOut, dictionarySize = 1114112):
        """
        Encode file content string to file

        :param fileIn: string path to file
        :param fileOut: string path to file
        :param dictionarySize: max UTF-8 char value
        """
        try:
            fileContent = FileWork.getFileContent(fileIn)

            dictionary = {}
            for i in range(0, dictionarySize):
                dictionary[chr(i)] = i

            currentCode = dictionarySize

            encodedFileContent = ""
            buffer = fileContent[0]
            for pos in range(1, len(fileContent)):
                character = fileContent[pos]
                if (buffer + character) in dictionary:
                    buffer += character
                else:
                    dictionary[buffer + character] = currentCode
                    currentCode += 1
                    encodedFileContent += str(dictionary[buffer]) + " "
                    buffer = character

            encodedFileContent += str(dictionary[buffer])

            FileWork.writeToFile(fileOut, encodedFileContent)
            return True
        except Exception:
            return False

    @staticmethod
    def decodeLZ(fileIn, fileOut, dictionarySize = 1114112):
        """
        Decode file content from file

        :param fileIn: string path to file
        :param fileOut: string path to file
        :param dictionarySize: max UTF-8 char value
        """
        try:
            fileContent = FileWork.getFileContent(fileIn)

            getCharByCode = {}
            getCodeByChar = {}

            for i in range(0, dictionarySize):
                getCharByCode[i] = chr(i)
                getCodeByChar[chr(i)] = i

            currentCode = dictionarySize

            fileContent = fileContent.split(' ')
            buffer = getCharByCode[int(fileContent[0])]
            decodeFileContent = ""
            for i in range(1, len(fileContent)):
                character = ""
                if int(fileContent[i]) in getCharByCode:
                    character = getCharByCode[int(fileContent[i])]
                else:
                    getCharByCode[currentCode] = buffer + buffer[0]
                    getCodeByChar[buffer + buffer[0]] = currentCode
                    currentCode += 1
                    decodeFileContent += buffer
                    character = buffer[0]

                if (buffer + character[0]) in getCodeByChar:
                    buffer = buffer + character[0]
                else:
                    getCharByCode[currentCode] = buffer + character[0]
                    getCodeByChar[buffer + character[0]] = currentCode
                    currentCode += 1
                    decodeFileContent += buffer
                    buffer = character
            decodeFileContent += buffer
            FileWork.writeToFile(fileOut, decodeFileContent)
            return True
        except Exception:
            return False


if LZWAlgorithm.encodeLZ("LZWBest.txt", "LZWEncodedBest.txt"):
    print("All done. LZW encoded")
else:
    print("LZW encoding error")

if LZWAlgorithm.decodeLZ("LZWEncodedBest.txt", "LZWDecoded.txt"):
    print("All done. LZW decoded")
else:
    print("LZW decoding error")
"""
--End LZW--
"""

