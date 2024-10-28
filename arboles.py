import matplotlib.pyplot as plt
import networkx as nx


class Nodo:
    def __init__(self, valor):
        self.valor = valor
        self.izquierda = None
        self.derecha = None


class ArbolBinario:
    def __init__(self):
        self.raiz = None

    def esVacio(self):
        return self.raiz is None

    def insertar(self, valor):
        if self.raiz is None:
            self.raiz = Nodo(valor)
        else:
            self._insertar_recursivo(self.raiz, valor)

    def _insertar_recursivo(self, nodo, valor):
        if valor < nodo.valor:
            if nodo.izquierda is None:
                nodo.izquierda = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.izquierda, valor)
        else:
            if nodo.derecha is None:
                nodo.derecha = Nodo(valor)
            else:
                self._insertar_recursivo(nodo.derecha, valor)

    def buscar(self, valor):
        return self._buscar_recursivo(self.raiz, valor)

    def _buscar_recursivo(self, nodo, valor):
        if nodo is None:
            return False
        if nodo.valor == valor:
            return True
        elif valor < nodo.valor:
            return self._buscar_recursivo(nodo.izquierda, valor)
        else:
            return self._buscar_recursivo(nodo.derecha, valor)

    def mostrar_arbol(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz
        if nodo.derecha:
            self.mostrar_arbol(nodo.derecha, nivel + 1)
        print('   ' * nivel + f'-> {nodo.valor}')
        if nodo.izquierda:
            self.mostrar_arbol(nodo.izquierda, nivel + 1)

    def preorden(self, nodo):
        if nodo:
            print(nodo.valor, end=' ')
            self.preorden(nodo.izquierda)
            self.preorden(nodo.derecha)

    def inorden(self, nodo):
        if nodo:
            self.inorden(nodo.izquierda)
            print(nodo.valor, end=' ')
            self.inorden(nodo.derecha)

    def postorden(self, nodo):
        if nodo:
            self.postorden(nodo.izquierda)
            self.postorden(nodo.derecha)
            print(nodo.valor, end=' ')

    def eliminar(self, valor, metodo="PREDECESOR"):
        if metodo == "PREDECESOR":
            predecesor = self._predecesor(valor)
            if predecesor is not None:
                print(f"Predecesor de {valor} es {predecesor.valor}")
            else:
                print("No hay predecesor disponible.")
        elif metodo == "SUCESOR":
            sucesor = self._sucesor(valor)
            if sucesor is not None:
                print(f"Sucesor de {valor} es {sucesor.valor}")
            else:
                print("No hay sucesor disponible.")
        
        
        confirmacion = input(f"¿Quieres eliminar el nodo {valor} usando {metodo}? (s/n): ").lower()
        if confirmacion == 's':
            self.raiz = self._eliminar_nodo(self.raiz, valor, metodo)

    def _eliminar_nodo(self, nodo, valor, metodo):
        if nodo is None:
            return nodo
        if valor < nodo.valor:
            nodo.izquierda = self._eliminar_nodo(nodo.izquierda, valor, metodo)
        elif valor > nodo.valor:
            nodo.derecha = self._eliminar_nodo(nodo.derecha, valor, metodo)
        else:
            if nodo.izquierda is None:
                return nodo.derecha
            elif nodo.derecha is None:
                return nodo.izquierda
            if metodo == "PREDECESOR":
                temp = self._maximo(nodo.izquierda)
                nodo.valor = temp.valor
                nodo.izquierda = self._eliminar_nodo(nodo.izquierda, temp.valor, metodo)
            else:
                temp = self._minimo(nodo.derecha)
                nodo.valor = temp.valor
                nodo.derecha = self._eliminar_nodo(nodo.derecha, temp.valor, metodo)
        return nodo

    def _predecesor(self, valor):
        nodo = self.raiz
        predecesor = None
        while nodo:
            if valor > nodo.valor:
                predecesor = nodo
                nodo = nodo.derecha
            elif valor < nodo.valor:
                nodo = nodo.izquierda
            else:
                if nodo.izquierda:
                    predecesor = self._maximo(nodo.izquierda)
                break
        return predecesor

    def _sucesor(self, valor):
        nodo = self.raiz
        sucesor = None
        while nodo:
            if valor < nodo.valor:
                sucesor = nodo
                nodo = nodo.izquierda
            elif valor > nodo.valor:
                nodo = nodo.derecha
            else:
                if nodo.derecha:
                    sucesor = self._minimo(nodo.derecha)
                break
        return sucesor

    def _maximo(self, nodo):
        while nodo.derecha:
            nodo = nodo.derecha
        return nodo

    def _minimo(self, nodo):
        while nodo.izquierda:
            nodo = nodo.izquierda
        return nodo

    def graficar_arbol(self):
        if self.raiz is None:
            print("El árbol está vacío.")
            return

        grafo = nx.DiGraph()
        pos = {}

        def construir_grafo(nodo, x=0, y=0, nivel=1):
            if nodo:
                grafo.add_node(nodo.valor)
                pos[nodo.valor] = (x, y)
                if nodo.izquierda:
                    grafo.add_edge(nodo.valor, nodo.izquierda.valor)
                    construir_grafo(nodo.izquierda, x - 1 / nivel, y - 1, nivel + 1)
                if nodo.derecha:
                    grafo.add_edge(nodo.valor, nodo.derecha.valor)
                    construir_grafo(nodo.derecha, x + 1 / nivel, y - 1, nivel + 1)

        construir_grafo(self.raiz)

        plt.figure(figsize=(12, 8))
        nx.draw(grafo, pos, with_labels=True, node_size=700, node_color="skyblue", font_size=10, font_weight="bold", arrows=False)
        plt.title("Árbol Binario")
        plt.show()



arbol = ArbolBinario()
valores = [50, 30, 70, 20, 40, 60, 80]
for valor in valores:
    arbol.insertar(valor)

# Menú 
while True:
    print("\nMenú:")
    print("[1] Insertar elemento")
    print("[2] Mostrar árbol completo acostado con la raíz a la izquierda")
    print("[3] Graficar árbol completo")
    print("[4] Buscar un elemento en el árbol")
    print("[5] Recorrer el árbol en PreOrden")
    print("[6] Recorrer el árbol en InOrden")
    print("[7] Recorrer el árbol en PostOrden")
    print("[8] Eliminar un nodo del árbol PREDECESOR")
    print("[9] Eliminar un nodo del árbol SUCESOR")
    print("[0] Salir")

    opcion = int(input("Selecciona una opción: "))

    if opcion == 1:
        valor = int(input("Ingresa el valor a insertar: "))
        arbol.insertar(valor)
    elif opcion == 2:
        print("Árbol completo:")
        arbol.mostrar_arbol()
    elif opcion == 3:
        print("Graficando árbol...")
        arbol.graficar_arbol()
    elif opcion == 4:
        valor = int(input("Ingresa el valor a buscar: "))
        encontrado = arbol.buscar(valor)
        print("Elemento encontrado." if encontrado else "Elemento no encontrado.")
    elif opcion == 5:
        print("Recorrido PreOrden:")
        arbol.preorden(arbol.raiz)
        print()
    elif opcion == 6:
        print("Recorrido InOrden:")
        arbol.inorden(arbol.raiz)
        print()
    elif opcion == 7:
        print("Recorrido PostOrden:")
        arbol.postorden(arbol.raiz)
        print()
    elif opcion == 8:
        valor = int(input("Ingresa el valor a eliminar con PREDECESOR: "))
        arbol.eliminar(valor, metodo="PREDECESOR")
    elif opcion == 9:
        valor = int(input("Ingresa el valor a eliminar con SUCESOR: "))
        arbol.eliminar(valor, metodo="SUCESOR")
    elif opcion == 0:
        print("Saliendo...")
        break
    else:
        print("Opción no válida.")
