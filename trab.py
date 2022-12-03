import os                           

class Node:
    def __init__(self, dado):
        self.dado = dado            
        self.anterior = None        
        self.prox = None            

    def __str__(self):
        return str(self.dado)       

class ListaDupla:
    def __init__(self):
        self.inicio = None              
        self.fim = None                 
        self.pos = None                 
        self.n = 0                      

    def __len__(self):
        return self.n                   

    def __str__(self):
        curr = self.inicio              
        st = ''                         
        while curr is not None:         
            st += str(curr)             
            curr = curr.prox            
        return st                       

    def append(self, dado):
        new_node = Node(dado)            
        if self.inicio is None:         
            self.inicio = new_node       
            self.fim = self.inicio      
        else:                           
            self.fim.prox = new_node     
            new_node.anterior = self.fim 
            self.fim = new_node          
        self.n += 1                     

    def preppend(self, dado):
        new_node = Node(dado)            
        if self.inicio is None:         
            self.inicio = new_node       
            self.fim = self.inicio      
        else:                           
            self.inicio.anterior = new_node 
            new_node.prox = self.inicio  
            self.inicio = new_node       
        self.n += 1                     

    def set_pos(self, i):
        if i == 0:                      
            self.pos = self.inicio      
        elif i == self.n - 1:           
            self.pos = self.fim         
        elif 2*i < self.n:              
            self.pos = self.inicio      
            while i > 0:                
                self.pos = self.pos.prox 
                i -= 1                  
        else:                           
            self.pos = self.fim         
            while i < self.n-1:         
                self.pos = self.pos.anterior 
                i += 1                  

    def set_next(self):
        self.pos = self.pos.prox        
        if self.pos is None:            
            self.append(' ')            
            self.pos = self.fim         

    def set_prev(self):
        self.pos = self.pos.anterior    
        if self.pos is None:            
            self.preppend(' ')          
            self.pos = self.inicio      

    def set_data(self, dado):
        self.pos.dado = dado            

    def get_data(self):
        if self.pos is None:            
            return None                 
        return self.pos.dado           


class FitaTuring:
    def __init__(self, st):
        self.lista = ListaDupla()       
        for c in ' '+st:                
            self.lista.append(c)        
        self.lista.set_pos(0)           
        self.estadoatual = 'q0'         
        self.pos = 0                    

    def __str__(self):
        return f'{self.estadoatual},{self.pos},{self.lista}'

    def deslCabDir(self):
        self.lista.set_next()           
        self.pos += 1                   

    def deslCabEsq(self):
        self.lista.set_prev()           
        self.pos = max(0, self.pos-1)   

    def escrever_caractere(self, c):
        self.lista.set_data(c)

    def ler_caractere(self):
        return self.lista.get_data()

    def estado_dado(self):
        return self.estadoatual, self.ler_caractere()

    # Tarefa 4
    def executar(self, quad):
        e1, let, act, e2 = self.componentes(quad)   
        if e1 == self.estadoatual and self.lista.get_data() == let:
            if act == '>':                          
                self.deslCabDir()     
            elif act == '<':                        
                self.deslCabEsq()     
            else:                                   
                self.escrever_caractere(act)        
            self.estadoatual = e2                   

    @staticmethod
    # Tarefa 1
    def componentes(st):
        return tuple(st.split(','))

def executarMTengine(entrada, quads, debug):
    mt = FitaTuring(entrada)                        
    transicoes = {mt.componentes(quad)[:2]: quad    
                  for quad in quads}                
    while mt.estado_dado() in transicoes:           
        mt.executar(transicoes[mt.estado_dado()])   
        if debug:                                   
            print(mt)                               
            input('Tecle [enter] para continuar...\n')  
    if not debug:                                   
        print(mt)                                   

# Tarefa 5
def executarMT(entrada, quads):
    executarMTengine(entrada, quads, debug=False)  

# Tarefe 6
def executarMTDebug(entrada, quads):
    executarMTengine(entrada, quads, debug=True)    

def le_arquivos(fentrada, fquads):
    with open(fentrada) as fin:                     
        entrada = fin.read().strip()                
    with open(fquads) as fin:                       
        quads = map((lambda x: x.strip()), fin.read().splitlines())
    return entrada, quads

# Tarefa 7
def executarMTArq(fentrada, fquads):
    entrada, quads = le_arquivos(fentrada, fquads)  
    executarMT(entrada, quads)

def executarMTArqDebug(fentrada, fquads):
    entrada, quads = le_arquivos(fentrada, fquads)
    executarMTDebug(entrada, quads)

if __name__ == '__main__':
    fentrada = input('Insira o arquivo com a entrada da máquina: ')
    assert os.path.exists(fentrada), f'Arquivo {fentrada} não encontrado'
    fquads = input('Insira o arquivo com as quadruplas: ')
    assert os.path.exists(fquads), f'Arquivo {fquads} não encontrado'
    debug = input('Modo debug? (s/N) ').strip() == 's'
    if debug:
        executarMTArqDebug(fentrada, fquads)
    else:
        executarMTArq(fentrada, fquads)
