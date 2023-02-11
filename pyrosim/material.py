from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self,c1='<material name="Cyan">',c2='    <color rgba="0 1.0 1.0 1.0"/>'):

        self.depth  = 3

        self.string1 = c1

        self.string2 = c2

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
