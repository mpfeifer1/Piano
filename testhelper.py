
class TestHelp():
    def __init__(self):
        pass
    
    def prettyTreeComp(self, tree1, tree2):
        tree1 = tree1.strip().split('\n')
        tree2 = tree2.strip().split('\n')
        
        if len(tree1) != len(tree2):
            return False
            
        for line1, line2 in zip(tree1, tree2):
            line1 = ''.join(''.join(line1.strip().split(' ')).split('\t'))
            line2 = ''.join(''.join(line2.strip().split(' ')).split('\t'))
            if line1 != line2:
                return False
        return True
        
