import math
class Point:
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def set_x(self, x):
        self._x = x

    def get_x(self):
        return self._x

    def set_y(self, y):
        self._y = y

    def get_y(self):
        return self._y

    def compute_distance(self, other):
        return ((self._x - other._x) ** 2 + (self._y - other._y) ** 2) ** 0.5


class Line:
    def __init__(self, start_point, end_point):
        self._start_point = start_point
        self._end_point = end_point
        self.length = start_point.compute_distance(end_point)

    def get_start_point(self):
        return self._start_point

    def set_start_point(self, start_point):
        self._start_point = start_point

    def get_end_point(self):
        return self._end_point

    def set_end_point(self, end_point):
        self._end_point = end_point


class Shape:
    def __init__(self, vertices, inner_angles):
        self.vertices = vertices
        self._inner_angles = inner_angles
        self.edges = [Line(vertices[i], vertices[(i + 1) % len(vertices)]) for i in range(len(vertices))]
        self._inner_angles = self.compute_inner_angles()
        self.is_regular = self.compute_is_regular()

    def compute_inner_angles(self):
        angles = []
        for i in range(len(self.vertices)):
            p1 = self.vertices[i]
            p2 = self.vertices[(i + 1) % len(self.vertices)]
            p3 = self.vertices[(i + 2) % len(self.vertices)]
            angle = self.compute_angle(p1, p2, p3)
            angles.append(angle)
        return angles

    def compute_angle(self, p1, p2, p3):
        d1 = p1.compute_distance(p2)
        d2 = p2.compute_distance(p3)
        d3 = p3.compute_distance(p1)
        numerator = d1 ** 2 + d3 ** 2 - d2 ** 2
        denominator = 2 * d1 * d3
        # Manejar divisiones por cero
        if denominator == 0:
            return 0
        # Calcular el ángulo utilizando teorema de coseno
        angle_rad = math.acos(numerator / denominator)
        # Convertir radianes a grados
        angle_deg = angle_rad * 180 / math.pi
        return angle_deg

    def compute_is_regular(self):
        return len(set(self._inner_angles)) == 1

    def get_vertices(self):
        return self._vertices

    def set_vertices(self, vertices):
        self._vertices = vertices

    def get_inner_angles(self):
        return self._inner_angles

    def set_inner_angles(self, inner_angles):
        self._inner_angles = inner_angles


class Triangle(Shape):
    def __init__(self, vertices, inner_angles):
        super().__init__(vertices, inner_angles)
        self.type = self.determine_type()

    def determine_type(self):
        a, b, c = sorted([edge.length for edge in self.edges])
        # tolerancia de error (1e-6) para comparar las longitudes de los lados.
        if abs(a ** 2 + b ** 2 - c ** 2) < 1e-6:
            return "Rectangulo"
        elif a == b == c:
            return "Equilatero"
        elif a == b or b == c:
            return "Isosceles"
        else:
            return "Escaleno"

    def compute_area(self):
        a, b, c = sorted([edge.length for edge in self.edges])
        if self.type == "Rectangulo":
            # Para un triangulo rectangulo, el área es (base * altura)/2
            return 0.5 * a * b
        elif self.type == "Isósceles":
            # Para un triángulo isósceles, el area es base * raiz cuadrada((lado^2) - (base^2 / 4)) / 2
            base = a if a != b else c
            side = b if a == b else a
            return base * ((side ** 2 - (base ** 2 / 4)) ** 0.5) / 2
        elif self.type=="Equilatero":
            #Para un tirangulo equilatero calculamos el area con ((raizcuadrada 3)/) * lado al cuadrado
            a = self.edges[0].length
            return ((3 ** 0.5) / 4) * a ** 2
        else:
            # Para un triángulo escaleno, utilizamos la formula de Heron donde s=semiperimetro
            s = (a + b + c) / 2
            return (s * (s - a) * (s - b) * (s - c)) ** 0.5

    def compute_perimeter(self):
        # La suma de los lados
        return sum(edge.length for edge in self.edges)
    
class EquilateralTriangle(Triangle):
    def __init__(self, vertices, inner_angles):
        super().__init__(vertices, inner_angles)

    def compute_area(self):
        # Área de un triángulo equilátero
        a = self.edges[0].length
        return ((3 ** 0.5) / 4) * a ** 2

    def get_vertices(self):
        return super().get_vertices()

    def set_vertices(self, vertices):
        super().set_vertices(vertices)


class RectangleTriangle(Triangle):
    def __init__(self, vertices, inner_angles):
        super().__init__(vertices, inner_angles)

    def compute_area(self):
        # area de un triángulo rectangulo
        a = self.edges[0].length
        b = self.edges[1].length
        return 0.5 * a * b

    def get_vertices(self):
        return super().get_vertices()

    def set_vertices(self, vertices):
        super().set_vertices(vertices)


class ScaleneTriangle(Triangle):
    def __init__(self, vertices, inner_angles):
        super().__init__(vertices, inner_angles)

    def compute_area(self):
        # Usando la fórmula de Heron
        a = self.edges[0].length
        b = self.edges[1].length
        c = self.edges[2].length
        s = (a + b + c) / 2
        return (s * (s - a) * (s - b) * (s - c)) ** 0.5

    def get_vertices(self):
        return super().get_vertices()

    def set_vertices(self, vertices):
        super().set_vertices(vertices)


class IsoscelesTriangle(Triangle):
    def __init__(self, vertices, inner_angles):
        super().__init__(vertices, inner_angles)

    def compute_area(self):
        # area de un triángulo isosceles
        a, b, c = sorted([edge.length for edge in self.edges])
        base = a if a != b else c
        side = b if a == b else a
        return base * ((side ** 2 - (base ** 2 / 4)) ** 0.5) / 2

    def get_vertices(self):
        return super().get_vertices()

    def set_vertices(self, vertices):
        super().set_vertices(vertices)


class Rectangle(Shape):
    def compute_area(self):
        # la multiplicacion de los lados b*h
        return self.edges[0].length * self.edges[1].length

    def compute_perimeter(self):
        # se suma la medida de los lados 
        return 2 * (self.edges[0].length + self.edges[1].length)

    def get_vertices(self):
        return super().get_vertices()

    def set_vertices(self, vertices):
        super().set_vertices(vertices)


class Square(Rectangle):
    def compute_area(self):
        # para el area multiplicamos l*l
        return self.edges[0].length ** 2

    def compute_perimeter(self):
        # sumamos 4 veces la medida del lado  
        return 4 * self.edges[0].length

    def get_vertices(self):
        return super().get_vertices()

    def set_vertices(self, vertices):
        super().set_vertices(vertices)

p1 = Point(0, 0)
p2 = Point(0, 2)
p3 = Point(11, 11)

# Crea un triángulo y determina su tipo
triangle = Triangle(vertices=[p1, p2, p3], inner_angles=[p1, p2, p3])
triangle_type = triangle.type
print("Tipo de triángulo:", triangle_type)

# Dependiendo del tipo de triángulo, crea una instancia de la clase correcta
if triangle_type == "Rectángulo":
    triangle = Rectangle(vertices=[p1, p2, p3], inner_angles=[p1, p2, p3])
elif triangle_type == "Isosceles":
    triangle = IsoscelesTriangle(vertices=[p1, p2, p3], inner_angles=[p1, p2, p3])
elif triangle_type == "Equilatero":
    triangle = EquilateralTriangle(vertices=[p1, p2, p3], inner_angles=[p1, p2, p3])
elif triangle_type == "Escaleno":
    triangle = EquilateralTriangle(vertices=[p1, p2, p3], inner_angles=[p1, p2, p3])

# Calcula e imprime el area y el perímetro del triangulo
print("Área del triángulo:", triangle.compute_area())
print("Perímetro del triángulo:", triangle.compute_perimeter())

# Para el rectángulo y el cuadrado, el código permanece igual
rectangle = Rectangle(vertices=[p1, Point(5, 0), Point(5, 3), Point(0, 3)], inner_angles=[p1, Point(5, 0), Point(5, 3), Point(0, 3)])
print("Área del rectángulo:", rectangle.compute_area())
print("Perímetro del rectángulo:", rectangle.compute_perimeter())

square = Square(vertices=[p1, Point(3, 0), Point(3, 3), Point(0, 3)], inner_angles=[p1, Point(3, 0), Point(3, 3), Point(0, 3)])
print("Área del cuadrado:", square.compute_area())
print("Perímetro del cuadrado:", square.compute_perimeter())